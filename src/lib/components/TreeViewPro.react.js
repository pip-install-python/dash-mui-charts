/**
 * TreeViewPro — Dash wrapper for MUI X RichTreeViewPro (Pro)
 *
 * Pro features: drag-and-drop reordering and lazy loading. Requires MUI Pro license key.
 *
 * Per-item controls (slider + kebab menu) can be enabled via `showItemControls`.
 * The slider stays responsive on desktop by holding a local value during the drag,
 * and pushes back to Dash on every change AND on commit.
 *
 * MUI components inside this wrapper follow the Mantine color scheme on <html>,
 * so the checkbox / slider / kebab menu re-skin automatically in dark mode.
 */
import React, {
    useCallback,
    useEffect,
    useMemo,
    useRef,
    useState,
} from 'react';
import PropTypes from 'prop-types';
import {LicenseInfo} from '@mui/x-license';
import {RichTreeViewPro} from '@mui/x-tree-view-pro/RichTreeViewPro';
import {TreeItem} from '@mui/x-tree-view/TreeItem';
import {ThemeProvider, createTheme} from '@mui/material/styles';
import Slider from '@mui/material/Slider';
import IconButton from '@mui/material/IconButton';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import {resolveIcon} from '../fragments/iconResolver';

let licenseKeySet = false;

// --- Color scheme: watch <html data-mantine-color-scheme="..."> ---------------
const readMantineScheme = () => {
    if (typeof document === 'undefined') return 'light';
    const v = document.documentElement.getAttribute('data-mantine-color-scheme');
    return v === 'dark' ? 'dark' : 'light';
};

const useMantineColorScheme = () => {
    const [scheme, setScheme] = useState(readMantineScheme);
    useEffect(() => {
        if (typeof document === 'undefined') return undefined;
        const html = document.documentElement;
        const sync = () => setScheme(readMantineScheme());
        const obs = new MutationObserver(sync);
        obs.observe(html, {
            attributes: true,
            attributeFilter: ['data-mantine-color-scheme'],
        });
        sync();
        return () => obs.disconnect();
    }, []);
    return scheme;
};

const lightTheme = createTheme({palette: {mode: 'light'}});
const darkTheme = createTheme({palette: {mode: 'dark'}});

// --- Color resolver ---------------------------------------------------------
// Accept Mantine color names ("teal", "blue.5"), CSS color values
// ("#ff6b6b", "rgb(...)", "oklch(...)"), or pre-formed CSS expressions
// ("var(--mantine-color-teal-6)", "light-dark(...)"). Bare names default to
// shade 6, matching Mantine's primaryShade default.
const MANTINE_NAME_RE = /^([a-zA-Z][a-zA-Z0-9_-]*)(\.(\d+))?$/;
const resolveSliderColor = (color) => {
    if (!color || typeof color !== 'string') return undefined;
    const m = color.match(MANTINE_NAME_RE);
    if (m) {
        const name = m[1];
        const shade = m[3] != null ? m[3] : '6';
        return `var(--mantine-color-${name}-${shade})`;
    }
    return color;
};

// --- applyReorder: walk a tree, lift the moved node, splice it back in -----
// Returns a new array — does not mutate input. Used to keep our outbound
// `orderedItems` in sync with MUI's internal reorder state.
const applyReorder = (items, change, idField, childrenField) => {
    if (!items || !change || !change.itemId) return items;
    const idK = idField || 'id';
    const childK = childrenField || 'children';
    const clone = JSON.parse(JSON.stringify(items));
    let moved = null;

    const removeFrom = (nodes, parentId) => {
        if (parentId == null) {
            const idx = nodes.findIndex((n) => n[idK] === change.itemId);
            if (idx >= 0) moved = nodes.splice(idx, 1)[0];
            return moved != null;
        }
        for (const n of nodes) {
            if (n[idK] === parentId) {
                const kids = n[childK] || [];
                const idx = kids.findIndex((c) => c[idK] === change.itemId);
                if (idx >= 0) moved = kids.splice(idx, 1)[0];
                return moved != null;
            }
            if (n[childK] && removeFrom(n[childK], parentId)) return true;
        }
        return false;
    };

    const insertTo = (nodes, parentId, idx) => {
        if (parentId == null) {
            nodes.splice(idx, 0, moved);
            return true;
        }
        for (const n of nodes) {
            if (n[idK] === parentId) {
                if (!n[childK]) n[childK] = [];
                n[childK].splice(idx, 0, moved);
                return true;
            }
            if (n[childK] && insertTo(n[childK], parentId, idx)) return true;
        }
        return false;
    };

    removeFrom(clone, change.oldPosition ? change.oldPosition.parentId : null);
    if (moved) {
        insertTo(
            clone,
            change.newPosition ? change.newPosition.parentId : null,
            change.newPosition ? change.newPosition.index : 0
        );
    }
    return clone;
};

// --- Shared context for per-item slider + kebab ------------------------------
const ItemControlsContext = React.createContext(null);

const ItemLabelWithControls = ({itemId, originalLabel}) => {
    const ctx = React.useContext(ItemControlsContext);
    const [menuAnchor, setMenuAnchor] = useState(null);

    // Hooks must run unconditionally — keep the local-value state outside the
    // early return so the hook order stays stable across renders.
    const externalValue = ctx?.sliderValues?.[itemId];
    const initial = typeof externalValue === 'number' ? externalValue : 0;
    const [localValue, setLocalValue] = useState(initial);
    const isDraggingRef = useRef(false);

    // Re-sync local from props when the user isn't actively dragging.
    useEffect(() => {
        if (!isDraggingRef.current && typeof externalValue === 'number') {
            setLocalValue(externalValue);
        }
    }, [externalValue]);

    if (!ctx) {
        return <span style={{flex: 1}}>{originalLabel}</span>;
    }

    const {
        controlsItemSet,
        sliderMin,
        sliderMax,
        sliderStep,
        sliderColor,
        onSliderChange,
        kebabMenuItems,
        onKebabAction,
    } = ctx;

    const showControls = !controlsItemSet || controlsItemSet.has(itemId);
    if (!showControls) {
        return <span style={{flex: 1}}>{originalLabel}</span>;
    }

    // Don't preventDefault on pointer/touch events — they can be passive and
    // the browser logs a warning. stopPropagation alone is enough to keep the
    // TreeItem from interpreting these as drag-to-reorder gestures.
    const stopReact = (e) => {
        e.stopPropagation();
    };

    // dragstart is always cancelable, so we can safely call preventDefault here
    // to keep HTML5 native drag (used by itemsReordering) off the slider/kebab.
    const blockNativeDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    return (
        <span
            style={{
                display: 'flex',
                alignItems: 'center',
                flex: 1,
                minWidth: 0,
                gap: '8px',
            }}
            onDragStart={blockNativeDrag}
        >
            <span
                style={{
                    flex: '0 1 auto',
                    minWidth: '60px',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                }}
            >
                {originalLabel}
            </span>
            <span
                onClick={stopReact}
                onMouseDown={stopReact}
                onPointerDown={stopReact}
                onTouchStart={stopReact}
                onDragStart={blockNativeDrag}
                draggable={false}
                style={{
                    flex: '1 1 120px',
                    minWidth: '80px',
                    maxWidth: '220px',
                    marginLeft: '12px',
                    marginRight: '4px',
                    display: 'flex',
                    alignItems: 'center',
                    touchAction: 'none',
                }}
            >
                <Slider
                    size="small"
                    value={typeof localValue === 'number' ? localValue : 0}
                    min={sliderMin}
                    max={sliderMax}
                    step={sliderStep}
                    valueLabelDisplay="auto"
                    sx={
                        sliderColor
                            ? {
                                  color: sliderColor,
                                  '& .MuiSlider-track': {
                                      backgroundColor: sliderColor,
                                      borderColor: sliderColor,
                                  },
                                  '& .MuiSlider-thumb': {
                                      backgroundColor: sliderColor,
                                  },
                                  '& .MuiSlider-thumb:hover, & .MuiSlider-thumb.Mui-focusVisible': {
                                      boxShadow: `0 0 0 8px color-mix(in srgb, ${sliderColor} 16%, transparent)`,
                                  },
                                  '& .MuiSlider-valueLabel': {
                                      backgroundColor: sliderColor,
                                  },
                                  '& .MuiSlider-rail': {
                                      backgroundColor: sliderColor,
                                  },
                              }
                            : undefined
                    }
                    onChange={(_, v) => {
                        isDraggingRef.current = true;
                        setLocalValue(v);
                        onSliderChange(itemId, v, false);
                    }}
                    onChangeCommitted={(_, v) => {
                        isDraggingRef.current = false;
                        setLocalValue(v);
                        onSliderChange(itemId, v, true);
                    }}
                />
            </span>
            <IconButton
                size="small"
                aria-label="item actions"
                onClick={(e) => {
                    e.stopPropagation();
                    setMenuAnchor(e.currentTarget);
                }}
                onMouseDown={stopReact}
                onPointerDown={stopReact}
                onTouchStart={stopReact}
                onDragStart={blockNativeDrag}
            >
                <MoreVertIcon fontSize="small" />
            </IconButton>
            <Menu
                anchorEl={menuAnchor}
                open={Boolean(menuAnchor)}
                onClose={() => setMenuAnchor(null)}
                onClick={stopReact}
            >
                {(kebabMenuItems || []).map((m) => {
                    const IconComp = m.icon ? resolveIcon(m.icon) : null;
                    return (
                        <MenuItem
                            key={m.value}
                            onClick={(e) => {
                                e.stopPropagation();
                                setMenuAnchor(null);
                                onKebabAction(itemId, m.value);
                            }}
                        >
                            {IconComp ? (
                                <ListItemIcon>
                                    <IconComp fontSize="small" />
                                </ListItemIcon>
                            ) : null}
                            <ListItemText>{m.label}</ListItemText>
                        </MenuItem>
                    );
                })}
            </Menu>
        </span>
    );
};

ItemLabelWithControls.propTypes = {
    itemId: PropTypes.string,
    originalLabel: PropTypes.node,
};

const CustomTreeItem = React.forwardRef(function CustomTreeItem(props, ref) {
    const {itemId, label, ...rest} = props;
    return (
        <TreeItem
            ref={ref}
            itemId={itemId}
            label={
                <ItemLabelWithControls itemId={itemId} originalLabel={label} />
            }
            {...rest}
        />
    );
});

CustomTreeItem.propTypes = {
    itemId: PropTypes.string,
    label: PropTypes.node,
};

// --- Main component ----------------------------------------------------------
const TreeViewPro = ({
    id,
    items: itemsProp = [],
    licenseKey = '',
    // Item accessors
    getItemId: getItemIdProp = 'id',
    getItemLabel: getItemLabelProp = 'label',
    getItemChildren: getItemChildrenProp = 'children',
    // Selection
    selectedItems,
    defaultSelectedItems,
    multiSelect = false,
    checkboxSelection = false,
    disableSelection = false,
    selectionPropagation,
    // Expansion
    expandedItems,
    defaultExpandedItems,
    expansionTrigger = 'content',
    // Editing
    isItemEditable = false,
    editableItems,
    // Disabled
    disabledItems,
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
    // PRO: Ordering
    itemsReordering = false,
    reorderableItems,
    // PRO: Lazy Loading
    lazyLoading = false,
    lazyLoadedChildren,
    // Per-item controls
    showItemControls = false,
    controlsItems,
    sliderValues,
    sliderMin = 0,
    sliderMax = 100,
    sliderStep = 1,
    sliderColor,
    kebabMenuItems,
    // Dash
    setProps,
}) => {
    const colorScheme = useMantineColorScheme();
    const muiTheme = colorScheme === 'dark' ? darkTheme : lightTheme;

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

    // --- Per-item controls: slider + kebab handlers ---
    const sliderValuesRef = useRef(sliderValues || {});
    sliderValuesRef.current = sliderValues || sliderValuesRef.current || {};

    const handleSliderChange = useCallback(
        (itemId, value, committed) => {
            const next = {...sliderValuesRef.current, [itemId]: value};
            sliderValuesRef.current = next;
            if (setProps) {
                setProps({sliderValues: next});
                if (committed) {
                    setProps({
                        sliderChange: {
                            itemId,
                            value,
                            event_timestamp: Date.now(),
                        },
                    });
                }
            }
        },
        [setProps]
    );

    const handleKebabAction = useCallback(
        (itemId, action) => {
            if (setProps) {
                setProps({
                    kebabAction: {
                        itemId,
                        action,
                        event_timestamp: Date.now(),
                    },
                });
            }
        },
        [setProps]
    );

    const controlsItemSet = useMemo(() => {
        if (!controlsItems || controlsItems.length === 0) return null;
        return new Set(controlsItems);
    }, [controlsItems]);

    const resolvedSliderColor = useMemo(
        () => resolveSliderColor(sliderColor),
        [sliderColor]
    );

    const controlsContextValue = useMemo(
        () => ({
            controlsItemSet,
            sliderValues: sliderValues || {},
            sliderMin,
            sliderMax,
            sliderStep,
            sliderColor: resolvedSliderColor,
            onSliderChange: handleSliderChange,
            kebabMenuItems: kebabMenuItems || [],
            onKebabAction: handleKebabAction,
        }),
        [
            controlsItemSet,
            sliderValues,
            sliderMin,
            sliderMax,
            sliderStep,
            resolvedSliderColor,
            kebabMenuItems,
            handleSliderChange,
            handleKebabAction,
        ]
    );

    // --- Slots ---
    const slots = useMemo(() => {
        const s = {};
        if (collapseIcon) s.collapseIcon = resolveIcon(collapseIcon);
        if (expandIcon) s.expandIcon = resolveIcon(expandIcon);
        if (endIcon) s.endIcon = resolveIcon(endIcon);
        if (showItemControls) s.item = CustomTreeItem;
        return Object.keys(s).length > 0 ? s : undefined;
    }, [collapseIcon, expandIcon, endIcon, showItemControls]);

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
                        break;
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

    // Track the live (reordered) tree so we can emit it as `orderedItems`.
    // Re-seed from the items prop whenever it changes externally.
    const orderedRef = useRef(itemsProp || []);
    useEffect(() => {
        orderedRef.current = itemsProp || [];
    }, [itemsProp]);

    const handleItemPositionChange = useCallback(
        (params) => {
            const updated = applyReorder(
                orderedRef.current,
                params,
                getItemIdProp,
                getItemChildrenProp
            );
            orderedRef.current = updated;
            if (setProps) {
                setProps({
                    itemPositionChanged: {
                        itemId: params.itemId,
                        oldPosition: params.oldPosition,
                        newPosition: params.newPosition,
                        event_timestamp: Date.now(),
                    },
                    orderedItems: updated,
                });
            }
        },
        [setProps, getItemIdProp, getItemChildrenProp]
    );

    const containerStyle = useMemo(() => {
        const s = {};
        if (height) s.height = typeof height === 'number' ? `${height}px` : height;
        return s;
    }, [height]);

    return (
        <ThemeProvider theme={muiTheme}>
            <div id={id} style={containerStyle}>
                <ItemControlsContext.Provider value={controlsContextValue}>
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
                </ItemControlsContext.Provider>
            </div>
        </ThemeProvider>
    );
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

    /**
     * Output: the current tree after any drag-and-drop reorder, preserving
     * each node's original fields (id, label, children, etc.). Updates on
     * every reorder so Python callbacks can render the live order.
     */
    orderedItems: PropTypes.arrayOf(PropTypes.object),

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

    // --- Per-item controls (slider + kebab) ---
    /** Show a Slider + kebab menu on each item row. */
    showItemControls: PropTypes.bool,

    /** Restrict slider+kebab to a subset of item IDs. Empty/omitted means all items. */
    controlsItems: PropTypes.arrayOf(PropTypes.string),

    /** Controlled slider values keyed by itemId, e.g. {"task-1": 40}. Also updated as user drags. */
    sliderValues: PropTypes.object,

    /** Slider minimum. */
    sliderMin: PropTypes.number,

    /** Slider maximum. */
    sliderMax: PropTypes.number,

    /** Slider step. */
    sliderStep: PropTypes.number,

    /**
     * Slider color. Accepts a Mantine theme color name ("teal", "blue.5"),
     * a CSS color literal ("#ff6b6b", "rgb(...)"), or a CSS expression
     * ("var(--mantine-color-teal-6)", "light-dark(...)"). Bare names use
     * shade 6 by default. When omitted, the slider falls back to MUI's
     * `primary` palette color.
     */
    sliderColor: PropTypes.string,

    /** Kebab menu options: [{label, value, icon?}]. `value` is sent back as `action`. */
    kebabMenuItems: PropTypes.arrayOf(
        PropTypes.exact({
            label: PropTypes.string.isRequired,
            value: PropTypes.string.isRequired,
            icon: PropTypes.string,
        })
    ),

    /** Output: fires once on each commit (mouse-up) of a slider drag. {itemId, value, event_timestamp} */
    sliderChange: PropTypes.exact({
        itemId: PropTypes.string,
        value: PropTypes.number,
        event_timestamp: PropTypes.number,
    }),

    /** Output: fires when a kebab menu item is chosen. {itemId, action, event_timestamp} */
    kebabAction: PropTypes.exact({
        itemId: PropTypes.string,
        action: PropTypes.string,
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
