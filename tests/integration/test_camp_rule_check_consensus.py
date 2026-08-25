"""Five-validator GLSim flow for authority-layer review and exception."""

import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _context():
    validators = get_validator_factory().batch_create_mock_validators(
        5,
        mock_llm_response={"nondet_exec_prompt": {"Apply one frozen camp rule": json.dumps({"result": "REVIEW"})}},
    )
    return {"validators": [validator.to_dict() for validator in validators]}


def test_five_validator_layer_exception_and_resolution():
    coordinator_account, authority_account, camper_account = create_accounts(3)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "camp_rule_check.py")
    deployed = factory.deploy_contract_tx(args=[], account=coordinator_account, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(deployed)
    address = extract_contract_address(deployed)
    coordinator = factory.build_contract(address, account=coordinator_account)
    authority = factory.build_contract(address, account=authority_account)
    camper = factory.build_contract(address, account=camper_account)
    camp_id = f"{str(coordinator_account.address).lower()}:PINE"
    request_id = f"{str(camper_account.address).lower()}:REQUEST-1"
    rule = "Activities after dusk require low light, no amplified sound, and explicit authority review when visitor numbers exceed ten people."
    _ok(coordinator.create_camp(args=["PINE", "Pine learning camp"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(coordinator.add_rule_layer(args=[camp_id, "LAYER-1", authority_account.address, 100, rule, "fixture://camp-rule"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(coordinator.freeze_rule_stack(args=[camp_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(camper.open_request(args=[camp_id, "REQUEST-1", "A twelve-person astronomy lesson proposes shielded red lights, no amplified sound, and a two-hour session after dusk."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(camper.evaluate_layer(args=[request_id, "LAYER-1"]).transact(transaction_context=_context(), wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(camper.request_exception(args=[request_id, "LAYER-1", "The activity uses shielded light and requests a one-time supervised exception."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(authority.decide_exception(args=[request_id, "LAYER-1", True, "Authority grants the supervised one-time exception under the stated controls."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(camper.resolve_request(args=[request_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert camper.get_request(args=[request_id]).call()["status"] == "PERMITTED"
