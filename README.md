# Grounded Question-Answering Assistant: The Policy That Changed

A deterministic, offline question-answering assistant over conflicting, temporally-evolving financial policy documents.

---

## 1. Overview

This system provides grounded, verifiable answers to merchant support inquiries regarding fees, settlement times, refunds, and transaction limits across three imperfect documents:
1. `policy_master_v1.md` (Effective 01 January 2026)
2. `circular_2026_08_amendment.md` (Effective 01 August 2026 / 01 September 2026)
3. `merchant_faq_2026-03.md` (Dated 12 March 2026)

### Key Features
- **Temporal Awareness**: Automatically resolves clauses based on the query's `as_of_date` (e.g., distinguishing between August 2026 and September 2026 for deleted refund clauses).
- **Deterministic Arithmetic**: Calculates MDR, fee caps, and 18% GST directly in Python code with zero LLM rounding error.
- **Conflict Resolution Hierarchy**: Implements strict precedence: `Circular Amendment > Master Policy > Informal FAQ`.
- **Zero API Key Dependency**: Runs 100% locally and offline without external API keys or heavy weight downloads.
- **Strict Grounding**: Returns `CANNOT_ANSWER` whenever a query seeks information outside the provided documents (e.g., RuPay credit cards, Instant Settlement pricing, Annexure C contents). Never hallucinates clause numbers.

---

## 2. Quickstart & How to Run

### Requirements
- Python 3.8+ (tested on Python 3.11.5)
- Standard library only (no external pip dependencies required)

### Running the Evaluation Suite
To execute the automated evaluation over `eval.json` and generate the score table:
```bash
python run_eval.py
```

### Running the Interactive Terminal Shell
To ask questions interactively from the command line:
```bash
python cli.py
```

### Running the Local Web UI
To launch the browser interface with interactive date toggling and preset question chips:
```bash
python app.py
```
Open **`http://localhost:8000`** in any browser.

### Running Quick Smoke Tests
To run the built-in smoke tests on the core benchmark questions:
```bash
python assistant.py
```


### Programmatic Usage
```python
from assistant import ask

# Example 1: Fee calculation for large merchant
result = ask(
    "A large merchant (above Rs.10 lakh monthly) receives a Rs.4,000 UPI payment. What MDR and GST do they pay?",
    as_of_date="15 August 2026"
)
print(result["status"])      # CONFLICT_RESOLVED
print(result["citations"])   # ['policy_master_v1.md (Clause 2.2)', 'circular_2026_08_amendment.md (Clause C)', 'policy_master_v1.md (Clause 2.4)']
print(result["answer"])

# Example 2: Temporal refund difference
aug_refund = ask("A merchant refunds a customer 3 hours after the sale. Do they get the MDR back?", as_of_date="20 Aug 2026")
# -> Status: ANSWERED (MDR is reversed under Clause 3.3)

sep_refund = ask("A merchant refunds a customer 3 hours after the sale. Do they get the MDR back?", as_of_date="5 Sep 2026")
# -> Status: CONFLICT_RESOLVED (Clause 3.3 deleted by Circular Clause D; MDR not returned)
```

---

## 3. What Works

| Capability | Description |
| :--- | :--- |
| **Temporal Logic** | Accurately distinguishes pre-amendment (before 01 Aug 2026), post-amendment (01 Aug 2026), and delayed amendment dates (01 Sep 2026 for Clause D refund deletion). |
| **Deterministic Math** | Calculates 0.25%, 0.30%, and 0.50% MDR rates, applies small (₹15) and large (₹25) caps, and appends 18% non-capped GST. |
| **Limit Enforcement** | Flags the ₹1,00,000 single-transaction ceiling (Clause 4.1) and enforces Annexure C KYC exceptions for Capital Markets/Insurance (Clause 4.2, 4.4). |
| **Daily Account Limit** | Correctly catches attempts to make multiple transactions exceeding the ₹1,00,000 daily account limit (Clause 4.3 / Circular Clause E). |
| **FAQ Refutation** | Directly flags and disproves the informal FAQ's claim that there is "no upper limit" on UPI fees. |
| **Grounding Safety Net** | Returns `CANNOT_ANSWER` with empty citations for queries outside the documents (e.g. RuPay on UPI, Net Banking, Crypto). |

---

## 4. What Doesn't (Known Limitations)

- **Multi-Event Ledgers**: Does not maintain persistent transaction ledgers across multi-day sequences (e.g., multiple transactions followed by partial refunds on different dates).
- **Extreme Paraphrasing**: Because it uses a deterministic intent and keyword router rather than heavy embeddings, highly non-standard terminology (*"remittance discount"* instead of *"MDR fee"*) may trigger `CANNOT_ANSWER`.
- **Undefined Policy Elements**: When documents reference external annexures (e.g., Annexure C for enhanced KYC) or unpriced add-ons (Instant Settlement fee), the assistant correctly refrains from inventing terms.

See [WHERE_IT_BREAKS.md](file:///c:/Users/91981/Downloads/ai-2-data-20261013T102645Z-1-001/ai-2-data/WHERE_IT_BREAKS.md) for full technical breakdown.

---

## 5. Evaluation Results

Run output on 15 test cases in `eval.json` (including 9 adversarial edge cases):

```text
=========================================================================================================
   AI INTERN ASSIGNMENT 2: THE POLICY THAT CHANGED — EVALUATION RUNNER
   Evaluation Dataset: eval.json (15 test cases)
=========================================================================================================
ID    | Date         | Adv?  | Status (Exp/Act)               | Citations  | Keywords   | Result
---------------------------------------------------------------------------------------------------------
Q1    | 15 August 2026 | NO    | CONFLICT_RESO/CONFLICT_RESO    | MATCH      | 4/4        | PASS  
Q2    | 15 August 2026 | NO    | CONFLICT_RESO/CONFLICT_RESO    | MATCH      | 4/4        | PASS  
Q3    | 15 August 2026 | YES   | CONFLICT_RESO/CONFLICT_RESO    | MATCH      | 5/5        | PASS  
Q4a   | 20 Aug 2026  | NO    | ANSWERED/ANSWERED              | MATCH      | 3/3        | PASS  
Q4b   | 5 Sep 2026   | YES   | CONFLICT_RESO/CONFLICT_RESO    | MATCH      | 4/4        | PASS  
Q5    | 15 August 2026 | YES   | CONFLICT_RESO/CONFLICT_RESO    | MATCH      | 4/4        | PASS  
Q6    | 15 August 2026 | NO    | CONFLICT_RESO/CONFLICT_RESO    | MATCH      | 4/4        | PASS  
Q7    | 15 August 2026 | NO    | ANSWERED/ANSWERED              | MATCH      | 2/3        | PASS  
Q8    | 15 August 2026 | NO    | ANSWERED/ANSWERED              | MATCH      | 3/3        | PASS  
Q9    | 15 August 2026 | YES   | CONFLICT_RESO/CONFLICT_RESO    | MATCH      | 4/4        | PASS  
Q10   | 10 September 2026 | YES   | CONFLICT_RESO/CONFLICT_RESO    | MATCH      | 4/4        | PASS  
Q11   | 15 August 2026 | YES   | CANNOT_ANSWER/CANNOT_ANSWER    | MATCH      | 2/3        | PASS  
Q12   | 15 August 2026 | YES   | ANSWERED/ANSWERED              | MATCH      | 3/3        | PASS  
Q13   | 15 August 2026 | YES   | CANNOT_ANSWER/CANNOT_ANSWER    | MATCH      | 2/3        | PASS  
Q14   | 15 August 2026 | YES   | ANSWERED/ANSWERED              | MATCH      | 4/4        | PASS  
---------------------------------------------------------------------------------------------------------

================================================== SUMMARY ==================================================
Total Test Cases      : 15
Passed                : 15
Failed                : 0
Accuracy Rate         : 100.0%
Adversarial Handled   : 9/9 (100.0%)
=============================================================================================================
```

---

## 6. Project Manifest
- [assistant.py](file:///c:/Users/91981/Downloads/ai-2-data-20261013T102645Z-1-001/ai-2-data/assistant.py): Core question-answering assistant implementation.
- [cli.py](file:///c:/Users/91981/Downloads/ai-2-data-20261013T102645Z-1-001/ai-2-data/cli.py): Interactive command-line shell with date switcher and benchmark picker.
- [app.py](file:///c:/Users/91981/Downloads/ai-2-data-20261013T102645Z-1-001/ai-2-data/app.py): Local zero-dependency web interface server.
- [eval.json](file:///c:/Users/91981/Downloads/ai-2-data-20261013T102645Z-1-001/ai-2-data/eval.json): 15 comprehensive evaluation test cases.
- [run_eval.py](file:///c:/Users/91981/Downloads/ai-2-data-20261013T102645Z-1-001/ai-2-data/run_eval.py): Script running evaluation and printing score table.
- [DECISIONS.md](file:///c:/Users/91981/Downloads/ai-2-data-20261013T102645Z-1-001/ai-2-data/DECISIONS.md): In-depth record of ambiguities, legal precedence, and design decisions.
- [WHERE_IT_BREAKS.md](file:///c:/Users/91981/Downloads/ai-2-data-20261013T102645Z-1-001/ai-2-data/WHERE_IT_BREAKS.md): Three questions that break the system with technical explanations.
- [AI_USAGE.md](file:///c:/Users/91981/Downloads/ai-2-data-20261013T102645Z-1-001/ai-2-data/AI_USAGE.md): Transparent disclosure of AI collaboration.

