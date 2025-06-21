import solara
from solara.toestand import Ref

from aiidalab_qe.common.models.codes import CodeModel
from aiidalab_qe.common.services.aiida import AiiDAService


@solara.component
def ResourceCard(model: solara.Reactive[CodeModel], disabled: bool = False):
    name = Ref(model.fields.name)
    description = Ref(model.fields.description)
    default_calcjob_plugin = Ref(model.fields.default_calcjob_plugin)
    code = Ref(model.fields.code)
    nodes = Ref(model.fields.nodes)
    cpus = Ref(model.fields.cpus)
    ntasks = Ref(model.fields.ntasks_per_node)
    cpus_task = Ref(model.fields.cpus_per_task)
    wallclock = Ref(model.fields.max_wallclock_seconds)

    code_options = solara.use_memo(
        lambda: AiiDAService.get_codes(default_calcjob_plugin.value),
        [default_calcjob_plugin.value],
    )

    def initialize_code_selector():
        if disabled:
            return

        if not code.value:
            code.set(code_options[0])

    solara.use_effect(
        initialize_code_selector,
        [],
    )

    with solara.Div(class_="col-12 col-md-6 col-xl-4 resource"):
        with solara.v.Card(class_="m-0"):
            with solara.v.CardTitle(class_="pb-0"):
                solara.Text(name.value)
                if description.value:
                    with solara.Tooltip(description.value):
                        solara.v.Icon(children=["mdi-information"], class_="ml-2")
            with solara.v.CardText():
                solara.Select(
                    label="Code",
                    values=code_options,
                    value=code,
                    disabled=disabled,
                )
                solara.InputInt(
                    label="Nodes",
                    value=nodes,
                    disabled=disabled,
                )
                solara.InputInt(
                    label="CPUs",
                    value=cpus,
                    disabled=disabled,
                )
                solara.InputInt(
                    label="Tasks per node",
                    value=ntasks,
                    disabled=disabled,
                )
                solara.InputInt(
                    label="CPUs per task",
                    value=cpus_task,
                    disabled=disabled,
                )
                solara.InputInt(
                    label="Wallclock time (s)",
                    value=wallclock,
                    disabled=disabled,
                )
