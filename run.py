"""Insurance Claims Triage - Processor with HITL support."""

import time, json, uuid
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from langgraph.types import Command
from agent import create_triage_agent

load_dotenv()

console = Console()
ROOT = Path(__file__).parent
CLAIMS = ROOT / "claims"
RESULTS = ROOT / "results"

CLAIMS.mkdir(exist_ok=True)
RESULTS.mkdir(exist_ok=True)


def get_pending_claims():
    """Get claims that don't have results yet."""
    for claim_dir in sorted(CLAIMS.iterdir()):
        if not claim_dir.is_dir():
            continue
        claim_file = claim_dir / "claim.json"
        result_file = RESULTS / f"{claim_dir.name}.json"
        if claim_file.exists() and not result_file.exists():
            yield claim_dir.name, claim_file


def process_claim(agent, claim_id: str, claim_file: Path):
    """Process a single claim with HITL support."""
    claim = json.loads(claim_file.read_text())
    console.print(f"\n[bold]Processing:[/bold] {claim_id}")

    start = time.time()
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    seen, shown_plan = set(), False
    final_decision = None

    # Initial invoke
    result = agent.invoke(
        {"messages": [{"role": "user", "content": f"Process this claim:\n{json.dumps(claim, indent=2)}"}]},
        config=config
    )

    # Process messages for display
    for msg in result.get("messages", []):
        for tc in getattr(msg, "tool_calls", []) or []:
            tid, name = tc.get("id"), tc.get("name")
            if tid in seen:
                continue
            seen.add(tid)
            if name == "write_todos" and not shown_plan:
                console.print("  [bold]Plan:[/bold]")
                for todo in tc.get("args", {}).get("todos", []):
                    content = todo.get('content', todo) if isinstance(todo, dict) else todo
                    console.print(f"    - {content}")
                shown_plan = True
            elif name == "task":
                console.print(f"  [cyan]>[/cyan] {tc['args'].get('subagent_type')}")

    # Check for interrupt (HITL)
    while result.get("__interrupt__"):
        interrupt = result["__interrupt__"][0]
        action_requests = interrupt.value.get("action_requests", [])

        for action in action_requests:
            if action.get("action") == "submit_decision":
                args = action.get("args", {})
                decision = args.get("decision", "UNKNOWN")

                console.print(f"\n  [bold yellow]PENDING REVIEW:[/bold yellow]")
                console.print(f"    Decision: [bold]{decision}[/bold]")
                console.print(f"    Coverage: {args.get('coverage')}")
                console.print(f"    Fraud: {args.get('fraud_risk')}")
                console.print(f"    Damage: ${args.get('damage_estimate')}")
                console.print(f"    Reason: {args.get('reason')}")

                # Human decision
                choice = Prompt.ask(
                    "\n  [bold]Action[/bold]",
                    choices=["approve", "reject", "edit"],
                    default="approve"
                )

                if choice == "approve":
                    final_decision = args
                    result = agent.invoke(
                        Command(resume={"decisions": [{"type": "approve"}]}),
                        config=config
                    )
                elif choice == "reject":
                    console.print("  [red]Rejected[/red] - claim sent back for re-evaluation")
                    return
                else:  # edit
                    new_decision = Prompt.ask("  New decision", choices=["AUTO-APPROVE", "DENY", "MANUAL REVIEW"])
                    final_decision = {**args, "decision": new_decision}
                    result = agent.invoke(
                        Command(resume={"decisions": [{"type": "edit", "args": final_decision}]}),
                        config=config
                    )

    # Get final decision from messages if not from interrupt
    if not final_decision:
        for msg in reversed(result.get("messages", [])):
            if hasattr(msg, "content") and msg.content:
                final_decision = {"raw": msg.content}
                break

    # Display final decision
    console.print(f"\n  [bold green]APPROVED:[/bold green]")
    if isinstance(final_decision, dict) and "decision" in final_decision:
        console.print(f"    **Outcome**: {final_decision.get('decision')}")
        console.print(f"    Coverage: {final_decision.get('coverage')} | Fraud: {final_decision.get('fraud_risk')} | Damage: ${final_decision.get('damage_estimate')}")
        console.print(f"    Reason: {final_decision.get('reason')}")
    elif final_decision:
        console.print(Markdown(final_decision.get("raw", str(final_decision))))

    # Save result
    result_data = {
        "claim_id": claim_id,
        "processed_at": datetime.now().isoformat(),
        "decision": final_decision,
    }
    (RESULTS / f"{claim_id}.json").write_text(json.dumps(result_data, indent=2))

    console.print(f"\n[green]Done[/green] [dim]({time.time() - start:.1f}s)[/dim]")


def main():
    console.print(f"\n[bold]Insurance Claims Triage[/bold]\nWatching: {CLAIMS}\n")
    agent = create_triage_agent()

    try:
        while True:
            pending = list(get_pending_claims())
            for claim_id, claim_file in pending:
                try:
                    process_claim(agent, claim_id, claim_file)
                except Exception as e:
                    console.print(f"[yellow]Failed:[/yellow] {e}")
                    import traceback
                    traceback.print_exc()
            if not pending:
                print("Waiting...", end="\r")
                time.sleep(3)
    except KeyboardInterrupt:
        console.print(f"\n[bold]Stopped[/bold]\n")


if __name__ == "__main__":
    main()
