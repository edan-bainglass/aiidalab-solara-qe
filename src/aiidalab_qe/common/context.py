from __future__ import annotations

from contextlib import contextmanager

import solara

from aiidalab_qe.common.hooks import use_workflows

workbench_context = solara.create_context(use_workflows)


@contextmanager
def WorkflowContextProvider(children: list[solara.Element] | None = None):
    workbench_context.provide(use_workflows())
    yield
