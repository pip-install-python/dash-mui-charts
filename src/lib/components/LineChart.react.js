import React, { useId, useMemo, useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { LicenseInfo } from '@mui/x-license';
import { ChartDataProviderPro } from '@mui/x-charts-pro/ChartDataProviderPro';
import { ChartsSurface } from '@mui/x-charts-pro/ChartsSurface';
import { LinePlot, AreaPlot, MarkPlot } from '@mui/x-charts-pro/LineChart';
import { ChartsXAxis } from '@mui/x-charts-pro/ChartsXAxis';
import { ChartsYAxis } from '@mui/x-charts-pro/ChartsYAxis';
import { ChartsGrid } from '@mui/x-charts-pro/ChartsGrid';
import { ChartsTooltip } from '@mui/x-charts-pro/ChartsTooltip';
import { ChartsAxisHighlight } from '@mui/x-charts-pro/ChartsAxisHighlight';
import { ChartsLegend } from '@mui/x-charts-pro/ChartsLegend';
import { ChartsClipPath } from '@mui/x-charts-pro/ChartsClipPath';
import { ChartZoomSlider } from '@mui/x-charts-pro/ChartZoomSlider';

// Track if license key has been set globally
let licenseKeySet = false;

/**
 * LineChart component wrapping MUI X Charts Pro with composition API.
 * Renders interactive line charts with support for multiple series,
 * customizable axes, tooltips, click event callbacks, and Pro features
 * like zoom, pan, and zoom slider.
 */
export default function LineChart(props) {
    const {
        id,
        licenseKey,
        series = [],
        xAxis,
        yAxis,
        height = 400,
        width,
        margin,
        grid,
        colors,
        hideLegend = false,
        tooltip,
        skipAnimation = false,
        loading = false,
        // Pro zoom features
        zoom,
        initialZoom,
        showSlider = false,
        // Dash-specific output props (not passed to MUI)
        zoomData,
        clickData,
        n_clicks = 0,
        setProps,
    } = props;

    // Generate unique clip path ID
    const clipPathId = useId();

    // Set license key once globally (before any render)
    if (licenseKey && !licenseKeySet) {
        LicenseInfo.setLicenseKey(licenseKey);
        licenseKeySet = true;
    }

    // Internal state for controlled zoom - syncs with external zoom prop
    // Initialize from zoom or initialZoom, prioritizing zoom for controlled mode
    const [controlledZoom, setControlledZoom] = useState(() => {
        if (zoom && Array.isArray(zoom) && zoom.length > 0) {
            return zoom;
        }
        if (initialZoom && Array.isArray(initialZoom) && initialZoom.length > 0) {
            return initialZoom;
        }
        return [];
    });

    // Use ref to track the last zoom value we know about (either from props or from user interaction)
    // Refs update synchronously, avoiding race conditions with Dash callback echoes
    const lastKnownZoomRef = useRef(JSON.stringify(zoom || initialZoom || []));

    // Key counter to force ChartDataProviderPro re-mount on external zoom changes
    // This is necessary because MUI's chart doesn't always respond to zoom prop changes
    const [chartKey, setChartKey] = useState(0);

    // Sync external zoom prop changes to internal state (for programmatic control from Dash)
    useEffect(() => {
        const currentZoomStr = JSON.stringify(zoom);
        // Only update if the zoom prop is genuinely different from what we last knew
        // This prevents remounting when Dash echoes back the same value from user interaction
        if (zoom && Array.isArray(zoom) && currentZoomStr !== lastKnownZoomRef.current) {
            lastKnownZoomRef.current = currentZoomStr;
            setControlledZoom(zoom);
            // Increment key to force chart re-mount with new zoom state
            setChartKey(k => k + 1);
        }
    }, [zoom]);

    // Handle zoom changes from chart interaction (Pro feature)
    // MUI can pass either an array or a functional update
    const handleZoomChange = (newZoomData) => {
        // Handle functional updates from MUI
        const resolvedZoomData = typeof newZoomData === 'function'
            ? newZoomData(controlledZoom)
            : newZoomData;

        // Update internal state
        setControlledZoom(resolvedZoomData);

        // CRITICAL: Update ref synchronously BEFORE calling setProps
        // This ensures that when Dash echoes back the value, we recognize it
        // as the same value and don't trigger an unwanted remount
        lastKnownZoomRef.current = JSON.stringify(resolvedZoomData);

        // Report to Dash
        if (setProps) {
            setProps({ zoomData: resolvedZoomData });
        }
    };

    // Handle axis click events
    const handleAxisClick = (event, params) => {
        if (setProps) {
            setProps({
                clickData: {
                    type: 'axis',
                    axisValue: params.axisValue,
                    dataIndex: params.dataIndex,
                    seriesValues: params.seriesValues,
                    timestamp: new Date().toISOString()
                },
                n_clicks: (n_clicks || 0) + 1
            });
        }
    };

    // Handle mark (data point) click events
    const handleMarkClick = (event, params) => {
        if (setProps) {
            setProps({
                clickData: {
                    type: 'mark',
                    seriesId: params.seriesId,
                    dataIndex: params.dataIndex,
                    timestamp: new Date().toISOString()
                },
                n_clicks: (n_clicks || 0) + 1
            });
        }
    };

    // Handle line click events
    const handleLineClick = (event, params) => {
        if (setProps) {
            setProps({
                clickData: {
                    type: 'line',
                    seriesId: params.seriesId,
                    timestamp: new Date().toISOString()
                },
                n_clicks: (n_clicks || 0) + 1
            });
        }
    };

    // Handle area click events
    const handleAreaClick = (event, params) => {
        if (setProps) {
            setProps({
                clickData: {
                    type: 'area',
                    seriesId: params.seriesId,
                    timestamp: new Date().toISOString()
                },
                n_clicks: (n_clicks || 0) + 1
            });
        }
    };

    // Check if any series has area enabled
    const hasAreaSeries = useMemo(() => {
        return series.some(s => s.area);
    }, [series]);

    // Check if any series has showMark enabled
    const hasMarks = useMemo(() => {
        return series.some(s => s.showMark !== false);
    }, [series]);

    // Build processed series with 'type': 'line'
    const processedSeries = useMemo(() => {
        return series.map(s => ({
            type: 'line',
            ...s,
        }));
    }, [series]);

    // Process xAxis to inject slider config when showSlider is true
    const processedXAxis = useMemo(() => {
        if (!xAxis) return undefined;
        if (!showSlider) return xAxis;

        // Inject slider: { enabled: true } into zoom config for each axis
        return xAxis.map(axis => {
            const existingZoom = axis.zoom || {};
            // If zoom is just a boolean true, convert to object
            const zoomConfig = existingZoom === true ? {} : (typeof existingZoom === 'object' ? existingZoom : {});
            return {
                ...axis,
                zoom: {
                    ...zoomConfig,
                    slider: { enabled: true },
                },
            };
        });
    }, [xAxis, showSlider]);

    // Build the props for ChartDataProviderPro
    const providerProps = {
        height,
        series: processedSeries,
        onZoomChange: handleZoomChange,
    };

    // Add optional props only if defined
    if (processedXAxis) providerProps.xAxis = processedXAxis;
    if (yAxis) providerProps.yAxis = yAxis;
    if (width) providerProps.width = width;
    if (margin) providerProps.margin = margin;
    if (colors) providerProps.colors = colors;
    if (skipAnimation) providerProps.skipAnimation = skipAnimation;

    // Zoom props - use initialZoom for mounting since we force remount on external changes
    // This ensures MUI properly initializes with the desired zoom state
    if (controlledZoom && controlledZoom.length > 0) {
        providerProps.initialZoom = controlledZoom;
    }

    // Extract Y-axis IDs for rendering multiple axes
    const yAxisIds = useMemo(() => {
        if (!yAxis) return [undefined];
        return yAxis.map(axis => axis.id).filter(Boolean);
    }, [yAxis]);

    return (
        <div id={id}>
            <ChartDataProviderPro key={chartKey} {...providerProps}>
                {/* Legend - positioned above chart */}
                {!hideLegend && (
                    <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 8 }}>
                        <ChartsLegend />
                    </div>
                )}

                <ChartsSurface>
                    <ChartsClipPath id={clipPathId} />

                    {/* Grid */}
                    {grid && (
                        <ChartsGrid
                            horizontal={grid.horizontal}
                            vertical={grid.vertical}
                        />
                    )}

                    {/* Clipped plot area */}
                    <g clipPath={`url(#${clipPathId})`}>
                        {/* Area plots (rendered first, below lines) */}
                        {hasAreaSeries && (
                            <AreaPlot
                                onItemClick={handleAreaClick}
                                skipAnimation={skipAnimation}
                            />
                        )}

                        {/* Line plots */}
                        <LinePlot
                            onItemClick={handleLineClick}
                            skipAnimation={skipAnimation}
                        />

                        {/* Mark plots (data points) */}
                        {hasMarks && (
                            <MarkPlot
                                onItemClick={handleMarkClick}
                                skipAnimation={skipAnimation}
                            />
                        )}
                    </g>

                    {/* Axes */}
                    <ChartsXAxis />
                    {yAxisIds.length > 0 ? (
                        yAxisIds.map(axisId => (
                            <ChartsYAxis key={axisId || 'default'} axisId={axisId} />
                        ))
                    ) : (
                        <ChartsYAxis />
                    )}

                    {/* Axis highlight for tooltips */}
                    <ChartsAxisHighlight x="line" />

                    {/* Zoom slider */}
                    {showSlider && <ChartZoomSlider />}
                </ChartsSurface>

                {/* Tooltip */}
                {tooltip?.trigger !== 'none' && (
                    <ChartsTooltip trigger={tooltip?.trigger || 'axis'} />
                )}
            </ChartDataProviderPro>

            {/* Loading overlay */}
            {loading && (
                <div style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    backgroundColor: 'rgba(255, 255, 255, 0.7)',
                }}>
                    Loading...
                </div>
            )}
        </div>
    );
}

LineChart.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * MUI X Pro license key. Required to enable Pro features like zoom/pan
     * without watermarks. Get your license key from https://mui.com/x/introduction/licensing/
     */
    licenseKey: PropTypes.string,

    /**
     * Array of series configurations. Each series represents a line in the chart.
     * Each series object can have:
     * - id (string): Unique identifier for the series
     * - data (array of numbers): Y-axis values, supports null for gaps
     * - label (string): Label shown in legend and tooltip
     * - color (string): Custom color for this series
     * - area (boolean): Fill area under the line
     * - stack (string): Stack identifier for stacked area charts
     * - curve (string): Interpolation method - 'linear', 'monotoneX', 'monotoneY',
     *   'natural', 'step', 'stepBefore', 'stepAfter', 'catmullRom', 'bumpX', 'bumpY'
     * - showMark (boolean): Whether to show data point markers
     * - connectNulls (boolean): Whether to bridge gaps across null values
     * - yAxisId (string): ID of the y-axis to use for this series (for biaxial charts)
     * - xAxisId (string): ID of the x-axis to use for this series
     */
    series: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.string,
        data: PropTypes.arrayOf(PropTypes.number),
        label: PropTypes.string,
        color: PropTypes.string,
        area: PropTypes.bool,
        stack: PropTypes.string,
        curve: PropTypes.oneOf([
            'linear', 'monotoneX', 'monotoneY', 'natural',
            'step', 'stepBefore', 'stepAfter', 'catmullRom',
            'bumpX', 'bumpY'
        ]),
        showMark: PropTypes.bool,
        connectNulls: PropTypes.bool,
        yAxisId: PropTypes.string,
        xAxisId: PropTypes.string,
    })),

    /**
     * X-axis configuration. Array of axis config objects.
     * Each axis object can have:
     * - data (array): X-axis values
     * - label (string): Axis label
     * - scaleType (string): 'band', 'point', 'linear', 'log', 'time'
     * - position (string): 'top' or 'bottom'
     * - id (string): Axis identifier for referencing in series and zoom
     * - zoom (boolean or object): Enable zoom on this axis. Can be true or object with:
     *   - minStart (number): Minimum start position (0-100)
     *   - maxEnd (number): Maximum end position (0-100)
     *   - minSpan (number): Minimum zoom span
     *   - maxSpan (number): Maximum zoom span
     *   - step (number): Zoom step size
     *   - panning (boolean): Enable panning
     *   - filterMode (string): 'keep' or 'discard'
     *   - slider (object): Slider config with { enabled: true }
     */
    xAxis: PropTypes.arrayOf(PropTypes.shape({
        data: PropTypes.array,
        label: PropTypes.string,
        scaleType: PropTypes.oneOf(['band', 'point', 'linear', 'log', 'time']),
        position: PropTypes.oneOf(['top', 'bottom']),
        id: PropTypes.string,
        zoom: PropTypes.oneOfType([
            PropTypes.bool,
            PropTypes.object,
        ]),
    })),

    /**
     * Y-axis configuration. Array of axis config objects.
     * Each axis object can have:
     * - label (string): Axis label
     * - min (number): Minimum domain value
     * - max (number): Maximum domain value
     * - width (number): Width allocated for axis
     * - position (string): 'left' or 'right'
     * - id (string): Axis identifier for referencing in series
     * - zoom (boolean or object): Enable zoom on this axis (same options as xAxis)
     */
    yAxis: PropTypes.arrayOf(PropTypes.shape({
        label: PropTypes.string,
        min: PropTypes.number,
        max: PropTypes.number,
        width: PropTypes.number,
        position: PropTypes.oneOf(['left', 'right']),
        id: PropTypes.string,
        zoom: PropTypes.oneOfType([
            PropTypes.bool,
            PropTypes.object,
        ]),
    })),

    /**
     * Chart height in pixels. Default is 400.
     */
    height: PropTypes.number,

    /**
     * Chart width in pixels. If not specified, the chart expands to fill
     * the available space.
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
     * Grid configuration. Object with vertical and horizontal boolean keys.
     */
    grid: PropTypes.shape({
        vertical: PropTypes.bool,
        horizontal: PropTypes.bool,
    }),

    /**
     * Array of colors for the series palette.
     */
    colors: PropTypes.arrayOf(PropTypes.string),

    /**
     * If true, the legend is hidden.
     */
    hideLegend: PropTypes.bool,

    /**
     * Tooltip configuration. Object with trigger key.
     * - trigger (string): 'item', 'axis', or 'none'
     */
    tooltip: PropTypes.shape({
        trigger: PropTypes.oneOf(['item', 'axis', 'none']),
    }),

    /**
     * If true, animations are skipped.
     */
    skipAnimation: PropTypes.bool,

    /**
     * If true, a loading overlay is displayed.
     */
    loading: PropTypes.bool,

    /**
     * Controlled zoom state for the chart. Array of objects with:
     * - axisId (string): The axis identifier
     * - start (number): Start position (0-100)
     * - end (number): End position (0-100)
     */
    zoom: PropTypes.arrayOf(PropTypes.shape({
        axisId: PropTypes.string,
        start: PropTypes.number,
        end: PropTypes.number,
    })),

    /**
     * Initial zoom state for uncontrolled mode. Array of objects with:
     * - axisId (string): The axis identifier
     * - start (number): Start position (0-100)
     * - end (number): End position (0-100)
     */
    initialZoom: PropTypes.arrayOf(PropTypes.shape({
        axisId: PropTypes.string,
        start: PropTypes.number,
        end: PropTypes.number,
    })),

    /**
     * If true, shows a zoom slider below the chart for easy zoom control.
     * The slider allows users to select a range and pan through the data.
     */
    showSlider: PropTypes.bool,

    /**
     * Current zoom state. Read-only output property updated when zoom changes.
     * Array of objects with axisId, start, and end values.
     */
    zoomData: PropTypes.oneOfType([
        PropTypes.arrayOf(PropTypes.shape({
            axisId: PropTypes.string,
            start: PropTypes.number,
            end: PropTypes.number,
        })),
        PropTypes.any, // Accept any type to handle Dash's callback binding
    ]),

    /**
     * Data from the most recent click event. Read-only output property.
     * Contains type ('axis', 'mark', 'line', 'area'), relevant IDs/values,
     * and timestamp.
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
