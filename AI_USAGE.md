# AI Usage Log

This document transparently describes how Antigravity AI assisted with
the assignment and distinguishes that assistance from my analysis,
review, and verification. AI tools were permitted for this assignment,
but the final implementation and its limitations must be understood and
explainable.

------------------------------------------------------------------------

## Tool Used

-   **Assistant:** Antigravity AI Assistant (Google DeepMind agentic
    coding environment)
-   **Role:** AI-assisted pair programmer for document analysis,
    implementation, evaluation scaffolding, and troubleshooting.

## 1. Human Contribution: Analysis, Decisions, and Oversight

My contribution focused on understanding the policy problem, reviewing
the intended behavior, considering edge cases, and checking the
resulting implementation.

-   **Policy reconciliation:** Reviewed the three supplied
    documents---`policy_master_v1.md`, `circular_2026_08_amendment.md`,
    and `merchant_faq_2026-03.md`---to understand where their claims
    differed. The solution treats the policy and applicable circular as
    governing sources rather than blindly accepting the FAQ.
-   **Temporal reasoning:** Considered the difference between the
    circular's general effective date of 1 August 2026 and Clause D's
    deferred effective date of 1 September 2026. This distinction
    affects the refund question asked for 20 August and 5 September
    2026.
-   **Transaction-limit reasoning:** Identified that a ₹1,50,000
    transaction exceeds the standard ₹1,00,000 limit and that the stated
    exception depends on merchant category and enhanced KYC under
    Annexure C.
-   **Calculation review:** Reviewed the intended separation between
    policy selection and deterministic MDR/GST arithmetic, including
    rates, caps, and GST treatment, against the supplied policy text.
-   **Adversarial cases:** Focused on failure modes the assistant should
    handle, including a stale FAQ, a deleted clause, missing policy
    details, false premises, and confusion between monthly merchant
    volume and the actual payment amount.
-   **Verification:** The project log records that the local evaluation
    suite was run and all 15 test cases passed. This result applies to
    the cases and checks in that suite; it does not prove correctness
    for every possible question.

These points describe the reasoning and review performed during the
work. Antigravity also helped identify document traps and translate the
intended behavior into implementation, so the analysis should be
understood as AI-assisted rather than wholly independent of AI.

## 2. AI Assistant Contributions: Analysis and Implementation Assistance

Antigravity was used as a pair-programming and implementation assistant.
Its assistance included:

-   **Document analysis:** Cross-checking the supplied documents and
    surfacing contradictions, effective-date details, and exception
    conditions.
-   **Core implementation (`assistant.py`):** Generating and refining
    the `ask(question, as_of_date)` logic, date parsing, rule matching,
    currency-amount extraction, citations, response statuses, and
    deterministic fee calculations.
-   **Fee calculation logic:** Implementing the Python calculations for
    MDR rates, caps, and 18% GST, along with checks for the documented
    transaction-limit exception.
-   **Evaluation support (`eval.json`, `run_eval.py`):** Helping
    structure evaluation cases and implement a runner that compares
    results and prints a score table.
-   **Interfaces (`cli.py`, `app.py`):** Assisting with the interactive
    command-line interface and local web interface, if these files are
    included in the submitted repository.
-   **Troubleshooting and documentation:** Helping with Windows console
    UTF-8 output and preparing Markdown documentation.

## 3. Verification and Limitations

The implementation uses deterministic Python rules and calculations
rather than relying on an LLM to calculate fees at runtime. The
question-answering behavior is primarily rule- and keyword-based; it is
not a general-purpose semantic retrieval system, so unfamiliar phrasing
may not match the intended rule.

The evaluation result should be interpreted in context: a 100% pass rate
means the tested cases passed the checks implemented in the evaluation
runner. It is not a guarantee of correctness on unseen inputs. The code
may also return a fee calculation together with a transaction-limit
warning rather than preventing the calculation for an invalid
transaction; this behavior should be considered when interpreting Q3.

I am responsible for understanding the submitted solution, explaining
the policy decisions and limitations, and accurately describing which
work was AI-assisted. This log is intended as an honest disclosure, not
a claim that all code was written independently.
