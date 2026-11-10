# Releases

Every revision of this specification is published as a GitHub release whose
tag is the version (`v<major>.<minor>.<patch>`) and whose assets are the whole
specification as one PDF and its SHA-256.

1. Bump **Version** and **Date** in `README.md` and add a `CHANGELOG.md` entry.
2. Land the change on `main` after review, then create a signed tag `v<version>`.
3. Render the PDF from the tagged sources only (`git archive v<version>`), in this
   order: `README.md`, `KEY-MAP.md`, `protocol/names.md`, `protocol/issuance.md`,
   `protocol/observation.md`, `protocol/revocation.md`, `decisions/*`, `lips/*`,
   `conformance/README.md`, `LICENSE.md`, `LICENSE-MIT`; Markdown → HTML with pandoc, HTML → PDF
   with WeasyPrint, a serif print theme.
4. Check the PDF: page count, every section title present in `pdftotext` output.
5. Publish: `gh release create v<version> --verify-tag` with
   `swarma-link-spec-v<version>.pdf` and `swarma-link-spec-v<version>.pdf.sha256`.
