# CampRuleCheck

A reusable multi-authority rule stack where each frozen layer is evaluated independently, only its named authority can grant an exception, and code resolves the combined request.

## Why GenLayer

Validators agree on PERMIT, DENY, or REVIEW separately for each authority layer. Pending layers and exceptions block resolution; any non-granted DENY or REVIEW produces BLOCKED, otherwise the request becomes PERMITTED.

## Roles

- camp coordinator
- layer authorities
- camper
- GenLayer validators

## Lifecycle

create camp -> add prioritized authority layers -> freeze stack -> open request -> evaluate every layer -> optional exceptions -> resolve

## Contract interface

- Constructor: none
- Write methods: add_rule_layer, create_camp, decide_exception, evaluate_layer, freeze_rule_stack, open_request, request_exception, resolve_request
- View methods: get_camp, get_camp_count, get_camp_id, get_request, get_request_count, get_request_id
- Runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

## Public-data warning

All contract inputs, evidence, notes, addresses, model results, and state are public. Do not submit secrets, private documents, personal contact information, or confidential identifiers.

## Source model

No web collection occurs. Rules and source references are coordinator declarations, and each source_reference is explicitly unverified.

## Verification

```text
genvm-lint check contracts/camp_rule_check.py
genvm-lint typecheck contracts/camp_rule_check.py --strict
python -m pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
python -m pytest tests/integration -q -s
```

The repository contains seven direct tests and one full five-validator GLSim flow. StudioNet evidence is recorded separately under `deployments/` after network execution.

## Limitations

Authority wallet assignment is not identity verification. Rule completeness and source authenticity remain the coordinator's responsibility.

Licensed under MIT. See `LICENSE`.
