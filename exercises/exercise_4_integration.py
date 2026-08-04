"""
Exercise 4: Integration Challenge
===================================

Build a mini data pipeline that processes text documents.
This exercise has three levels — complete as far as you can.

- BASE: File reading and text processing (no LLM needed)
- STANDARD: Add LLM-based analysis
- ADVANCED: Production-grade pipeline with error recovery

Uses the same LLM provider configured in utils/llm_client.py.
"""

import json
from pathlib import Path
from collections import Counter

from utils import call_llm  # noqa: configured in utils/llm_client.py


DOCUMENTS_PATH = Path(__file__).parent.parent / "data" / "documents"


# ============================================================
# BASE LEVEL — File I/O and text processing (no LLM needed)
# ============================================================

def read_documents(folder: Path) -> list[dict]:
    """
    Read all .txt files from the given folder.
    Return a list of dicts: [{"filename": str, "content": str}, ...]
    """
    documents = []
    txt_files = sorted(folder.glob("*.txt"))
    for file_path in txt_files:
        filename = file_path.name
        content = file_path.read_text(encoding="utf-8")
        documents.append({"filename": filename, "content": content})
    return documents


def word_count(text: str) -> int:
    """Return the number of words in a text."""
    words = text.split()
    return len(words)


STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "not", "no", "so", "if", "than", "then",
    "of", "in", "on", "at", "to", "for", "by", "from", "with", "as", "into", "about",
    "up", "out", "over", "under", "off", "per", "via", "during", "across", "around",
    "is", "are", "was", "were", "be", "been", "being", "has", "have", "had", "do",
    "does", "did", "will", "would", "shall", "should", "can", "could", "may", "might",
    "must", "this", "that", "these", "those", "its", "it", "their", "they", "them",
    "we", "our", "you", "your", "he", "she", "his", "her", "i", "all", "any", "both",
    "each", "few", "more", "most", "some", "such", "own", "same", "also", "very", "too",
    "including", "new", "make", "made", "use", "used", "using", "one", "two",
}


def extract_keywords_simple(text: str, top_n: int = 5) -> list[str]:
    """
    Extract the top N most frequent meaningful words from text.
    Exclude common stop words (the, a, is, in, of, and, to, for, etc.)
    Return as a list of lowercase words.
    """
    #split the text into lowercase words
    raw_words = text.lower().split()

    #clean each word and keep only the meaningful ones
    meaningful = []
    for word in raw_words:
        word = word.strip(".,;:!?()[]{}\"'")
        if word and word not in STOP_WORDS and not word.isdigit():
            meaningful.append(word)

    # count how often each word appears
    counter = Counter(meaningful)

    #pick the top N most frequent words
    keywords = []
    for word, _ in counter.most_common(top_n):
        keywords.append(word)
    return keywords


def basic_stats(documents: list[dict]) -> dict:
    """
    Return basic statistics about the document set:
    - total_documents: int
    - total_words: int
    - avg_words_per_doc: float
    - shortest_doc: str (filename)
    - longest_doc: str (filename)
    """
    #count the words in each document
    word_counts = {}
    for doc in documents:
        filename = doc["filename"]
        word_counts[filename] = word_count(doc["content"])

    #add up the word counts of all documents
    total_words = 0
    for filename in word_counts:
        total_words = total_words + word_counts[filename]

    #find the file with the fewest words (shortest doc)
    shortest_doc = None
    for filename in word_counts:
        if shortest_doc is None or word_counts[filename] < word_counts[shortest_doc]:
            shortest_doc = filename

    #find the file with the most words (longest doc)
    longest_doc = None
    for filename in word_counts:
        if longest_doc is None or word_counts[filename] > word_counts[longest_doc]:
            longest_doc = filename

    #average words per document
    avg_words_per_doc = total_words / len(documents)

    stats = {}
    stats["total_documents"] = len(documents)
    stats["total_words"] = total_words
    stats["avg_words_per_doc"] = avg_words_per_doc
    stats["shortest_doc"] = shortest_doc
    stats["longest_doc"] = longest_doc
    return stats


# ============================================================
# STANDARD LEVEL — LLM-powered analysis
# ============================================================

def _parse_json_response(response: str) -> dict:
    """Parse an LLM response into a dict, tolerating markdown fences."""
    text = response.strip()
    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.lower().startswith("json"):
            text = text[4:].strip()
    return json.loads(text)


def analyze_document(content: str) -> dict:
    """
    Use an LLM to analyze a single document and return:
    - summary: str (one sentence)
    - keywords: list[str] (3-5 keywords)
    - sentiment: str (positive/neutral/negative)
    """
    prompt = (
        "Analyze the document below. Return ONLY valid JSON with exactly three fields:\n"
        '- "summary": a one-sentence summary,\n'
        '- "keywords": an array of 3-5 keywords,\n'
        '- "sentiment": exactly one of "positive", "neutral", "negative".\n'
        "Do not add any other text.\n\n"
        f"DOCUMENT:\n{content}"
    )
    data = _parse_json_response(call_llm(prompt))

    #extract the summary
    summary = data.get("summary", "")
    summary = str(summary).strip()

    #extract the keywords as a list of strings
    keywords = []
    for keyword in data.get("keywords", []):
        keywords.append(str(keyword))

    #extract the sentiment
    sentiment = data.get("sentiment", "neutral")
    sentiment = str(sentiment).strip().lower()

    analysis = {
        "summary": summary,
        "keywords": keywords,
        "sentiment": sentiment,
    }
    return analysis


def process_all_documents(documents: list[dict]) -> list[dict]:
    """
    Process all documents and return enriched results.
    Each result should contain: filename, summary, keywords, sentiment.
    """
    results = []
    for doc in documents:
        analysis = analyze_document(doc["content"])
        result = {
            "filename": doc["filename"],
            "summary": analysis["summary"],
            "keywords": analysis["keywords"],
            "sentiment": analysis["sentiment"],
        }
        results.append(result)
    return results

def save_results(results: list[dict], output_path: Path) -> None:
    """Save results to a JSON file."""
    # TODO: Implement output saving
    pass


def generate_report(results: list[dict]) -> str:
    """
    Generate a formatted summary report containing:
    - Total documents processed
    - Sentiment distribution (how many positive/neutral/negative)
    - Top 10 most common keywords across all documents
    """
    # TODO: Implement report generation
    pass



# ============================================================
# ADVANCED LEVEL — Production-ready pipeline
# ============================================================

def process_with_recovery(documents: list[dict]) -> dict:
    """
    Process documents but handle failures gracefully:
    - If a document fails, log the error and continue
    - Retry failed documents once
    - Return both results and error log

    Return: {
        "results": [...],
        "errors": [{"filename": ..., "error": ...}],
        "success_rate": float
    }
    """
    # TODO: Implement fault-tolerant processing
    pass


def incremental_processing(documents: list[dict], output_path: Path) -> list[dict]:
    """
    Process documents incrementally:
    - Check if output file already exists
    - If yes, only process documents not already in the output
    - Append new results to existing output
    - This avoids re-processing and wasting API calls

    Return the complete results (existing + new).
    """
    # TODO: Implement incremental/resumable processing
    pass


def generate_comparison_report(results: list[dict]) -> str:
    """
    Generate an advanced report that also includes:
    - Document similarity (which documents cover similar topics?)
    - Topic clusters (group documents by dominant keyword overlap)
    - Confidence notes (which analyses might be unreliable and why?)
    """
    # TODO: Implement advanced reporting
    pass


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Exercise 4: Integration Challenge")
    print("=" * 60)

    # --- BASE ---
    print("\n--- BASE LEVEL ---")
    documents = read_documents(DOCUMENTS_PATH)
    if documents:
        print(f"Loaded {len(documents)} documents")
        stats = basic_stats(documents)
        if stats:
            print(f"Total words: {stats.get('total_words')}")
            print(f"Avg words/doc: {stats.get('avg_words_per_doc', 0):.0f}")
            print(f"Shortest: {stats.get('shortest_doc')}")
            print(f"Longest: {stats.get('longest_doc')}")

        # Show simple keyword extraction for first doc
        if documents:
            kw = extract_keywords_simple(documents[0]["content"])
            if kw:
                print(f"Keywords ({documents[0]['filename']}): {kw}")
    else:
        print("read_documents() not implemented yet")

    # --- STANDARD ---
    print("\n--- STANDARD LEVEL ---")
    if documents:
        results = process_all_documents(documents)
        if results:
            for result in results:
                print(f"\n{result['filename']}:")
                print(f"  Summary: {result['summary']}")
                print(f"  Keywords: {result['keywords']}")
                print(f"  Sentiment: {result['sentiment']}")
        else:
            print("process_all_documents() not implemented yet")

    # --- ADVANCED ---
    print("\n--- ADVANCED LEVEL ---")
    if documents:
        recovered = process_with_recovery(documents)
        if recovered:
            print(f"Success rate: {recovered.get('success_rate', 0):.0%}")
            if recovered.get("errors"):
                print(f"Errors: {len(recovered['errors'])}")
        else:
            print("process_with_recovery() not implemented yet")
