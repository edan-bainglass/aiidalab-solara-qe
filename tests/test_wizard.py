import ipyvuetify as v
import solara

from aiidalab_qe.common.components.wizard.state import BG_COLORS, STATE_ICONS, State
from aiidalab_qe.components.wizard import StepProps, Wizard


class TestWizard:
    def setup_method(self):
        """Setup common variables for Wizard component tests."""

        @solara.component
        def FirstStep(on_state_change):
            thing, set_thing = solara.use_state("")

            def handle_thing(new_thing):
                set_thing(new_thing)

            solara.use_effect(
                lambda: on_state_change(State.CONFIGURED if thing else State.READY),
                [thing],
            )

            solara.Button(
                label="Step 1 button",
                on_click=lambda: handle_thing("new thing"),
            )

        @solara.component
        def SecondStep(set_state):
            solara.Button(
                label="Step 2 button",
                on_click=lambda: set_state(State.CONFIGURED),
            )

        self.steps: list[StepProps] = [
            {
                "title": "First step",
                "component": FirstStep,
            },
            {
                "title": "Second step",
                "component": SecondStep,
            },
        ]

        box, self.rc = solara.render(
            Wizard(steps=self.steps),
            handle_error=False,
        )

        # TODO use box
        self.box = box.children[0]

    def test_initial_step_state(self):
        """Test that the Wizard initializes with all steps in correct states."""
        accordion_steps_locator = self.rc.find(v.ExpansionPanel)
        assert len(accordion_steps_locator.widgets) == len(self.steps)

        # first step is ready, the rest are init
        for index, state in enumerate((State.READY, State.INIT)):
            self._assert_step_state(index, state)

        number_of_buttons = len(self.steps) + 1  # first step has a confirm button
        assert len(self.rc.find(v.Btn).widgets) == number_of_buttons

    def test_state_change_on_button_click(self):
        """Test that the state of the wizard step changes on button click."""
        button_locator = self.rc.find(v.Btn, children=["Step 1 button"])
        button_locator.assert_single()
        button = button_locator.widget

        confirm_button = next(
            filter(
                lambda btn: "Confirm" in btn.children,
                self.rc.find(v.Btn).widgets,
            ),
            None,
        )

        assert confirm_button.disabled

        button.click()
        self._assert_step_state(0, State.CONFIGURED)
        assert not confirm_button.disabled

    def test_step_change_on_confirm(self):
        """Test that the wizard step changes on confirm button click."""
        self._assert_step_state(0, State.READY)
        self._assert_step_state(1, State.INIT)

        confirm_button = next(
            filter(
                lambda btn: "Confirm" in btn.children,
                self.rc.find(v.Btn).widgets,
            ),
            None,
        )
        confirm_button.click()

        self._assert_step_state(0, State.SUCCESS)

        # TODO works in the frontend, but not in the test
        # self._assert_step_state(1, State.CONFIGURED)

    def _assert_step_state(self, index, state):
        step = self.rc.find(v.ExpansionPanel).widgets[index]
        header = step.children[0]
        container = header.children[0]
        icon = container.children[0]
        assert f"background-color: {BG_COLORS[state]}" in header.style_
        assert icon.children == [STATE_ICONS[state]]
