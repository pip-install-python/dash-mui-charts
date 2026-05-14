/**
 * BarChart — Dash wrapper for MUI X BarChart (Free + Pro)
 *
 * Follows the exact same pattern as the existing LineChart component.
 * This is a STUB — Claude Code should implement the full component.
 */
import React, {useCallback, useMemo, useEffect} from 'react';
import PropTypes from 'prop-types';

const BarChart = (props) => {
    const {
        id,
        series,
        dataset,
        xAxis,
        yAxis,
        // Layout & Appearance
        layout,
        borderRadius,
        height,
        width,
        margin,
        grid,
        colors,
        skipAnimation,
        loading,
        hideLegend,
        renderer,
        // Interaction
        axisHighlight,
        highlightedItem,
        // Pro
        licenseKey,
        initialZoom,
        showSlider,
        showToolbar,
        brushConfig,
        brushOverlay,
        // Reference lines (same pattern as LineChart)
        referenceLines,
        // Dash
        setProps,
    } = props;

    // --- License key activation ---
    useEffect(() => {
        if (licenseKey) {
            // TODO: Import LicenseInfo and set key
            // Same pattern as existing LineChart/Heatmap Pro components
            // import { LicenseInfo } from '@mui/x-license';
            // LicenseInfo.setLicenseKey(licenseKey);
        }
    }, [licenseKey]);

    // --- Determine which MUI component to use ---
    // If Pro features are requested, use BarChartPro; otherwise use BarChart
    const usePro = Boolean(
        licenseKey && (initialZoom || showSlider || showToolbar || brushConfig ||
        (xAxis && xAxis.some(a => a.zoom)))
    );

    // --- Callbacks ---
    const handleItemClick = useCallback(
        (event, barItemIdentifier) => {
            if (setProps) {
                setProps({
                    clickData: {
                        seriesId: barItemIdentifier.seriesId,
                        dataIndex: barItemIdentifier.dataIndex,
                        event_timestamp: Date.now(),
                    },
                });
            }
        },
        [setProps]
    );

    const handleAxisClick = useCallback(
        (event, data) => {
            if (setProps && data) {
                setProps({
                    axisClickData: {
                        axisValue: data.axisValue,
                        event_timestamp: Date.now(),
                    },
                });
            }
        },
        [setProps]
    );

    const handleHighlightChange = useCallback(
        (highlightedItem) => {
            if (setProps) {
                setProps({highlightedItem});
            }
        },
        [setProps]
    );

    // --- Build MUI props ---
    const muiProps = {
        series: series || [],
        dataset,
        xAxis,
        yAxis,
        layout,
        borderRadius,
        height: height || 300,
        width,
        margin,
        grid,
        colors,
        skipAnimation,
        loading,
        hideLegend,
        renderer,
        axisHighlight,
        highlightedItem,
        onItemClick: handleItemClick,
        onAxisClick: handleAxisClick,
        onHighlightChange: handleHighlightChange,
        // Pro features
        ...(showToolbar && {showToolbar}),
        ...(initialZoom && {initialZoom}),
        ...(brushConfig && {brushConfig}),
    };

    // TODO: Dynamically import BarChart vs BarChartPro based on `usePro`
    // For now, import both and conditionally render:
    //
    // if (usePro) {
    //     const { BarChartPro } = require('@mui/x-charts-pro/BarChartPro');
    //     return <div id={id}><BarChartPro {...muiProps} /></div>;
    // }
    // const { BarChart: MuiBarChart } = require('@mui/x-charts/BarChart');
    // return <div id={id}><MuiBarChart {...muiProps} /></div>;

    // Placeholder — Claude Code replaces with actual implementation
    return <div id={id}>BarChart placeholder</div>;
};

BarChart.defaultProps = {
    series: [],
    layout: 'vertical',
    height: 300,
    loading: false,
    licenseKey: '',
};

BarChart.propTypes = {
    /** Dash component id */
    id: PropTypes.string,

    /** Array of bar series objects. Each: {data, dataKey, label, color, stack, barLabel, barLabelPlacement, highlightScope, yAxisId} */
    series: PropTypes.arrayOf(PropTypes.object),

    /** Array of row objects for dataKey-based series. */
    dataset: PropTypes.arrayOf(PropTypes.object),

    /** X-axis config. For bars: [{data, scaleType: 'band', label, categoryGapRatio, barGapRatio, tickPlacement, tickLabelPlacement, colorMap, zoom}] */
    xAxis: PropTypes.arrayOf(PropTypes.object),

    /** Y-axis config. [{label, min, max, position, id, colorMap}] */
    yAxis: PropTypes.arrayOf(PropTypes.object),

    /** Bar direction: "vertical" or "horizontal". */
    layout: PropTypes.oneOf(['vertical', 'horizontal']),

    /** Border radius for bar corners. */
    borderRadius: PropTypes.number,

    /** Chart height in pixels. */
    height: PropTypes.number,

    /** Chart width in pixels. If not set, uses parent width. */
    width: PropTypes.number,

    /** Chart margins {top, bottom, left, right}. */
    margin: PropTypes.oneOfType([PropTypes.number, PropTypes.object]),

    /** Grid lines: {horizontal: bool, vertical: bool}. */
    grid: PropTypes.object,

    /** Color palette array. */
    colors: PropTypes.arrayOf(PropTypes.string),

    /** Disable animations. */
    skipAnimation: PropTypes.bool,

    /** Show loading overlay. */
    loading: PropTypes.bool,

    /** Hide legend. */
    hideLegend: PropTypes.bool,

    /** Renderer strategy: "svg-single" (default) or "svg-batch" for large datasets. */
    renderer: PropTypes.oneOf(['svg-single', 'svg-batch']),

    /** Axis highlight config: {x: 'band'/'line'/'none', y: 'band'/'line'/'none'}. */
    axisHighlight: PropTypes.object,

    /** Controlled highlight state {seriesId, dataIndex}. Also an output prop. */
    highlightedItem: PropTypes.object,

    /** Reference lines. [{x, y, label, lineStyle, labelStyle, labelAlign}] */
    referenceLines: PropTypes.arrayOf(PropTypes.object),

    // --- Pro ---
    /** MUI Pro license key for zoom, brush, toolbar. */
    licenseKey: PropTypes.string,

    /** Initial zoom state (Pro). [{axisId, start, end}] */
    initialZoom: PropTypes.arrayOf(PropTypes.object),

    /** Show zoom range slider (Pro). */
    showSlider: PropTypes.bool,

    /** Show zoom/export toolbar (Pro). */
    showToolbar: PropTypes.bool,

    /** Brush config (Pro). {enabled: bool, preventTooltip: bool} */
    brushConfig: PropTypes.object,

    /** Brush overlay display mode. */
    brushOverlay: PropTypes.string,

    // --- Output Props ---
    /** Fired on bar click. {seriesId, dataIndex, event_timestamp} */
    clickData: PropTypes.object,

    /** Fired on axis click. {axisValue, event_timestamp} */
    axisClickData: PropTypes.object,

    /** Dash setProps callback */
    setProps: PropTypes.func,
};

export default BarChart;
