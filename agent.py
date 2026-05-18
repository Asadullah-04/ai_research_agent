import json
import anthropic
from config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS, MAX_ITERATIONS
from tools import calculate, read_file, search_web

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = (
    "You are a practical research assistant. You have three tools available:\n"
    "- calculator: solve math expressions\n"
    "- file_reader: read the contents of a local file (text or CSV)\n"
    "- web_search: look up information on the internet\n\n"
    "Use tools whenever they would give a more accurate answer than guessing. "
    "Keep your final responses clear and to the point."
)

TOOLS = [
    {
        "name": "calculator",
        "description": "Evaluate a safe arithmetic expression and return the numeric result.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A math expression, e.g. '(120 * 0.15) + 50' or '2 ** 10'",
                }
            },
            "required": ["expression"],
        },
    },
    {
        "name": "file_reader",
        "description": "Read the contents of a local text or CSV file by its path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative or absolute path to the file.",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "web_search",
        "description": "Search the web for up-to-date information on any topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A clear search query, e.g. 'Python 3.13 new features'",
                }
            },
            "required": ["query"],
        },
    },
]

TOOL_MAP = {
    "calculator": lambda inp: calculate(inp["expression"]),
    "file_reader": lambda inp: read_file(inp["path"]),
    "web_search": lambda inp: search_web(inp["query"]),
}


def _dispatch_tool(name: str, tool_input: dict) -> str:
    fn = TOOL_MAP.get(name)
    if fn is None:
        return f"Error: unknown tool '{name}'"
    return fn(tool_input)


def run_agent(user_input: str, verbose: bool = True) -> str:
    messages = [{"role": "user", "content": user_input}]

    for iteration in range(MAX_ITERATIONS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return "(no text response)"

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type != "tool_use":
                    continue

                if verbose:
                    print(f"  → [{block.name}] {json.dumps(block.input)}")

                result = _dispatch_tool(block.name, block.input)

                if verbose:
                    preview = result[:120].replace("\n", " ")
                    print(f"  ← {preview}")

                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                )

            messages.append({"role": "user", "content": tool_results})
        else:
            break

    return "Agent could not complete the request within the iteration limit."
