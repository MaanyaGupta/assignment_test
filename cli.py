"""
Interactive Terminal CLI for Policy QA Assistant
Allows interactive questioning, date switching, and benchmark testing.
"""

import sys
from datetime import datetime

# UTF-8 stdout configuration for Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from assistant import ask

SAMPLE_QUESTIONS = [
    ("When does a small merchant receive UPI money?", "15 August 2026"),
    ("A large merchant (above Rs.10 lakh monthly) receives a Rs.4,000 UPI payment. What MDR and GST do they pay?", "15 August 2026"),
    ("Same merchant, a Rs.1,50,000 payment. What do they pay?", "15 August 2026"),
    ("A merchant refunds a customer 3 hours after the sale. Do they get the MDR back? (20 Aug 2026)", "20 Aug 2026"),
    ("A merchant refunds a customer 3 hours after the sale. Do they get the MDR back? (5 Sep 2026)", "5 Sep 2026"),
    ("What does the FAQ say about the MDR cap, and is the FAQ right?", "15 August 2026"),
    ("Can a customer pay Rs.1,00,000 twice in one day to a merchant?", "15 August 2026"),
    ("I closed my account yesterday. When will I get my money?", "15 August 2026"),
    ("Does the policy allow me to settle card payments same day?", "15 August 2026"),
    ("What is the MDR fee for RuPay credit cards processed over UPI? (Adversarial)", "15 August 2026"),
    ("How much does the Instant Settlement add-on cost per month? (Adversarial)", "15 August 2026"),
]


def print_banner(current_date: str):
    print("=" * 78)
    print("      POLICY QA ASSISTANT — INTERACTIVE TERMINAL SHELL")
    print(f"      Current Default Date: {current_date}")
    print("=" * 78)
    print("Commands:")
    print("  - Type any question to get an answer")
    print("  - Type 'samples' to view and select benchmark questions by number")
    print("  - Type 'date <new_date>' to change current as_of_date (e.g. 'date 5 Sep 2026')")
    print("  - Type 'eval' to run the automated test suite")
    print("  - Type 'exit' or 'quit' to close")
    print("=" * 78 + "\n")


def format_response(res: dict, q: str, dt: str):
    status = res.get("status", "UNKNOWN")
    citations = res.get("citations", [])
    answer = res.get("answer", "")
    conflict_res = res.get("conflict_resolution")

    print("\n" + "-" * 78)
    print(f"Query    : {q}")
    print(f"As Of    : {dt}")
    print(f"Status   : [{status}]")
    if citations:
        print("Citations: " + ", ".join(citations))
    else:
        print("Citations: None (Out of scope)")
    if conflict_res:
        print(f"Conflict Resolution: {conflict_res}")
    print("-" * 78)
    print(f"Answer:\n{answer}")
    print("-" * 78 + "\n")


def run_cli():
    current_date = "15 August 2026"
    print_banner(current_date)

    while True:
        try:
            user_input = input(f"[{current_date}] Ask >> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting CLI. Goodbye!")
            break

        if not user_input:
            continue

        cmd = user_input.lower()
        if cmd in ["exit", "quit", "q"]:
            print("Exiting CLI. Goodbye!")
            break

        if cmd.startswith("date "):
            new_date = user_input[5:].strip()
            if new_date:
                current_date = new_date
                print(f">> Updated as_of_date to: {current_date}\n")
            continue

        if cmd == "eval":
            import run_eval
            run_eval.run_evaluation()
            print()
            continue

        if cmd in ["samples", "sample", "list"]:
            print("\nBenchmark Questions:")
            for idx, (sq, sdate) in enumerate(SAMPLE_QUESTIONS, 1):
                print(f"  [{idx:2d}] ({sdate}) {sq}")
            print("\nEnter number to run, or press Enter to return to prompt.")
            choice = input("Select # >> ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(SAMPLE_QUESTIONS):
                sq, sdate = SAMPLE_QUESTIONS[int(choice) - 1]
                res = ask(sq, sdate)
                format_response(res, sq, sdate)
            continue

        # Regular question query
        res = ask(user_input, current_date)
        format_response(res, user_input, current_date)


if __name__ == "__main__":
    run_cli()
