/**
 * SimpleTreeView — Dash wrapper for MUI X SimpleTreeView (Community)
 *
 * Converts a nested items array into <TreeItem> JSX children.
 * This is a STUB — Claude Code should implement the full component.
 */
import React, {useCallback, useMemo} from 'react';
import PropTypes from 'prop-types';
import {SimpleTreeView as MuiSimpleTreeView} from '@mui/x-tree-view/SimpleTreeView';
import {TreeItem} from '@mui/x-tree-view/TreeItem';
import {resolveIcon} from '../fragments/iconResolver';

/** Recursively render items as TreeItem children */
const renderItems = (items) => {
    if (!items || items.length === 0) return null;
    return items.map((item) => (
        <TreeItem
            key={item.itemId}
            itemId={item.itemId}
            label={item.label}
            disabled={item.disabled}
            disableSelection={item.disableSelection}
        >
            {renderItems(item.children)}
        </TreeItem>
    ));
};

const SimpleTreeView = (props) => {
    const {
        id,
        items,
        // Selection
        selectedItems,
        defaultSelectedItems,
        multiSelect,
        checkboxSelection,
        disableSelection,
        // Expansion
        expandedItems,
        defaultExpandedItems,
        expansionTrigger,
        // Disabled
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
        // Dash
        setProps,
    } = props;

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

SimpleTreeView.defaultProps = {
    items: [],
    multiSelect: false,
    checkboxSelection: false,
    disableSelection: false,
    disabledItemsFocusable: false,
    expansionTrigger: 'content',
    itemChildrenIndentation: '12px',
};

SimpleTreeView.propTypes = {
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

    // Selection
    selectedItems: PropTypes.oneOfType([PropTypes.string, PropTypes.arrayOf(PropTypes.string)]),
    defaultSelectedItems: PropTypes.oneOfType([PropTypes.string, PropTypes.arrayOf(PropTypes.string)]),
    multiSelect: PropTypes.bool,
    checkboxSelection: PropTypes.bool,
    disableSelection: PropTypes.bool,

    // Expansion
    expandedItems: PropTypes.arrayOf(PropTypes.string),
    defaultExpandedItems: PropTypes.arrayOf(PropTypes.string),
    expansionTrigger: PropTypes.oneOf(['content', 'iconContainer']),

    // Disabled
    disabledItemsFocusable: PropTypes.bool,

    // Appearance
    itemChildrenIndentation: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    height: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    sx: PropTypes.object,

    // Icons
    collapseIcon: PropTypes.string,
    expandIcon: PropTypes.string,
    endIcon: PropTypes.string,

    // Accessibility
    ariaLabel: PropTypes.string,
    ariaLabelledBy: PropTypes.string,

    // Output
    clickedItem: PropTypes.exact({
        itemId: PropTypes.string,
        event_timestamp: PropTypes.number,
    }),

    setProps: PropTypes.func,
};

export default SimpleTreeView;
