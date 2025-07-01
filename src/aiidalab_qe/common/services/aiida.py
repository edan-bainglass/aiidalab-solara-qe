from __future__ import annotations

import contextlib
import typing as t

import requests as req
from aiida import load_profile, orm
from aiida.common.exceptions import NotExistent
from aiida_pseudo.groups.family import PseudoPotentialFamily
from aiida_pseudo.groups.mixins import RecommendedCutoffMixin

_ = load_profile()

PseudoFamilyNode = t.Union[PseudoPotentialFamily, RecommendedCutoffMixin]


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

    @classmethod
    async def submit(cls, data: dict):
        label = data.pop("label")
        description = data.pop("description")
        structure: orm.StructureData = data.pop("input_structure")
        print(f"Submitting {label} ({description=})")
        payload = {
            "label": label,
            "description": description,
            "structure_pk": structure.pk,
            "parameters": data,
        }
        print(f"Payload: {payload}")
        response: req.Response = req.post(
            "http://localhost:5000/submit-workflow/",
            json=payload,
        )
        if response.ok:
            process_uuid = t.cast(dict, response.json()).get("process_uuid", "")
            process_node = cls.load_process(process_uuid)
            process_node.base.extras.set(
                "structure",
                structure.get_formula(),
            )
            process_node.base.extras.set(
                "workchain",
                data.get("workchain", {}),
            )
            process_node.base.extras.set(
                "ui_parameters",
                orm.utils.serialize.serialize(data),
            )
            print(f"Process UUID: {process_uuid}")
        else:
            process_uuid = ""
            print(f"Error submitting workflow: {response.text}")
        return process_uuid

    @staticmethod
    def load_code(code: str) -> t.Optional[orm.Code]:
        try:
            return orm.load_code(code)
        except NotExistent:
            return print(f"Code '{code}' does not exist in AiiDA.")

    @staticmethod
    def get_codes(default_calcjob_plugin: str) -> list[str]:
        codes: list[orm.Code] = orm.Code.collection.all()
        return [
            code.full_label
            for code in codes
            if code.default_calc_job_plugin == default_calcjob_plugin
        ]

    @staticmethod
    def load_pseudo_family(label: str) -> t.Optional[PseudoFamilyNode]:
        try:
            return orm.Group.collection.get(label=label)  # type: ignore
        except NotExistent:
            return print(f"Pseudo family '{label}' does not exist in AiiDA.")

    @staticmethod
    def get_pseudo(uuid: str) -> t.Optional[orm.UpfData]:
        try:
            return orm.load_node(uuid)  # type: ignore
        except NotExistent:
            return print(f"Pseudo with UUID '{uuid}' does not exist in AiiDA.")
        except ValueError:
            return

    @staticmethod
    def load_node(
        identifier: t.Union[int, str],
        error_message: str = "Node with UUID '{}' does not exist in AiiDA.",
    ) -> t.Optional[orm.Node]:
        try:
            return orm.load_node(identifier)  # type: ignore
        except NotExistent:
            return print(error_message.format(identifier))
        except ValueError:
            return

    @classmethod
    def load_process(cls, identifier: t.Union[int, str]) -> t.Optional[orm.ProcessNode]:
        process_node = cls.load_node(
            identifier,
            error_message="Process with UUID '{}' does not exist in AiiDA.",
        )
        return t.cast(orm.ProcessNode, process_node) if process_node else None
