"""/privacy — what this site records, stated from the code that records it.

Sync 1.6.44 item 15, deliberately built AFTER item 16. The prose below
describes the tracker as it is now: no address stored, no outbound lookup,
a salted key. Written before item 16 it would have described a mechanism
this host did not have — which is why the spec orders 16 first.

The binding is not a promise, it is a test.
``tests/test_legal_pages.py`` builds a REAL visit row through the real
tracker and asserts every key in it is named in ``DESCRIBED_KEYS`` below, so
adding a field to the ledger without describing it here turns the suite red.
"""
from __future__ import annotations

import dash

from lib.constants import (
    OG_IMAGE_URL,
    PAGE_TITLE_PREFIX,
    PUBLISHER,
    SITE_SHORT_NAME,
)
from pages.legal import legal_layout

UPDATED = "2026-09-05"

PRIVACY_DESCRIPTION = (
    f"What {SITE_SHORT_NAME} records when you read the documentation, and "
    f"what it does not."
)

# Every key this site may write to a visit row, and where the prose covers
# it. The test walks a real row against this mapping — it is the contract
# between the ledger and the page, not a comment.
DESCRIBED_KEYS = {
    "timestamp": "when",
    "path": "which page",
    "device_type": "device type",
    "user_agent": "browser identification",
    "visitor_key": "visitor key",
    "location": "approximate location",
    # Off by default; described because an operator may enable it.
    "ip_address": "network address",
    # Crawler-only keys.
    "bot_type": "crawler",
    "vendor_key": "crawler",
    "vendor_class": "crawler",
    "verified": "crawler",
    "lane": "crawler",
}

LLMS_DOC = f"""# Privacy

> {PRIVACY_DESCRIPTION}

**Last updated {UPDATED}.**

## The short version

This is a documentation site. It records which pages are read, by roughly
what kind of client, from roughly where. It does not store your network
address, it does not send anything about you to a third party, and there
is nothing here to log into.

## What is recorded when you read a page

Every page request writes one row containing:

- **when** — the time of the request;
- **which page** — the path, and nothing about what you did on it;
- **device type** — desktop, mobile, tablet or crawler, derived from your
  browser identification string;
- **browser identification** — the `User-Agent` your browser sends, stored
  as sent;
- **visitor key** — a salted, one-way hash of your network address together
  with that identification string. It exists so that ten pages read in one
  sitting count as one reader rather than ten. It cannot be turned back
  into your address: the salt is generated per deployment, is never
  committed to this project's source, and is not sent anywhere;
- **approximate location** — a country, and a city where the network in
  front of this site supplies one. This is read from the headers that
  network attaches to your request. **Nothing is looked up.**

## What is not recorded

- **Your network address is not stored.** It is used to compute the visitor
  key described above and then discarded. (An operator running their own
  copy of this site can switch address storage on; on this deployment it is
  off, and the switch is off by default in the source.)
- **No third party is told anything about you.** This site makes no
  outbound request about your visit — no analytics service, no
  geolocation service, no advertising identifier. An earlier version of
  this software sent each reader's address to a third-party geolocation
  API; that was removed on {UPDATED} and the code that did it is gone.
- **No cookies are set for analytics.** There is no cross-site tracking,
  no fingerprinting beyond what is described above, and no profile.
- **Nothing about what you type.** There are no forms on the
  documentation pages that submit anything anywhere.

## Crawlers

A request from an identified crawler additionally records which crawler it
was, whether that identity could be verified against the ranges its
operator publishes, and which document was served. This is how the site
answers "did this AI crawler actually read the documentation?" — a question
about machines, not about people.

## How long it is kept

Rows are kept for 45 days on this host and then deleted. A daily summary —
counts, not rows — is sent to {PUBLISHER}'s network dashboard so several
documentation sites can be compared side by side. The summary contains no
visitor keys and no addresses.

## Internal traffic

Requests made by this network's own machinery — health checks, link audits,
deployment tests — are identified by their `User-Agent` and are not
recorded at all.

## Contact

Questions about this policy: raise an issue on the project's repository.
"""


dash.register_page(
    __name__,
    path="/privacy",
    name="Privacy",
    title=PAGE_TITLE_PREFIX + "Privacy",
    description=PRIVACY_DESCRIPTION,
    image_url=OG_IMAGE_URL,
    icon="tabler:shield-lock",
    category="Legal",
    order=2,
)


def layout(**_kwargs):
    return legal_layout(LLMS_DOC, UPDATED)


from dash_improve_my_llms import register_page_metadata  # noqa: E402

from lib import page_tiers, page_visibility  # noqa: E402

page_visibility.register_default("/privacy", "Privacy", visibility="public",
                                 llms_public=True)
page_tiers.register("/privacy", "public", llms_public=True)
register_page_metadata(
    path="/privacy",
    name="Privacy",
    description=PRIVACY_DESCRIPTION,
    title=PAGE_TITLE_PREFIX + "Privacy",
    image_url=OG_IMAGE_URL,
    schema_type="WebPage",
    lastmod=UPDATED,
    llms_doc=LLMS_DOC,
)
