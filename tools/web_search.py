from duckduckgo_search import DDGS

MAX_RESULTS = 4


def search_web(query: str) -> str:
    query = query.strip()
    if not query:
        return "Error: empty search query"

    try:
        with DDGS() as ddgs:
            hits = list(ddgs.text(query, max_results=MAX_RESULTS))

        if not hits:
            return "No results found for this query"

        parts = []
        for hit in hits:
            title = hit.get("title", "").strip()
            body = hit.get("body", "").strip()
            if title or body:
                parts.append(f"{title}\n{body}" if title else body)

        return "\n\n---\n\n".join(parts)

    except Exception as e:
        return f"Search failed: {e}"
