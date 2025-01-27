import solara

from aiidalab_qe.common.components.header import Header


class TestHeaderWithLogo:
    def setup_method(self):
        """Setup common variables for `Header` component tests."""
        self.logo_props = {"src": "https://example.com/logo.png", "alt": "Example Logo"}
        self.title = "Main title"
        self.subtitle = "Subtitle"

        box, self.rc = solara.render(
            Header(
                title=self.title,
                subtitle=self.subtitle,
                logo=self.logo_props,
            ),
            handle_error=False,
        )

        self.box = box.children[0]

    def test_logo_is_rendered(self):
        """Test that the logo is rendered with correct properties."""
        locator = self.rc.find(solara.v.Img)
        locator.assert_single()
        logo = locator.widget
        assert self.box.children[0] is logo
        assert logo.src == self.logo_props["src"]
        assert logo.alt == self.logo_props["alt"]

    def test_title_is_rendered(self):
        """Test that the title is rendered with correct properties."""
        locator = self.rc.find(solara.v.Html, tag="h1")
        locator.assert_single()
        title = locator.widget
        container = self.box.children[1]
        assert container.children[0] is title
        assert title.children == [self.title]

    def test_subtitle_is_rendered(self):
        """Test that the subtitle is rendered with correct properties."""
        locator = self.rc.find(solara.v.Html, tag="h2")
        locator.assert_single()
        subtitle = locator.widget
        container = self.box.children[1]
        assert container.children[1] is subtitle
        assert subtitle.children == [self.subtitle]
