import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("chat_script", ROOT / "scripts" / "06_chat.py")
CHAT_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHAT_MODULE)


def test_build_source_citations_orders_database_and_external_evidence():
    retrieved_chunks = [
        {"sheet": "Sheet2", "text": "Cancer_Type: Breast\nTreatment: Chemotherapy\nProtein: 1.2-1.5 g/kg"},
        {"sheet": "Sheet4", "text": "Calories: 25-30 kcal/kg\nProtein: 1.2-1.5 g/kg"},
    ]
    external_evidence = [
        {
            "id": "12345",
            "title": "Ginger and antiemetic efficacy",
            "source": "PubMed",
            "url": "https://pubmed.ncbi.nlm.nih.gov/12345/",
            "abstract": "Brief abstract excerpt for testing.",
        }
    ]

    citations = CHAT_MODULE.build_source_citations(retrieved_chunks, external_evidence)

    assert [citation["id"] for citation in citations] == [1, 2, 3]
    assert citations[0]["kind"] == "database"
    assert citations[1]["kind"] == "database"
    assert citations[2]["kind"] == "external"
    assert citations[2]["url"] == "https://pubmed.ncbi.nlm.nih.gov/12345/"


def test_split_answer_sections_separates_sources_block():
    answer_text = "Here is the answer [1].\n\nSources:\n[1] CanNeutro Database\n"

    body, sources = CHAT_MODULE.split_answer_sections(answer_text)

    assert body.strip() == "Here is the answer [1]."
    assert sources.strip() == "[1] CanNeutro Database"


def test_should_search_external_evidence_when_quantitative_support_is_missing():
    retrieved_chunks = [{"sheet": "Sheet1", "text": "Food_Name: Cantaloupe\nClinical_Benefits: May reduce cancer risk"}]

    should_search = CHAT_MODULE.should_search_external_evidence(
        "exact protein grams for stage IV blood cancer",
        retrieved_chunks,
        {"needs_external_evidence": False},
        {"needs_external_evidence": False},
    )

    assert should_search is True
