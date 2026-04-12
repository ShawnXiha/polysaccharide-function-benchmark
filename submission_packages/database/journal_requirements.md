# Database Journal Requirements Notes

Official source checked on 2026-03-29:

- Instructions to Authors: <https://academic.oup.com/database/pages/instructions_for_authors>

## Scope fit

- The journal publishes detailed descriptions of databases and database tools in biology, updates to established databases, methodology and technical notes on database development, and ontology-related resources.
- Authors are strongly encouraged to include a biological discovery or a testable hypothesis.

## Key manuscript requirements

- Manuscripts are submitted online.
- Word is preferred, but LaTeX is allowed if necessary.
- Section headings are flexible, but must follow this order:
  - Abstract
  - Introduction
  - Materials and Methods
  - Results
  - Discussion
  - Conclusion
  - Supplementary Data
  - Acknowledgements
  - References
- A `Database URL:` line must appear directly beneath the abstract.
- References must be cited by sequential number only, in order of appearance, and listed numerically.
- Funding should appear in a separate `Funding` section before `Acknowledgements`.
- Figures:
  - minimum 600 dpi for line art
  - minimum 300 dpi for color or greyscale
  - color figures should be CMYK rather than RGB
  - PDF is not an accepted figure format
  - alt text is required for all images
- Tables should be supplied separately from the main body in editable form.
- ORCID is required for the submitting author.

## Current package decisions

- Manuscript section order was adapted to the journal's required order.
- A `Database URL` placeholder line was inserted beneath the abstract.
- Bibliography style was switched to `unsrt` to move toward sequential numbering.
- `Supplementary Data` and `Acknowledgements` sections were added.

## Current compliance status

- Venue-specific manuscript source prepared: yes
- Database URL inserted: placeholder only
- Section order aligned: yes
- Sequential references configured: yes, pending final compile check
- Funding section added: not yet
- Alt text file prepared: yes
- Figure color mode checked for CMYK: not yet
- Figure submission formats checked against OUP preference: partially
