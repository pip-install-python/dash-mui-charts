"""`.. kwargs::Package.Component` — the browser lane's props table.

The parse lives in `lib/api_reference.py` and is shared with the machine
lane's markdown expansion in `pages/markdown.py`. It used to live here,
which is precisely why the two lanes could disagree: this directive
rendered 371 rows into the React tree while `/api/llms.txt` and the
prerender carried none, because a markdown2dash directive produces
COMPONENTS and the machine lane is built from the markdown SOURCE.

One parse, two renderings. Do not reintroduce a second one here.
"""
from markdown2dash.src.directives.kwargs import Kwargs as KwargsBase

from lib.api_reference import props_for


class Kwargs(KwargsBase):

    def hook(self, md, state):
        for section in state.tokens:
            if section["type"] != self.block_name:
                continue
            attrs = section["attrs"]
            # `library:` stays supported for the bare-name form; a dotted
            # spec ("dash_mui_charts.LineChart") names its own package.
            default_package = attrs.pop("library", "dash_mantine_components")
            attrs["kwargs"] = props_for(attrs["title"], default_package)
