from __future__ import annotations

import typing as t
from contextlib import contextmanager

import solara
from reacton.core import UserContext

from .schema import QeAppModel

################################## FOR GENERAL USE ####################################

ContextType = t.TypeVar("ContextType")


@contextmanager
def ContextProvider(context: UserContext[ContextType], defaults: ContextType):
    null_context = solara.create_context(None)
    context.provide(defaults) if context else null_context.provide(None)
    yield


################################# SPECIFIC TO QE APP ##################################


qe_context = solara.create_context(QeAppModel)
