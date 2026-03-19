import React from 'react';
import PropTypes from 'prop-types';
import { PieChart as MuiPieChart } from '@mui/x-charts/PieChart';

/**
 * PieChart component wrapping MUI X Charts PieChart.
 * Renders pie and donut charts with customizable arcs, labels, and interactions.
 * Supports single series (via data prop) or multiple series (via series prop) for nested pies.
 * This is a free feature - no MUI X Pro license required.
 */
export default function PieChart(props) {
    const {
        id,
        data = [],
        series: seriesProp,
        width,
        height = 300,
        // Arc geometry (used when data prop is provided, ignored when series prop is used)
        innerRadius,
        outerRadius,
        paddingAngle = 0,
        cornerRadius = 0,
        startAngle = 0,
        endAngle = 360,
        cx,
        cy,
        // Labels
        arcLabel,
        arcLabelMinAngle,
        // Styling
        colors,
        hideLegend = false,
        margin,
        // Behavior
        highlightScope,
        tooltip,
        skipAnimation = false,
        // Dash-specific output props
        clickData,
        n_clicks = 0,
        highlightedItem,
        setProps,
    } = props;

    // Handle item click
    const handleItemClick = (event, params) => {
        if (setProps) {
            // MUI X Charts returns { seriesId, dataIndex } - find series by ID
            let clickedItem;
            let seriesIndex = 0;

            if (seriesProp && seriesProp.length > 0) {
                // Find series index by matching seriesId
                seriesIndex = seriesProp.findIndex(
                    (s, idx) => (s.id || `series-${idx}`) === params.seriesId
                );
                if (seriesIndex === -1) seriesIndex = 0;
                const seriesData = seriesProp[seriesIndex]?.data || [];
                clickedItem = seriesData[params.dataIndex];
            } else {
                clickedItem = data[params.dataIndex];
            }
            setProps({
                clickData: {
                    id: clickedItem?.id,
                    seriesId: params.seriesId,
                    seriesIndex: seriesIndex,
                    dataIndex: params.dataIndex,
                    value: clickedItem?.value,
                    label: clickedItem?.label,
                    timestamp: new Date().toISOString(),
                },
                n_clicks: (n_clicks || 0) + 1,
            });
        }
    };

    // Handle highlight change
    const handleHighlightChange = (item) => {
        if (setProps) {
            setProps({ highlightedItem: item });
        }
    };

    // Build series configuration
    let chartSeries;

    if (seriesProp && seriesProp.length > 0) {
        // Use the series prop directly for multi-series/nested pies
        chartSeries = seriesProp.map((s, index) => ({
            ...s,
            id: s.id || `series-${index}`,
        }));
    } else {
        // Build single series from individual props (backward compatibility)
        const seriesConfig = { data };

        if (innerRadius !== undefined) seriesConfig.innerRadius = innerRadius;
        if (outerRadius !== undefined) seriesConfig.outerRadius = outerRadius;
        if (paddingAngle) seriesConfig.paddingAngle = paddingAngle;
        if (cornerRadius) seriesConfig.cornerRadius = cornerRadius;
        if (startAngle !== 0) seriesConfig.startAngle = startAngle;
        if (endAngle !== 360) seriesConfig.endAngle = endAngle;
        if (cx !== undefined) seriesConfig.cx = cx;
        if (cy !== undefined) seriesConfig.cy = cy;
        if (arcLabel) seriesConfig.arcLabel = arcLabel;
        if (arcLabelMinAngle) seriesConfig.arcLabelMinAngle = arcLabelMinAngle;
        if (highlightScope) seriesConfig.highlightScope = highlightScope;

        chartSeries = [seriesConfig];
    }

    // Build chart props
    const chartProps = {
        series: chartSeries,
        height,
        skipAnimation,
        onItemClick: handleItemClick,
        onHighlightChange: handleHighlightChange,
    };

    // Add optional chart-level props
    if (width) chartProps.width = width;
    if (colors) chartProps.colors = colors;
    if (hideLegend) chartProps.hideLegend = hideLegend;
    if (margin) chartProps.margin = margin;
    if (tooltip) {
        chartProps.slotProps = {
            ...chartProps.slotProps,
            tooltip: { trigger: tooltip.trigger || 'item' },
        };
    }

    // Controlled highlight input - allows external control of highlighted item
    if (highlightedItem !== undefined) {
        chartProps.highlightedItem = highlightedItem;
    }

    return (
        <div id={id}>
            <MuiPieChart {...chartProps} />
        </div>
    );
}

PieChart.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * Pie chart data as an array of objects (for single series).
     * Each object should have:
     * - id (number/string): Unique identifier for the slice
     * - value (number): The numeric value (required)
     * - label (string): Display label for the slice
     * - color (string): Optional color override for this slice
     *
     * Example: [
     *   { id: 0, value: 35, label: 'Marketing' },
     *   { id: 1, value: 25, label: 'Engineering', color: '#1976d2' },
     * ]
     *
     * Note: Use either 'data' for single series or 'series' for multiple series (nested pies).
     */
    data: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
            value: PropTypes.number.isRequired,
            label: PropTypes.string,
            color: PropTypes.string,
        })
    ),

    /**
     * Array of series configurations for multi-series/nested pie charts.
     * Each series can have its own data, geometry, and styling.
     * When provided, the 'data' prop and individual geometry props are ignored.
     *
     * Example for nested pie:
     * [
     *   {
     *     data: innerRingData,
     *     innerRadius: 0,
     *     outerRadius: 80,
     *     cornerRadius: 3,
     *     highlightScope: { fade: 'global', highlight: 'item' },
     *   },
     *   {
     *     data: outerRingData,
     *     innerRadius: 90,
     *     outerRadius: 120,
     *     cornerRadius: 3,
     *     highlightScope: { fade: 'global', highlight: 'item' },
     *   },
     * ]
     */
    series: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.string,
            data: PropTypes.arrayOf(
                PropTypes.shape({
                    id: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
                    value: PropTypes.number.isRequired,
                    label: PropTypes.string,
                    color: PropTypes.string,
                })
            ).isRequired,
            innerRadius: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
            outerRadius: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
            paddingAngle: PropTypes.number,
            cornerRadius: PropTypes.number,
            startAngle: PropTypes.number,
            endAngle: PropTypes.number,
            arcLabel: PropTypes.oneOf(['value', 'label', 'formattedValue']),
            arcLabelMinAngle: PropTypes.number,
            arcLabelRadius: PropTypes.number,
            highlightScope: PropTypes.shape({
                highlight: PropTypes.oneOf(['item', 'none']),
                fade: PropTypes.oneOf(['global', 'none']),
            }),
        })
    ),

    /**
     * Chart width in pixels. If not specified, the chart expands to fill
     * the available space.
     */
    width: PropTypes.number,

    /**
     * Chart height in pixels. Default is 300.
     */
    height: PropTypes.number,

    /**
     * Inner radius of the pie in pixels or percentage string.
     * Set to a value > 0 to create a donut chart.
     * Examples: 50, '50%', '40%'
     */
    innerRadius: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),

    /**
     * Outer radius of the pie in pixels or percentage string.
     * Examples: 100, '80%'
     */
    outerRadius: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),

    /**
     * Gap between arcs in degrees. Creates visual separation between slices.
     */
    paddingAngle: PropTypes.number,

    /**
     * Corner radius of the arcs in pixels. Rounds the corners of each slice.
     */
    cornerRadius: PropTypes.number,

    /**
     * Start angle of the first arc in degrees. Default is 0 (3 o'clock position).
     * Use -90 for 12 o'clock start position.
     */
    startAngle: PropTypes.number,

    /**
     * End angle of the last arc in degrees. Default is 360 (full circle).
     * Use 90 with startAngle=-90 for a half-pie/gauge chart.
     */
    endAngle: PropTypes.number,

    /**
     * X position of the pie center. Can be pixels or percentage string.
     * Default is '50%' (centered).
     */
    cx: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),

    /**
     * Y position of the pie center. Can be pixels or percentage string.
     * Default is '50%' (centered).
     */
    cy: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),

    /**
     * Type of label to display on arcs.
     * - 'value': Shows the numeric value
     * - 'label': Shows the label text
     * - 'formattedValue': Shows formatted value
     */
    arcLabel: PropTypes.oneOf(['value', 'label', 'formattedValue']),

    /**
     * Minimum arc angle in degrees required to display a label.
     * Prevents labels from appearing on very small slices.
     */
    arcLabelMinAngle: PropTypes.number,

    /**
     * Array of colors to use for the pie slices.
     * If not provided, uses the default MUI color palette.
     * Example: ['#1976d2', '#dc004e', '#ff9800', '#4caf50']
     */
    colors: PropTypes.arrayOf(PropTypes.string),

    /**
     * If true, the legend is hidden.
     */
    hideLegend: PropTypes.bool,

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
     * Highlight scope configuration for slice highlighting behavior.
     * - highlight: 'item' or 'none'
     * - fade: 'global' or 'none'
     *
     * Example: { highlight: 'item', fade: 'global' }
     */
    highlightScope: PropTypes.shape({
        highlight: PropTypes.oneOf(['item', 'none']),
        fade: PropTypes.oneOf(['global', 'none']),
    }),

    /**
     * Tooltip configuration.
     * - trigger (string): 'item' to show on slice hover, 'none' to disable
     */
    tooltip: PropTypes.shape({
        trigger: PropTypes.oneOf(['item', 'none']),
    }),

    /**
     * If true, disables chart animations. Also respects prefers-reduced-motion.
     */
    skipAnimation: PropTypes.bool,

    /**
     * Data from the most recent click event. Read-only output property.
     * Contains id, dataIndex, value, label, and timestamp.
     */
    clickData: PropTypes.object,

    /**
     * Number of times the chart has been clicked. Increments on each click event.
     */
    n_clicks: PropTypes.number,

    /**
     * Currently highlighted item. Can be used as both input (controlled mode) and
     * output (updated when user hovers over a slice).
     * Object with:
     * - seriesId (string): The series identifier
     * - dataIndex (number): The data index within the series
     * Set to null to clear highlight.
     */
    highlightedItem: PropTypes.shape({
        seriesId: PropTypes.string,
        dataIndex: PropTypes.number,
    }),

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func,
};
