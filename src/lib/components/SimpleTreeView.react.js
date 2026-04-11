/**
 * SimpleTreeView — Dash wrapper for MUI X SimpleTreeView (Community)
 *
 * Converts a nested items array into TreeItem JSX children.
 * Lighter alternative to TreeView for static/simple trees.
 */
import React, {useCallback, useMemo} from 'react';
import PropTypes from 'prop-types';
import {SimpleTreeView as MuiSimpleTreeView} from '@mui/x-tree-view/SimpleTreeView';
import {TreeItem} from '@mui/x-tree-view/TreeItem';
import {resolveIcon} from '../fragments/iconResolver';

/** Recursively render items as TreeItem children, with optional per-item icons */
const renderItems = (items) => {
    if (!items || items.length === 0) return null;
    return items.map((item) => {
        const IconComponent = item.icon ? resolveIcon(item.icon) : null;
        const label = IconComponent ? (
            <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <IconComponent style={{ fontSize: 18, opacity: 0.7, flexShrink: 0 }} />
                <span>{item.label}</span>
            </span>
        ) : item.label;

        return (
            <TreeItem
                key={item.itemId}
                itemId={item.itemId}
                label={label}
                disabled={item.disabled}
                disableSelection={item.disableSelection}
            >
                {renderItems(item.children)}
            </TreeItem>
        );
    });
};

const SimpleTreeView = ({
    id,
    items = [],
    // Selection
    selectedItems,
    defaultSelectedItems,
    multiSelect = false,
    checkboxSelection = false,
    disableSelection = false,
    // Expansion
    expandedItems,
    defaultExpandedItems,
    expansionTrigger = 'content',
    // Disabled
    disabledItemsFocusable = false,
    // Appearance
    itemChildrenIndentation = '12px',
    height,
    sx,
    // Icons
    collapseIcon,
    expandIcon,
    endIcon,
    // Accessibility
    ariaLabel,
    ariaLabelledBy,
    // Dash
    setProps,
}) => {

    const slots = useMemo(() => {
        const s = {};
        if (collapseIcon) s.collapseIcon = resolveIcon(collapseIcon);
        if (expandIcon) s.expandIcon = resolveIcon(expandIcon);
        if (endIcon) s.endIcon = resolveIcon(endIcon);
        return Object.keys(s).length > 0 ? s : undefined;
    }, [collapseIcon, expandIcon, endIcon]);

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

    const containerStyle = useMemo(() => {
        const s = {};
        if (height) s.height = typeof height === 'number' ? `${height}px` : height;
        return s;
    }, [height]);

    return (
        <div id={id} style={containerStyle}>
            <MuiSimpleTreeView
                selectedItems={selectedItems}
                defaultSelectedItems={defaultSelectedItems}
                multiSelect={multiSelect}
                checkboxSelection={checkboxSelection}
                disableSelection={disableSelection}
                expandedItems={expandedItems}
                defaultExpandedItems={defaultExpandedItems}
                expansionTrigger={expansionTrigger}
                disabledItemsFocusable={disabledItemsFocusable}
                itemChildrenIndentation={itemChildrenIndentation}
                sx={sx}
                slots={slots}
                onSelectedItemsChange={handleSelectedItemsChange}
                onExpandedItemsChange={handleExpandedItemsChange}
                onItemClick={handleItemClick}
                aria-label={ariaLabel}
                aria-labelledby={ariaLabelledBy}
            >
                {renderItems(items)}
            </MuiSimpleTreeView>
        </div>
    );
};

SimpleTreeView.propTypes = {
    /** Dash component id */
    id: PropTypes.string,

    /**
     * Nested items array. Each item: {itemId: string, label: string, children?: [], disabled?: bool, disableSelection?: bool}
     */
    items: PropTypes.arrayOf(
        PropTypes.shape({
            itemId: PropTypes.string.isRequired,
            label: PropTypes.string.isRequired,
            children: PropTypes.array,
            disabled: PropTypes.bool,
            disableSelection: PropTypes.bool,
        })
    ),

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

    // --- Expansion ---
    /** Controlled expanded item IDs. */
    expandedItems: PropTypes.arrayOf(PropTypes.string),

    /** Default expanded items (uncontrolled). */
    defaultExpandedItems: PropTypes.arrayOf(PropTypes.string),

    /** What triggers expansion: "content" or "iconContainer". */
    expansionTrigger: PropTypes.oneOf(['content', 'iconContainer']),

    // --- Disabled ---
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

    /** Dash setProps callback */
    setProps: PropTypes.func,
};

export default SimpleTreeView;
