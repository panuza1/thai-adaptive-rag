# AUCC 2027 requirements verification

Checked 2026-10-29. Sources:
- https://aucc-conf.org/ : conference 3–5 February 2027 at Nakhon Phanom University; homepage submission deadline **4 December 2026**.
- https://aucc-conf.org/submission/ : 2027 portal opens 15 October and deadline **16 November 2026**. This conflicts with homepage. Plan for the earlier date; confirm with organizers before relying on an extension.
- https://aucc-conf.org/submission.php : oral paper 8–10 pages; maximum five authors; signed primary-advisor certification; similarity index <=40%, each primary source <=10%. Host-year requirements take precedence.
- Downloaded https://aucc-conf.org/files/template_oral_english.docx as `aucc_oral_english.docx`; text extracted to `template_extracted.txt`. Template says **5–10 pages**, conflicting with submission page. Target 8–10 to satisfy both, pending confirmation.

Template: English or Thai; abstract 100–150 words; A4, two columns 82 mm wide with 6 mm gap; Times New Roman 10 pt body, 14 pt bold uppercase title, 12 pt authors, 10 pt affiliations, 8 pt captions; first-page top margin 30 mm, other top/bottom margins 25 mm, left 20 mm; numbered IEEE citations in first-use order; no page numbering; grayscale figures. Preserve supplied template geometry rather than reconstructing contradictory dimensions.

The Markdown draft is content preparation, not a typeset or submission-ready paper. Final template placement, page count, visual proof, author/affiliation details, advisor signature, similarity report and deadline reconciliation remain pending. No submission or contact with organizers has been made.

## Follow-up verification and implemented draft

Official homepage, submission information and submission portal were rechecked during validation; the 4 December versus 16 November deadline discrepancy remains. The oral guideline still says 8–10 pages; the retained English template says 5–10. The typeset working draft targets 8–10 pages. Author supplied: Panupong Chaichun, panuponghaichun@gmail.com. Affiliation and advisor remain explicitly pending.

Template rendering and XML audit show two sections with slightly different actual margins from the prose instructions. The manuscript preserves the source section XML, Times New Roman roles, two-column body and grayscale figures. It removes instructional arrows/examples and fills the conference header without inventing an edition number. Original reference bytes and unrelated package parts are checked by hash. Rendering uses the packaged Python renderer with installed LibreOffice because bundled LibreOffice requires unavailable GLIBC 2.38; logs and the fallback wrapper are retained in `paper/qa/`.

No advisor certification, independent human judgments, similarity report, organizer deadline clarification or submission has been completed. These are submission gates, not implied by a correctly formatted draft.
