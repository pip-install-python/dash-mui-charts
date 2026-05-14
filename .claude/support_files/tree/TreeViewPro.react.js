/**
 * TreeViewPro — Dash wrapper for MUI X RichTreeViewPro (Pro)
 *
 * Extends TreeView with drag-and-drop ordering, lazy loading, virtualization.
 * Requires MUI Pro license key.
 * This is a STUB — Claude Code should implement the full component.
 */
import React, {useCallback, useMemo, useEffect, useRef} from 'react';
import PropTypes from 'prop-types';
import {RichTreeViewPro} from '@mui/x-tree-view-pro/RichTreeViewPro';
import {resolveIcon} from '../fragments/iconResolver';

const TreeViewPro = (props) => {
    const {
        id,
        items,
        licenseKey,
        // Item accessors
        getItemId: getItemIdProp,
        getItemLabel: getItemLabelProp,
        getItemChildren: getItemChildrenProp,
        // Selection (same as TreeView)
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
        // Icons
        collapseIcon,
        expandIcon,
        endIcon,
        // Accessibility
        ariaLabel,
        ariaLabelledBy,
        // --- PRO: Ordering ---
        itemsReordering,
        reorderableItems,
        // --- PRO: Lazy Loading ---
        lazyLoading,
        lazyLoadedChildren,
        // Dash
        setProps,
        ...otherProps
    } = props;

    // --- Accessor conversion (same as TreeView) ---
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

    // --- Disabled/editable conversion ---
    const isItemDisabledFn = useMemo(() => {
        if (!disabledItems || disabledItems.length === 0) return undefined;
        const s = new Set(disabledItems);
        return (item) => s.has(getItemId(item));
    }, [disabledItems, getItemId]);

    const isItemEditableFn = useMemo(() => {
        if (typeof isItemEditable === 'boolean') return isItemEditable;
        if (editableItems && editableItems.length > 0) {
            const s = new Set(editableItems);
            return (item) => s.has(getItemId(item));
        }
        return false;
    }, [isItemEditable, editableItems, getItemId]);

    // --- PRO: Reorderable conversion ---
    const isItemReorderableFn = useMemo(() => {
        if (!reorderableItems || reorderableItems.length === 0) return undefined;
        const s = new Set(reorderableItems);
        return (itemId) => s.has(itemId);
    }, [reorderableItems]);

    // --- Slots ---
    const slots = useMemo(() => {
        const s = {};
        if (collapseIcon) s.collapseIcon = resolveIcon(collapseIcon);
        if (expandIcon) s.expandIcon = resolveIcon(expandIcon);
        if (endIcon) s.endIcon = resolveIcon(endIcon);
        return Object.keys(s).length > 0 ? s : undefined;
    }, [collapseIcon, expandIcon, endIcon]);

    // --- Callbacks ---
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

    // --- PRO: Reorder callback ---
    const handleItemPositionChange = useCallback(
        (params) => {
            if (setProps) {
                setProps({
                    itemPositionChanged: {
                        itemId: params.itemId,
                        oldPosition: params.oldPosition,
                        newPosition: params.newPosition,
                        event_timestamp: Date.now(),
                    },
                });
            }
        },
        [setProps]
    );

    // --- PRO: Lazy loading bridge ---
    // TODO: Implement the dataSource bridge pattern.
    // When a node with no children is expanded, fire lazyLoadRequest.
    // When lazyLoadedChildren changes, merge into the tree.
    // This requires maintaining internal items state that merges
    // the original `items` prop with dynamically loaded children.

    const containerStyle = useMemo(() => {
        const s = {};
        if (height) s.height = typeof height === 'number' ? `${height}px` : height;
        return s;
    }, [height]);

    return (
        <div id={id} style={containerStyle}>
            <RichTreeViewPro
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
                // PRO: Ordering
                itemsReordering={itemsReordering}
                isItemReorderable={isItemReorderableFn}
                onItemPositionChange={handleItemPositionChange}
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

TreeViewPro.defaultProps = {
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
    itemsReordering: false,
    lazyLoading: false,
    licenseKey: '',
};

TreeViewPro.propTypes = {
    /** Dash component id */
    id: PropTypes.string,

    /** MUI X Pro license key. Required for Pro features. */
    licenseKey: PropTypes.string,

    /** Array of item objects. */
    items: PropTypes.arrayOf(PropTypes.object),

    // --- Accessors ---
    getItemId: PropTypes.string,
    getItemLabel: PropTypes.string,
    getItemChildren: PropTypes.string,

    // --- Selection (same as TreeView) ---
    selectedItems: PropTypes.oneOfType([PropTypes.string, PropTypes.arrayOf(PropTypes.string)]),
    defaultSelectedItems: PropTypes.oneOfType([PropTypes.string, PropTypes.arrayOf(PropTypes.string)]),
    multiSelect: PropTypes.bool,
    checkboxSelection: PropTypes.bool,
    disableSelection: PropTypes.bool,
    selectionPropagation: PropTypes.exact({
        parents: PropTypes.bool,
        descendants: PropTypes.bool,
    }),

    // --- Expansion ---
    expandedItems: PropTypes.arrayOf(PropTypes.string),
    defaultExpandedItems: PropTypes.arrayOf(PropTypes.string),
    expansionTrigger: PropTypes.oneOf(['content', 'iconContainer']),

    // --- Editing ---
    isItemEditable: PropTypes.bool,
    editableItems: PropTypes.arrayOf(PropTypes.string),

    // --- Disabled ---
    disabledItems: PropTypes.arrayOf(PropTypes.string),
    disabledItemsFocusable: PropTypes.bool,

    // --- Appearance ---
    itemChildrenIndentation: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    height: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    sx: PropTypes.object,

    // --- Icons ---
    collapseIcon: PropTypes.string,
    expandIcon: PropTypes.string,
    endIcon: PropTypes.string,

    // --- Accessibility ---
    ariaLabel: PropTypes.string,
    ariaLabelledBy: PropTypes.string,

    // --- PRO: Ordering ---
    /** Enable drag-and-drop item reordering. */
    itemsReordering: PropTypes.bool,

    /** List of item IDs that can be reordered. If empty, all items are reorderable. */
    reorderableItems: PropTypes.arrayOf(PropTypes.string),

    /** Output: Fired after item reorder. {itemId, oldPosition, newPosition, event_timestamp} */
    itemPositionChanged: PropTypes.object,

    // --- PRO: Lazy Loading ---
    /** Enable lazy loading mode. */
    lazyLoading: PropTypes.bool,

    /** Input: Children loaded by Dash callback. {parentItemId: [childItems]} */
    lazyLoadedChildren: PropTypes.object,

    /** Output: Fired when unloaded node is expanded. {itemId, event_timestamp} */
    lazyLoadRequest: PropTypes.exact({
        itemId: PropTypes.string,
        event_timestamp: PropTypes.number,
    }),

    // --- Output Props (same as TreeView) ---
    clickedItem: PropTypes.exact({
        itemId: PropTypes.string,
        event_timestamp: PropTypes.number,
    }),
    focusedItem: PropTypes.exact({
        itemId: PropTypes.string,
        event_timestamp: PropTypes.number,
    }),
    editedItemLabel: PropTypes.exact({
        itemId: PropTypes.string,
        newLabel: PropTypes.string,
        event_timestamp: PropTypes.number,
    }),

    /** Dash setProps callback */
    setProps: PropTypes.func,
};

export default TreeViewPro;
