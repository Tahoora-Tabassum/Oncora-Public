import unittest

from core.evidence_fusion import build_fused_evidence_summary
from core.answer_generator import generate_clinical_answer
from core.query_understanding import understand_question
from core.planner import build_query_plan
from core.reranker import rerank_chunks
from core.retriever import retrieve_chunks
from core.external_research import build_pubmed_query


class ReasoningPipelineTests(unittest.TestCase):
    def test_build_fused_evidence_summary_merges_sources(self):
        retrieved_chunks = [
            {
                "sheet": "Sheet3",
                "text": "Chemotherapy-related nausea may improve with small frequent meals, cold foods, ginger, and hydration.",
                "metadata": {"Food_Name": "Ginger"},
            }
        ]
        external_evidence = [
            {"title": "ASCO antiemesis guidance", "source": "ASCO", "url": "https://example.org/asco"},
        ]

        fused = build_fused_evidence_summary(
            "What should I eat when chemotherapy causes nausea?",
            {"symptoms": ["nausea"], "treatment": ["chemotherapy"]},
            retrieved_chunks,
            external_evidence,
            "nausea chemotherapy small frequent meals ginger",
        )

        self.assertTrue(fused["uses_external_evidence"])
        self.assertIn("nausea", fused["summary"].lower())
        self.assertIn("ginger", fused["summary"].lower())

    def test_generate_clinical_answer_has_structured_sections(self):
        answer = generate_clinical_answer(
            question="What should I eat when chemotherapy causes nausea?",
            entities={"symptoms": ["nausea"], "treatment": ["chemotherapy"]},
            retrieved_chunks=[
                {"sheet": "Sheet3", "text": "Small frequent meals and ginger may reduce chemotherapy-related nausea."},
            ],
            external_evidence=[{"title": "ASCO antiemesis guidance", "source": "ASCO", "url": "https://example.org/asco"}],
            expanded_query="nausea chemotherapy small frequent meals ginger",
            ai_brain="You are an oncology nutrition assistant.",
        )

        self.assertIn("Clinical Summary", answer)
        self.assertIn("Key Recommendations", answer)
        self.assertIn("Scientific Reasoning", answer)
        self.assertIn("Evidence Strength", answer)
        self.assertIn("Research Gaps", answer)
        self.assertNotIn("Database Evidence", answer)
        self.assertNotIn("External Evidence", answer)

    def test_generate_clinical_answer_mentions_missing_local_evidence(self):
        answer = generate_clinical_answer(
            question="What should I eat for mucositis after radiation?",
            entities={"symptoms": ["mucositis"], "treatment": ["radiation"]},
            retrieved_chunks=[],
            external_evidence=[{"title": "ESPEN guideline", "source": "ESPEN", "url": "https://example.org/esp"}],
            expanded_query="mucositis radiation soft foods hydration",
            ai_brain="You are an oncology nutrition assistant.",
        )

        self.assertIn("local oncology database", answer.lower())
        self.assertIn("clinical guidance", answer.lower())

    def test_generate_clinical_answer_includes_confidence_and_caution(self):
        answer = generate_clinical_answer(
            question="What should I eat when chemotherapy causes nausea?",
            entities={"symptoms": ["nausea"], "treatment": ["chemotherapy"]},
            retrieved_chunks=[],
            external_evidence=[{"title": "ASCO antiemesis guidance", "source": "ASCO", "url": "https://example.org/asco"}],
            expanded_query="nausea chemotherapy small frequent meals ginger",
            ai_brain="You are an oncology nutrition assistant.",
        )

        self.assertIn("Confidence", answer)
        self.assertIn("caution", answer.lower())

    def test_generate_clinical_answer_tailors_to_cancer_and_treatment_context(self):
        answer = generate_clinical_answer(
            question="What should I eat for nausea after chemotherapy for colorectal cancer?",
            entities={"cancer": ["colorectal cancer"], "treatment": ["chemotherapy"], "symptoms": ["nausea"]},
            retrieved_chunks=[{"sheet": "Sheet3", "text": "Small frequent meals and ginger can help nausea during chemotherapy."}],
            external_evidence=[{"title": "ASCO antiemesis guidance", "source": "ASCO", "url": "https://example.org/asco"}],
            expanded_query="nausea chemotherapy colorectal cancer small frequent meals ginger",
            ai_brain="You are an oncology nutrition assistant.",
        )

        self.assertIn("colorectal", answer.lower())
        self.assertIn("chemotherapy", answer.lower())
        self.assertIn("small, frequent meals", answer.lower())

    def test_understand_question_normalizes_messy_clinical_inputs(self):
        understanding = understand_question("lymph cancer nutrient")

        self.assertEqual(understanding["intent"], "nutrition_recommendation")
        self.assertIn("lymphoma", understanding["normalized_question"].lower())
        self.assertIn("nutrition", understanding["normalized_question"].lower())
        self.assertIn("lymphoma", understanding["retrieval_plan"][0].lower())

    def test_build_query_plan_requests_external_guidance_for_incomplete_local_context(self):
        plan = build_query_plan(
            question="lymph cancer food",
            entities={"cancer": ["lymphoma"], "symptoms": ["poor appetite"], "treatment": ["chemotherapy"]},
            understanding={"intent": "nutrition_recommendation", "cancer": "lymphoma", "treatment": "chemotherapy", "symptoms": ["poor appetite"]},
        )

        self.assertTrue(plan["needs_external_evidence"])
        self.assertIn("espen", plan["external_sources"][0].lower())
        self.assertIn("Sheet3", plan["local_sheets"])

    def test_choose_sheets_prioritizes_treatment_and_cancer_context(self):
        sheets = build_query_plan(
            question="What should I eat for nausea after chemotherapy for colorectal cancer?",
            entities={"cancer": ["colorectal cancer"], "treatment": ["chemotherapy"], "symptoms": ["nausea"]},
            understanding={"intent": "symptom_management", "cancer": "colorectal cancer", "treatment": "chemotherapy", "symptoms": ["nausea"]},
        )["local_sheets"]

        self.assertIn("Sheet3", sheets)
        self.assertIn("Sheet2", sheets)

    def test_reranker_assigns_higher_score_to_clinically_relevant_chunk(self):
        chunks = [
            {"text": "The kitchen is bright and the table is red."},
            {"text": "Chemotherapy-related nausea may improve with small frequent meals, ginger, and hydration."},
        ]

        reranked = rerank_chunks(chunks, "What should I eat when chemotherapy causes nausea?")
        self.assertGreater(reranked[0].get("evidence_score", 0.0), reranked[1].get("evidence_score", 0.0))

    def test_retrieve_chunks_uses_query_text_when_vector_search_is_unavailable(self):
        chunks = [
            {"id": "generic", "text": "The kitchen is bright and the table is red."},
            {"id": "clinical", "text": "Chemotherapy and nausea can be eased with small frequent meals, ginger, and hydration."},
        ]

        retrieved = retrieve_chunks(index=None, chunks=chunks, query_vector=None, allowed_sheets=None, top_k=2, query_text="chemotherapy nausea ginger")
        self.assertEqual(retrieved[0]["id"], "clinical")

    def test_reranker_uses_entities_for_treatment_specific_boost(self):
        chunks = [
            {"text": "General nutrition advice for cancer patients."},
            {"text": "Chemotherapy-related nausea may improve with small frequent meals, ginger, and hydration."},
        ]

        reranked = rerank_chunks(chunks, "What should I eat after chemotherapy?", entities={"treatment": ["chemotherapy"], "symptoms": ["nausea"]})
        self.assertGreater(reranked[0].get("evidence_score", 0.0), reranked[1].get("evidence_score", 0.0))

    def test_build_pubmed_query_uses_cancer_and_treatment_context(self):
        query = build_pubmed_query(
            "What should I eat for nausea?",
            {"cancer": ["colorectal cancer"], "treatment": ["chemotherapy"], "symptoms": ["nausea"]},
        )

        self.assertIn("colorectal", query.lower())
        self.assertIn("chemotherapy", query.lower())
        self.assertIn("nausea", query.lower())


if __name__ == "__main__":
    unittest.main()
