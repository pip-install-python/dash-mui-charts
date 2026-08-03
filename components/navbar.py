import dash_mantine_components as dmc
from dash import Input, Output, clientside_callback
from dash_iconify import DashIconify

from lib.constants import HEADER_HEIGHT

# ---------------------------------------------------------------------------
# Family-grouped navigation.
#
# The boilerplate's navbar is a flat "Documentation" section ordered by a
# page_order list — right for pannellum's 11 pages, unreadable for this
# site's 40. This fork groups by component family instead, in the same
# visual language (create_nav_section). The map below is the nav ORDER
# AUTHORITY (what page_order is to the boilerplate): a page missing from it
# still renders, in a trailing "Other" section, so a newly added page is
# visible-but-unsorted rather than lost.
#
# Each entry is (path, label, icon). LABELS ARE SHORT ON PURPOSE — the
# section header already says the family, so the row says only what varies
# ("Examples", "Pro Features"), exactly as the old SimpleTreeView sidebar
# did. Registry names stay long-form ("Bar Chart - Basic") for the search
# Select and page titles; rendering them here read as "BARCHART / Bar
# Chart - Basic" — the redundancy this map exists to remove.
#
# Paths, not names, key the map: names are frontmatter/register_page
# strings that migration phases may polish, while the endpoints are
# contractually stable (BOILERPLATE_MIGRATION_PLAN.md decision 1).
# ---------------------------------------------------------------------------
FAMILIES = [
    ("SparklineChart", [
        ("/sparkline", "Examples", "material-symbols:play-arrow"),
        ("/sparkline-style", "Styling", "material-symbols:palette-outline"),
        ("/sparkline-style-advanced", "Advanced",
         "material-symbols:auto-graph"),
    ]),
    ("PieChart", [
        ("/pie", "Examples", "material-symbols:play-arrow"),
        ("/pie-props", "Props Explorer", "material-symbols:tune"),
    ]),
    ("BarChart", [
        ("/barchart-basic", "Basic", "material-symbols:play-arrow"),
        ("/barchart-dataset", "Dataset Mode",
         "material-symbols:table-chart-outline"),
        ("/barchart-stacking", "Stacking",
         "material-symbols:stacked-bar-chart"),
        ("/barchart-interaction", "Interaction",
         "material-symbols:touch-app-outline"),
        ("/barchart-reference", "Reference Lines", "material-symbols:rule"),
        ("/barchart-pro", "Pro Features", "material-symbols:diamond-outline"),
    ]),
    ("Heatmap", [
        ("/heatmap", "Examples", "material-symbols:play-arrow"),
        ("/heatmap-props", "Props Explorer", "material-symbols:tune"),
    ]),
    ("ScatterChart", [
        ("/scatter", "Examples", "material-symbols:play-arrow"),
    ]),
    ("LineChart", [
        ("/linechart-basic", "Basics", "material-symbols:play-arrow"),
        ("/linechart-pro", "Pro Features",
         "material-symbols:diamond-outline"),
        ("/linechart-brush", "Brush Selection", "material-symbols:brush"),
        ("/linechart-referencelines", "Reference Lines",
         "material-symbols:rule"),
        ("/linechart-highlighting", "Highlighting",
         "material-symbols:highlight"),
        ("/highlighting-sync", "Highlighting Sync", "material-symbols:sync"),
        ("/linechart-zoom-preview", "Zoom Preview",
         "material-symbols:zoom-in"),
        ("/linechart-tick-hover", "Ticks & Hover",
         "material-symbols:mouse-outline"),
        ("/crosshair", "Crosshair", "material-symbols:point-scan"),
    ]),
    ("CandlestickChart", [
        ("/candlestick", "OHLC Charts", "material-symbols:candlestick-chart-outline"),
    ]),
    ("LiveTradingChart", [
        ("/live-trading", "Examples", "material-symbols:trending-up"),
    ]),
    ("CompositeChart", [
        ("/composite", "Examples", "material-symbols:play-arrow"),
        ("/composite-v120", "v1.2.1", "material-symbols:star-outline"),
        ("/composite-render-bp", "Render BP", "material-symbols:speed-outline"),
    ]),
    ("TreeView", [
        ("/tree-basic", "Basic", "material-symbols:play-arrow"),
        ("/tree-simple", "Simple", "material-symbols:view-list-outline"),
        ("/tree-selection", "Selection",
         "material-symbols:check-box-outline"),
        ("/tree-expansion", "Expansion", "material-symbols:unfold-more"),
        ("/tree-editing", "Editing", "material-symbols:edit-outline"),
        ("/tree-icons", "Icons", "material-symbols:palette-outline"),
        ("/tree-disabled", "Disabled", "material-symbols:block"),
        ("/tree-pro", "Pro", "material-symbols:diamond-outline"),
    ]),
    ("Date & Time Pickers", [
        ("/time-clock", "Time Clock", "material-symbols:schedule-outline"),
        ("/time-clock-lab", "TimeClock Lab", "material-symbols:science-outline"),
    ]),
    ("Reference", [
        ("/api", "API Reference", "material-symbols:api"),
    ]),
]

# Rendered with Home at the top rather than inside a family.
TOP_LINKS = [("/", "Home", "material-symbols:home-outline"),
             ("/changelog", "Changelog", "material-symbols:history")]


def create_nav_link(icon, text, href, external=False):
    """Create a styled navigation link with icon"""
    return dmc.Anchor(
        dmc.Group(
            [
                DashIconify(icon=icon, width=18),
                dmc.Text(text, size="sm", fw=500),
            ],
            gap="sm",
        ),
        href=href,
        target="_blank" if external else None,
        className="navbar-link",
        underline=False,
    )


def create_nav_section(title, links):
    """Create a navigation section with a title and links"""
    return dmc.Stack(
        [
            dmc.Text(
                title,
                size="xs",
                fw=700,
                tt="uppercase",
                c="dimmed",
                mb="xs",
            ),
            dmc.Stack(links, gap="xs"),
        ],
        gap="sm",
    )


def create_content(data):
    """Navbar content: Home/Changelog, one section per component family,
    then the network's standing sections."""
    by_path = {entry["path"]: entry for entry in data}

    placed = set()
    sections = []

    top = []
    for path, label, icon in TOP_LINKS:
        if path in by_path:
            top.append(create_nav_link(icon, label, path))
            placed.add(path)

    for family, entries in FAMILIES:
        links = [create_nav_link(icon, label, path)
                 for path, label, icon in entries if path in by_path]
        placed.update(path for path, _l, _i in entries if path in by_path)
        if links:
            sections.append(create_nav_section(family, links))

    # The safety net: registered pages the map does not know yet — shown
    # under their full registry name, unsorted, so they are visible rather
    # than lost.
    leftovers = [
        create_nav_link(by_path[p].get("icon") or "fluent:document-24-regular",
                        by_path[p]["name"], p)
        for p in sorted(by_path) if p not in placed
    ]
    if leftovers:
        sections.append(create_nav_section("Other", leftovers))

    return dmc.ScrollArea(
        offsetScrollbars=True,
        type="scroll",
        style={"height": "100%"},
        children=dmc.Stack(
            [
                *top,
                dmc.Divider(mt="xs", mb="xs"),
                *sections,

                # Pip Components Section — the network's own package index,
                # the catalogue a reader of these docs most likely wants next.
                dmc.Divider(mt="md", mb="sm"),
                create_nav_section(
                    "Pip Components",
                    [
                        create_nav_link(
                            "solar:box-bold-duotone",
                            "Browse components",
                            "https://2plot.dev/pip",
                            external=True,
                        ),
                    ],
                ),

                dmc.Divider(mt="md", mb="sm"),
                create_nav_section(
                    "Resources",
                    [
                        create_nav_link(
                            "simple-icons:mui",
                            "MUI X Charts",
                            "https://mui.com/x/react-charts/",
                            external=True,
                        ),
                        create_nav_link(
                            "fluent-mdl2:forum",
                            "Dash Community",
                            "https://community.plotly.com/",
                            external=True,
                        ),
                        create_nav_link(
                            "ic:baseline-design-services",
                            "DMC",
                            "https://www.dash-mantine-components.com/",
                            external=True,
                        ),
                        # 2plot.dev, NOT pip-install-python.com — the package
                        # index is the network host, and that domain is not a
                        # link this app publishes.
                        create_nav_link(
                            "mdi:package-variant-closed",
                            "2plot.dev",
                            "https://2plot.dev",
                            external=True,
                        ),
                    ],
                ),
            ],
            gap="xs",
            p="md",
        ),
    )


def create_mobile_content(data):
    """Drawer body: a sticky search field above the scrolling nav sections.

    The header's search Select is `visibleFrom="sm"`, so phones otherwise have
    no way to jump straight to a page. This is that missing entry point.
    """
    return dmc.Stack(
        [
            dmc.Box(
                dmc.Select(
                    id="mobile-select-component",
                    placeholder="Search pages...",
                    searchable=True,
                    clearable=True,
                    size="md",
                    nothingFoundMessage="No pages found",
                    leftSection=DashIconify(icon="mingcute:search-3-line", width=18),
                    data=[
                        {"label": component["name"], "value": component["path"]}
                        for component in data
                        if component["name"] not in ["Home", "Not found 404"]
                    ],
                    comboboxProps={"zIndex": 2000},
                ),
                p="md",
                pb="xs",
            ),
            dmc.Divider(),
            # flex/minHeight give the ScrollArea a definite box to scroll inside.
            dmc.Box(create_content(data), style={"flex": 1, "minHeight": 0}),
        ],
        gap=0,
        className="mobile-nav",
        style={"height": "100%"},
    )


def create_navbar(data):
    """Create the main application navbar"""
    return dmc.AppShellNavbar(
        children=create_content(data),
        style={"borderRight": "1px solid var(--mantine-color-gray-3)"}
    )


def create_navbar_drawer(data):
    """Mobile navigation: a solid, full-height side panel.

    Runs from the bottom of the fixed header to the bottom of the viewport —
    no floating card, no close-button header row. The hamburger toggles it and
    the header stays visible (and tappable) above the overlay.
    """
    return dmc.Drawer(
        id="components-navbar-drawer",
        overlayProps={"opacity": 0.55, "blur": 3},
        zIndex=1500,
        withCloseButton=False,  # removes the whole Drawer header row
        size="300px",
        padding=0,
        children=create_mobile_content(data),
        trapFocus=False,
        position="left",
        styles={
            # Dock below the fixed header. dvh (not vh) so a collapsing mobile
            # URL bar doesn't leave a dead gap at the bottom.
            "inner": {
                "top": HEADER_HEIGHT,
                "height": f"calc(100dvh - {HEADER_HEIGHT}px)",
            },
            # Overlay starts below the header too, keeping the hamburger tappable.
            "overlay": {"top": HEADER_HEIGHT},
            # Solid panel: fill the inner, square corners.
            "content": {
                "height": "100%",
                "maxHeight": "100%",
                "borderRadius": 0,
                "display": "flex",
                "flexDirection": "column",
            },
            # Definite height so create_content's ScrollArea can actually scroll.
            "body": {"flex": 1, "minHeight": 0, "height": "100%", "padding": 0},
        },
    )


# Mobile drawer search → navigate (the header Select is hidden below `sm`).
clientside_callback(
    """
    function(value) {
        if (value) {
            return value
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("url", "href", allow_duplicate=True),
    Input("mobile-select-component", "value"),
    prevent_initial_call=True,
)
