import React, { useMemo, useState, useEffect, useRef, useCallback } from 'react';
import PropTypes from 'prop-types';
import { LicenseInfo } from '@mui/x-license';
import { BarChart as MuiBarChart } from '@mui/x-charts/BarChart';
import { BarChartPro } from '@mui/x-charts-pro/BarChartPro';
import { ChartsReferenceLine } from '@mui/x-charts/ChartsReferenceLine';

// Track if license key has been set globally
let licenseKeySet = false;

/**
 * BarChart — Dash wrapper for MUI X BarChart (Community) and BarChartPro (Pro).
 *
 * Renders vertical or horizontal bar charts with support for stacking, bar labels,
 * dataset mode, color maps, reference lines, highlighting, and Pro features
 * (zoom, toolbar, brush).
 */
export default function BarChart(props) {
    const {
        id,
        series = [],
        dataset,
        xAxis,
        yAxis,
        // Layout & Appearance
        layout = 'vertical',
        borderRadius,
        height = 300,
        width,
        margin,
        grid,
        colors,
        skipAnimation = false,
        loading = false,
        hideLegend = false,
        renderer,
        // Interaction
        axisHighlight,
        tooltip,
        highlightedItem,
        // Reference lines
        referenceLines = [],
        // Pro features
        licenseKey,
        initialZoom,
        showSlider = false,
        showToolbar = false,
        brushConfig,
        zoomInteractionConfig,
        // Dash output props (not passed to MUI)
        clickData,
        axisClickData,
        zoomData,
        n_clicks = 0,
        setProps,
    } = props;

    // Set license key once globally
    if (licenseKey && !licenseKeySet) {
        LicenseInfo.setLicenseKey(licenseKey);
        licenseKeySet = true;
    }

    // Determine if Pro features are needed
    const usePro = Boolean(
        licenseKey && (
            initialZoom || showSlider || showToolbar || brushConfig ||
            zoomInteractionConfig ||
            (xAxis && xAxis.some(a => a.zoom)) ||
            (yAxis && yAxis.some(a => a.zoom))
        )
    );

    // --- Controlled Highlight State ---
    const lastKnownHighlightedItemRef = useRef(JSON.stringify(highlightedItem ?? null));
    const [controlledHighlightedItem, setControlledHighlightedItem] = useState(() =>
        highlightedItem ?? null
    );

    useEffect(() => {
        const currentStr = JSON.stringify(highlightedItem ?? null);
        if (currentStr !== lastKnownHighlightedItemRef.current) {
            lastKnownHighlightedItemRef.current = currentStr;
            setControlledHighlightedItem(highlightedItem ?? null);
        }
    }, [highlightedItem]);

    const handleHighlightChange = useCallback((newValue) => {
        const value = newValue ?? null;
        setControlledHighlightedItem(value);
        lastKnownHighlightedItemRef.current = JSON.stringify(value);
        if (setProps) {
            setProps({ highlightedItem: value });
        }
    }, [setProps]);

    // --- Controlled Zoom State (Pro) ---
    const lastKnownZoomRef = useRef(JSON.stringify(initialZoom || []));
    const [controlledZoom, setControlledZoom] = useState(() =>
        initialZoom && Array.isArray(initialZoom) ? initialZoom : []
    );

    const handleZoomChange = useCallback((newZoomData) => {
        const resolved = typeof newZoomData === 'function'
            ? newZoomData(controlledZoom)
            : newZoomData;
        setControlledZoom(resolved);
        lastKnownZoomRef.current = JSON.stringify(resolved);
        if (setProps) {
            setProps({ zoomData: resolved });
        }
    }, [setProps, controlledZoom]);

    // --- Click Handlers ---
    const handleItemClick = useCallback((event, barItemIdentifier) => {
        if (setProps) {
            setProps({
                clickData: {
                    seriesId: barItemIdentifier.seriesId,
                    dataIndex: barItemIdentifier.dataIndex,
                    timestamp: new Date().toISOString(),
                },
                n_clicks: (n_clicks || 0) + 1,
            });
        }
    }, [setProps, n_clicks]);

    const handleAxisClick = useCallback((event, data) => {
        if (setProps && data) {
            setProps({
                axisClickData: {
                    axisValue: data.axisValue,
                    dataIndex: data.dataIndex,
                    seriesValues: data.seriesValues,
                    timestamp: new Date().toISOString(),
                },
            });
        }
    }, [setProps]);

    // Process xAxis: inject zoom slider config when showSlider is true
    const processedXAxis = useMemo(() => {
        if (!xAxis) return undefined;
        return xAxis.map(axis => {
            let result = { ...axis };
            if (showSlider) {
                const existingZoom = result.zoom || {};
                const zoomConfig = existingZoom === true ? {} : (typeof existingZoom === 'object' ? existingZoom : {});
                result.zoom = {
                    ...zoomConfig,
                    slider: { ...zoomConfig.slider, enabled: true },
                };
            }
            return result;
        });
    }, [xAxis, showSlider]);

    // Build chart props
    const chartProps = {
        series: series || [],
        height,
        layout,
        skipAnimation,
        loading,
        hideLegend,
        onItemClick: handleItemClick,
        onAxisClick: handleAxisClick,
        onHighlightChange: handleHighlightChange,
        highlightedItem: controlledHighlightedItem,
    };

    // Optional props — only pass if defined
    if (processedXAxis) chartProps.xAxis = processedXAxis;
    else if (xAxis) chartProps.xAxis = xAxis;
    if (yAxis) chartProps.yAxis = yAxis;
    if (dataset) chartProps.dataset = dataset;
    if (width) chartProps.width = width;
    if (margin) chartProps.margin = margin;
    if (grid) chartProps.grid = grid;
    if (colors) chartProps.colors = colors;
    if (borderRadius !== undefined) chartProps.borderRadius = borderRadius;
    if (renderer) chartProps.renderer = renderer;
    if (axisHighlight) chartProps.axisHighlight = axisHighlight;

    // Tooltip
    if (tooltip) {
        chartProps.slotProps = {
            ...chartProps.slotProps,
            tooltip: { trigger: tooltip.trigger || 'axis' },
        };
    }

    // Pro features
    if (usePro) {
        if (controlledZoom && controlledZoom.length > 0) {
            chartProps.initialZoom = controlledZoom;
        }
        chartProps.onZoomChange = handleZoomChange;
        if (showToolbar) chartProps.showToolbar = true;
        if (brushConfig) chartProps.brushConfig = brushConfig;
        if (zoomInteractionConfig) chartProps.zoomInteractionConfig = zoomInteractionConfig;
    }

    // Reference line children
    const refLineChildren = referenceLines && referenceLines.length > 0
        ? referenceLines.map((refLine, idx) => (
            <ChartsReferenceLine
                key={`ref-line-${idx}`}
                x={refLine.x}
                y={refLine.y}
                axisId={refLine.axisId}
                label={refLine.label || undefined}
                labelAlign={refLine.labelAlign || 'middle'}
                lineStyle={refLine.lineStyle || undefined}
                labelStyle={refLine.labelStyle || undefined}
                spacing={refLine.spacing || undefined}
            />
        ))
        : null;

    const ChartComponent = usePro ? BarChartPro : MuiBarChart;

    return (
        <div id={id}>
            <ChartComponent {...chartProps}>
                {refLineChildren}
            </ChartComponent>
        </div>
    );
}

BarChart.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * Array of bar series objects. Each series can contain:
     * - data (number[]): Bar values
     * - dataKey (string): Column key when using dataset prop
     * - label (string): Series label for legend/tooltip
     * - color (string): Series color
     * - stack (string): Stack group ID (series with same value are stacked)
     * - stackOffset (string): 'none', 'expand', 'diverging', 'silhouette', 'wiggle'
     * - stackOrder (string): 'none', 'appearance', 'ascending', 'descending', 'insideOut', 'reverse'
     * - barLabel (string): 'value' or 'formattedValue' to show labels on bars
     * - barLabelPlacement (string): 'center' or 'outside'
     * - highlightScope (object): {highlight, fade} highlight behavior
     * - yAxisId (string): Y-axis binding for biaxial charts
     * - id (string): Unique series identifier
     */
    series: PropTypes.arrayOf(PropTypes.object),

    /**
     * Array of row objects for dataKey-based series.
     * Example: [{month: 'Jan', sales: 100}, {month: 'Feb', sales: 150}]
     */
    dataset: PropTypes.arrayOf(PropTypes.object),

    /**
     * X-axis configuration array. For bar charts, typically uses scaleType: 'band'.
     * Each axis can contain:
     * - data (array): Category labels
     * - dataKey (string): Column key from dataset
     * - scaleType (string): 'band' (required for bars), 'linear', 'log', etc.
     * - label (string): Axis label text
     * - categoryGapRatio (number): Gap between categories (0-1)
     * - barGapRatio (number): Gap between bars in same category (-1 to Infinity)
     * - tickPlacement (string): 'start', 'end', 'middle', 'extremities'
     * - tickLabelPlacement (string): 'tick' or 'middle'
     * - colorMap (object): Color mapping configuration
     * - zoom (object): Zoom config for Pro features
     * - id (string): Axis identifier
     * - position (string): 'top', 'bottom', 'none'
     * - min/max (number): Domain limits
     * - reverse (bool): Reverse axis direction
     * - tickNumber (number): Approximate tick count
     * - tickMinStep/tickMaxStep (number): Control tick spacing
     * - tickLabelStyle (object): CSS for tick labels
     * - labelStyle (object): CSS for axis label
     * - disableLine (bool): Hide axis line
     * - disableTicks (bool): Hide tick marks
     * - domainLimit (string): 'nice' or 'strict'
     * - height (number): Space reserved for axis
     */
    xAxis: PropTypes.arrayOf(PropTypes.object),

    /**
     * Y-axis configuration array. Same structure as xAxis.
     */
    yAxis: PropTypes.arrayOf(PropTypes.object),

    /**
     * Bar direction: 'vertical' (default) or 'horizontal'.
     */
    layout: PropTypes.oneOf(['vertical', 'horizontal']),

    /**
     * Border radius for bar corners in pixels.
     */
    borderRadius: PropTypes.number,

    /**
     * Chart height in pixels.
     */
    height: PropTypes.number,

    /**
     * Chart width in pixels. If not set, uses parent container width.
     */
    width: PropTypes.number,

    /**
     * Chart margins: {top, bottom, left, right} in pixels.
     */
    margin: PropTypes.exact({
        top: PropTypes.number,
        bottom: PropTypes.number,
        left: PropTypes.number,
        right: PropTypes.number,
    }),

    /**
     * Background grid lines: {horizontal: bool, vertical: bool}.
     */
    grid: PropTypes.exact({
        horizontal: PropTypes.bool,
        vertical: PropTypes.bool,
    }),

    /**
     * Color palette array for series colors.
     */
    colors: PropTypes.arrayOf(PropTypes.string),

    /**
     * Disable animations.
     */
    skipAnimation: PropTypes.bool,

    /**
     * Show loading overlay.
     */
    loading: PropTypes.bool,

    /**
     * Hide the legend.
     */
    hideLegend: PropTypes.bool,

    /**
     * Renderer strategy: 'svg-single' (default) or 'svg-batch' for large datasets.
     */
    renderer: PropTypes.oneOf(['svg-single', 'svg-batch']),

    /**
     * Axis highlight configuration: {x: 'band'|'line'|'none', y: 'band'|'line'|'none'}.
     */
    axisHighlight: PropTypes.exact({
        x: PropTypes.oneOf(['band', 'line', 'none']),
        y: PropTypes.oneOf(['band', 'line', 'none']),
    }),

    /**
     * Tooltip configuration: {trigger: 'item'|'axis'|'none'}.
     */
    tooltip: PropTypes.exact({
        trigger: PropTypes.oneOf(['item', 'axis', 'none']),
    }),

    /**
     * Controlled highlight state. Both input (to set highlight) and output
     * (fires on hover). Object: {seriesId, dataIndex} or null.
     */
    highlightedItem: PropTypes.object,

    /**
     * Reference lines array. Each object:
     * - x (string|number): Vertical line at this x value
     * - y (number): Horizontal line at this y value
     * - axisId (string): Which axis (when multiple)
     * - label (string): Text label
     * - labelAlign (string): 'start', 'middle', 'end'
     * - lineStyle (object): SVG style for the line
     * - labelStyle (object): SVG style for the label
     * - spacing (object): Label offset
     */
    referenceLines: PropTypes.arrayOf(PropTypes.object),

    // --- Pro Features ---

    /**
     * MUI X Pro license key. Required for zoom, brush, and toolbar features.
     */
    licenseKey: PropTypes.string,

    /**
     * Initial zoom state (Pro). Array of {axisId, start, end}.
     */
    initialZoom: PropTypes.arrayOf(PropTypes.object),

    /**
     * Show zoom range slider below the chart (Pro).
     */
    showSlider: PropTypes.bool,

    /**
     * Show zoom/export toolbar above the chart (Pro).
     */
    showToolbar: PropTypes.bool,

    /**
     * Brush selection config (Pro): {enabled: bool, preventTooltip: bool, preventHighlight: bool}.
     */
    brushConfig: PropTypes.object,

    /**
     * Zoom interaction configuration (Pro). Controls drag, wheel, pinch, brush zoom behaviors.
     */
    zoomInteractionConfig: PropTypes.object,

    // --- Output Props ---

    /**
     * Fires on bar click. Contains: {seriesId, dataIndex, timestamp}.
     */
    clickData: PropTypes.object,

    /**
     * Fires on axis area click. Contains: {axisValue, dataIndex, seriesValues, timestamp}.
     */
    axisClickData: PropTypes.object,

    /**
     * Zoom state output (Pro). Fires on zoom change.
     */
    zoomData: PropTypes.arrayOf(PropTypes.object),

    /**
     * Number of times bars have been clicked.
     */
    n_clicks: PropTypes.number,

    /**
     * Dash callback function.
     */
    setProps: PropTypes.func,
};
