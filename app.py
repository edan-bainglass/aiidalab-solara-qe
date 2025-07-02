import solara
from aiida import engine, load_profile, orm
from aiida.calculations.arithmetic.add import ArithmeticAddCalculation

_ = load_profile()


@solara.component
def Page():
    uuid = solara.use_reactive("")

    def submit_workflow():
        code = orm.load_code(7185)
        process_node = engine.submit(ArithmeticAddCalculation, x=1, y=2, code=code)
        uuid.set(process_node.uuid)

    solara.Button("Submit", on_click=submit_workflow)

    if uuid.value:
        solara.Text(f"Submitted workflow with UUID: {uuid.value}")
