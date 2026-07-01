# AI Search CLI

A minimal CLI search assistant: you type a query, it searches the web, and an LLM summarizes the best results.

---

## Architecture (3 moving parts)

```
You → CLI → Search API → LLM → Answer
              (Tavily)  (Gemini)
```

```
custom-search-engine/
├── search_engine/
│   ├── __init__.py
│   ├── searcher.py
│   ├── llm.py
│   └── cache.py
├── main.py
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

---

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt

copy .env.example .env

python main.py "What is the James Webb telescope?"
python main.py "best Python web frameworks 2024" --results 5
python main.py "how does CRISPR work" --no-cache
```

---

## API Keys (free tiers available)

| Service | Free Tier | Sign Up |
|---------|-----------|---------|
| **Tavily** | 1,000 searches/month | https://tavily.com |
| **Gemini** | 15 req/min (free) | https://aistudio.google.com |

---

## Demo Output

```
$ python main.py "What is quantum computing?"

>> Searching: What is quantum computing?
Found 5 results

Generating answer...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ANSWER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Quantum computing uses quantum bits (qubits) which can exist in
superposition — being 0 and 1 simultaneously. This allows quantum
computers to solve certain problems exponentially faster than
classical computers, including cryptography and drug discovery.

 SOURCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1] What is Quantum Computing? — IBM
    https://www.ibm.com/topics/quantum-computing

[2] Quantum computing explained — MIT News
    https://news.mit.edu/quantum-computing
```
