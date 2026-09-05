"""/terms — the terms this documentation site is offered under.

Sync 1.6.44 item 15. One markdown string, rendered for the browser and
handed to the machine lane, for the reason pages/legal.py gives.
"""
from __future__ import annotations

import dash

from lib.constants import (
    GITHUB_URL,
    OG_IMAGE_URL,
    PAGE_TITLE_PREFIX,
    PUBLISHER,
    SITE_SHORT_NAME,
)
from pages.legal import legal_layout

UPDATED = "2026-09-05"

TERMS_DESCRIPTION = (
    f"The terms {SITE_SHORT_NAME}'s documentation and component library are "
    f"offered under."
)

LLMS_DOC = f"""# Terms

> {TERMS_DESCRIPTION}

**Last updated {UPDATED}.**

## What this site is

{SITE_SHORT_NAME} is open-source software and this site is its
documentation. Both are published by {PUBLISHER}. The source, the licence,
and the issue tracker are at <{GITHUB_URL}>.

## Use of the documentation

You may read, quote, and link to this documentation freely, including for
training and for retrieval by automated agents. Code examples are provided
so that you can use them: they are part of the software's documentation and
are covered by the project's licence, which is in the repository.

## Use by automated clients

Machine access is deliberately supported. `/llms.txt` and the per-page
`llms.txt` documents exist for exactly that purpose, and `robots.txt`
states this site's current posture. Two conditions:

- **Identify yourself.** Send a `User-Agent` that names your crawler or
  client. Requests that identify themselves are treated better than those
  that do not, and every read is recorded as described in the
  [privacy policy](/privacy).
- **Be proportionate.** Fetch what you need. This site is served from a
  small deployment; a crawler that behaves like a denial-of-service attack
  will be treated as one.

## No warranty

The software and this documentation are provided "as is", without warranty
of any kind, express or implied. Nothing here is a guarantee that a
component behaves as described in a given version, and nothing here creates
a support obligation. The authoritative statement of warranty and liability
is the licence in the repository; this section does not replace it.

## Third-party components

This documentation demonstrates components that wrap third-party libraries.
Those libraries carry their own licences and their own terms, and some
features shown here require a commercial licence from their vendor. Where
that is the case the page says so.

## Changes

These terms may change. The date at the top of this page is when they last
did, and the repository's history records what changed.

## Contact

Questions: raise an issue at <{GITHUB_URL}>.
"""


dash.register_page(
    __name__,
    path="/terms",
    name="Terms",
    title=PAGE_TITLE_PREFIX + "Terms",
    description=TERMS_DESCRIPTION,
    image_url=OG_IMAGE_URL,
    icon="tabler:file-text",
    category="Legal",
    order=1,
)


def layout(**_kwargs):
    return legal_layout(LLMS_DOC, UPDATED)


from dash_improve_my_llms import register_page_metadata  # noqa: E402

from lib import page_tiers, page_visibility  # noqa: E402

page_visibility.register_default("/terms", "Terms", visibility="public",
                                 llms_public=True)
page_tiers.register("/terms", "public", llms_public=True)
register_page_metadata(
    path="/terms",
    name="Terms",
    description=TERMS_DESCRIPTION,
    title=PAGE_TITLE_PREFIX + "Terms",
    image_url=OG_IMAGE_URL,
    schema_type="WebPage",
    lastmod=UPDATED,
    llms_doc=LLMS_DOC,
)
