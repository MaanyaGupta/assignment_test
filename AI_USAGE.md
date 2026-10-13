# AI Usage Log

This document provides a transparent and detailed disclosure of AI tool usage during the completion of this assignment.

---

## Tool Used
- **Assistant**: Antigravity AI Assistant (Google DeepMind Advanced Agentic Coding environment)
- **Role**: Pair-programming assistant and architectural co-pilot

---

## Nature of Collaboration

### 1. Document Analysis & Trap Identification
- The AI was used to cross-examine `policy_master_v1.md`, `circular_2026_08_amendment.md`, and `merchant_faq_2026-03.md`.
- **Key Traps Uncovered**:
  1. **Delayed Effective Date in Circular**: Circular MS/2026/17 had a general effective date of 01 August 2026, but Clause D explicitly deferred its effective date to 01 September 2026. This is crucial for answering Q4 on 20 August 2026 (where Clause 3.3 was still active) versus 5 September 2026 (where Clause 3.3 was deleted).
  2. **The Stale/Erroneous FAQ**: `merchant_faq_2026-03.md` claimed "there is no upper limit on the fee". Master Policy v1.0 Clause 2.3 already had a ₹15 cap in January 2026, meaning the FAQ was inaccurate even when written.
  3. **Transaction Limit Trap (Q3)**: The prompt asked for MDR on a ₹1,50,000 transaction for a large merchant. Clause 4.1 sets a ₹1,00,000 per-transaction limit, which would reject this transaction unless the merchant is in Capital Markets/Insurance and completed enhanced KYC under Annexure C (Clause 4.2 & 4.4).
  4. **Amount Parsing Trap (Q2)**: In the question *"A large merchant (above Rs.10 lakh monthly) receives a Rs.4,000 UPI payment"*, a naive regex would capture `10` from `Rs.10 lakh` instead of `4,000`. The code was engineered to distinguish volume threshold modifiers from payment amounts.

### 2. Code Generation & Architecture
- Structured the modular architecture:
  - `assistant.py`: Core `ask(question, as_of_date)` API, deterministic date parsing, pure Python math engine for MDR/GST, and grounded clause matching.
  - `eval.json`: 15 test cases including 9 adversarial edge cases covering stale FAQs, deleted clauses, missing data, and false premises.
  - `run_eval.py`: Automated testing script printing an ASCII evaluation matrix.
- Implemented deterministic Python math rather than LLM generation to guarantee precision and eliminate hallucinations in fee and tax computations.

### 3. Human Oversight & Verification
- Manually reviewed and verified all mathematical formulas, rate tiers, caps, and GST rules against official policy clauses.
- Executed local tests and Windows console Unicode adjustments (handling ₹ `\u20b9` with UTF-8 reconfigured stdout).
- Validated all 15 test cases against `run_eval.py` (100% pass rate).
