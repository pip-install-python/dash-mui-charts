# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args

ComponentType = typing.Union[
    str,
    int,
    float,
    Component,
    None,
    typing.Sequence[typing.Union[str, int, float, Component, None]],
]

NumberType = typing.Union[
    typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
]


class SimpleTreeView(Component):
    """A SimpleTreeView component.


Keyword arguments:

- id (string; optional):
    Dash component id.

- ariaLabel (string; optional):
    ARIA label for the tree.

- ariaLabelledBy (string; optional):
    ID of element that labels the tree.

- checkboxSelection (boolean; default False):
    Show checkboxes for selection.

- clickedItem (dict; optional):
    Fired when item is clicked. {itemId, event_timestamp}.

    `clickedItem` is a dict with keys:

    - itemId (string; optional)

    - event_timestamp (number; optional)

- collapseIcon (string; optional):
    MUI icon name for collapse icon (e.g. \"ExpandMore\").

- defaultExpandedItems (list of strings; optional):
    Default expanded items (uncontrolled).

- defaultSelectedItems (string | list of strings; optional):
    Default selected items (uncontrolled).

- disableSelection (boolean; default False):
    Disable all selection.

- disabledItemsFocusable (boolean; default False):
    Allow focus on disabled items.

- endIcon (string; optional):
    MUI icon name for leaf/end icon.

- expandIcon (string; optional):
    MUI icon name for expand icon (e.g. \"ChevronRight\").

- expandedItems (list of strings; optional):
    Controlled expanded item IDs.

- expansionTrigger (a value equal to: 'content', 'iconContainer'; default 'content'):
    What triggers expansion: \"content\" or \"iconContainer\".

- height (number | string; optional):
    Container height.

- itemChildrenIndentation (number | string; default '12px'):
    Indentation of children. Number (px) or string (\"24px\",
    \"2rem\").

- items (list of dicts; optional):
    Nested items array. Each item: {itemId: string, label: string,
    children?: [], disabled?: bool, disableSelection?: bool}.

    `items` is a list of dicts with keys:

    - itemId (string; required)

    - label (string; required)

    - children (list; optional)

    - disabled (boolean; optional)

    - disableSelection (boolean; optional)

- multiSelect (boolean; default False):
    Allow selecting multiple items.

- selectedItems (string | list of strings; optional):
    Controlled selected item(s). String when multiSelect=False, array
    when True.

- sx (dict; optional):
    MUI sx styling object."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_mui_charts'
    _type = 'SimpleTreeView'
    Items = TypedDict(
        "Items",
            {
            "itemId": str,
            "label": str,
            "children": NotRequired[typing.Sequence],
            "disabled": NotRequired[bool],
            "disableSelection": NotRequired[bool]
        }
    )

    ClickedItem = TypedDict(
        "ClickedItem",
            {
            "itemId": NotRequired[str],
            "event_timestamp": NotRequired[NumberType]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        items: typing.Optional[typing.Sequence["Items"]] = None,
        selectedItems: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        defaultSelectedItems: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        multiSelect: typing.Optional[bool] = None,
        checkboxSelection: typing.Optional[bool] = None,
        disableSelection: typing.Optional[bool] = None,
        expandedItems: typing.Optional[typing.Sequence[str]] = None,
        defaultExpandedItems: typing.Optional[typing.Sequence[str]] = None,
        expansionTrigger: typing.Optional[Literal["content", "iconContainer"]] = None,
        disabledItemsFocusable: typing.Optional[bool] = None,
        itemChildrenIndentation: typing.Optional[typing.Union[NumberType, str]] = None,
        height: typing.Optional[typing.Union[NumberType, str]] = None,
        sx: typing.Optional[dict] = None,
        collapseIcon: typing.Optional[str] = None,
        expandIcon: typing.Optional[str] = None,
        endIcon: typing.Optional[str] = None,
        ariaLabel: typing.Optional[str] = None,
        ariaLabelledBy: typing.Optional[str] = None,
        clickedItem: typing.Optional["ClickedItem"] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'ariaLabel', 'ariaLabelledBy', 'checkboxSelection', 'clickedItem', 'collapseIcon', 'defaultExpandedItems', 'defaultSelectedItems', 'disableSelection', 'disabledItemsFocusable', 'endIcon', 'expandIcon', 'expandedItems', 'expansionTrigger', 'height', 'itemChildrenIndentation', 'items', 'multiSelect', 'selectedItems', 'sx']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ariaLabel', 'ariaLabelledBy', 'checkboxSelection', 'clickedItem', 'collapseIcon', 'defaultExpandedItems', 'defaultSelectedItems', 'disableSelection', 'disabledItemsFocusable', 'endIcon', 'expandIcon', 'expandedItems', 'expansionTrigger', 'height', 'itemChildrenIndentation', 'items', 'multiSelect', 'selectedItems', 'sx']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(SimpleTreeView, self).__init__(**args)

setattr(SimpleTreeView, "__init__", _explicitize_args(SimpleTreeView.__init__))
