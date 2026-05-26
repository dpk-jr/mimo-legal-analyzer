# MiMo Legal Analyzer

AI-powered contract review and legal document analysis.

> MiMo 100T Program — intelligent legal tech

---

## What It Does

Upload a contract → MiMo extracts clauses, identifies risks, tracks obligations, checks compliance.

## Features

| Feature | Description |
|---------|-------------|
| **Clause Extraction** | Identify and categorize all contract clauses |
| **Risk Scoring** | Flag ambiguous, missing, or unfavorable terms |
| **Obligation Tracking** | Who owes what to whom, deadlines, penalties |
| **Compliance Check** | GDPR, SOX, HIPAA, industry standards |
| **Contract Comparison** | Side-by-side diff of two contracts |

## Usage

```bash
# Analyze a contract
python main.py analyze contract.pdf

# Check compliance
python main.py compliance contract.pdf --standard gdpr

# Extract obligations with timeline
python main.py obligations contract.pdf --timeline

# Compare two contracts
python main.py compare old_contract.pdf new_contract.pdf

# Risk assessment
python main.py risks contract.pdf --severity high
```

## Example Output

```
Contract Analysis: Series_A_Termsheet.pdf
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Parties: [Company] vs [Investor]
Governing Law: Delaware
Total Clauses: 47

Risk Flags:
  CRITICAL  Section 4.2 — Broad drag-along rights with no floor price
  HIGH      Section 7.1 — Unlimited indemnification with no cap
  MEDIUM    Section 3.4 — Vague "material adverse change" definition
  LOW       Section 9.3 — Standard non-compete (12 months)

Obligations Timeline:
  Day 0    — Execution by both parties
  Day 30   — Company provides audited financials
  Day 60   — Investor wires funds
  Day 90   — Board reconstitution
  Ongoing  — Quarterly reporting, information rights

Missing Clauses:
  * No force majeure provision
  * No dispute resolution mechanism
  * No data protection addendum
```

## Why MiMo?

- **Legal reasoning**: Understands contract language and implications
- **Risk assessment**: Contextual risk scoring, not just keyword matching
- **Compliance knowledge**: GDPR, SOX, HIPAA requirements built-in

---

*Powered by Xiaomi MiMo-V2.5-Pro*
