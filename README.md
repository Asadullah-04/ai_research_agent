# AI Research Agent

A command-line AI assistant that answers questions by using three tools: a calculator, a local file reader, and a web search module. The agent decides which tool to use depending on the question and combines results into a final answer.

---

## What it does

- Receives a question or task from the user via the terminal
- Decides autonomously which tool(s) to call
- Executes the tools and interprets the results
- Returns a clear, final answer

### Available tools

| Tool | What it does |
|---|---|
| `calculator` | Evaluates arithmetic expressions safely (no `eval`) |
| `file_reader` | Reads text or CSV files from the local filesystem |
| `web_search` | Searches the internet using DuckDuckGo |

---

## Requirements

- Python 3.10 or higher
- An Anthropic API key (get one at https://console.anthropic.com)

---

## Installation

```bash
git clone https://github.com/Asadullah-04/ai_research_agent.git
cd ai_research_agent
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_key_here
```

---

## Running the agent

```bash
python main.py
```

You will see a prompt where you can type questions:

```
==================================================
  AI Research Agent
  Type 'exit' or press Ctrl+C to quit
==================================================

You: What is 15% of 340?
  → [calculator] {"expression": "340 * 0.15"}
  ← 51

Agent: 15% of 340 is 51.
```

---

## Example questions to try

- `What is (1500 / 12) * 1.21?`
- `Read the file data/example.csv and tell me the most expensive product`
- `What are the main features of Python 3.12?`
- `How much would 8 units of Laptop cost according to data/example.csv?`

---

## Running tests

```bash
pytest tests/ -v
```

Tests do not require an API key — the agent tests use mocking.

---

## Project structure

```
ai_research_agent/
├── main.py          # entry point, CLI loop
├── agent.py         # agent logic and tool dispatch
├── config.py        # settings loaded from .env
├── tools/
│   ├── calculator.py
│   ├── file_reader.py
│   └── web_search.py
├── tests/
│   ├── test_calculator.py
│   ├── test_file_reader.py
│   ├── test_web_search.py
│   └── test_agent.py
├── data/
│   └── example.csv
├── requirements.txt
├── .env.example
└── README.md
```

---

## Deployment

This is designed to run locally as a CLI tool. To run it on another machine:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set the `ANTHROPIC_API_KEY` in a `.env` file
4. Run `python main.py`

No server, no Docker, no extra setup needed. 

---

## Notes

- The calculator uses Python's `ast` module instead of `eval` to prevent code injection
- File reading is limited to 3000 characters for text files and 60 rows for CSV files
- Web search uses DuckDuckGo and does not require an API key
