/**
 * TreeViewPro — Dash wrapper for MUI X RichTreeViewPro (Pro)
 *
 * Extends TreeView with drag-and-drop ordering, lazy loading.
 * Requires MUI Pro license key.
 */
import React, {useCallback, useMemo, useState, useEffect} from 'react';
import PropTypes from 'prop-types';
import {LicenseInfo} from '@mui/x-license';
import {RichTreeViewPro} from '@mui/x-tree-view-pro/RichTreeViewPro';
import {resolveIcon} from '../fragments/iconResolver';

let licenseKeySet = false;

const TreeViewPro = (props) => {
    const {
        id,
        items: itemsProp,
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

    // --- License key ---
    if (licenseKey && !licenseKeySet) {
        LicenseInfo.setLicenseKey(licenseKey);
        licenseKeySet = true;
    }

    // --- Lazy loading: merge loaded children into items ---
    const items = useMemo(() => {
        if (!lazyLoading || !lazyLoadedChildren || !itemsProp) return itemsProp || [];
        const childrenProp = getItemChildrenProp || 'children';
        const idProp = getItemIdProp || 'id';

        const mergeChildren = (nodeList) => {
            if (!nodeList) return nodeList;
            return nodeList.map((node) => {
                const nodeId = node[idProp];
                const loadedKids = lazyLoadedChildren[nodeId];
                const existingChildren = node[childrenProp];
                const mergedChildren = loadedKids || existingChildren;
                return {
                    ...node,
                    [childrenProp]: mergeChildren(mergedChildren),
                };
            });
        };
        return mergeChildren(itemsProp);
    }, [itemsProp, lazyLoadedChildren, lazyLoading, getItemChildrenProp, getItemIdProp]);

    // --- Accessor conversion ---
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

            // Lazy loading: fire request for items that have no children
            if (lazyLoading && setProps && itemIds) {
                const idProp = getItemIdProp || 'id';
                const childrenProp = getItemChildrenProp || 'children';
                const findItem = (nodes, targetId) => {
                    if (!nodes) return null;
                    for (const node of nodes) {
                        if (node[idProp] === targetId) return node;
                        const found = findItem(node[childrenProp], targetId);
                        if (found) return found;
                    }
                    return null;
                };

                // Check newly expanded items for missing children
                for (const itemId of itemIds) {
                    const item = findItem(items, itemId);
                    if (item && !item[childrenProp]) {
                        setProps({
                            lazyLoadRequest: {
                                itemId,
                                event_timestamp: Date.now(),
                            },
                        });
                        break; // one request at a time
                    }
                }
            }
        },
        [setProps, lazyLoading, items, getItemIdProp, getItemChildrenProp]
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

    /** Auto-propagate selection to parents/descendants. */
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
    /** Enable label editing for all items. */
    isItemEditable: PropTypes.bool,

    /** List of item IDs that are editable. */
    editableItems: PropTypes.arrayOf(PropTypes.string),

    // --- Disabled ---
    /** List of item IDs that should be disabled. */
    disabledItems: PropTypes.arrayOf(PropTypes.string),

    /** Allow focus on disabled items. */
    disabledItemsFocusable: PropTypes.bool,

    // --- Appearance ---
    /** Indentation of children. */
    itemChildrenIndentation: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),

    /** Container height. */
    height: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),

    /** MUI sx styling object. */
    sx: PropTypes.object,

    // --- Icons ---
    /** MUI icon name for collapse icon. */
    collapseIcon: PropTypes.string,

    /** MUI icon name for expand icon. */
    expandIcon: PropTypes.string,

    /** MUI icon name for leaf/end icon. */
    endIcon: PropTypes.string,

    // --- Accessibility ---
    /** ARIA label for the tree. */
    ariaLabel: PropTypes.string,

    /** ID of element that labels the tree. */
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

export default TreeViewPro;
