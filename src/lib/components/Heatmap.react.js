import React, { useMemo } from 'react';
import PropTypes from 'prop-types';
import { LicenseInfo } from '@mui/x-license';
import { Heatmap as MuiHeatmap } from '@mui/x-charts-pro/Heatmap';

// Track if license key has been set globally
let licenseKeySet = false;

/**
 * Default cell component with click handling.
 * Simple rectangle that passes click events to parent.
 */
function DefaultCell(props) {
    const { x, y, width, height, ownerState, onCellClick, ...other } = props;

    const handleClick = (event) => {
        if (onCellClick) {
            onCellClick(event, {
                dataIndex: ownerState.dataIndex,
                value: ownerState.value,
                color: ownerState.color,
            });
        }
    };

    return (
        <rect
            {...other}
            x={x}
            y={y}
            width={width}
            height={height}
            fill={ownerState.color}
            onClick={handleClick}
            style={{ cursor: 'pointer' }}
        />
    );
}

/**
 * Custom cell component for rounded corners with gap and optional value display.
 * Inspired by MUI X Charts custom cell example.
 */
function RoundedCell(props) {
    const { x, y, width, height, ownerState, cellConfig, onCellClick, ...other } = props;
    const {
        gap = 4,
        borderRadius = 10,
        showValue = true,
        fontSize = 12,
        fontWeight = 500,
        textColor = '#ffffff',
    } = cellConfig || {};

    const handleClick = (event) => {
        if (onCellClick) {
            onCellClick(event, {
                dataIndex: ownerState.dataIndex,
                value: ownerState.value,
                color: ownerState.color,
            });
        }
    };

    return (
        <React.Fragment>
            <rect
                {...other}
                x={x + gap}
                y={y + gap}
                width={Math.max(0, width - 2 * gap)}
                height={Math.max(0, height - 2 * gap)}
                fill={ownerState.color}
                clipPath={ownerState.isHighlighted ? undefined : `inset(0px round ${borderRadius}px)`}
                rx={borderRadius}
                ry={borderRadius}
                onClick={handleClick}
                style={{ cursor: 'pointer' }}
            />
            {showValue && (
                <text
                    x={x + width / 2}
                    y={y + height / 2}
                    textAnchor="middle"
                    dominantBaseline="middle"
                    pointerEvents="none"
                    style={{
                        fontSize: `${fontSize}px`,
                        fontWeight,
                        fill: textColor,
                        fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif',
                    }}
                >
                    {ownerState.value}
                </text>
            )}
        </React.Fragment>
    );
}

/**
 * Heatmap component wrapping MUI X Charts Pro Heatmap.
 * Renders a matrix visualization where color intensity represents values.
 * This is a Pro feature - requires MUI X Pro license key.
 */
export default function Heatmap(props) {
    const {
        id,
        licenseKey,
        data = [],
        xAxis,
        yAxis,
        colorScale,
        width,
        height = 400,
        margin,
        hideLegend = false,
        tooltip,
        highlightScope,
        cellStyle,
        slotProps,
        // Dash-specific output props
        highlightedItem,
        clickData,
        n_clicks = 0,
        setProps,
    } = props;

    // Set license key once globally (before any render)
    if (licenseKey && !licenseKeySet) {
        LicenseInfo.setLicenseKey(licenseKey);
        licenseKeySet = true;
    }

    // Process data into series format required by MUI Heatmap
    // Input: [[x, y, value], ...] or already in series format
    const processedSeries = useMemo(() => {
        if (!data || data.length === 0) return [{ data: [] }];

        // Check if data is already in series format
        if (data[0] && typeof data[0] === 'object' && 'data' in data[0]) {
            return data;
        }

        // Convert flat array of [x, y, value] tuples to series format
        return [{
            data: data,
        }];
    }, [data]);

    // Process colorScale into zAxis format
    const zAxisConfig = useMemo(() => {
        if (!colorScale) return undefined;

        if (colorScale.type === 'piecewise') {
            return [{
                colorMap: {
                    type: 'piecewise',
                    thresholds: colorScale.thresholds || [],
                    colors: colorScale.colors || [],
                },
            }];
        }

        // Default to continuous
        return [{
            colorMap: {
                type: 'continuous',
                min: colorScale.min ?? 0,
                max: colorScale.max ?? 100,
                color: colorScale.colors || ['#e3f2fd', '#1565c0'],
            },
        }];
    }, [colorScale]);

    // Handle highlight change
    const handleHighlightChange = (item) => {
        if (setProps) {
            setProps({ highlightedItem: item });
        }
    };

    // Handle cell click (called from custom cell components)
    const handleCellClick = (event, params) => {
        if (setProps && params) {
            setProps({
                clickData: {
                    x: params.dataIndex?.[0],
                    y: params.dataIndex?.[1],
                    value: params.value,
                    color: params.color,
                    timestamp: new Date().toISOString(),
                },
                n_clicks: (n_clicks || 0) + 1,
            });
        }
    };

    // Build props for MUI Heatmap
    const heatmapProps = {
        series: processedSeries,
        height,
    };

    // Add optional props
    if (xAxis) {
        // Ensure xAxis is in array format and has band scaleType
        heatmapProps.xAxis = Array.isArray(xAxis) ? xAxis : [{
            ...xAxis,
            scaleType: xAxis.scaleType || 'band',
        }];
    }

    if (yAxis) {
        // Ensure yAxis is in array format and has band scaleType
        heatmapProps.yAxis = Array.isArray(yAxis) ? yAxis : [{
            ...yAxis,
            scaleType: yAxis.scaleType || 'band',
        }];
    }

    if (zAxisConfig) heatmapProps.zAxis = zAxisConfig;
    if (width) heatmapProps.width = width;
    if (margin) heatmapProps.margin = margin;
    if (hideLegend) heatmapProps.hideLegend = hideLegend;

    // Tooltip configuration
    if (tooltip) {
        heatmapProps.slotProps = {
            ...heatmapProps.slotProps,
            tooltip: { trigger: tooltip.trigger || 'item' },
        };
    }

    // Always use custom cell component for click handling
    // Use RoundedCell if cellStyle is specified, otherwise DefaultCell
    if (cellStyle === 'rounded' || (cellStyle && typeof cellStyle === 'object')) {
        const cellConfig = typeof cellStyle === 'object' ? cellStyle : {};

        // Create a wrapped component that passes cellConfig and click handler
        const CustomCell = (cellProps) => (
            <RoundedCell {...cellProps} cellConfig={cellConfig} onCellClick={handleCellClick} />
        );

        heatmapProps.slots = {
            ...heatmapProps.slots,
            cell: CustomCell,
        };
    } else {
        // Default cell with click handling
        const CustomCell = (cellProps) => (
            <DefaultCell {...cellProps} onCellClick={handleCellClick} />
        );

        heatmapProps.slots = {
            ...heatmapProps.slots,
            cell: CustomCell,
        };
    }

    // Additional slotProps from user
    if (slotProps) {
        heatmapProps.slotProps = {
            ...heatmapProps.slotProps,
            ...slotProps,
        };
    }

    // Highlight scope for series
    if (highlightScope) {
        heatmapProps.series = processedSeries.map(s => ({
            ...s,
            highlightScope,
        }));
    }

    // Event handlers (onHighlightChange only - click handled via custom cell)
    heatmapProps.onHighlightChange = handleHighlightChange;

    return (
        <div id={id}>
            <MuiHeatmap {...heatmapProps} />
        </div>
    );
}

Heatmap.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * MUI X Pro license key. Required to enable Pro features without watermarks.
     * Get your license key from https://mui.com/x/introduction/licensing/
     */
    licenseKey: PropTypes.string,

    /**
     * Heatmap data as an array of [x, y, value] tuples.
     * - x: X-axis index (0-based)
     * - y: Y-axis index (0-based)
     * - value: Numeric value for the cell (mapped to color)
     *
     * Example: [[0, 0, 25], [0, 1, 45], [1, 0, 30], [1, 1, 60]]
     */
    data: PropTypes.arrayOf(
        PropTypes.arrayOf(PropTypes.number)
    ),

    /**
     * X-axis configuration object.
     * - data (array): Category labels for x-axis
     * - label (string): Axis label
     * - scaleType (string): Scale type, defaults to 'band' for heatmaps
     */
    xAxis: PropTypes.shape({
        data: PropTypes.array,
        label: PropTypes.string,
        scaleType: PropTypes.oneOf(['band', 'point']),
    }),

    /**
     * Y-axis configuration object.
     * - data (array): Category labels for y-axis
     * - label (string): Axis label
     * - scaleType (string): Scale type, defaults to 'band' for heatmaps
     */
    yAxis: PropTypes.shape({
        data: PropTypes.array,
        label: PropTypes.string,
        scaleType: PropTypes.oneOf(['band', 'point']),
    }),

    /**
     * Color scale configuration for mapping values to colors.
     *
     * Continuous scale (interpolates between colors):
     * { type: 'continuous', min: 0, max: 100, colors: ['#e3f2fd', '#1565c0'] }
     *
     * Piecewise scale (discrete color bands):
     * { type: 'piecewise', thresholds: [20, 40, 60, 80],
     *   colors: ['#color1', '#color2', '#color3', '#color4', '#color5'] }
     *
     * Note: For piecewise, you need n+1 colors for n thresholds.
     */
    colorScale: PropTypes.shape({
        type: PropTypes.oneOf(['continuous', 'piecewise']),
        min: PropTypes.number,
        max: PropTypes.number,
        colors: PropTypes.arrayOf(PropTypes.string),
        thresholds: PropTypes.arrayOf(PropTypes.number),
    }),

    /**
     * Chart width in pixels. If not specified, the chart expands to fill
     * the available space.
     */
    width: PropTypes.number,

    /**
     * Chart height in pixels. Default is 400.
     */
    height: PropTypes.number,

    /**
     * Chart margins in pixels. Object with top, right, bottom, left keys.
     */
    margin: PropTypes.shape({
        top: PropTypes.number,
        right: PropTypes.number,
        bottom: PropTypes.number,
        left: PropTypes.number,
    }),

    /**
     * If true, the color legend is hidden.
     */
    hideLegend: PropTypes.bool,

    /**
     * Tooltip configuration.
     * - trigger (string): 'item' to show on cell hover, 'none' to disable
     */
    tooltip: PropTypes.shape({
        trigger: PropTypes.oneOf(['item', 'none']),
    }),

    /**
     * Highlight scope configuration for cell highlighting behavior.
     * - highlight: 'item' or 'none'
     * - fade: 'global' or 'none'
     */
    highlightScope: PropTypes.shape({
        highlight: PropTypes.oneOf(['item', 'none']),
        fade: PropTypes.oneOf(['global', 'none']),
    }),

    /**
     * Custom cell style. Use 'rounded' for default rounded corners with gap,
     * or provide an object for detailed configuration:
     * - gap (number): Spacing between cells in pixels (default: 4)
     * - borderRadius (number): Corner radius in pixels (default: 10)
     * - showValue (boolean): Display value text in cells (default: true)
     * - fontSize (number): Font size for value text (default: 12)
     * - fontWeight (number): Font weight for value text (default: 500)
     * - textColor (string): Color for value text (default: '#ffffff')
     */
    cellStyle: PropTypes.oneOfType([
        PropTypes.oneOf(['rounded']),
        PropTypes.shape({
            gap: PropTypes.number,
            borderRadius: PropTypes.number,
            showValue: PropTypes.bool,
            fontSize: PropTypes.number,
            fontWeight: PropTypes.number,
            textColor: PropTypes.string,
        }),
    ]),

    /**
     * Props passed to internal slot components for customization.
     */
    slotProps: PropTypes.object,

    /**
     * Currently highlighted item. Read-only output property updated when
     * the user hovers over a cell.
     */
    highlightedItem: PropTypes.object,

    /**
     * Data from the most recent click event. Read-only output property.
     * Contains x, y, value, seriesId, and timestamp.
     */
    clickData: PropTypes.object,

    /**
     * Number of times the chart has been clicked. Increments on each click event.
     */
    n_clicks: PropTypes.number,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func,
};
