# Architecture & Policy Decisions Log

This document records every ambiguity, contradiction, and edge case encountered in the policy documents, along with the reasoning behind the architectural choices and interpretations implemented in the assistant.

---

## 1. Document Precedence & Legal Authority Hierarchy

### Ambiguity Encountered
The workspace contains three documents with overlapping and conflicting clauses:
1. `policy_master_v1.md` (Effective 01 January 2026) — Master policy contract.
2. `circular_2026_08_amendment.md` (Issued 20 July 2026, Effective 01 August 2026 / 01 September 2026) — Formal regulatory amendment circular.
3. `merchant_faq_2026-03.md` (Last updated 12 March 2026) — Informal support FAQ.

### Decision
We established an explicit hierarchical legal priority model:
$$\text{Circular MS/2026/17} \succ \text{Policy Master Document v1.0} \succ \text{Merchant FAQ}$$

- **Statutory Circulars override Master Policies**: Where a circular explicitly amends or deletes a clause (e.g., Clause 1.1, 2.1, 2.3, 3.3, 4.3), the circular's terms supersede the master document as of the circular's stated effective date.
- **Informal FAQs do not create policy**: FAQs are non-binding informational summaries. Where an FAQ contradicts the Master Document or Circular (or omits legal conditions such as "working days" or fee caps), the governing legal documents prevail. When an FAQ contradiction is detected, the status is set to `CONFLICT_RESOLVED`, citing both the faulty FAQ and the governing clause.

---

## 2. Temporal Validity & Delayed Effective Dates

### Ambiguity Encountered
Circular MS/2026/17 states in its header:
> *"Effective 01 August 2026 unless stated otherwise"*

However, Clause D of the Circular specifies:
> *"D. Clause 3.3 is deleted. Clause 3.2 now applies without exception. (Effective 01 September 2026.)"*

### Trap & Resolution
A naive system applying Circular MS/2026/17 globally as of 01 August 2026 would erroneously delete Clause 3.3 for queries in August 2026.
- **On 20 August 2026**: Clause 3.3 was **still in active effect**. A merchant initiating a refund within 24 hours receives the MDR back in full (`policy_master_v1.md` Clause 3.3). Status is `ANSWERED`.
- **On 05 September 2026**: Clause D took effect on 01 September 2026, permanently deleting Clause 3.3. Under Clause 3.2 (which now applies without exception), MDR is **never returned** to the merchant. Status is `CONFLICT_RESOLVED`.

---

## 3. The FAQ MDR Cap Contradiction (Q5)

### Contradiction Encountered
In `merchant_faq_2026-03.md`, the FAQ claims:
> *"There is no upper limit on the fee, so very large transactions cost more."*

### Resolution
This statement is factually incorrect and contradicted official policy even when the FAQ was written in March 2026:
- Under Master Policy v1.0 Clause 2.3 (effective 01 Jan 2026), MDR was capped at ₹15 for all UPI transactions.
- Under Circular MS/2026/17 Clause C (effective 01 Aug 2026), the cap was updated to ₹15 (small merchants) and ₹25 (large merchants).
The system explicitly identifies that the FAQ is wrong, explains why, and provides the binding cap with citations (`merchant_faq_2026-03.md`, `policy_master_v1.md (Clause 2.3)`, `circular_2026_08_amendment.md (Clause C)`).

---

## 4. Single-Transaction Limits vs Fee Calculation (Q3)

### Ambiguity Encountered
Question 3 asks: *"Same merchant, a Rs.1,50,000 payment. What do they pay?"*

### Trap & Resolution
There is a critical boundary condition trap:
1. **Limits Clause**: Master Policy Clause 4.1 sets the maximum per-transaction UPI limit at **₹1,00,000**.
2. **Category Exception**: Clause 4.2 & 4.4 allow transactions up to **₹2,00,000** *only* for merchants in "Capital Markets" and "Insurance" who have completed enhanced KYC (Annexure C).
3. If the merchant is a standard retail merchant, a payment of ₹1,50,000 is **not permitted**.
4. If eligible under the exception, the fee arithmetic is:
   - Uncapped MDR: $0.50\% \times 1,50,000 = ₹750$
   - Cap (Circular Clause C): ₹25.00
   - Final MDR: ₹25.00
   - GST @ 18% (Clause 2.4, outside cap): $18\% \times 25 = ₹4.50$
   - Total Fee: ₹29.50

**Decision**: The assistant calculates the deterministic fee (₹29.50) while explicitly flagging the ₹1,00,000 transaction limit and the required Annexure C KYC condition.

---

## 5. Settlement Timelines & Add-On Qualification (Q1, Q8)

### Ambiguity Encountered
- Policy Master 1.1 specified T+1 for all UPI.
- Circular Clause A amended Clause 1.1: T+0 (same day by 11:59 PM) for merchants with an active "Instant Settlement" add-on, and T+1 for all others.
- Question 8 asks if card payments can be settled same-day.

### Resolution
- For UPI on or after 01 August 2026, settlement is conditional: T+0 for add-on holders, T+1 for standard merchants (`CONFLICT_RESOLVED`).
- For Card transactions, Circular Clause A applies *only* to UPI. Circular Clause F affirms all other clauses remain unchanged. Hence, card payments remain strictly T+2 (`policy_master_v1.md` Clause 1.2).

---

## 6. Grounding Boundaries & Out-of-Scope Queries

### Ambiguity Encountered
Questions asking about:
- RuPay credit card on UPI fees
- Monthly cost or enrollment procedure for the Instant Settlement add-on
- Checklist of documents required under Annexure C
- Net banking, NEFT, or crypto settlement

### Resolution
Rather than guessing or synthesizing external banking knowledge, the assistant strictly outputs `CANNOT_ANSWER` with an empty citation list (or citation to the mentioning clause if pointing out that details are omitted). This ensures 100% precision against hallucination.

---

## 7. Deterministic Code vs LLM Arithmetic

### Decision
Language models frequently make rounding mistakes, hallucinate rates, or misapply non-inclusive GST rules. All calculations (base rate percentage, volume tier selection, fee cap ceiling, 18% GST outside cap, and total fee) are executed purely in Python code.
