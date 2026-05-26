#!/usr/bin/env python3
"""MiMo Legal Analyzer CLI"""
import sys, argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.timeline import Timeline

sys.path.insert(0, str(Path(__file__).parent))
from src.mimo_client import MiMoClient

console = Console()
SYS = "You are an experienced legal contract analyst. Extract clauses, identify risks, track obligations, check compliance. Be precise with section references and provide actionable insights."

def cmd_analyze(args):
    client = MiMoClient(system_prompt=SYS)
    path = Path(args.file)
    content = path.read_text()[:10000] if path.suffix in [".txt",".md"] else f"[PDF: {path.name} - content would be extracted]"
    console.print(f"\n\U0001f4dc Analyzing [bold]{path.name}[/bold]...\n")
    with console.status("[bold green]MiMo is reviewing contract..."):
        result = client.analyze_json(
            f"Analyze this contract. Return: parties (list), governing_law, total_clauses, "
            f"clause_categories (dict), risk_flags (list with severity, section, description), "
            f"missing_clauses (list), summary."
        )
    console.print(f"  Parties: {', '.join(result.get('parties',[]))}")
    console.print(f"  Governing Law: {result.get('governing_law','N/A')}")
    console.print(f"  Total Clauses: {result.get('total_clauses','N/A')}")
    table = Table(title="Risk Flags")
    table.add_column("Severity", style="bold", width=10), table.add_column("Section", style="cyan", width=10), table.add_column("Issue", style="white")
    colors = {"CRITICAL":"red","HIGH":"dark_orange","MEDIUM":"yellow","LOW":"green"}
    for rf in result.get("risk_flags",[]):
        sev = rf.get("severity","LOW")
        table.add_row(f"[{colors.get(sev,'white')}]{sev}[/{colors.get(sev,'white')}]", rf.get("section",""), rf.get("description",""))
    console.print(table)
    if result.get("missing_clauses"):
        console.print("\n[bold red]Missing Clauses:[/bold red]")
        for mc in result["missing_clauses"]: console.print(f"  \u2022 {mc}")
    console.print(f"\n[bold]Summary:[/bold] {result.get('summary','')}\n")

def cmd_obligations(args):
    client = MiMoClient(system_prompt=SYS)
    path = Path(args.file)
    content = path.read_text()[:10000]
    console.print(f"\n\U0001f4cb Extracting obligations from [bold]{path.name}[/bold]...\n")
    with console.status("[bold green]Extracting obligations..."):
        result = client.analyze_json(
            f"Extract all obligations from this contract. For each: obligor, obligee, description, deadline, penalty. "
            f"Return: obligations (list), timeline (list with day/event).\n\n{content}"
        )
    table = Table(title="Obligations")
    table.add_column("Who", style="cyan"), table.add_column("Owes", style="yellow"), table.add_column("To Whom", style="green"), table.add_column("Deadline", style="white")
    for o in result.get("obligations",[])[:10]:
        table.add_row(o.get("obligor",""), o.get("description","")[:50], o.get("obligee",""), o.get("deadline",""))
    console.print(table)
    if args.timeline and result.get("timeline"):
        console.print("\n[bold]Timeline:[/bold]")
        for t in result["timeline"]:
            console.print(f"  {t.get('day','?'):>6}  {t.get('event','')}")
    console.print()

def cmd_compliance(args):
    client = MiMoClient(system_prompt=SYS)
    path = Path(args.file)
    content = path.read_text()[:10000]
    console.print(f"\n\U0001f4dc Compliance check ({args.standard.upper()}): [bold]{path.name}[/bold]\n")
    with console.status("[bold green]Checking compliance..."):
        result = client.analyze_json(
            f"Check this contract for {args.standard.upper()} compliance. Return: compliant (bool), "
            f"violations (list with article, description, severity), recommendations (list), score (0-100)."
        )
    score = result.get("score", 0)
    color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
    console.print(f"  Compliance Score: [{color}]{score}/100[/{color}]")
    console.print(f"  Status: [{'green' if result.get('compliant') else 'red'}]{'COMPLIANT' if result.get('compliant') else 'NON-COMPLIANT'}")
    for v in result.get("violations",[]):
        console.print(f"  \u274c [{v.get('severity','HIGH')}] {v.get('article','')} — {v.get('description','')}")
    console.print()

def main():
    parser = argparse.ArgumentParser(description="MiMo Legal Analyzer")
    sub = parser.add_subparsers(dest="command")
    p = sub.add_parser("analyze"); p.add_argument("file"); p.set_defaults(func=cmd_analyze)
    p = sub.add_parser("obligations"); p.add_argument("file"); p.add_argument("--timeline", action="store_true"); p.set_defaults(func=cmd_obligations)
    p = sub.add_parser("compliance"); p.add_argument("file"); p.add_argument("--standard", default="gdpr"); p.set_defaults(func=cmd_compliance)
    args = parser.parse_args()
    if not args.command: parser.print_help(); return
    args.func(args)

if __name__ == "__main__": main()
