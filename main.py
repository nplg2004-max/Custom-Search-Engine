import argparse
import os
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.rule import Rule

from search_engine import cache as result_cache
from search_engine.llm import LLMClient
from search_engine.searcher import Searcher

load_dotenv()

console = Console()


def print_answer(answer: str, sources: list) -> None:
    console.print()
    console.print(Rule("[bold cyan] ANSWER[/bold cyan]", style="cyan"))
    console.print()
    console.print(answer, style="white")
    console.print()
    console.print(Rule("[bold cyan] SOURCES[/bold cyan]", style="cyan"))
    console.print()
    for i, src in enumerate(sources, start=1):
        console.print(f"[bold yellow][{i}][/bold yellow] [bold]{src['title']}[/bold]")
        console.print(f"    [blue underline]{src['url']}[/blue underline]")
        console.print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI-powered CLI search engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "What is quantum computing?"
  python main.py "best Python frameworks 2024" --results 3
  python main.py "how does CRISPR work" --no-cache
  python main.py --clear-cache
        """,
    )

    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--results", "-r", type=int,
                        default=int(os.getenv("MAX_SEARCH_RESULTS", 5)),
                        metavar="N", help="Number of results (default: 5)")
    parser.add_argument("--no-cache", action="store_true", help="Skip cache")
    parser.add_argument("--clear-cache", action="store_true", help="Clear cache and exit")

    args = parser.parse_args()

    if args.clear_cache:
        result_cache.clear()
        sys.exit(0)

    if not args.query:
        parser.print_help()
        sys.exit(1)

    query = args.query.strip()
    use_cache = not args.no_cache and os.getenv("CACHE_ENABLED", "true").lower() == "true"

    if use_cache:
        cached = result_cache.get(query)
        if cached:
            console.print(f"\n[bold green]>> Query:[/bold green] {query}")
            console.print("[dim italic]  (from cache — use --no-cache to refresh)[/dim italic]")
            print_answer(cached["answer"], cached["sources"])
            sys.exit(0)

    console.print(f"\n[bold green]>> Searching:[/bold green] {query}")

    try:
        searcher = Searcher(max_results=args.results)
        results = searcher.search(query)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Search failed:[/bold red] {e}")
        sys.exit(1)

    if not results:
        console.print("[yellow]No results found. Try a different query.[/yellow]")
        sys.exit(0)

    console.print(f"[dim]Found {len(results)} results[/dim]")
    console.print("[dim]Generating answer...[/dim]")

    try:
        llm = LLMClient()
        answer = llm.answer(query, results)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]LLM error:[/bold red] {e}")
        sys.exit(1)

    sources = [{"title": r.title, "url": r.url} for r in results]

    if use_cache:
        result_cache.set(query, answer, sources)

    print_answer(answer, sources)


if __name__ == "__main__":
    main()
