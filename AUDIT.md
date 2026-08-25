# Audit Record

Audit date: 2026-08-25

## Automated results

- GenVM lint and SDK validation: PASS
- Strict Pyright through genvm-lint: PASS
- Direct-mode tests: 7 PASS
- Five-validator GLSim integration: 1 PASS
- ABI regenerated from final source: PASS
- Pinned runner header: PASS
- Dependency vulnerability audit: PASS, zero known vulnerabilities
- Full-workspace structural originality scan: PASS, 121 contracts scanned; every nearest external match is below 0.35 and has a different public method shape
- StudioNet: PASS - fresh owner-isolated wallets, all transactions finalized and executed successfully, deployed source/schema matched, and mechanism-specific bound state read back
- GitHub publication: PASS - private remote and clean one-commit reachable history verified

## Artifact hashes

- Source: `4a1896b3514ab84a6379461194e54694960b365948dfead7ccece2ea9fc3e28a`
- ABI: `5196014c6fb4e7948361301c42ae6cba195ef004f4a73a4d4cd0cb3738430428`

## Manual findings

The substantive validator independently reruns the task. The contract documents caller-attested source limitations, public-data exposure, role boundaries, terminal states, and residual risk. It composes multiple governed decisions with authority-specific exception rights instead of renaming one assessment protocol. The StudioNet manifest records the contract address, transaction receipts, fresh public test roles, exact source and schema readback, and the mechanism-specific terminal assertion.
