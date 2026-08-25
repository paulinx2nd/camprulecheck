# Reviewer Guide

## Mechanism in one sentence

A reusable multi-authority rule stack where each frozen layer is evaluated independently, only its named authority can grant an exception, and code resolves the combined request.

## What consensus actually decides

Validators agree on PERMIT, DENY, or REVIEW separately for each authority layer.

## What code settles afterward

Pending layers and exceptions block resolution; any non-granted DENY or REVIEW produces BLOCKED, otherwise the request becomes PERMITTED.

## Why this is distinct

It composes multiple governed decisions with authority-specific exception rights instead of renaming one assessment protocol.

## Fast review path

1. Confirm the pinned dependency on the first source line.
2. Inspect the custom validator and verify it reruns the substantive task.
3. Trace role checks and terminal-state guards in each write method.
4. Run lint, strict type checking, seven direct tests, and the five-validator integration test.
5. Compare `abi.json` and the StudioNet manifest to the committed source hash.

## Known limitations

Authority wallet assignment is not identity verification. Rule completeness and source authenticity remain the coordinator's responsibility.
