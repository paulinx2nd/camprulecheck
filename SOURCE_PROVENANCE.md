# Source Provenance

## Collection behavior

No web collection occurs. Rules and source references are coordinator declarations, and each source_reference is explicitly unverified.

The contract performs no live web request, does not scrape a page, and does not silently claim that a label or URL authenticates its publisher. This avoids validator drift from changing pages. If an application needs live retrieval, that retrieval belongs in a separately reviewed mechanism whose validators independently fetch and normalize the same source.

## Integrity bindings

- Contract source SHA-256: `4a1896b3514ab84a6379461194e54694960b365948dfead7ccece2ea9fc3e28a`
- ABI SHA-256: `5196014c6fb4e7948361301c42ae6cba195ef004f4a73a4d4cd0cb3738430428`
- Frozen text and canonical JSON records are hashed inside the contract where the workflow needs a content binding.
- Human-readable source references, when present, are expressly marked unverified.

## Fixture policy

Tests use synthetic public fixtures written for this repository. They are not copied production records and do not represent real people.
