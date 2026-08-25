# Deployment Evidence

`studionet.json` is the machine-readable record for a fresh StudioNet deployment.

Required fields are network, status, chain ID, contract address, deploy transaction hash, source SHA-256, ABI SHA-256, isolated wallet-set identifier, exercised roles, successful write transactions, and read-back assertions.

Lifecycle status alone is not considered success. The final record must confirm execution success and source/schema/state read-back.

Expected constructor: none.
