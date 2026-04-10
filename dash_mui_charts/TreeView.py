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


class TreeView(Component):
    """A TreeView component.


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

- disabledItems (list of strings; optional):
    List of item IDs that should be disabled.

- disabledItemsFocusable (boolean; default False):
    Allow focus on disabled items.

- editableItems (list of strings; optional):
    List of item IDs that are editable (alternative to
    isItemEditable=True).

- editedItemLabel (dict; optional):
    Fired when label edit completes. {itemId, newLabel,
    event_timestamp}.

    `editedItemLabel` is a dict with keys:

    - itemId (string; optional)

    - newLabel (string; optional)

    - event_timestamp (number; optional)

- endIcon (string; optional):
    MUI icon name for leaf/end icon.

- expandIcon (string; optional):
    MUI icon name for expand icon (e.g. \"ChevronRight\").

- expandedItems (list of strings; optional):
    Controlled expanded item IDs.

- expansionTrigger (a value equal to: 'content', 'iconContainer'; default 'content'):
    What triggers expansion: \"content\" or \"iconContainer\".

- focusedItem (dict; optional):
    Fired when item is focused. {itemId, event_timestamp}.

    `focusedItem` is a dict with keys:

    - itemId (string; optional)

    - event_timestamp (number; optional)

- getItemChildren (string; default 'children'):
    Property name for item children (default: \"children\").

- getItemId (string; default 'id'):
    Property name for item ID (default: \"id\").

- getItemLabel (string; default 'label'):
    Property name for item label (default: \"label\").

- height (number | string; optional):
    Container height.

- isItemEditable (boolean; default False):
    Enable label editing. True = all items, or use editableItems for
    per-item control.

- itemChildrenIndentation (number | string; default '12px'):
    Indentation of children. Number (px) or string (\"24px\",
    \"2rem\").

- items (list of dicts; optional):
    Array of item objects. Each must have an id and label (or use
    getItemId/getItemLabel).

- multiSelect (boolean; default False):
    Allow selecting multiple items.

- selectedItems (string | list of strings; optional):
    Controlled selected item(s). String when multiSelect=False, array
    when True.

- selectionPropagation (dict; optional):
    Auto-propagate selection to parents/descendants. {parents: bool,
    descendants: bool}.

    `selectionPropagation` is a dict with keys:

    - parents (boolean; optional)

    - descendants (boolean; optional)

- sx (dict; optional):
    MUI sx styling object."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_mui_charts'
    _type = 'TreeView'
    SelectionPropagation = TypedDict(
        "SelectionPropagation",
            {
            "parents": NotRequired[bool],
            "descendants": NotRequired[bool]
        }
    )

    ClickedItem = TypedDict(
        "ClickedItem",
            {
            "itemId": NotRequired[str],
            "event_timestamp": NotRequired[NumberType]
        }
    )

    FocusedItem = TypedDict(
        "FocusedItem",
            {
            "itemId": NotRequired[str],
            "event_timestamp": NotRequired[NumberType]
        }
    )

    EditedItemLabel = TypedDict(
        "EditedItemLabel",
            {
            "itemId": NotRequired[str],
            "newLabel": NotRequired[str],
            "event_timestamp": NotRequired[NumberType]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        items: typing.Optional[typing.Sequence[dict]] = None,
        getItemId: typing.Optional[str] = None,
        getItemLabel: typing.Optional[str] = None,
        getItemChildren: typing.Optional[str] = None,
        selectedItems: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        defaultSelectedItems: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        multiSelect: typing.Optional[bool] = None,
        checkboxSelection: typing.Optional[bool] = None,
        disableSelection: typing.Optional[bool] = None,
        selectionPropagation: typing.Optional["SelectionPropagation"] = None,
        expandedItems: typing.Optional[typing.Sequence[str]] = None,
        defaultExpandedItems: typing.Optional[typing.Sequence[str]] = None,
        expansionTrigger: typing.Optional[Literal["content", "iconContainer"]] = None,
        isItemEditable: typing.Optional[bool] = None,
        editableItems: typing.Optional[typing.Sequence[str]] = None,
        disabledItems: typing.Optional[typing.Sequence[str]] = None,
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
        focusedItem: typing.Optional["FocusedItem"] = None,
        editedItemLabel: typing.Optional["EditedItemLabel"] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'ariaLabel', 'ariaLabelledBy', 'checkboxSelection', 'clickedItem', 'collapseIcon', 'defaultExpandedItems', 'defaultSelectedItems', 'disableSelection', 'disabledItems', 'disabledItemsFocusable', 'editableItems', 'editedItemLabel', 'endIcon', 'expandIcon', 'expandedItems', 'expansionTrigger', 'focusedItem', 'getItemChildren', 'getItemId', 'getItemLabel', 'height', 'isItemEditable', 'itemChildrenIndentation', 'items', 'multiSelect', 'selectedItems', 'selectionPropagation', 'sx']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ariaLabel', 'ariaLabelledBy', 'checkboxSelection', 'clickedItem', 'collapseIcon', 'defaultExpandedItems', 'defaultSelectedItems', 'disableSelection', 'disabledItems', 'disabledItemsFocusable', 'editableItems', 'editedItemLabel', 'endIcon', 'expandIcon', 'expandedItems', 'expansionTrigger', 'focusedItem', 'getItemChildren', 'getItemId', 'getItemLabel', 'height', 'isItemEditable', 'itemChildrenIndentation', 'items', 'multiSelect', 'selectedItems', 'selectionPropagation', 'sx']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(TreeView, self).__init__(**args)

setattr(TreeView, "__init__", _explicitize_args(TreeView.__init__))
