---
name: wop-invoice-generator
description: Generate single-page WOP Sdn Bhd invoice PDF.
capability_tier: fed-long-context
ecology_state: WARM
---

# Web Of Projects (WOP) Invoice Generator

Generate clean, professional single-page PDF invoices for **Web Of Projects Sdn. Bhd.** in a reuseable format.

## When to load this skill

- User asks to "generate an invoice", "buatkan invoice", "invoice baru"
- User pastes/sends vendor, bill-to, line items, payment details
- User iterates on a draft invoice already in progress

## Format standard

- **Invoice number convention:** `YYYYMMDD-NNN` (e.g., `20260801-001`)
- **Invoice date:** explicit date provided by user; never invent
- **Layout:** single page, vertical sections, dark borders only where they group content
- **No SST/tax line unless specified**

## Document structure (top to bottom)

1. Header bar — `INVOICE` (large, letter-spaced)
2. Vendor (left) + Invoice No / Date (right)
3. Bill To box (single bordered box, multi-line address)
4. Items table — columns: No, Description, Qty (center), Unit Price (right), Amount (right)
5. Totals table (right-aligned, width ~320px) — Subtotal, Tax, Total Contract Value (border-top)
6. Optional **Payment Schedule** sub-table when installments apply — Milestone / Percentage / Amount / Due Period + tfoot Total row
7. Payment Information box (bordered, light bg) — Account Name, Bank, Account No
8. Footer line — *Issued by Web Of Projects Sdn. Bhd.*

## Defaults to remember

- Account name: `Web Projects Sdn. Bhd.` (no "Of")
- Bank: Maybank Berhad
- Account No: `5686 0301 9472`

If user supplies *different* payment info, use theirs and override the default.

## Generation procedure

1. Capture from user:
   - Bill To (company name + address)
   - Item description
   - Quantity + unit price
   - Tax rate (default 0%)
   - Date (explicit; never back-date without confirmation)
   - Invoice number (or default to today's date)
   - Payment terms (single full payment vs. installment schedule)

2. For installments:
   - Compute milestone amounts (each milestone % × total = amount; all milestones sum to total)
   - Use sub-table: Milestone / Percentage / Amount / Due Period
   - Specify due period verbatim from user (e.g., "Within August 2026")

3. Build HTML template at `/tmp/invoice_wop.html`. Use `&amp;` for ampersands; `&mdash;` for empty cells.

4. Render via `weasyprint` (wkhtmltopdf NOT installed):
   ```bash
   weasyprint /tmp/invoice_wop.html /tmp/invoice.pdf
   ```

5. Verify:
   ```bash
   ls -la /tmp/invoice.pdf
   ```

6. Deliver via `MEDIA:/absolute/path/to/invoice.pdf`.

## Verification before delivery

- File exists, > 5KB
- Total math: sum(line items) == subtotal == total
- For installments: sum(milestone amounts) == total
- Vendor/issuer name spelled consistently
- Date spelled out ("1 August 2026")

## Tone rules

- Output minimal — file + 1-line summary
- Don't repeat line items back to user after delivery
- Flag anything you assumed (default tax rate, default invoice number pattern)

## Common mistakes to avoid

- Inventing dates
- Auto-assuming installment terms (always ask if unclear)
- 4 decimal places on round numbers
- Adding SST line unless rate specified
- Forgetting payment info box on subsequent invoices

## Output language

Match user's input language.