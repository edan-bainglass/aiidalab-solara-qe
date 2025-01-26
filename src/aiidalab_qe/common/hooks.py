from __future__ import annotations

import typing as t

import solara

from aiidalab_qe.components.wizard.models import WorkflowDataModel


def use_workflows():
    workflows, set_workflows = solara.use_state([solara.reactive(WorkflowDataModel())])
    active_workflow, set_active_workflow = solara.use_state(t.cast(int, None))

    def add_workflow(pk: int | None = None):
        set_workflows([*workflows, solara.reactive(WorkflowDataModel(pk=pk))])
        set_active_workflow(len(workflows))

    return (
        workflows,
        active_workflow,
        add_workflow,
    )
