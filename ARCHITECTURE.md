# Architecture

## Boundary

- Frontend or backend: wallet UX, indexing, private drafts, non-authoritative previews, notifications, and optional off-chain source retrieval.
- GenLayer contract: Validators agree on PERMIT, DENY, or REVIEW separately for each authority layer. Pending layers and exceptions block resolution; any non-granted DENY or REVIEW produces BLOCKED, otherwise the request becomes PERMITTED.
- External world: No web collection occurs. Rules and source references are coordinator declarations, and each source_reference is explicitly unverified.

## Event path

create camp -> add prioritized authority layers -> freeze stack -> open request -> evaluate every layer -> optional exceptions -> resolve

## Actors

- camp coordinator
- layer authorities
- camper
- GenLayer validators

## Consensus design

The leader produces a normalized bounded result. Each validator independently reruns the substantive task from the same frozen public inputs. Validators compare the decision fields that change state, not merely JSON shape. Invalid model output raises `[LLM_ERROR]` so a broken leader is not accepted.

## Deterministic layer

Pending layers and exceptions block resolution; any non-granted DENY or REVIEW produces BLOCKED, otherwise the request becomes PERMITTED. Identifiers, bounds, access checks, ordering, counters, masks, hashes, and terminal-state guards are computed deterministically.

## Persistence

State uses GenLayer storage types only. Public composite records are serialized as canonical JSON where appropriate. Source SHA-256 at evidence generation: `4a1896b3514ab84a6379461194e54694960b365948dfead7ccece2ea9fc3e28a`.
