import typing as t

import solara

from aiidalab_qe.common.components.wizard import BG_COLORS
from aiidalab_qe.common.models.schema import QeAppModel


@solara.component
def ParametersConfigurationSubstep(
    label: str,
    content: t.Callable[[t.Any], solara.Element],
    model: solara.Reactive[QeAppModel],
):
    with solara.v.ExpansionPanel(class_="accordion-item"):
        with solara.v.ExpansionPanelHeader(
            class_="accordion-header",
            style_=f"background-color: {BG_COLORS['INIT']}",
        ):
            with solara.Div(class_="accordion-header-content"):
                solara.Text(label, classes=["accordion-header-text"])
        with solara.v.ExpansionPanelContent(class_="accordion-collapse"):
            content(model)
