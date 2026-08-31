import dash_mantine_components as dmc
from dash import Output, Input, State, clientside_callback
from dash_iconify import DashIconify

from components.backend_badge import create_backend_badge
from components.navbar import search_data
from dash_mui_charts import __version__ as _COMPONENT_VERSION
from lib.backend import get_backend_info
from lib.constants import (
    BASE_URL, GITHUB_URL, HEADER_HEIGHT, LOGO_ASSET, LOGO_STYLE, WORDMARK,
    WORDMARK_COLOR, WORDMARK_VISIBLE_FROM,
)


def create_clerk_avatar():
    """Clerk avatar / sign-in control, sat beside the colour-scheme toggle.

    Returns None when Clerk is not configured, so local development and any
    deploy without the keys renders the header exactly as before rather than
    erroring on a missing component. `lib/auth.py` registers Clerk with
    `headless=True`, meaning the package injects NO UI of its own — without
    this widget there is no way to sign in even though Clerk initialises.
    The package renders `#clerk-login-button` inside it; since
    dash-clerk-auth 0.9.2 that button's own handler is satellite-safe, so it
    needs nothing from us.
    """
    from lib.auth import clerk_enabled

    if not clerk_enabled():
        return None
    from dash_clerk_auth import create_clerk_menu

    return create_clerk_menu(show_dropdown=True, dropdown_align="right")


def create_link(icon, href, label):
    """Create an external link icon button.

    ``label`` is REQUIRED: an icon-only link has no accessible name, so
    screen readers announce it as "link" and AI agents can't tell what it
    does — the exact Lighthouse/Agentic-Browsing failure measured on the
    fleet 2026-08-21. The label lands on both the anchor and the button.

    `aria-label`, never `title=`: DMC 2.8's ActionIcon and Anchor accept
    `aria-*` wildcards but REJECT `title`, and they reject it by raising
    during app construction — a tooltip typo takes the whole site down
    rather than rendering wrong. Hover text belongs in dmc.Tooltip.
    """
    return dmc.Anchor(
        dmc.ActionIcon(
            DashIconify(icon=icon, width=22),
            variant="subtle",
            size="lg",
            color="gray",
            **{"aria-label": label},
        ),
        href=href,
        target="_blank",
        **{"aria-label": label},
    )


def create_other_apps_menu():
    """*Other Apps* — the network, from ONE registry (sync item 16).

    A hover menu in the top bar (the 2plot.dev shape the owner named as the
    reference), populated from lib.network_directory's PRIMARY set: the hub,
    the catalogue and the affiliated sites, this app omitted, labelled by
    domain. The sidebar's "Pip Components" and "2plot.dev" links are GONE in
    the same change — the network is listed once, here, so it cannot be
    listed twice.
    """
    from lib.network_directory import other_apps_for

    return dmc.Menu(
        [
            dmc.MenuTarget(
                dmc.Button(
                    "Other Apps",
                    variant="subtle",
                    color="gray",
                    size="sm",
                    leftSection=DashIconify(icon="svg-spinners:blocks-scale", width=18),
                    visibleFrom="md",
                    id="other-apps-menu-target",
                )
            ),
            dmc.MenuDropdown(
                [
                    dmc.MenuItem(
                        entry["label"],
                        leftSection=DashIconify(icon=entry["icon"], width=16),
                        href=entry["url"],
                        target="_blank",
                    )
                    for entry in other_apps_for(BASE_URL)
                ],
                id="other-apps-menu",
                # Solid, themed panel (the visual pass): the seat found the
                # dropdown near-transparent with washed-out items in dark mode.
                styles={"dropdown": {
                    "backgroundColor": "var(--mantine-color-body)",
                    "border": "1px solid var(--mantine-color-default-border)",
                    "boxShadow": "var(--mantine-shadow-md)",
                }},
            ),
        ],
        trigger="hover",
        openDelay=100,
        closeDelay=200,
    )


def create_search(data):
    """Create searchable dropdown for component navigation"""
    return dmc.Select(
        id="select-component",
        placeholder="Search pages...",
        searchable=True,
        clearable=True,
        w=240,
        size="sm",
        nothingFoundMessage="No pages found",
        leftSection=DashIconify(icon="mingcute:search-3-line", width=18),
        # ONE definition of "a page the reader may navigate to", in
        # components/navbar: not Home, not /admin/*, not the 404, not a
        # hidden-tier page. The header used to carry its own copy of that
        # rule and the two could disagree — a page missing from the sidebar
        # but reachable from the search box is the same leak with an extra
        # step (sync item 16, contract 1).
        data=search_data(data),
        visibleFrom="sm",
        comboboxProps={"zIndex": 2000},
        **{"aria-label": "Search pages"},
        styles={
            "input": {
                "borderColor": "var(--mantine-color-gray-4)",
            }
        }
    )


def _create_openapi_link():
    """Show a Swagger UI link only when the FastAPI backend is active."""
    info = get_backend_info()
    if info.name != "fastapi":
        return None
    return dmc.Tooltip(
        label="OpenAPI docs (Swagger UI) — available on the FastAPI backend",
        position="bottom",
        withArrow=True,
        children=dmc.Anchor(
            dmc.Badge(
                "OpenAPI",
                leftSection=DashIconify(icon="logos:swagger", width=14),
                variant="light",
                color="cyan",
                radius="sm",
                styles={"root": {"textTransform": "none", "fontWeight": 600}},
            ),
            href="/docs",
            target="_blank",
            underline=False,
        ),
    )


def create_header(data):
    """Create application header with logo, search, and theme toggle"""
    return dmc.AppShellHeader(
        dmc.Group(
            [
                # Left section: Hamburger (mobile) + Burger (desktop collapse) + Logo
                dmc.Group(
                    [
                        dmc.ActionIcon(
                            DashIconify(icon="radix-icons:hamburger-menu", width=22),
                            id="drawer-hamburger-button",
                            variant="subtle",
                            size="lg",
                            color="gray",
                            hiddenFrom="md",
                            **{"aria-label": "Open navigation menu"},
                        ),
                        # Desktop-only burger: collapses/expands the AppShell navbar
                        # on md-xl screens. Default opened=True so users see the X
                        # state on first load (navbar visible).
                        dmc.Burger(
                            id="desktop-navbar-toggle",
                            opened=True,
                            size="sm",
                            visibleFrom="md",
                            **{"aria-label": "Collapse or expand the sidebar"},
                        ),
                        dmc.Anchor(
                            dmc.Group(
                                [
                                    # id "header-avatar" is a contract with the
                                    # random favicon swapper in
                                    # templates/index.html — it re-points this
                                    # image to the area/bar-chart icon it chose
                                    # for the tab. Rename both or neither.
                                    dmc.Avatar(
                                        id="header-avatar",
                                        src=f"/assets/{LOGO_ASSET}",
                                        size="sm",
                                        radius="sm",
                                        style=LOGO_STYLE,
                                    ),
                                    # visibleFrom="xs": at 390px the wordmark
                                    # plus two burgers, the avatar, the badge
                                    # and the whole right group wrapped the
                                    # header onto two rows (the ops seat's
                                    # phone pass, 2026-08-30). Hidden below
                                    # xs rather than dropped, so the node
                                    # stays in the DOM for anything that
                                    # addresses it by id.
                                    dmc.Text(
                                        WORDMARK,
                                        size="lg",
                                        fw=700,
                                        c=WORDMARK_COLOR,
                                        id="dash-docs-title",
                                        visibleFrom=WORDMARK_VISIBLE_FROM,
                                    ),
                                    # Version from the package (package-info.json),
                                    # the same source setup.py builds from —
                                    # never hardcode it here; a stale badge
                                    # shipped as "v1.3.0" for a full release
                                    # cycle. tests/test_version_parity pins this.
                                    dmc.Badge(f"v{_COMPONENT_VERSION}",
                                              variant="light", size="sm",
                                              color="blue", visibleFrom="xs"),
                                ],
                                gap="sm",
                            ),
                            href="/",
                            underline=False,
                            # The home link's accessible name comes from HERE,
                            # not from the wordmark text: `visibleFrom` is
                            # display:none, which removes the Text from the
                            # accessibility tree, and the avatar is decorative.
                            # Without this label the home link would have no
                            # name at all on a phone — the a11y half of the
                            # line above, and the reason the two ship together.
                            **{"aria-label": f"{WORDMARK} — home"},
                        ),
                    ],
                    gap="md",
                ),

                # Right section: Backend badge + OpenAPI (fastapi only) + Search + links + Theme toggle
                dmc.Group(
                    [
                        dmc.Box(create_backend_badge(), visibleFrom="sm"),
                        dmc.Box(_create_openapi_link(), visibleFrom="md"),
                        create_search(data),
                        create_other_apps_menu(),
                        # The "More Dash components" link to
                        # pip-install-python.com is RETIRED (sync item 16):
                        # the domain is retired network-wide — the same
                        # reason lib/network_directory has kept it out of
                        # the directory since the retire sweep — and this
                        # header was still sending readers there.
                        create_link(
                            "radix-icons:github-logo",
                            GITHUB_URL,
                            "View the source on GitHub",
                        ),
                        dmc.ActionIcon(
                            [
                                DashIconify(
                                    icon="radix-icons:sun",
                                    width=22,
                                    id="light-theme-icon",
                                ),
                                DashIconify(
                                    icon="radix-icons:moon",
                                    width=22,
                                    id="dark-theme-icon",
                                ),
                            ],
                            variant="subtle",
                            color="yellow",
                            id="color-scheme-toggle",
                            size="lg",
                            **{"aria-label": "Toggle light / dark color scheme"},
                        ),
                        create_clerk_avatar(),
                    ],
                    gap="sm",
                ),
            ],
            justify="space-between",
            h=HEADER_HEIGHT,
            px="xl",
        ),
    )


clientside_callback(
    """
    function(value) {
        if (value) {
            return value
        }
    }
    """,
    Output("url", "href"),
    Input("select-component", "value"),
)

# Mobile drawer search → navigate (the header Select is hidden below `sm`).
clientside_callback(
    """
    function(value) {
        if (value) {
            return value
        }
        return window.dash_clientside.no_update
    }
    """,
    Output("url", "href", allow_duplicate=True),
    Input("mobile-select-component", "value"),
    prevent_initial_call=True,
)

# The overlay no longer covers the header, so the hamburger stays reachable
# while the drawer is open — make a second tap close it.
clientside_callback(
    """function(n_clicks, opened) { return !opened }""",
    Output("components-navbar-drawer", "opened"),
    Input("drawer-hamburger-button", "n_clicks"),
    State("components-navbar-drawer", "opened"),
    prevent_initial_call=True,
)
