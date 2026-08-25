"""Direct tests for layered authorities and exception resolution."""

import json


RULE = "Activities after dusk require low light, no amplified sound, and explicit authority review when visitor numbers exceed ten people."
ACTIVITY = "A twelve-person astronomy lesson proposes shielded red lights, no amplified sound, and a two-hour session after dusk."


def _camp(contract, direct_vm, coordinator, authorities):
    direct_vm.sender = coordinator
    camp_id = contract.create_camp("PINE", "Pine learning camp")
    for index, authority in enumerate(authorities):
        contract.add_rule_layer(
            camp_id,
            f"LAYER-{index + 1}",
            authority,
            100 - index,
            RULE,
            f"fixture://camp-layer-{index + 1}",
        )
    contract.freeze_rule_stack(camp_id)
    return camp_id


def _request(contract, direct_vm, camper, camp_id):
    direct_vm.sender = camper
    return contract.open_request(camp_id, "REQUEST-1", ACTIVITY)


def _evaluate(contract, direct_vm, camper, request_id, layer_id, result):
    direct_vm.sender = camper
    direct_vm.clear_mocks()
    direct_vm.mock_llm(r".*Apply one frozen camp rule.*", json.dumps({"result": result}))
    contract.evaluate_layer(request_id, layer_id)


def test_priorities_must_be_unique(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    direct_vm.sender = direct_alice
    camp_id = contract.create_camp("BAD", "Camp with duplicate priorities")
    contract.add_rule_layer(camp_id, "ONE", direct_bob, 10, RULE, "fixture://one")
    with direct_vm.expect_revert("duplicate_priority"):
        contract.add_rule_layer(camp_id, "TWO", direct_charlie, 10, RULE, "fixture://two")


def test_only_coordinator_builds_rule_stack(contract, direct_vm, direct_alice, direct_bob):
    direct_vm.sender = direct_alice
    camp_id = contract.create_camp("PINE", "Pine learning camp")
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_coordinator"):
        contract.add_rule_layer(camp_id, "ONE", direct_bob, 10, RULE, "fixture://one")


def test_all_permits_resolve_permitted(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    camp_id = _camp(contract, direct_vm, direct_alice, [direct_bob, direct_charlie])
    request_id = _request(contract, direct_vm, direct_alice, camp_id)
    _evaluate(contract, direct_vm, direct_alice, request_id, "LAYER-1", "PERMIT")
    _evaluate(contract, direct_vm, direct_alice, request_id, "LAYER-2", "PERMIT")
    contract.resolve_request(request_id)
    assert contract.get_request(request_id)["status"] == "PERMITTED"


def test_review_requires_authority_exception(contract, direct_vm, direct_alice, direct_bob):
    camp_id = _camp(contract, direct_vm, direct_alice, [direct_bob])
    request_id = _request(contract, direct_vm, direct_alice, camp_id)
    _evaluate(contract, direct_vm, direct_alice, request_id, "LAYER-1", "REVIEW")
    with direct_vm.expect_revert("review_requires_authority_decision"):
        contract.resolve_request(request_id)
    contract.request_exception(request_id, "LAYER-1", "The activity uses shielded light and requests a one-time supervised exception.")
    direct_vm.sender = direct_bob
    contract.decide_exception(request_id, "LAYER-1", True, "Authority grants the supervised one-time exception under the stated controls.")
    direct_vm.sender = direct_alice
    contract.resolve_request(request_id)
    assert contract.get_request(request_id)["status"] == "PERMITTED"


def test_unoverridden_deny_blocks_request(contract, direct_vm, direct_alice, direct_bob):
    camp_id = _camp(contract, direct_vm, direct_alice, [direct_bob])
    request_id = _request(contract, direct_vm, direct_alice, camp_id)
    _evaluate(contract, direct_vm, direct_alice, request_id, "LAYER-1", "DENY")
    contract.resolve_request(request_id)
    assert contract.get_request(request_id)["status"] == "BLOCKED"


def test_only_layer_authority_decides_exception(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    camp_id = _camp(contract, direct_vm, direct_alice, [direct_bob])
    request_id = _request(contract, direct_vm, direct_alice, camp_id)
    _evaluate(contract, direct_vm, direct_alice, request_id, "LAYER-1", "DENY")
    contract.request_exception(request_id, "LAYER-1", "The camper requests a narrowly bounded exception with supervision.")
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_layer_authority"):
        contract.decide_exception(request_id, "LAYER-1", True, "An unrelated account cannot decide this authority layer.")


def test_invalid_layer_output_fails_without_evaluation(contract, direct_vm, direct_alice, direct_bob):
    camp_id = _camp(contract, direct_vm, direct_alice, [direct_bob])
    request_id = _request(contract, direct_vm, direct_alice, camp_id)
    direct_vm.mock_llm(r".*Apply one frozen camp rule.*", json.dumps({"result": "MAYBE"}))
    with direct_vm.expect_revert("invalid_layer_result"):
        contract.evaluate_layer(request_id, "LAYER-1")
    assert contract.get_request(request_id)["evaluations"][0]["result"] == "PENDING"
