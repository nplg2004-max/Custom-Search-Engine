# 🔍 AI Search CLI

A minimal, powerful command-line search assistant. 
You type a query, it searches the web in real-time, and a Large Language Model generates a concise summary of the best results with direct citations.

---

## ✨ Features

- ⚡ **Real-time Search:** Powered by the Tavily search API for accurate web results.
- 🧠 **AI Summarization:** Uses Google's Gemini models for intelligent answer generation.
- 🔗 **Source Citations:** Fully cited answers with links to the original sources.
- 💾 **Smart Caching:** Local JSON caching for fast, cost-free repeat queries.

---

## 🏗️ Architecture

```text
You  →  CLI  →  Search API  →  LLM  →  Answer
                 (Tavily)    (Gemini)
```

## 📂 Directory Structure

```text
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

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- Free API keys for Tavily and Google AI Studio

### Installation

```bash
python -m venv .venv

.venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt

copy .env.example .env
```

---

## 💻 Usage

Run the search engine directly from your terminal by passing your query:

```bash
python main.py "What is the James Webb telescope?"
```

### Advanced Options

Customize the search behavior using the available flags:

```bash
python main.py "best Python web frameworks 2024" --results 5
python main.py "how does CRISPR work" --no-cache
python main.py --clear-cache
```

---

## 🔑 API Providers (Free Tiers)

| Service | Free Tier Allowance | Registration |
|---------|---------------------|--------------|
| **Tavily** | 1,000 searches / month | https://tavily.com |
| **Gemini** | 1,500 requests / day (15 req/min) | https://aistudio.google.com |

---

## 📜 Example Output

```text
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
