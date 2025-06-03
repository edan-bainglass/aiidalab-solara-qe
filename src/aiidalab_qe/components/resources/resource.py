import solara
import solara.toestand
from aiida import orm

from aiidalab_qe.common.models.codes import CodeModel


@solara.component
def ResourceCard(model: solara.Reactive[CodeModel], label: str):
    code_ref = solara.toestand.Ref(model.fields.code)
    nodes = solara.toestand.Ref(model.fields.nodes)
    cpus = solara.toestand.Ref(model.fields.cpus)
    ntasks = solara.toestand.Ref(model.fields.ntasks_per_node)
    cpus_task = solara.toestand.Ref(model.fields.cpus_per_task)
    wallclock = solara.toestand.Ref(model.fields.max_wallclock_seconds)

    def get_codes_by_entry_point() -> list[str]:
        codes: list[orm.Code] = orm.Code.collection.all()
        return [
            code.full_label
            for code in codes
            if code.default_calc_job_plugin == model.value.default_calcjob_plugin
        ]

    with solara.Div(class_="col-12 col-md-6 col-xl-4 p-0"):
        with solara.v.Card(class_="m-0"):
            with solara.v.CardTitle(class_="pb-0"):
                solara.HTML("h5", label)
            with solara.v.CardText():
                solara.Select(
                    label="Code",
                    values=get_codes_by_entry_point(),
                    value=code_ref,
                )
                solara.InputInt(label="Nodes", value=nodes)
                solara.InputInt(label="CPUs", value=cpus)
                solara.InputInt(label="Tasks per node", value=ntasks)
                solara.InputInt(label="CPUs per task", value=cpus_task)
                solara.InputInt(label="Wallclock time (s)", value=wallclock)
                solara.v.Input()
