from __future__ import annotations

import contextlib
import json
import typing as t

from aiida import load_profile, orm
from aiida.common.exceptions import NotExistent

_ = load_profile()


class AiiDAService:
    @staticmethod
    def load_qe_app_workflow_node(pk: int) -> t.Optional[orm.WorkChainNode]:
        with contextlib.suppress(NotExistent):
            process = orm.load_node(pk)
            if (
                isinstance(process, orm.WorkChainNode)
                and process.process_label == "QeAppWorkChain"
            ):
                return process

    @staticmethod
    def submit(data: dict):
        label = data.pop("label", "Untitled Workflow")
        description = data.pop("description", "No description provided")
        print(f"Submitting {label} ({description}) with the following inputs:")
        print(json.dumps(data, indent=2))

    @staticmethod
    def load_code(code: str) -> t.Optional[orm.Code]:
        try:
            return orm.load_code(code)
        except NotExistent:
            raise ValueError(f"Code '{code}' does not exist in AiiDA.")
        return None
