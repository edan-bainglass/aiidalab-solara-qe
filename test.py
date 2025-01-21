import solara


# Define a page with a sidebar and burger button
def page_with_sidebar():
    # State to track sidebar visibility
    sidebar_open, set_sidebar_open = solara.use_state(True)

    # Sidebar items
    menu_items = ["Dashboard", "Settings", "Profile"]

    # Sidebar and main content with smooth transition
    with solara.Columns(
        [3 if sidebar_open else 0, 9],  # Adjust widths for sidebar visibility
        style={"transition": "all 0.3s ease-in-out"},
    ):
        # Sidebar column
        if sidebar_open:
            with solara.Column(
                style={
                    "backgroundColor": "#f8f9fa",
                    "padding": "1rem",
                    "boxShadow": "2px 0px 5px rgba(0,0,0,0.1)",
                    "height": "100vh",
                    "transition": "transform 0.3s ease-in-out",
                }
            ):
                # Burger button inside the sidebar, at the top
                with solara.Row(style={"marginBottom": "1rem"}):
                    solara.Button(
                        "☰",
                        on_click=lambda: set_sidebar_open(not sidebar_open),
                        style={
                            "backgroundColor": "transparent",
                            "border": "none",
                            "fontSize": "1.5rem",
                            "cursor": "pointer",
                        },
                    )
                # Sidebar menu items
                solara.Markdown("### Navigation")
                for item in menu_items:
                    solara.Button(
                        item, on_click=lambda item=item: print(f"Clicked {item}")
                    )

        # Main content column
        with solara.Column(
            style={
                "padding": "1rem",
                "transition": "margin-left 0.3s ease-in-out",
            }
        ):
            # Content with a fallback burger button when sidebar is hidden
            if not sidebar_open:
                solara.Button(
                    "☰",
                    on_click=lambda: set_sidebar_open(not sidebar_open),
                    style={
                        "backgroundColor": "transparent",
                        "border": "none",
                        "fontSize": "1.5rem",
                        "cursor": "pointer",
                        "marginBottom": "1rem",
                    },
                )
            solara.Markdown("# Page with Sidebar")
            solara.Text("This is the main content area.")


# Define the main app with navigation
@solara.component
def Page():
    # State to manage navigation
    current_page, set_current_page = solara.use_state("Page with Sidebar")

    # Available pages
    pages = {"Page with Sidebar": page_with_sidebar}

    with solara.Column():  # App container
        # Custom app bar
        with solara.Row(
            style={"backgroundColor": "#343a40", "padding": "1rem", "color": "white"}
        ):
            solara.Text("My App", style={"fontWeight": "bold", "marginRight": "2rem"})
            for name in pages.keys():
                solara.Button(
                    name,
                    on_click=lambda name=name: set_current_page(name),
                    style={
                        "color": "white",
                        "backgroundColor": "transparent",
                        "border": "none",
                        "marginRight": "1rem",
                        "cursor": "pointer",
                    },
                )

        # Render selected page
        pages[current_page]()
