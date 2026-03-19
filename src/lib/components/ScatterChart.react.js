import React, { useMemo } from 'react';
import PropTypes from 'prop-types';
import { ScatterChart as MuiScatterChart } from '@mui/x-charts/ScatterChart';

/**
 * ScatterChart component wrapping MUI X Charts ScatterChart.
 * Renders scatter/point charts showing relationships between two variables.
 * Supports multiple series, z-axis color mapping, voronoi interaction,
 * custom marker sizes, and click/highlight callbacks.
 */
export default function ScatterChart(props) {
    const {
        id,
        series = [],
        xAxis,
        yAxis,
        zAxis,
        dataset,
        height = 400,
        width,
        margin,
        grid,
        colors,
        voronoiMaxRadius,
        disableVoronoi = false,
        axisHighlight,
        tooltip,
        hideLegend = false,
        skipAnimation = false,
        loading = false,
        renderer,
        slotProps,
        // Dash output props
        highlightedItem,
        clickData,
        n_clicks = 0,
        setProps,
    } = props;

    // Process series - ensure each has an id
    const processedSeries = useMemo(() => {
        if (!series || series.length === 0) return [];
        return series.map((s, index) => ({
            ...s,
            id: s.id || `series-${index}`,
        }));
    }, [series]);

    // Handle item click
    const handleItemClick = (event, params) => {
        if (setProps && params) {
            // Find the clicked data point
            const seriesConfig = processedSeries.find(s => s.id === params.seriesId);
            const dataPoint = seriesConfig?.data?.[params.dataIndex];

            setProps({
                clickData: {
                    seriesId: params.seriesId,
                    dataIndex: params.dataIndex,
                    x: dataPoint?.x,
                    y: dataPoint?.y,
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

    // Build chart props
    const chartProps = {
        series: processedSeries,
        height,
        onItemClick: handleItemClick,
        onHighlightChange: handleHighlightChange,
        disableVoronoi,
        skipAnimation,
        loading,
    };

    // Optional props
    if (xAxis) chartProps.xAxis = xAxis;
    if (yAxis) chartProps.yAxis = yAxis;
    if (zAxis) chartProps.zAxis = zAxis;
    if (dataset) chartProps.dataset = dataset;
    if (width) chartProps.width = width;
    if (margin) chartProps.margin = margin;
    if (grid) chartProps.grid = grid;
    if (colors) chartProps.colors = colors;
    if (voronoiMaxRadius !== undefined) chartProps.voronoiMaxRadius = voronoiMaxRadius;
    if (axisHighlight) chartProps.axisHighlight = axisHighlight;
    if (hideLegend) chartProps.hideLegend = hideLegend;
    if (renderer) chartProps.renderer = renderer;
    if (slotProps) chartProps.slotProps = slotProps;

    // Tooltip
    if (tooltip) {
        chartProps.slotProps = {
            ...chartProps.slotProps,
            tooltip: { trigger: tooltip.trigger || 'item' },
        };
    }

    // Controlled highlight
    if (highlightedItem !== undefined) {
        chartProps.highlightedItem = highlightedItem;
    }

    return (
        <div id={id}>
            <MuiScatterChart {...chartProps} />
        </div>
    );
}

ScatterChart.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * Array of scatter series to display. Each series contains:
     * - id (string): Unique series identifier
     * - label (string): Display label for legend/tooltip
     * - color (string): Series color
     * - data (array): Array of {x, y, id, z?} point objects
     * - datasetKeys (object): {x, y, id?, z?} keys mapping to dataset columns
     * - markerSize (number): Radius of scatter markers in pixels
     * - highlightScope (object): {highlight, fade} highlighting behavior
     */
    series: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.string,
        label: PropTypes.string,
        color: PropTypes.string,
        data: PropTypes.arrayOf(PropTypes.shape({
            x: PropTypes.number,
            y: PropTypes.number,
            id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
            z: PropTypes.number,
        })),
        datasetKeys: PropTypes.shape({
            x: PropTypes.string,
            y: PropTypes.string,
            id: PropTypes.string,
            z: PropTypes.string,
        }),
        markerSize: PropTypes.number,
        highlightScope: PropTypes.shape({
            highlight: PropTypes.oneOf(['item', 'series', 'none']),
            fade: PropTypes.oneOf(['global', 'series', 'none']),
        }),
        xAxisId: PropTypes.string,
        yAxisId: PropTypes.string,
    })),

    /**
     * X-axis configuration. Array of axis config objects.
     * - id (string): Axis identifier
     * - label (string): Axis label
     * - scaleType (string): 'linear', 'log', 'time', 'band', 'point', 'sqrt', 'symlog', 'utc'
     * - min/max (number): Domain bounds
     * - data (array): Axis data values
     * - dataKey (string): Key for dataset-driven axis
     * - position (string): 'top', 'bottom', 'none'
     * - reverse (bool): Reverse axis direction
     * - colorMap (object): Color mapping configuration
     * - tickLabelStyle (object): CSS for tick labels
     * - labelStyle (object): CSS for axis label
     * - tickMinStep (number): Minimum step between ticks
     * - tickMaxStep (number): Maximum step between ticks
     * - tickNumber (number): Approximate tick count
     * - tickSize (number): Tick mark length in pixels
     * - height (number): Space reserved for axis
     * - disableLine (bool): Hide axis line
     * - disableTicks (bool): Hide tick marks
     * - domainLimit (string): 'nice' or 'strict'
     */
    xAxis: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
        label: PropTypes.string,
        scaleType: PropTypes.oneOf(['linear', 'log', 'time', 'band', 'point', 'sqrt', 'symlog', 'utc', 'pow']),
        min: PropTypes.number,
        max: PropTypes.number,
        data: PropTypes.array,
        dataKey: PropTypes.string,
        position: PropTypes.oneOf(['top', 'bottom', 'none']),
        reverse: PropTypes.bool,
        colorMap: PropTypes.object,
        tickLabelStyle: PropTypes.object,
        labelStyle: PropTypes.object,
        tickMinStep: PropTypes.number,
        tickMaxStep: PropTypes.number,
        tickNumber: PropTypes.number,
        tickSize: PropTypes.number,
        tickSpacing: PropTypes.number,
        tickLabelMinGap: PropTypes.number,
        tickLabelPlacement: PropTypes.oneOf(['middle', 'tick']),
        tickPlacement: PropTypes.oneOf(['start', 'end', 'middle', 'extremities']),
        height: PropTypes.number,
        disableLine: PropTypes.bool,
        disableTicks: PropTypes.bool,
        domainLimit: PropTypes.oneOf(['nice', 'strict']),
        categoryGapRatio: PropTypes.number,
        barGapRatio: PropTypes.number,
        width: PropTypes.number,
    })),

    /**
     * Y-axis configuration. Array of axis config objects.
     * Same properties as xAxis, plus:
     * - width (number): Space reserved for axis
     * - position (string): 'left', 'right', 'none'
     */
    yAxis: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
        label: PropTypes.string,
        scaleType: PropTypes.oneOf(['linear', 'log', 'time', 'band', 'point', 'sqrt', 'symlog', 'utc', 'pow']),
        min: PropTypes.number,
        max: PropTypes.number,
        data: PropTypes.array,
        dataKey: PropTypes.string,
        position: PropTypes.oneOf(['left', 'right', 'none']),
        reverse: PropTypes.bool,
        colorMap: PropTypes.object,
        tickLabelStyle: PropTypes.object,
        labelStyle: PropTypes.object,
        tickMinStep: PropTypes.number,
        tickMaxStep: PropTypes.number,
        tickNumber: PropTypes.number,
        tickSize: PropTypes.number,
        tickSpacing: PropTypes.number,
        tickLabelMinGap: PropTypes.number,
        tickLabelPlacement: PropTypes.oneOf(['middle', 'tick']),
        tickPlacement: PropTypes.oneOf(['start', 'end', 'middle', 'extremities']),
        width: PropTypes.number,
        disableLine: PropTypes.bool,
        disableTicks: PropTypes.bool,
        domainLimit: PropTypes.oneOf(['nice', 'strict']),
    })),

    /**
     * Z-axis configuration for color mapping scatter points.
     * Color priority: z-axis > y-axis > x-axis > series color.
     * - data (array): Z-axis values
     * - dataKey (string): Key for dataset-driven z values
     * - id (string): Axis identifier
     * - min/max (number): Domain bounds
     * - colorMap (object): Color mapping - continuous, piecewise, or ordinal
     *   Continuous: {type: 'continuous', min, max, color: ['#start', '#end']}
     *   Piecewise: {type: 'piecewise', thresholds: [...], colors: [...]}
     *   Ordinal: {type: 'ordinal', values: [...], colors: [...]}
     */
    zAxis: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.string,
        data: PropTypes.array,
        dataKey: PropTypes.string,
        min: PropTypes.number,
        max: PropTypes.number,
        colorMap: PropTypes.object,
    })),

    /**
     * Dataset array for datasetKeys-driven series.
     * Array of objects where keys map to series datasetKeys.
     * Example: [{x1: 10, y1: 20, x2: 30, y2: 40}, ...]
     */
    dataset: PropTypes.arrayOf(PropTypes.object),

    /**
     * Chart height in pixels. Default is 400.
     */
    height: PropTypes.number,

    /**
     * Chart width in pixels. If not set, fills available space.
     */
    width: PropTypes.number,

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
     * Grid configuration. Object with horizontal and vertical boolean keys.
     */
    grid: PropTypes.shape({
        horizontal: PropTypes.bool,
        vertical: PropTypes.bool,
    }),

    /**
     * Color palette array for multiple series.
     */
    colors: PropTypes.arrayOf(PropTypes.string),

    /**
     * Maximum distance between pointer and scatter point for interaction.
     * - number: Distance in pixels
     * - 'item': Only trigger on direct hover over marker
     * - undefined: Infinite radius (default)
     */
    voronoiMaxRadius: PropTypes.oneOfType([
        PropTypes.number,
        PropTypes.oneOf(['item']),
    ]),

    /**
     * If true, disables Voronoi cell interaction and falls back to hover events.
     */
    disableVoronoi: PropTypes.bool,

    /**
     * Axis highlight configuration on hover.
     * - x: 'none', 'line', or 'band'
     * - y: 'none', 'line', or 'band'
     */
    axisHighlight: PropTypes.shape({
        x: PropTypes.oneOf(['none', 'line', 'band']),
        y: PropTypes.oneOf(['none', 'line', 'band']),
    }),

    /**
     * Tooltip configuration.
     * - trigger: 'item' (on point hover), 'axis' (all at x position), 'none' (disabled)
     */
    tooltip: PropTypes.shape({
        trigger: PropTypes.oneOf(['item', 'axis', 'none']),
    }),

    /**
     * If true, the legend is hidden.
     */
    hideLegend: PropTypes.bool,

    /**
     * If true, animations are disabled.
     */
    skipAnimation: PropTypes.bool,

    /**
     * If true, shows a loading overlay.
     */
    loading: PropTypes.bool,

    /**
     * Renderer type for performance optimization.
     * - 'svg-single': Default, renders each point as a <circle> element
     * - 'svg-batch': Batch renders points in <path> elements for large datasets
     *   Note: svg-batch has limitations (no CSS per-point, no custom markers)
     */
    renderer: PropTypes.oneOf(['svg-single', 'svg-batch']),

    /**
     * Props passed to internal slot components for customization.
     */
    slotProps: PropTypes.object,

    /**
     * Currently highlighted item. Works as both input (controlled) and output.
     * Object with seriesId and dataIndex.
     */
    highlightedItem: PropTypes.object,

    /**
     * Data from the most recent click event. Read-only output property.
     * Contains seriesId, dataIndex, x, y, and timestamp.
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