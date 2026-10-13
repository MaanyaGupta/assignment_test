# Where It Breaks

This document identifies three realistic questions that this system cannot reliably answer, gets wrong, or shouldn't be trusted with, along with technical explanations of the root architectural causes.

---

## Question 1: Multi-Hop Cross-Temporal Multi-Event Accounting

### The Question
> *"A merchant on 15 August 2026 received a ₹50,000 payment, which was refunded 2 days later, followed by another ₹30,000 transaction. What is the total fee debited to the merchant across all these transactions?"*

### Why It Breaks / Shouldn't Be Trusted
- **Root Cause**: Stateless Point-in-Time Evaluation.
- **Explanation**: The current system is designed to evaluate a single transaction or policy query given a single `as_of_date`. It does not maintain a multi-event state machine or ledger simulator that tracks sequences of events occurring on different dates with distinct refund latencies (e.g., 2 days > 24 hours vs under 24 hours). Answering this question accurately requires simulating successive balances, checking refund eligibility for individual transaction IDs, and compounding fees.

---

## Question 2: Ambiguous Hybrid Merchant Volume & Volume-Tier Boundaries

### The Question
> *"Our company had exactly ₹10,00,000.00 in UPI transaction volume in July 2026. What is our MDR rate on 15 August 2026 for a ₹3,000 transaction?"*

### Why It Breaks / Shouldn't Be Trusted
- **Root Cause**: Ambiguity in Statutory Threshold Definitions ("up to" vs "above").
- **Explanation**: Master Policy Clause 2.1 specifies: *"merchants with monthly volume up to ₹10 lakh is 0.30% (amended to 0.25%)"*. Clause 2.2 specifies: *"merchants with monthly volume above ₹10 lakh is 0.50%"*. While a strict mathematical boundary places ₹10,00,000 in the "up to" tier, in payment banking practice, volume tiering often looks at preceding calendar month vs rolling 30-day window, or includes/excludes refunds and failed transactions. Our system does not ingest raw billing volume logs; if the prompt does not explicitly declare the tier as "small" or "large", it must infer it from linguistic cues, which can fail on boundary cases.

---

## Question 3: Obfuscated or Highly Domain-Paraphrased Terminology

### The Question
> *"Our client's client reversed a remittance three hours post-settlement. Will the discount percentage charged be credited back to our ledger?"*

### Why It Breaks / Shouldn't Be Trusted
- **Root Cause**: Reliance on Standard Policy Terminology.
- **Explanation**: The system's deterministic intent router looks for canonical payment terminology such as `refund`, `reversal`, `mdr`, `fee`, `upi`, etc. When users formulate inquiries using non-standard financial synonyms (*"reversed a remittance"* instead of *"refunded a payment"*, *"discount percentage"* instead of *"MDR"*, *"credited back to our ledger"* instead of *"MDR reversed"*), a strict keyword/regex pattern matcher may fail to trigger the refund fee reversal branch and fall back to `CANNOT_ANSWER`. While this preserves safety by avoiding hallucinated answers, it causes false negatives for heavily paraphrased inputs.
