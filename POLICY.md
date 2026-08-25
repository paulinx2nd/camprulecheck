# Contract Policy

## Intended use

A reusable multi-authority rule stack where each frozen layer is evaluated independently, only its named authority can grant an exception, and code resolves the combined request.

## Allowed data

- Short reusable identifiers containing ASCII letters, digits, underscore, or hyphen.
- Public descriptions and public evidence within the limits enforced in code.
- Wallet addresses for protocol roles.
- Structured JSON only where the ABI explicitly requires it.

## Forbidden or unsupported use

- Secrets, private personal data, credentials, or confidential files.
- Treating caller-attested text, addresses, source references, quantities, or sensor values as authenticated external facts.
- Treating the result as legal, medical, financial, safety, professional, or identity certification.
- Bypassing an assigned role, prerequisite, state, or terminal transition.

## Error classes

- `[EXPECTED]`: deterministic input, role, state, bound, or business-rule rejection.
- `[LLM_ERROR]`: malformed, out-of-domain, or non-consensual model output; validators should rotate rather than commit it.

## Reuse

The contract can hold multiple independently scoped records over time. Creator-derived identifiers avoid collisions across wallets, and terminal records remain auditable.
