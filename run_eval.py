"""
Evaluation Script for Grounded Policy Assistant
Runs questions from eval.json through assistant.ask() and prints a detailed score table.
"""

import json
import os
import sys
from datetime import datetime

# Ensure utf-8 output on Windows consoles
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from assistant import ask


def run_evaluation(eval_path: str = "eval.json"):
    if not os.path.exists(eval_path):
        print(f"Error: Evaluation file '{eval_path}' not found.")
        sys.exit(1)

    with open(eval_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    print("=" * 105)
    print("   AI INTERN ASSIGNMENT 2: THE POLICY THAT CHANGED — EVALUATION RUNNER")
    print(f"   Evaluation Dataset: {eval_path} ({len(test_cases)} test cases)")
    print("=" * 105)

    header = f"{'ID':<5} | {'Date':<12} | {'Adv?':<5} | {'Status (Exp/Act)':<30} | {'Citations':<10} | {'Keywords':<10} | {'Result':<6}"
    print(header)
    print("-" * 105)

    passed_count = 0
    total_count = len(test_cases)
    adversarial_total = 0
    adversarial_passed = 0

    results = []

    for item in test_cases:
        qid = item["id"]
        q = item["question"]
        as_of = item.get("as_of_date", "15 August 2026")
        is_adv = item.get("is_adversarial", False)
        exp_status = item["expected_status"]
        exp_citations = set(item.get("expected_citations", []))
        exp_keywords = item.get("expected_answer_keywords", [])

        if is_adv:
            adversarial_total += 1

        actual = ask(q, as_of)
        act_status = actual["status"]
        act_citations = set(actual.get("citations", []))
        act_answer = actual.get("answer", "")

        status_match = (exp_status == act_status)

        # Check citations: for CANNOT_ANSWER or specific citations
        if not exp_citations:
            citations_match = (len(act_citations) == 0) or (exp_status == "CANNOT_ANSWER")
        else:
            # Overlap check
            citations_match = bool(exp_citations.intersection(act_citations)) or (exp_citations == act_citations)

        # Check keyword presence
        found_keywords = [kw for kw in exp_keywords if kw.lower() in act_answer.lower()]
        kw_ratio = len(found_keywords) / len(exp_keywords) if exp_keywords else 1.0
        kw_match = kw_ratio >= 0.5

        case_passed = status_match and citations_match and kw_match
        if case_passed:
            passed_count += 1
            if is_adv:
                adversarial_passed += 1

        res_str = "PASS" if case_passed else "FAIL"
        adv_tag = "YES" if is_adv else "NO"
        status_disp = f"{exp_status[:13]}/{act_status[:13]}"
        cit_disp = "MATCH" if citations_match else "DIFF"
        kw_disp = f"{len(found_keywords)}/{len(exp_keywords)}"

        print(f"{qid:<5} | {as_of:<12} | {adv_tag:<5} | {status_disp:<30} | {cit_disp:<10} | {kw_disp:<10} | {res_str:<6}")

        results.append({
            "id": qid,
            "passed": case_passed,
            "status_match": status_match,
            "citations_match": citations_match,
            "kw_match": kw_match,
            "actual": actual,
            "item": item
        })

    print("-" * 105)
    score_pct = (passed_count / total_count) * 100
    adv_pct = (adversarial_passed / adversarial_total * 100) if adversarial_total else 0

    print("\n" + "=" * 50 + " SUMMARY " + "=" * 50)
    print(f"Total Test Cases      : {total_count}")
    print(f"Passed                : {passed_count}")
    print(f"Failed                : {total_count - passed_count}")
    print(f"Accuracy Rate         : {score_pct:.1f}%")
    print(f"Adversarial Handled   : {adversarial_passed}/{adversarial_total} ({adv_pct:.1f}%)")
    print("=" * 109)

    return passed_count == total_count


if __name__ == "__main__":
    success = run_evaluation()
    sys.exit(0 if success else 1)
