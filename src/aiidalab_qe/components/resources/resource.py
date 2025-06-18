import solara
import solara.toestand
from aiida import orm

from aiidalab_qe.common.models.codes import CodeModel


@solara.component
def ResourceCard(model: solara.Reactive[CodeModel]):
    code_ref = solara.toestand.Ref(model.fields.code)
    nodes = solara.toestand.Ref(model.fields.nodes)
    cpus = solara.toestand.Ref(model.fields.cpus)
    ntasks = solara.toestand.Ref(model.fields.ntasks_per_node)
    cpus_task = solara.toestand.Ref(model.fields.cpus_per_task)
    wallclock = solara.toestand.Ref(model.fields.max_wallclock_seconds)
    code_options = solara.use_reactive([])

    def initialize_code_selector():
        codes: list[orm.Code] = orm.Code.collection.all()
        code_options.set(
            [
                code.full_label
                for code in codes
                if code.default_calc_job_plugin == model.value.default_calcjob_plugin
            ]
        )
        if not code_ref.value:
            code_ref.set(code_options.value[0])

    solara.use_effect(
        initialize_code_selector,
    )

    with solara.Div(class_="col-12 col-md-6 col-xl-4 resource"):
        with solara.v.Card(class_="m-0"):
            with solara.v.CardTitle(class_="pb-0"):
                solara.Text(model.value.name)
                if description := model.value.description:
                    with solara.Tooltip(description):
                        solara.v.Icon(children=["mdi-information"], class_="ml-2")
            with solara.v.CardText():
                solara.Select(
                    label="Code",
                    values=code_options.value,
                    value=code_ref,
                )
                solara.InputInt(label="Nodes", value=nodes)
                solara.InputInt(label="CPUs", value=cpus)
                solara.InputInt(label="Tasks per node", value=ntasks)
                solara.InputInt(label="CPUs per task", value=cpus_task)
                solara.InputInt(label="Wallclock time (s)", value=wallclock)
