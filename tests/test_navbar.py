import solara

from aiidalab_qe.components.navbar import NavBar


class TestNavBar:
    def setup_method(self):
        """Setup common variables for `NavBar` component tests."""
        self.nav_items = [
            {"label": "Home", "icon": "home"},
            {"label": "Docs", "icon": "book-open", "href": "https://docs.example.com"},
        ]

        box, self.rc = solara.render(
            NavBar(items=self.nav_items),
            handle_error=False,
        )

        # TODO use box
        self.box = box.children[0]

    def test_nav_items_are_rendered(self):
        """Test that the correct number of `NavItem` components are rendered."""
        assert len(self.rc.find(solara.v.Btn).widgets) == len(self.nav_items)

    def test_nav_item_content(self):
        """Test that NavItem content is rendered correctly."""
        locator = self.rc.find(solara.v.Btn)
        for idx, nav_item in enumerate(self.nav_items):
            button = locator.widgets[idx]
            icon = button.children[0]
            label = button.children[1]
            assert icon.children == [f"mdi-{nav_item['icon']}"]
            assert label == nav_item["label"]

    def test_link_nav_item_properties(self):
        """Test that `LinkNavItem` is rendered with correct link properties."""
        locator = self.rc.find(solara.v.Btn, link=True)
        locator.assert_single()
        button = locator.widget
        assert button.href == self.nav_items[1]["href"]
        assert button.target == "_blank"
