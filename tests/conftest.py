"""Shared direct-mode deployment fixture."""

from pathlib import Path

import pytest

from tests.gltest_windows_compat import install_windows_direct_compatibility


CONTRACT_PATH = Path(__file__).resolve().parents[1] / "contracts" / "camp_rule_check.py"
CONSTRUCTOR_ARGS = ()
DIRECT_SDK_VERSION = "v0.2.16"

install_windows_direct_compatibility()


@pytest.fixture
def contract(direct_vm, direct_deploy, direct_alice):
    direct_vm.sender = direct_alice
    direct_vm.warp("2026-08-25T12:00:00Z")
    return direct_deploy(
        str(CONTRACT_PATH),
        *CONSTRUCTOR_ARGS,
        sdk_version=DIRECT_SDK_VERSION,
    )
