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


class TreeViewPro(Component):
    """A TreeViewPro component.


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
    MUI icon name for collapse icon.

- controlsItems (list of strings; optional):
    Restrict slider+kebab to a subset of item IDs. Empty/omitted means
    all items.

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
    List of item IDs that are editable.

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
    MUI icon name for expand icon.

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
    Enable label editing for all items.

- itemChildrenIndentation (number | string; default '12px'):
    Indentation of children.

- itemPositionChanged (dict; optional):
    Output: Fired after item reorder. {itemId, oldPosition,
    newPosition, event_timestamp}.

- items (list of dicts; optional):
    Array of item objects.

- itemsReordering (boolean; default False):
    Enable drag-and-drop item reordering.

- kebabAction (dict; optional):
    Output: fires when a kebab menu item is chosen. {itemId, action,
    event_timestamp}.

    `kebabAction` is a dict with keys:

    - itemId (string; optional)

    - action (string; optional)

    - event_timestamp (number; optional)

- kebabMenuItems (list of dicts; optional):
    Kebab menu options: [{label, value, icon?}]. `value` is sent back
    as `action`.

    `kebabMenuItems` is a list of dicts with keys:

    - label (string; required)

    - value (string; required)

    - icon (string; optional)

- lazyLoadRequest (dict; optional):
    Output: Fired when unloaded node is expanded. {itemId,
    event_timestamp}.

    `lazyLoadRequest` is a dict with keys:

    - itemId (string; optional)

    - event_timestamp (number; optional)

- lazyLoadedChildren (dict; optional):
    Input: Children loaded by Dash callback. {parentItemId:
    [childItems]}.

- lazyLoading (boolean; default False):
    Enable lazy loading mode.

- licenseKey (string; default ''):
    MUI X Pro license key. Required for Pro features.

- multiSelect (boolean; default False):
    Allow selecting multiple items.

- orderedItems (list of dicts; optional):
    Output: the current tree after any drag-and-drop reorder,
    preserving each node's original fields (id, label, children,
    etc.). Updates on every reorder so Python callbacks can render the
    live order.

- reorderableItems (list of strings; optional):
    List of item IDs that can be reordered. If empty, all items are
    reorderable.

- selectedItems (string | list of strings; optional):
    Controlled selected item(s). String when multiSelect=False, array
    when True.

- selectionPropagation (dict; optional):
    Auto-propagate selection to parents/descendants.

    `selectionPropagation` is a dict with keys:

    - parents (boolean; optional)

    - descendants (boolean; optional)

- showItemControls (boolean; default False):
    Show a Slider + kebab menu on each item row.

- sliderChange (dict; optional):
    Output: fires once on each commit (mouse-up) of a slider drag.
    {itemId, value, event_timestamp}.

    `sliderChange` is a dict with keys:

    - itemId (string; optional)

    - value (number; optional)

    - event_timestamp (number; optional)

- sliderColor (string; optional):
    Slider color. Accepts a Mantine theme color name (\"teal\",
    \"blue.5\"), a CSS color literal (\"#ff6b6b\", \"rgb(...)\"), or a
    CSS expression (\"var(--mantine-color-teal-6)\",
    \"light-dark(...)\"). Bare names use shade 6 by default. When
    omitted, the slider falls back to MUI's `primary` palette color.

- sliderMax (number; default 100):
    Slider maximum.

- sliderMin (number; default 0):
    Slider minimum.

- sliderStep (number; default 1):
    Slider step.

- sliderValues (dict; optional):
    Controlled slider values keyed by itemId, e.g. {\"task-1\": 40}.
    Also updated as user drags.

- sx (dict; optional):
    MUI sx styling object."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_mui_charts'
    _type = 'TreeViewPro'
    SelectionPropagation = TypedDict(
        "SelectionPropagation",
            {
            "parents": NotRequired[bool],
            "descendants": NotRequired[bool]
        }
    )

    LazyLoadRequest = TypedDict(
        "LazyLoadRequest",
            {
            "itemId": NotRequired[str],
            "event_timestamp": NotRequired[NumberType]
        }
    )

    KebabMenuItems = TypedDict(
        "KebabMenuItems",
            {
            "label": str,
            "value": str,
            "icon": NotRequired[str]
        }
    )

    SliderChange = TypedDict(
        "SliderChange",
            {
            "itemId": NotRequired[str],
            "value": NotRequired[NumberType],
            "event_timestamp": NotRequired[NumberType]
        }
    )

    KebabAction = TypedDict(
        "KebabAction",
            {
            "itemId": NotRequired[str],
            "action": NotRequired[str],
            "event_timestamp": NotRequired[NumberType]
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
        licenseKey: typing.Optional[str] = None,
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
        itemsReordering: typing.Optional[bool] = None,
        reorderableItems: typing.Optional[typing.Sequence[str]] = None,
        itemPositionChanged: typing.Optional[dict] = None,
        orderedItems: typing.Optional[typing.Sequence[dict]] = None,
        lazyLoading: typing.Optional[bool] = None,
        lazyLoadedChildren: typing.Optional[dict] = None,
        lazyLoadRequest: typing.Optional["LazyLoadRequest"] = None,
        showItemControls: typing.Optional[bool] = None,
        controlsItems: typing.Optional[typing.Sequence[str]] = None,
        sliderValues: typing.Optional[dict] = None,
        sliderMin: typing.Optional[NumberType] = None,
        sliderMax: typing.Optional[NumberType] = None,
        sliderStep: typing.Optional[NumberType] = None,
        sliderColor: typing.Optional[str] = None,
        kebabMenuItems: typing.Optional[typing.Sequence["KebabMenuItems"]] = None,
        sliderChange: typing.Optional["SliderChange"] = None,
        kebabAction: typing.Optional["KebabAction"] = None,
        clickedItem: typing.Optional["ClickedItem"] = None,
        focusedItem: typing.Optional["FocusedItem"] = None,
        editedItemLabel: typing.Optional["EditedItemLabel"] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'ariaLabel', 'ariaLabelledBy', 'checkboxSelection', 'clickedItem', 'collapseIcon', 'controlsItems', 'defaultExpandedItems', 'defaultSelectedItems', 'disableSelection', 'disabledItems', 'disabledItemsFocusable', 'editableItems', 'editedItemLabel', 'endIcon', 'expandIcon', 'expandedItems', 'expansionTrigger', 'focusedItem', 'getItemChildren', 'getItemId', 'getItemLabel', 'height', 'isItemEditable', 'itemChildrenIndentation', 'itemPositionChanged', 'items', 'itemsReordering', 'kebabAction', 'kebabMenuItems', 'lazyLoadRequest', 'lazyLoadedChildren', 'lazyLoading', 'licenseKey', 'multiSelect', 'orderedItems', 'reorderableItems', 'selectedItems', 'selectionPropagation', 'showItemControls', 'sliderChange', 'sliderColor', 'sliderMax', 'sliderMin', 'sliderStep', 'sliderValues', 'sx']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ariaLabel', 'ariaLabelledBy', 'checkboxSelection', 'clickedItem', 'collapseIcon', 'controlsItems', 'defaultExpandedItems', 'defaultSelectedItems', 'disableSelection', 'disabledItems', 'disabledItemsFocusable', 'editableItems', 'editedItemLabel', 'endIcon', 'expandIcon', 'expandedItems', 'expansionTrigger', 'focusedItem', 'getItemChildren', 'getItemId', 'getItemLabel', 'height', 'isItemEditable', 'itemChildrenIndentation', 'itemPositionChanged', 'items', 'itemsReordering', 'kebabAction', 'kebabMenuItems', 'lazyLoadRequest', 'lazyLoadedChildren', 'lazyLoading', 'licenseKey', 'multiSelect', 'orderedItems', 'reorderableItems', 'selectedItems', 'selectionPropagation', 'showItemControls', 'sliderChange', 'sliderColor', 'sliderMax', 'sliderMin', 'sliderStep', 'sliderValues', 'sx']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(TreeViewPro, self).__init__(**args)

setattr(TreeViewPro, "__init__", _explicitize_args(TreeViewPro.__init__))
