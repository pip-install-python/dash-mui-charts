import React, { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { SparkLineChart as MuiSparkLineChart } from '@mui/x-charts/SparkLineChart';

/**
 * SparklineChart component wrapping MUI X Charts SparkLineChart.
 * Renders compact, inline charts perfect for dashboards, tables, and KPI cards.
 * This is a Community feature - no license key required.
 *
 * Supports both controlled and uncontrolled highlight states for interactive
 * dashboards where hovering on a sparkline updates other components.
 */
export default function SparklineChart(props) {
    const {
        id,
        data = [],
        plotType = 'line',
        width,
        height = 36,
        color,
        colors,
        area = false,
        curve = 'linear',
        showTooltip = false,
        showHighlight = false,
        margin,
        xAxis,
        yAxis,
        axisHighlight,
        slotProps,
        clipAreaOffset,
        baseline,
        strokeWidth,
        disableClipping = false,
        // Controlled highlight props
        highlightedIndex,
        // Dash-specific output props
        highlightedItem,
        hoverIndex,
        hoverValue,
        n_hovers = 0,
        setProps,
    } = props;

    // Internal state for tracking highlight (for controlled mode)
    const [internalHighlightIndex, setInternalHighlightIndex] = useState(highlightedIndex);

    // Track last prop value to detect external changes
    const lastHighlightPropRef = useRef(highlightedIndex);

    // Sync external highlightedIndex prop to internal state
    useEffect(() => {
        if (highlightedIndex !== lastHighlightPropRef.current) {
            lastHighlightPropRef.current = highlightedIndex;
            setInternalHighlightIndex(highlightedIndex);
        }
    }, [highlightedIndex]);

    // Handle highlight change events from chart interaction
    const handleHighlightChange = (item) => {
        if (setProps) {
            setProps({ highlightedItem: item });
        }
    };

    // Handle axis highlight change (provides dataIndex)
    const handleHighlightedAxisChange = (axisItems) => {
        const dataIndex = axisItems?.[0]?.dataIndex ?? null;
        const value = dataIndex !== null && data[dataIndex] !== undefined ? data[dataIndex] : null;

        // Update internal state
        setInternalHighlightIndex(dataIndex);
        lastHighlightPropRef.current = dataIndex;

        if (setProps) {
            setProps({
                hoverIndex: dataIndex,
                hoverValue: value,
                n_hovers: (n_hovers || 0) + 1,
            });
        }
    };

    // Build props for MUI SparkLineChart
    const sparklineProps = {
        data,
        plotType,
        height,
    };

    // Add optional props only if defined
    if (width) sparklineProps.width = width;

    // Handle color - pass directly to MUI SparkLineChart
    // MUI accepts 'color' prop directly for single color
    if (color) {
        sparklineProps.color = color;
    } else if (colors) {
        sparklineProps.colors = colors;
    }

    // Disable clipping option
    if (disableClipping) {
        sparklineProps.disableClipping = true;
    }

    if (margin) sparklineProps.margin = margin;

    // X-axis configuration
    if (xAxis) {
        sparklineProps.xAxis = xAxis;
    }

    // Y-axis configuration
    if (yAxis) {
        sparklineProps.yAxis = yAxis;
    }

    // Line-specific props (only apply when plotType is 'line')
    if (plotType === 'line') {
        sparklineProps.area = area;
        sparklineProps.curve = curve;
        if (baseline !== undefined) {
            sparklineProps.baseline = baseline;
        }
    }

    // Interactive features
    sparklineProps.showTooltip = showTooltip;
    sparklineProps.showHighlight = showHighlight;

    // Axis highlight configuration
    if (axisHighlight) {
        sparklineProps.axisHighlight = axisHighlight;
    }

    // Slot props for customizing internal components
    // Merge strokeWidth into slotProps.line if provided
    if (slotProps || strokeWidth) {
        const mergedSlotProps = { ...slotProps };
        if (strokeWidth) {
            mergedSlotProps.line = {
                ...(slotProps?.line || {}),
                strokeWidth,
            };
        }
        sparklineProps.slotProps = mergedSlotProps;
    }

    // Clip area offset
    if (clipAreaOffset) {
        sparklineProps.clipAreaOffset = clipAreaOffset;
    }

    // Event handlers
    if (showHighlight) {
        sparklineProps.onHighlightChange = handleHighlightChange;
        sparklineProps.onHighlightedAxisChange = handleHighlightedAxisChange;
    }

    // Controlled highlight - set highlightedAxis based on internal state
    if (internalHighlightIndex !== null && internalHighlightIndex !== undefined && xAxis?.id) {
        sparklineProps.highlightedAxis = [{ axisId: xAxis.id, dataIndex: internalHighlightIndex }];
    }

    return (
        <div id={id} style={{ display: 'inline-block' }}>
            <MuiSparkLineChart {...sparklineProps} />
        </div>
    );
}

SparklineChart.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * Array of numeric values to display in the sparkline.
     * This is the primary data for the chart.
     */
    data: PropTypes.arrayOf(PropTypes.number).isRequired,

    /**
     * Type of plot to render.
     * - 'line': Renders a line chart (default)
     * - 'bar': Renders a bar chart
     */
    plotType: PropTypes.oneOf(['line', 'bar']),

    /**
     * Chart width in pixels. If not specified, the chart will
     * expand to fill the available space.
     */
    width: PropTypes.number,

    /**
     * Chart height in pixels. Default is 36 for compact inline display.
     */
    height: PropTypes.number,

    /**
     * Single color for the sparkline. Can be any valid CSS color string.
     * Example: '#1976d2', 'rgb(25, 118, 210)', 'blue'
     */
    color: PropTypes.string,

    /**
     * Array of colors for the sparkline. Use this for multi-color configurations.
     */
    colors: PropTypes.arrayOf(PropTypes.string),

    /**
     * If true, fills the area under the line. Only applies when plotType is 'line'.
     */
    area: PropTypes.bool,

    /**
     * Curve interpolation method for line charts.
     * Options: 'linear', 'monotoneX', 'monotoneY', 'natural', 'step',
     * 'stepBefore', 'stepAfter', 'catmullRom', 'bumpX', 'bumpY'
     */
    curve: PropTypes.oneOf([
        'linear', 'monotoneX', 'monotoneY', 'natural',
        'step', 'stepBefore', 'stepAfter', 'catmullRom',
        'bumpX', 'bumpY'
    ]),

    /**
     * If true, shows a tooltip on hover displaying the value.
     */
    showTooltip: PropTypes.bool,

    /**
     * If true, shows a visual highlight on the hovered data point.
     * For line charts, shows a dot. For bar charts, shows a band.
     */
    showHighlight: PropTypes.bool,

    /**
     * Chart margins in pixels. Object with top, right, bottom, left keys.
     * Default is { top: 5, right: 5, bottom: 5, left: 5 }.
     */
    margin: PropTypes.shape({
        top: PropTypes.number,
        right: PropTypes.number,
        bottom: PropTypes.number,
        left: PropTypes.number,
    }),

    /**
     * X-axis configuration object. Unlike LineChart, this is a single object,
     * not an array. The axis is hidden by default for compact display.
     * - id (string): Axis identifier for controlled highlighting
     * - data (array): X-axis labels/values
     * - scaleType (string): Scale type
     */
    xAxis: PropTypes.shape({
        id: PropTypes.string,
        data: PropTypes.array,
        scaleType: PropTypes.oneOf(['band', 'point', 'linear', 'log', 'time']),
    }),

    /**
     * Y-axis configuration object. Unlike LineChart, this is a single object,
     * not an array. The axis is hidden by default for compact display.
     */
    yAxis: PropTypes.shape({
        min: PropTypes.number,
        max: PropTypes.number,
    }),

    /**
     * Axis highlight configuration. Controls how the axis is highlighted on hover.
     * - x: 'line' | 'band' | 'none' - highlight style for x-axis
     * - y: 'line' | 'band' | 'none' - highlight style for y-axis
     */
    axisHighlight: PropTypes.shape({
        x: PropTypes.oneOf(['line', 'band', 'none']),
        y: PropTypes.oneOf(['line', 'band', 'none']),
    }),

    /**
     * Props passed to internal slot components for customization.
     * - lineHighlight: { r: number } - radius of the highlight dot
     * - tooltip: tooltip configuration
     */
    slotProps: PropTypes.object,

    /**
     * Offset for the clip area to prevent cutting off elements at edges.
     * Object with top, right, bottom, left keys (in pixels).
     */
    clipAreaOffset: PropTypes.shape({
        top: PropTypes.number,
        right: PropTypes.number,
        bottom: PropTypes.number,
        left: PropTypes.number,
    }),

    /**
     * Baseline for area charts. Determines where the area fill starts.
     * - 'min': fills from minimum value (default)
     * - 'max': fills from maximum value
     * - number: fills from a specific value
     */
    baseline: PropTypes.oneOfType([
        PropTypes.oneOf(['min', 'max']),
        PropTypes.number,
    ]),

    /**
     * Stroke width for the line in pixels. Only applies when plotType is 'line'.
     * Default is 2. Higher values create thicker lines.
     */
    strokeWidth: PropTypes.number,

    /**
     * If true, disables clipping of the chart content.
     * Useful when elements extend beyond the chart boundaries.
     */
    disableClipping: PropTypes.bool,

    /**
     * Controlled highlight index. Set this to programmatically highlight
     * a specific data point. Requires xAxis.id to be set.
     */
    highlightedIndex: PropTypes.number,

    /**
     * Currently highlighted item. Read-only output property updated when
     * the user hovers over a data point (requires showHighlight=true).
     * Contains the data index of the highlighted point.
     */
    highlightedItem: PropTypes.object,

    /**
     * Index of the currently hovered data point. Read-only output.
     * Use this to sync hover state with other components.
     */
    hoverIndex: PropTypes.number,

    /**
     * Value at the currently hovered data point. Read-only output.
     * Use this to display the hovered value in other components.
     */
    hoverValue: PropTypes.number,

    /**
     * Number of hover events. Increments each time a data point is hovered.
     */
    n_hovers: PropTypes.number,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func,
};
