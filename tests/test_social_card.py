"""The social card — the surface that fails silently and OUTSIDE the app.

Nobody sees their own unfurls, which is why this needs tests rather than a
look at the page. The two failure classes, both shipped somewhere on this
network before the standard existed:

1. **An empty og:image later in the document wins** (LESSONS §1). Dash emits
   `content=""` for any register_page missing `image_url=`/`description=`,
   and scrapers take the LAST tag. One page missing either and its card
   renders blank while every test of the template passes.
2. **A duplicate og:image, one of them unusable.** The template restating a
   tag Dash also emits gives scrapers two to choose from — and which
   duplicate wins is undefined.

Where each tag comes from decides which file to open when a check fails:
`description`, `og:type/title/description/image` and the `twitter:*` set are
DASH's (per page, from register_page); `og:site_name`, `og:url`, the
`og:image:*` auxiliaries and the icon links are `templates/index.html`'s.
dash-improve-my-llms adds a third set on the prerender path only, marked
`data-dimll-prerender` — social scrapers do not take that path, which is why
deleting the template would silently kill every unfurl.
"""
from __future__ import annotations

import re

from conftest import REPO_ROOT
from lib.constants import (
    OG_IMAGE_ALT,
    OG_IMAGE_HEIGHT,
    OG_IMAGE_TYPE,
    OG_IMAGE_URL,
    OG_IMAGE_WIDTH,
)

TEMPLATE = REPO_ROOT / "templates" / "index.html"


def _visible(html: str) -> str:
    """The document with HTML comments removed — the template documents
    itself with example tags a regex cannot tell from live ones."""
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def _meta(html: str, value: str) -> list[str]:
    """Every `content` for a property/name — a list, so duplicates show up.

    Tags carrying `data-dimll-prerender` are excluded: dash-improve-my-llms
    injects its own OG block on the prerender path and marks each tag
    precisely so it can be told apart. Counting those would make this fail
    on package behaviour nothing in this repo controls.
    """
    pattern = (
        rf'<meta[^>]*(?:property|name)="{re.escape(value)}"[^>]*content="([^"]*)"'
        rf'|<meta[^>]*content="([^"]*)"[^>]*(?:property|name)="{re.escape(value)}"'
    )
    body = re.sub(r'<meta[^>]*data-dimll-prerender[^>]*>', "", _visible(html))
    return ["".join(m) for m in re.findall(pattern, body)]


# --------------------------------------------------------- the registrations --


def test_every_page_registers_the_card_image_and_a_description(pages):
    """The root cause of LESSONS §1, asserted at the source: 40 pages, 40
    `image_url=`, 40 non-empty descriptions. One missing and Dash emits an
    empty tag that, later in document order, wins with scrapers."""
    missing = []
    for path, entry in pages:
        if entry.get("image_url") != OG_IMAGE_URL:
            missing.append(f"{path}: image_url={entry.get('image_url')!r}")
        if not (entry.get("description") or "").strip():
            missing.append(f"{path}: empty description")
    assert missing == [], missing


# ------------------------------------------------------------- the og image --


def test_the_og_image_is_never_empty_and_declared_exactly_once(client, page_paths):
    for path in page_paths:
        html = client.get(path).text
        images = _meta(html, "og:image")
        assert len(images) == 1, (
            f"{path} has og:image {images} — a scraper picks one, and it "
            "will not be the one you meant"
        )
        assert images[0].strip(), f"{path} serves an EMPTY og:image — blank card"
        assert len(_meta(html, "twitter:image")) == 1


def test_the_image_is_not_an_svg(client):
    """SVG is rejected by Facebook, Twitter/X, LinkedIn and Slack alike, and
    Dash's asset inference emits one the moment a register_page loses its
    image_url= while assets/ holds a logo."""
    for prop in ("og:image", "twitter:image"):
        for src in _meta(client.get("/").text, prop):
            assert not src.lower().endswith(".svg"), f"{prop} is an SVG: {src}"


def test_the_image_is_absolute_and_matches_the_constant(client):
    for prop in ("og:image", "twitter:image"):
        values = _meta(client.get("/").text, prop)
        assert values, f"no {prop} on the home page"
        for src in values:
            assert src.startswith("http"), f"{prop}={src!r} is not absolute"
            assert src == OG_IMAGE_URL


def test_the_image_is_hosted_off_the_app():
    """The card must be on the CDN, not served by this app: a card the app
    serves is fetched at unfurl time, and on a cold free-tier container that
    request times out and the platform caches the miss — the first person to
    share the link poisons it for everyone.

    That the URL RESOLVES is deliberately not checked here — reaching a
    third party would make this suite depend on Cloudflare being up.
    `scripts/smoke_live.py` fetches the real file after every deploy and
    checks its actual pixels against these constants.
    """
    assert OG_IMAGE_URL.startswith("https://cdn.2plot.ai/github_assets/"), (
        f"{OG_IMAGE_URL} is not on the network CDN"
    )
    assert "/assets/" not in OG_IMAGE_URL, "the app is serving its own card again"


def test_the_auxiliary_image_tags_match_the_constants(client):
    """index.html hard-codes the dimensions; lib/constants.py is the source.
    A declared width/height that disagrees with the file is worse than
    declaring none — the platform reserves the wrong box and crops."""
    html = client.get("/").text
    assert _meta(html, "og:image:width") == [str(OG_IMAGE_WIDTH)]
    assert _meta(html, "og:image:height") == [str(OG_IMAGE_HEIGHT)]
    assert _meta(html, "og:image:alt") == [OG_IMAGE_ALT]
    assert _meta(html, "og:image:type") == [OG_IMAGE_TYPE]
    assert _meta(html, "og:image:secure_url") == [OG_IMAGE_URL], (
        "secure_url must be the same file as og:image, not a stale copy"
    )


def test_the_declared_ratio_suits_a_large_image_card():
    """`summary_large_image` wants roughly 1.91:1 — narrower letterboxes,
    wider gets cropped."""
    ratio = OG_IMAGE_WIDTH / OG_IMAGE_HEIGHT
    assert 1.7 <= ratio <= 2.05, f"{OG_IMAGE_WIDTH}x{OG_IMAGE_HEIGHT} is {ratio:.2f}:1"


def test_the_twitter_card_is_a_large_image(client):
    """Two declarations, one value, and the readable one present.

    Twitter/X's parser predates the OG convention and reads `name=` only,
    while Dash hardcodes `property="twitter:card"` (dash/_pages.py). So the
    document carries two, and asserting a list of exactly one — as this fork
    did until 2026-08-26 — is what deleted the `name=` tag from
    templates/index.html and left the site declaring no card type any scraper
    could see. Compare the SET of values and pin the readable spelling.
    """
    html = client.get("/").text
    assert set(_meta(html, "twitter:card")) == {"summary_large_image"}
    assert 'name="twitter:card"' in html


def test_the_release_gate_agrees_that_the_card_type_is_not_a_duplicate(client):
    """The rule lived in THREE places, and all three had to be found.

    `scripts/check_release.py` carries its own "template does not restate
    per-page meta tags" list, and it is a gate the pytest suite does not
    run — CI invokes it in the `package` job. On 2026-08-26 the two tests
    above were fixed, the tag went back into templates/index.html, and that
    third copy failed the release consistency check and skipped the deploy:
    the fix could not ship because a fourth opinion still called it a
    duplicate. Pin the agreement rather than trusting three files to drift
    together.
    """
    gate = (REPO_ROOT / "scripts" / "check_release.py").read_text(encoding="utf-8")
    marker = 'name="twitter:card"'
    listed = [
        ln for ln in gate.splitlines()
        if marker in ln and not ln.lstrip().startswith("#")
    ]
    assert not listed, (
        "scripts/check_release.py still treats the name= card type as a "
        f"restated tag: {listed}"
    )
    # Non-vacuous: the tag really is in the template, so a gate that listed
    # it really would fire.
    assert marker in client.get("/").text


# --------------------------------------------------- template division rules --


def test_no_meta_tag_dash_emits_is_also_declared_statically(client):
    """The rule the whole template rebuild was built on: Dash emits all of
    these per page. A static copy makes two of each, and the static one
    describes the SITE where Dash's describes the PAGE — redundant and the
    less accurate of the two.

    `twitter:card` is the deliberate exception, and is absent from the list
    below for that reason: Dash declares it with `property=`, which Twitter
    does not read, so index.html's `name=` copy is not a duplicate — it is
    the only declaration a scraper can see. Both carry the same value, which
    the test above pins.
    """
    html = client.get("/").text
    for tag in ("description", "og:type", "og:title", "og:description",
                "og:image", "twitter:url", "twitter:title",
                "twitter:description", "twitter:image"):
        found = _meta(html, tag)
        assert len(found) <= 1, f"{tag} is declared {len(found)} times: {found}"


def test_the_tags_dash_omits_are_declared_here(client):
    """The other half of the rule — do not delete these thinking Dash covers
    them."""
    html = client.get("/").text
    for tag in ("og:site_name", "og:url", "og:image:alt", "twitter:image:alt",
                "og:image:secure_url", "og:image:type",
                "og:image:width", "og:image:height"):
        assert _meta(html, tag), f"{tag} is missing and Dash does not emit it"


def test_exactly_one_title_element(client):
    """The pre-Phase-1 template shipped a hardcoded <title> NEXT TO the Dash
    placeholder — two title elements on every response, and which one a
    scraper honours is undefined."""
    html = _visible(client.get("/").text)
    assert len(re.findall(r"<title[ >]", html)) == 1


# -------------------------------------------------------------- the template --


def test_the_index_template_is_still_wired_in(app):
    """`templates/index.html` looks removable and is not: dash-improve-my-llms
    appears to cover OG, but its injection runs only on the prerender path,
    which social scrapers do not take. Deleting the template kills every
    unfurl, the GA4 tag and the noscript surface at once."""
    index = TEMPLATE.read_text()
    for placeholder in ("{%metas%}", "{%title%}", "{%css%}", "{%app_entry%}",
                        "{%config%}", "{%scripts%}", "{%renderer%}"):
        assert placeholder in index, f"{placeholder} missing from the template"
    assert app.index_string.startswith("<!DOCTYPE html>")


def test_no_dash_placeholder_is_named_inside_a_comment():
    """Dash resolves `{%…%}` by plain string replacement over the whole
    index_string, comments included (LESSONS §2). dash-email's charset
    comment spelled the metas placeholder and every response carried the
    per-page meta block twice — invisible in a browser, fully visible to
    scrapers. Every `{%` in a comment must be broken or absent."""
    text = TEMPLATE.read_text()
    for comment in re.findall(r"<!--(.*?)-->", text, flags=re.S):
        hits = re.findall(r"\{%\w+%\}", comment)
        assert hits == [], (
            f"placeholder(s) {hits} named inside an HTML comment — Dash will "
            "substitute them there too, duplicating the block on every response"
        )


def test_the_template_carries_no_hardcoded_origin_or_version():
    """The origin and version are substituted at boot from lib/constants.py
    and the package — this template carried five conflicting version strings
    and og tags pinned to onrender.com before Phase 1."""
    text = _visible(TEMPLATE.read_text())
    assert "__CANONICAL_ORIGIN__" in text
    assert "__APP_VERSION__" in text
    assert "onrender.com" not in text
    assert not re.search(r'"version":\s*"\d', text), (
        "a literal version is back in the JSON-LD block"
    )


def test_every_asset_the_template_references_resolves(client):
    """The half-landed-commit guard: a template pointing at files that exist
    on disk but are untracked ships 404s from a deploy that builds from git,
    while every local boot looks perfect. A checkout is what CI tests, so
    this fails there the moment a referenced asset is not committed."""
    html = _visible(client.get("/").text)
    referenced = sorted(set(re.findall(r'(?:href|content|src)="(/assets/[^"]+)"', html)))
    assert referenced, "no /assets/ references found — did the template change?"
    missing = [ref for ref in referenced if not client.get(ref).ok]
    assert missing == [], (
        f"templates/index.html references assets that do not resolve: {missing}. "
        "If they exist on disk, they are untracked — the deploy builds from git."
    )


def test_the_apple_touch_icon_is_declared_and_resolves(client):
    """iOS uses this for Add to Home Screen."""
    html = _visible(client.get("/").text)
    match = re.search(r'<link[^>]*rel="apple-touch-icon"[^>]*href="([^"]+)"', html)
    assert match, "no apple-touch-icon link"
    assert client.get(match.group(1)).ok, f"{match.group(1)} does not resolve"


def test_both_favicon_variants_resolve(client):
    """The random favicon swapper flips between the area-chart and bar-chart
    icon sets per load (brand quirk, kept deliberately). Both halves of each
    pair must exist or half the loads 404 their icon.

    The AREA-CHART half is the canonical generated set (assets/favicon/*,
    root assets/favicon.ico) — the same files configure_seo declares and
    2.6's discovery finds — because one mark living in two places is how a
    tab icon and a search-result icon drift apart unnoticed. Only the
    bar-chart alternate still has standalone files.
    """
    for asset in (
        # area-chart: the declared identity
        "/assets/favicon.ico",
        "/assets/favicon/apple-touch-icon.png",
        # bar-chart: the browser-only alternate
        "/assets/favicon_barchart.ico",
        "/assets/apple-touch-icon_barchart.png",
    ):
        assert client.get(asset).ok, f"{asset} does not resolve"
