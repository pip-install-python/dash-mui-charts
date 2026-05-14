/**
 * TreeView — Dash wrapper for MUI X RichTreeView (Community)
 *
 * Data-driven tree with selection, expansion, editing, focus callbacks.
 * This is a STUB — Claude Code should implement the full component.
 */
import React, {useCallback, useMemo} from 'react';
import PropTypes from 'prop-types';
import {RichTreeView} from '@mui/x-tree-view/RichTreeView';
import {resolveIcon} from '../fragments/iconResolver';

const TreeView = (props) => {
    const {
        id,
        items,
        // Item accessors (string → function conversion)
        getItemId: getItemIdProp,
        getItemLabel: getItemLabelProp,
        getItemChildren: getItemChildrenProp,
        // Selection
        selectedItems,
        defaultSelectedItems,
        multiSelect,
        checkboxSelection,
        disableSelection,
        selectionPropagation,
        // Expansion
        expandedItems,
        defaultExpandedItems,
        expansionTrigger,
        // Editing
        isItemEditable,
        editableItems,
        // Disabled
        disabledItems,
        disabledItemsFocusable,
        // Appearance
        itemChildrenIndentation,
        height,
        sx,
        // Icons (string names)
        collapseIcon,
        expandIcon,
        endIcon,
        // Accessibility
        ariaLabel,
        ariaLabelledBy,
        // Dash
        setProps,
        ...otherProps
    } = props;

    // --- Convert string accessor props to functions ---
    const getItemId = useCallback(
        (item) => item[getItemIdProp || 'id'],
        [getItemIdProp]
    );
    const getItemLabel = useCallback(
        (item) => item[getItemLabelProp || 'label'],
        [getItemLabelProp]
    );
    const getItemChildren = useCallback(
        (item) => item[getItemChildrenProp || 'children'],
        [getItemChildrenProp]
    );

    // --- Convert list-based disabled/editable to functions ---
    const isItemDisabledFn = useMemo(() => {
        if (!disabledItems || disabledItems.length === 0) return undefined;
        const disabledSet = new Set(disabledItems);
        return (item) => disabledSet.has(getItemId(item));
    }, [disabledItems, getItemId]);

    const isItemEditableFn = useMemo(() => {
        if (typeof isItemEditable === 'boolean') return isItemEditable;
        if (editableItems && editableItems.length > 0) {
            const editableSet = new Set(editableItems);
            return (item) => editableSet.has(getItemId(item));
        }
        return false;
    }, [isItemEditable, editableItems, getItemId]);

    // --- Slots for icons ---
    const slots = useMemo(() => {
        const s = {};
        if (collapseIcon) s.collapseIcon = resolveIcon(collapseIcon);
        if (expandIcon) s.expandIcon = resolveIcon(expandIcon);
        if (endIcon) s.endIcon = resolveIcon(endIcon);
        return Object.keys(s).length > 0 ? s : undefined;
    }, [collapseIcon, expandIcon, endIcon]);

    // --- Callbacks → Dash output props ---
    const handleSelectedItemsChange = useCallback(
        (event, itemIds) => {
            if (setProps) setProps({selectedItems: itemIds});
        },
        [setProps]
    );

    const handleExpandedItemsChange = useCallback(
        (event, itemIds) => {
            if (setProps) setProps({expandedItems: itemIds});
        },
        [setProps]
    );

    const handleItemClick = useCallback(
        (event, itemId) => {
            if (setProps) setProps({clickedItem: {itemId, event_timestamp: Date.now()}});
        },
        [setProps]
    );

    const handleItemFocus = useCallback(
        (event, itemId) => {
            if (setProps) setProps({focusedItem: {itemId, event_timestamp: Date.now()}});
        },
        [setProps]
    );

    const handleItemLabelChange = useCallback(
        (itemId, newLabel) => {
            if (setProps) setProps({editedItemLabel: {itemId, newLabel, event_timestamp: Date.now()}});
        },
        [setProps]
    );

    // --- Container style ---
    const containerStyle = useMemo(() => {
        const s = {};
        if (height) s.height = typeof height === 'number' ? `${height}px` : height;
        return s;
    }, [height]);

    return (
        <div id={id} style={containerStyle}>
            <RichTreeView
                items={items || []}
                getItemId={getItemId}
                getItemLabel={getItemLabel}
                getItemChildren={getItemChildren}
                // Selection
                selectedItems={selectedItems}
                defaultSelectedItems={defaultSelectedItems}
                multiSelect={multiSelect}
                checkboxSelection={checkboxSelection}
                disableSelection={disableSelection}
                selectionPropagation={selectionPropagation}
                // Expansion
                expandedItems={expandedItems}
                defaultExpandedItems={defaultExpandedItems}
                expansionTrigger={expansionTrigger}
                // Editing
                isItemEditable={isItemEditableFn}
                // Disabled
                isItemDisabled={isItemDisabledFn}
                disabledItemsFocusable={disabledItemsFocusable}
                // Appearance
                itemChildrenIndentation={itemChildrenIndentation}
                sx={sx}
                slots={slots}
                // Callbacks
                onSelectedItemsChange={handleSelectedItemsChange}
                onExpandedItemsChange={handleExpandedItemsChange}
                onItemClick={handleItemClick}
                onItemFocus={handleItemFocus}
                onItemLabelChange={handleItemLabelChange}
                // Accessibility
                aria-label={ariaLabel}
                aria-labelledby={ariaLabelledBy}
            />
        </div>
    );
};

TreeView.defaultProps = {
    items: [],
    getItemId: 'id',
    getItemLabel: 'label',
    getItemChildren: 'children',
    multiSelect: false,
    checkboxSelection: false,
    disableSelection: false,
    disabledItemsFocusable: false,
    isItemEditable: false,
    expansionTrigger: 'content',
    itemChildrenIndentation: '12px',
};

TreeView.propTypes = {
    /** Dash component id */
    id: PropTypes.string,

    /** Array of item objects. Each must have an id and label (or use getItemId/getItemLabel). */
    items: PropTypes.arrayOf(PropTypes.object),

    /** Property name for item ID (default: "id") */
    getItemId: PropTypes.string,

    /** Property name for item label (default: "label") */
    getItemLabel: PropTypes.string,

    /** Property name for item children (default: "children") */
    getItemChildren: PropTypes.string,

    // --- Selection ---
    /** Controlled selected item(s). String when multiSelect=false, array when true. */
    selectedItems: PropTypes.oneOfType([PropTypes.string, PropTypes.arrayOf(PropTypes.string)]),

    /** Default selected items (uncontrolled). */
    defaultSelectedItems: PropTypes.oneOfType([PropTypes.string, PropTypes.arrayOf(PropTypes.string)]),

    /** Allow selecting multiple items. */
    multiSelect: PropTypes.bool,

    /** Show checkboxes for selection. */
    checkboxSelection: PropTypes.bool,

    /** Disable all selection. */
    disableSelection: PropTypes.bool,

    /** Auto-propagate selection to parents/descendants. {parents: bool, descendants: bool} */
    selectionPropagation: PropTypes.exact({
        parents: PropTypes.bool,
        descendants: PropTypes.bool,
    }),

    // --- Expansion ---
    /** Controlled expanded item IDs. */
    expandedItems: PropTypes.arrayOf(PropTypes.string),

    /** Default expanded items (uncontrolled). */
    defaultExpandedItems: PropTypes.arrayOf(PropTypes.string),

    /** What triggers expansion: "content" or "iconContainer". */
    expansionTrigger: PropTypes.oneOf(['content', 'iconContainer']),

    // --- Editing ---
    /** Enable label editing. true = all items, or use editableItems for per-item control. */
    isItemEditable: PropTypes.bool,

    /** List of item IDs that are editable (alternative to isItemEditable=true). */
    editableItems: PropTypes.arrayOf(PropTypes.string),

    // --- Disabled ---
    /** List of item IDs that should be disabled. */
    disabledItems: PropTypes.arrayOf(PropTypes.string),

    /** Allow focus on disabled items. */
    disabledItemsFocusable: PropTypes.bool,

    // --- Appearance ---
    /** Indentation of children. Number (px) or string ("24px", "2rem"). */
    itemChildrenIndentation: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),

    /** Container height. */
    height: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),

    /** MUI sx styling object. */
    sx: PropTypes.object,

    // --- Icons ---
    /** MUI icon name for collapse icon (e.g. "ExpandMore"). */
    collapseIcon: PropTypes.string,

    /** MUI icon name for expand icon (e.g. "ChevronRight"). */
    expandIcon: PropTypes.string,

    /** MUI icon name for leaf/end icon. */
    endIcon: PropTypes.string,

    // --- Accessibility ---
    /** ARIA label for the tree. */
    ariaLabel: PropTypes.string,

    /** ID of element that labels the tree. */
    ariaLabelledBy: PropTypes.string,

    // --- Output Props ---
    /** Fired when item is clicked. {itemId, event_timestamp} */
    clickedItem: PropTypes.exact({
        itemId: PropTypes.string,
        event_timestamp: PropTypes.number,
    }),

    /** Fired when item is focused. {itemId, event_timestamp} */
    focusedItem: PropTypes.exact({
        itemId: PropTypes.string,
        event_timestamp: PropTypes.number,
    }),

    /** Fired when label edit completes. {itemId, newLabel, event_timestamp} */
    editedItemLabel: PropTypes.exact({
        itemId: PropTypes.string,
        newLabel: PropTypes.string,
        event_timestamp: PropTypes.number,
    }),

    /** Dash setProps callback */
    setProps: PropTypes.func,
};

export default TreeView;
