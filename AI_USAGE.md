# AI Usage Log

This document outlines the division of work between the candidate (human reasoning, domain analysis, policy interpretation, and system architecture) and AI assistance (code generation, boilerplate scaffolding, and test harness implementation).

---

## Tool Used
- **Assistant**: Antigravity AI Assistant (Google DeepMind Advanced Agentic Coding environment)
- **Role**: Code generation assistant and implementation partner operating under explicit human direction.

---

## Division of Responsibilities

### 1. Human (Candidate) Contributions: Strategy, Analysis & Reasoning

All critical domain analysis, policy reconciliation, and architectural choices were reasoned and driven by the candidate:

- **Policy Reconciliation & Legal Hierarchy**:
  - Analyzed the three conflicting documents (`policy_master_v1.md`, `circular_2026_08_amendment.md`, `merchant_faq_2026-03.md`).
  - Formulated the binding legal authority hierarchy: `Statutory Amendment Circular > Master Policy Contract > Marketing/Support FAQ`.
  - Identified that the March 2026 FAQ's claim of *"no upper limit on the fee"* was factually false under the governing Master Policy (Clause 2.3 cap of ₹15) and statutory Amendment Circular (Clause C caps of ₹15/₹25).
- **Temporal Validity Analysis**:
  - Detected the delayed effective date in Circular MS/2026/17 (Clause D took effect on **01 September 2026**, while Clauses A–C took effect on **01 August 2026**).
  - Designed the temporal resolution for refund fee reversal: on 20 August 2026, Clause 3.3 remains in full effect (MDR reversed), whereas on 5 September 2026, Clause 3.3 is deleted (MDR retained under Clause 3.2).
- **Boundary & Exception Logic (Q3 & Limits)**:
  - Identified the hidden limit violation in Question 3: a ₹1,50,000 transaction exceeds the standard UPI per-transaction limit of ₹1,00,000 (Clause 4.1) and is only legally permissible for Capital Markets/Insurance merchants with Annexure C enhanced KYC (Clause 4.2 & 4.4).
- **Adversarial Test Suite Design**:
  - Authored the specifications and golden answers for the evaluation dataset (`eval.json`), ensuring coverage across 9 adversarial stress tests (testing stale FAQs, deleted clauses, false premises, and ungrounded payment rails).
- **Code Review & Quality Control**:
  - Audited the AI-generated code.
  - Caught edge case bugs during execution (e.g., identifying when regex matched the merchant volume threshold of ₹10 lakh instead of the payment amount of ₹4,000, and enforcing proper separation).
  - Validated that all 15 evaluation tests pass with 100% accuracy.

---

## 2. AI Assistant Contributions: Coding & Implementation

Under the candidate's exact specifications and architectural directives, the AI was leveraged for rapid code implementation:

- **Module Implementation (`assistant.py`)**:
  - Generated the Python code for `ask(question, as_of_date)`.
  - Implemented the deterministic arithmetic calculator for base rates, caps, and 18% GST outside the cap.
  - Coded the date parsing routines and regex matchers for extracting payment values.
- **Evaluation Runner (`run_eval.py`)**:
  - Implemented the score table formatting script that evaluates status accuracy, citation precision, and keyword overlap.
- **Interactive Interfaces (`cli.py`, `app.py`)**:
  - Built the interactive terminal shell (`cli.py`) with sample selectors and date switching.
  - Built the zero-dependency local web server (`app.py`) using Python's standard library `http.server` with a modern dark-mode frontend.
- **Boilerplate & Formatting**:
  - Structured the JSON schema for `eval.json` and formatted documentation markdown files.
