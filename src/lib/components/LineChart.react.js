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
import { ChartsReferenceLine } from '@mui/x-charts-pro/ChartsReferenceLine';
import { ChartsBrushOverlay } from '@mui/x-charts-pro/ChartsBrushOverlay';
import { ChartsToolbarPro } from '@mui/x-charts-pro/ChartsToolbarPro';
import {
    useBrush,
    useDrawingArea,
    useLineSeries,
    useXScale,
} from '@mui/x-charts/hooks';

// Track if license key has been set globally
let licenseKeySet = false;

/**
 * Resolve a function-as-prop value from a {function, options} descriptor.
 * Mirrors Dash Mantine Components' dashMantineFunctions pattern.
 * Users define functions in assets/*.js on window.dashMuiChartsFunctions.
 */
function resolveFunctionProp(value) {
    if (typeof value === 'function') return value;
    if (value && typeof value === 'object' && typeof value.function === 'string') {
        const registry = window.dashMuiChartsFunctions;
        if (registry && typeof registry[value.function] === 'function') {
            const fn = registry[value.function];
            const options = value.options || {};
            return (...args) => fn(...args, options);
        }
        console.warn(`dashMuiChartsFunctions.${value.function} not found. Define it in assets/*.js`);
    }
    return undefined;
}

/**
 * Built-in date formatter for time-scale axes.
 * Supports format tokens: YYYY, MMM, MM, M, dd, d, HH, mm
 * Optionally uses a shorter tickFormat for axis tick labels vs tooltips.
 */
const MONTHS_SHORT = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const pad2 = (n) => n < 10 ? '0' + n : '' + n;

function formatDateStr(date, pattern) {
    const d = date instanceof Date ? date : new Date(date);
    return pattern.replace(/YYYY|MMM|MM|dd|HH|mm|M|d/g, (token) => {
        switch (token) {
            case 'YYYY': return d.getFullYear();
            case 'MMM':  return MONTHS_SHORT[d.getMonth()];
            case 'MM':   return pad2(d.getMonth() + 1);
            case 'M':    return d.getMonth() + 1;
            case 'dd':   return pad2(d.getDate());
            case 'd':    return d.getDate();
            case 'HH':   return pad2(d.getHours());
            case 'mm':   return pad2(d.getMinutes());
            default:     return token;
        }
    });
}

function createDateFormatter(format, tickFormat) {
    const tf = tickFormat || format;
    return (value, context) => {
        const pattern = (context && context.location === 'tick') ? tf : format;
        return formatDateStr(value, pattern);
    };
}

/**
 * Custom brush overlay showing values at start/end positions with difference and percentage.
 * Used internally when brushOverlay='values' is specified.
 */
function CustomBrushOverlay({ seriesId, primaryColor = '#1976d2', positiveColor = '#4caf50', negativeColor = '#f44336' }) {
    const drawingArea = useDrawingArea();
    const brush = useBrush();
    const xScale = useXScale();
    const series = useLineSeries(seriesId);

    if (!brush || !series || !drawingArea) {
        return null;
    }

    const { left, top, width, height } = drawingArea;

    // Clamp coordinates to drawing area
    const clampX = (x) => Math.max(left, Math.min(left + width, x));
    const clampedStartX = clampX(brush.start.x || 0);
    const clampedCurrentX = clampX(brush.current.x || 0);

    const minX = Math.min(clampedStartX, clampedCurrentX);
    const maxX = Math.max(clampedStartX, clampedCurrentX);
    const rectWidth = maxX - minX;

    if (rectWidth < 1) {
        return null;
    }

    // Calculate data indices (for point/band scale)
    const getIndex = (x) => {
        if (xScale.step) {
            return Math.floor((x - Math.min(...xScale.range()) + xScale.step() / 2) / xScale.step());
        }
        // For linear scale, find closest point
        return Math.round((x - left) / width * (series.data.length - 1));
    };

    const startIndex = Math.max(0, Math.min(series.data.length - 1, getIndex(clampedStartX)));
    const currentIndex = Math.max(0, Math.min(series.data.length - 1, getIndex(clampedCurrentX)));

    const startValue = series.data[startIndex] || 0;
    const currentValue = series.data[currentIndex] || 0;
    const difference = currentValue - startValue;
    const percentChange = startValue !== 0 ? ((difference / startValue) * 100).toFixed(2) : '0.00';

    // Get labels from x-axis domain if available
    const startLabel = xScale.domain ? (xScale.domain()[startIndex] || startIndex) : startIndex;
    const currentLabel = xScale.domain ? (xScale.domain()[currentIndex] || currentIndex) : currentIndex;

    const diffColor = difference >= 0 ? positiveColor : negativeColor;

    return (
        <g>
            {/* Start line */}
            <line x1={clampedStartX} y1={top} x2={clampedStartX} y2={top + height}
                stroke={primaryColor} strokeWidth={2} strokeDasharray="5,5" pointerEvents="none" />

            {/* Current line */}
            <line x1={clampedCurrentX} y1={top} x2={clampedCurrentX} y2={top + height}
                stroke={primaryColor} strokeWidth={2} strokeDasharray="5,5" pointerEvents="none" />

            {/* Selection rectangle */}
            <rect x={minX} y={top} width={rectWidth} height={height}
                fill={primaryColor} fillOpacity={0.1} pointerEvents="none" />

            {/* Start label */}
            <g transform={`translate(${clampedStartX}, ${top + 15})`}>
                <rect x={-30} y={0} width={60} height={40} fill={primaryColor} rx={4} />
                <text x={0} y={16} textAnchor="middle" fill="white" fontSize={10}>{String(startLabel)}</text>
                <text x={0} y={32} textAnchor="middle" fill="white" fontSize={11} fontWeight="bold">
                    {typeof startValue === 'number' ? startValue.toFixed(2) : startValue}
                </text>
            </g>

            {/* End label */}
            <g transform={`translate(${clampedCurrentX}, ${top + 15})`}>
                <rect x={-30} y={0} width={60} height={40} fill={primaryColor} rx={4} />
                <text x={0} y={16} textAnchor="middle" fill="white" fontSize={10}>{String(currentLabel)}</text>
                <text x={0} y={32} textAnchor="middle" fill="white" fontSize={11} fontWeight="bold">
                    {typeof currentValue === 'number' ? currentValue.toFixed(2) : currentValue}
                </text>
            </g>

            {/* Difference label in middle */}
            <g transform={`translate(${(minX + maxX) / 2}, ${top + height - 30})`}>
                <rect x={-50} y={0} width={100} height={26} fill={diffColor} rx={4} />
                <text x={0} y={17} textAnchor="middle" fill="white" fontSize={12} fontWeight="bold">
                    {difference >= 0 ? '+' : ''}{difference.toFixed(2)} ({percentChange}%)
                </text>
            </g>
        </g>
    );
}

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
        zoomInteractionConfig,
        // Reference lines
        referenceLines = [],
        // Brush config (Pro feature)
        brushConfig,
        brushOverlay = 'none',  // 'none' | 'default' | 'values'
        brushSeriesId,  // Series ID for custom brush overlay calculations
        // Axis highlight configuration
        axisHighlight = { x: 'line', y: 'none' },
        // Controlled highlight props
        highlightedAxis,
        highlightedItem,
        // Controlled tooltip props
        tooltipItem,
        // Toolbar (Pro feature)
        showToolbar = false,
        // Dash-specific output props (not passed to MUI)
        brushData,
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

    // --- Controlled Axis Highlight State ---
    const lastKnownHighlightedAxisRef = useRef(JSON.stringify(highlightedAxis ?? []));
    const [controlledHighlightedAxis, setControlledHighlightedAxis] = useState(() =>
        highlightedAxis && Array.isArray(highlightedAxis) ? highlightedAxis : []
    );

    // Sync external highlightedAxis prop changes to internal state
    useEffect(() => {
        const currentStr = JSON.stringify(highlightedAxis ?? []);
        if (currentStr !== lastKnownHighlightedAxisRef.current) {
            lastKnownHighlightedAxisRef.current = currentStr;
            setControlledHighlightedAxis(highlightedAxis ?? []);
        }
    }, [highlightedAxis]);

    // Handle highlighted axis changes from chart interaction
    const handleHighlightedAxisChange = (newValue) => {
        const value = newValue ?? [];
        setControlledHighlightedAxis(value);
        lastKnownHighlightedAxisRef.current = JSON.stringify(value);
        if (setProps) {
            setProps({ highlightedAxis: value });
        }
    };

    // --- Controlled Item Highlight State ---
    // Initialize to null (not undefined) to ensure MUI uses controlled mode
    const lastKnownHighlightedItemRef = useRef(JSON.stringify(highlightedItem ?? null));
    const [controlledHighlightedItem, setControlledHighlightedItem] = useState(() =>
        highlightedItem ?? null
    );

    // Sync external highlightedItem prop changes to internal state
    useEffect(() => {
        const currentStr = JSON.stringify(highlightedItem ?? null);
        if (currentStr !== lastKnownHighlightedItemRef.current) {
            lastKnownHighlightedItemRef.current = currentStr;
            setControlledHighlightedItem(highlightedItem ?? null);
        }
    }, [highlightedItem]);

    // Handle highlight changes from chart interaction
    const handleHighlightChange = (newValue) => {
        // MUI passes null when clearing highlight
        const value = newValue ?? null;
        setControlledHighlightedItem(value);
        lastKnownHighlightedItemRef.current = JSON.stringify(value);
        if (setProps) {
            setProps({ highlightedItem: value });
        }
    };

    // --- Controlled Tooltip Item State ---
    const lastKnownTooltipItemRef = useRef(JSON.stringify(tooltipItem ?? null));
    const [controlledTooltipItem, setControlledTooltipItem] = useState(() =>
        tooltipItem ?? null
    );

    // Sync external tooltipItem prop changes to internal state
    useEffect(() => {
        const currentStr = JSON.stringify(tooltipItem ?? null);
        if (currentStr !== lastKnownTooltipItemRef.current) {
            lastKnownTooltipItemRef.current = currentStr;
            setControlledTooltipItem(tooltipItem ?? null);
        }
    }, [tooltipItem]);

    // Handle tooltip item changes from chart interaction
    const handleTooltipItemChange = (newValue) => {
        const value = newValue ?? null;
        setControlledTooltipItem(value);
        lastKnownTooltipItemRef.current = JSON.stringify(value);
        if (setProps) {
            setProps({ tooltipItem: value });
        }
    };

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

    // Detect if any axis config has zoom.slider.enabled set directly
    const hasSliderInAxisConfig = useMemo(() => {
        const checkAxes = (axes) => {
            if (!axes) return false;
            return axes.some(axis => {
                const zoom = axis.zoom;
                return zoom && typeof zoom === 'object' && zoom.slider && zoom.slider.enabled;
            });
        };
        return checkAxes(xAxis) || checkAxes(yAxis);
    }, [xAxis, yAxis]);

    // Process xAxis: resolve valueFormatter, apply dateFormat, inject slider config
    const processedXAxis = useMemo(() => {
        if (!xAxis) return undefined;

        return xAxis.map(axis => {
            let result = { ...axis };

            // Built-in dateFormat: creates a valueFormatter from format strings
            // Usage: dateFormat='M/d HH:mm', dateTickFormat='M/d'
            if (axis.dateFormat) {
                result.valueFormatter = createDateFormatter(axis.dateFormat, axis.dateTickFormat);
                delete result.dateFormat;
                delete result.dateTickFormat;
            }
            // DMC-style function-as-prop valueFormatter (for advanced use cases)
            else if (axis.valueFormatter && typeof axis.valueFormatter !== 'function') {
                const resolved = resolveFunctionProp(axis.valueFormatter);
                if (resolved) {
                    result.valueFormatter = resolved;
                } else {
                    delete result.valueFormatter;
                }
            }

            // Inject slider: { enabled: true } into zoom config when showSlider is true
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
    if (brushConfig) providerProps.brushConfig = brushConfig;
    if (zoomInteractionConfig) providerProps.zoomInteractionConfig = zoomInteractionConfig;

    // Zoom props - use initialZoom for mounting since we force remount on external changes
    // This ensures MUI properly initializes with the desired zoom state
    if (controlledZoom && controlledZoom.length > 0) {
        providerProps.initialZoom = controlledZoom;
    }

    // Controlled axis highlight - always pass to ensure controlled mode
    providerProps.highlightedAxis = controlledHighlightedAxis;
    providerProps.onHighlightedAxisChange = handleHighlightedAxisChange;

    // Controlled item highlight - always pass to ensure controlled mode
    // MUI uses undefined vs null to determine controlled vs uncontrolled
    providerProps.highlightedItem = controlledHighlightedItem;
    providerProps.onHighlightChange = handleHighlightChange;

    // Controlled tooltip item - for synchronized tooltips across charts
    providerProps.tooltipItem = controlledTooltipItem;
    providerProps.onTooltipItemChange = handleTooltipItemChange;

    // Rendering props that must be forwarded from axis config to ChartsXAxis/ChartsYAxis components.
    // In MUI's composition API, these are component props, not axis definition properties.
    const AXIS_RENDER_PROPS = [
        'tickSize', 'disableLine', 'disableTicks', 'tickLabelStyle', 'labelStyle',
        'tickLabelPlacement', 'tickPlacement', 'tickLabelMinGap', 'tickSpacing',
        'tickInterval', 'tickLabelInterval',
    ];

    // Extract rendering props from an axis config object
    const extractRenderProps = (axisConfig) => {
        if (!axisConfig) return {};
        const renderProps = {};
        for (const prop of AXIS_RENDER_PROPS) {
            if (axisConfig[prop] !== undefined) {
                renderProps[prop] = axisConfig[prop];
            }
        }
        return renderProps;
    };

    // Build x-axis rendering configs (array of {axisId, renderProps})
    const xAxisConfigs = useMemo(() => {
        const resolvedXAxis = processedXAxis || xAxis;
        if (!resolvedXAxis || resolvedXAxis.length === 0) return [{ renderProps: {} }];
        return resolvedXAxis.map(axis => ({
            axisId: axis.id,
            renderProps: extractRenderProps(axis),
        }));
    }, [processedXAxis, xAxis]);

    // Extract Y-axis IDs and rendering configs
    const yAxisConfigs = useMemo(() => {
        if (!yAxis) return [{ renderProps: {} }];
        return yAxis.map(axis => ({
            axisId: axis.id,
            renderProps: extractRenderProps(axis),
        }));
    }, [yAxis]);

    return (
        <div id={id}>
            <ChartDataProviderPro key={chartKey} {...providerProps}>
                {/* Toolbar (Pro feature) */}
                {showToolbar && <ChartsToolbarPro />}

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

                    {/* Axes - forward rendering props from axis config */}
                    {xAxisConfigs.map((config, idx) => (
                        <ChartsXAxis
                            key={config.axisId || `x-${idx}`}
                            axisId={config.axisId}
                            {...config.renderProps}
                        />
                    ))}
                    {yAxisConfigs.map((config, idx) => (
                        <ChartsYAxis
                            key={config.axisId || `y-${idx}`}
                            axisId={config.axisId}
                            {...config.renderProps}
                        />
                    ))}

                    {/* Reference lines */}
                    {referenceLines && referenceLines.map((refLine, idx) => (
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
                    ))}

                    {/* Axis highlight for tooltips */}
                    <ChartsAxisHighlight
                        x={axisHighlight?.x || 'none'}
                        y={axisHighlight?.y || 'none'}
                    />

                    {/* Brush overlays */}
                    {brushOverlay === 'default' && <ChartsBrushOverlay />}
                    {brushOverlay === 'values' && (
                        <CustomBrushOverlay seriesId={brushSeriesId || (series[0]?.id || 'auto-generated-id-0')} />
                    )}

                    {/* Zoom slider - render when showSlider is true OR any axis has zoom.slider.enabled */}
                    {(showSlider || hasSliderInAxisConfig) && <ChartZoomSlider />}
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
     * - highlightScope (object): Per-series highlight behavior with:
     *   - highlight: 'none', 'item', or 'series'
     *   - fade: 'none', 'series', or 'global'
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
        highlightScope: PropTypes.shape({
            highlight: PropTypes.oneOf(['none', 'item', 'series']),
            fade: PropTypes.oneOf(['none', 'series', 'global']),
        }),
    })),

    /**
     * X-axis configuration. Array of axis config objects.
     * Each axis object can have:
     * - data (array): X-axis values (timestamps in ms for 'time' scaleType)
     * - dataKey (string): Key to use from dataset for axis values
     * - label (string): Axis label
     * - scaleType (string): 'band', 'point', 'linear', 'log', 'time', 'utc', 'symlog', 'sqrt'
     * - position (string): 'top', 'bottom', or 'none' (hidden but still computed)
     * - id (string): Axis identifier for referencing in series and zoom
     * - min (number): Minimum domain value
     * - max (number): Maximum domain value
     * - reverse (boolean): Reverse axis direction
     * - tickNumber (number): Approximate number of ticks
     * - tickMinStep (number): Minimum step between ticks (ms for time axes)
     * - tickMaxStep (number): Maximum step between ticks
     * - tickSize (number): Tick mark length in pixels (default: 6)
     * - tickSpacing (number): Minimum spacing in px between ticks (ordinal axes only)
     * - tickInterval (array): Fixed tick positions as array of values
     * - tickLabelStyle (object): CSS style for tick labels (e.g. {angle: 45, fontSize: 12})
     * - tickLabelPlacement (string): 'middle' or 'tick' (band scale only)
     * - tickPlacement (string): 'end', 'extremities', 'middle', 'start' (band scale only)
     * - tickLabelMinGap (number): Minimum gap in px between tick labels (default: 4)
     * - labelStyle (object): CSS style for the axis label
     * - height (number): Space reserved for this x-axis in pixels
     * - disableLine (boolean): Hide the axis line
     * - disableTicks (boolean): Hide tick marks
     * - domainLimit (string): 'nice' (default, rounds to friendly values) or 'strict'
     * - categoryGapRatio (number): Gap ratio between bands (0-1, band scale only)
     * - barGapRatio (number): Gap ratio between bars within a band (band scale only)
     * - colorMap (object): Axis color mapping configuration
     * - zoom (boolean or object): Enable zoom on this axis. Can be true or object with:
     *   - minStart (number): Minimum start position (0-100)
     *   - maxEnd (number): Maximum end position (0-100)
     *   - minSpan (number): Minimum zoom span
     *   - maxSpan (number): Maximum zoom span
     *   - step (number): Zoom step size
     *   - panning (boolean): Enable panning
     *   - filterMode (string): 'keep' or 'discard'
     *   - slider (object): Slider config with { enabled, preview, size, showTooltip }
     */
    xAxis: PropTypes.arrayOf(PropTypes.shape({
        data: PropTypes.array,
        dataKey: PropTypes.string,
        label: PropTypes.string,
        scaleType: PropTypes.oneOf(['band', 'point', 'linear', 'log', 'time', 'utc', 'symlog', 'sqrt']),
        position: PropTypes.oneOf(['top', 'bottom', 'none']),
        id: PropTypes.string,
        min: PropTypes.number,
        max: PropTypes.number,
        reverse: PropTypes.bool,
        tickNumber: PropTypes.number,
        tickMinStep: PropTypes.number,
        tickMaxStep: PropTypes.number,
        tickSize: PropTypes.number,
        tickSpacing: PropTypes.number,
        tickInterval: PropTypes.array,
        tickLabelStyle: PropTypes.object,
        tickLabelPlacement: PropTypes.oneOf(['middle', 'tick']),
        tickPlacement: PropTypes.oneOf(['end', 'extremities', 'middle', 'start']),
        tickLabelMinGap: PropTypes.number,
        labelStyle: PropTypes.object,
        height: PropTypes.number,
        dateFormat: PropTypes.string,
        dateTickFormat: PropTypes.string,
        disableLine: PropTypes.bool,
        disableTicks: PropTypes.bool,
        domainLimit: PropTypes.oneOf(['nice', 'strict']),
        categoryGapRatio: PropTypes.number,
        barGapRatio: PropTypes.number,
        colorMap: PropTypes.object,
        zoom: PropTypes.oneOfType([
            PropTypes.bool,
            PropTypes.object,
        ]),
        valueFormatter: PropTypes.oneOfType([
            PropTypes.func,
            PropTypes.shape({
                function: PropTypes.string.isRequired,
                options: PropTypes.object,
            }),
        ]),
    })),

    /**
     * Y-axis configuration. Array of axis config objects.
     * Each axis object can have:
     * - data (array): Y-axis values (for horizontal bar charts)
     * - dataKey (string): Key to use from dataset for axis values
     * - label (string): Axis label
     * - scaleType (string): 'band', 'point', 'linear', 'log', 'time', 'utc', 'symlog', 'sqrt'
     * - position (string): 'left', 'right', or 'none' (hidden but still computed)
     * - id (string): Axis identifier for referencing in series
     * - min (number): Minimum domain value
     * - max (number): Maximum domain value
     * - width (number): Width allocated for axis in pixels
     * - reverse (boolean): Reverse axis direction
     * - tickNumber (number): Approximate number of ticks
     * - tickMinStep (number): Minimum step between ticks
     * - tickMaxStep (number): Maximum step between ticks
     * - tickSize (number): Tick mark length in pixels (default: 6)
     * - tickSpacing (number): Minimum spacing in px between ticks (ordinal axes only)
     * - tickInterval (array): Fixed tick positions as array of values
     * - tickLabelStyle (object): CSS style for tick labels (e.g. {angle: 45, fontSize: 12})
     * - tickLabelPlacement (string): 'middle' or 'tick' (band scale only)
     * - tickPlacement (string): 'end', 'extremities', 'middle', 'start' (band scale only)
     * - tickLabelMinGap (number): Minimum gap in px between tick labels (default: 4)
     * - labelStyle (object): CSS style for the axis label
     * - height (number): Space reserved for this y-axis in pixels
     * - disableLine (boolean): Hide the axis line
     * - disableTicks (boolean): Hide tick marks
     * - domainLimit (string): 'nice' (default, rounds to friendly values) or 'strict'
     * - categoryGapRatio (number): Gap ratio between bands (0-1, band scale only)
     * - barGapRatio (number): Gap ratio between bars within a band (band scale only)
     * - colorMap (object): Axis color mapping configuration
     * - zoom (boolean or object): Enable zoom on this axis (same options as xAxis)
     */
    yAxis: PropTypes.arrayOf(PropTypes.shape({
        data: PropTypes.array,
        dataKey: PropTypes.string,
        label: PropTypes.string,
        scaleType: PropTypes.oneOf(['band', 'point', 'linear', 'log', 'time', 'utc', 'symlog', 'sqrt']),
        position: PropTypes.oneOf(['left', 'right', 'none']),
        id: PropTypes.string,
        min: PropTypes.number,
        max: PropTypes.number,
        width: PropTypes.number,
        reverse: PropTypes.bool,
        dateFormat: PropTypes.string,
        dateTickFormat: PropTypes.string,
        tickNumber: PropTypes.number,
        tickMinStep: PropTypes.number,
        tickMaxStep: PropTypes.number,
        tickSize: PropTypes.number,
        tickSpacing: PropTypes.number,
        tickInterval: PropTypes.array,
        tickLabelStyle: PropTypes.object,
        tickLabelPlacement: PropTypes.oneOf(['middle', 'tick']),
        tickPlacement: PropTypes.oneOf(['end', 'extremities', 'middle', 'start']),
        tickLabelMinGap: PropTypes.number,
        labelStyle: PropTypes.object,
        height: PropTypes.number,
        disableLine: PropTypes.bool,
        disableTicks: PropTypes.bool,
        domainLimit: PropTypes.oneOf(['nice', 'strict']),
        categoryGapRatio: PropTypes.number,
        barGapRatio: PropTypes.number,
        colorMap: PropTypes.object,
        zoom: PropTypes.oneOfType([
            PropTypes.bool,
            PropTypes.object,
        ]),
        valueFormatter: PropTypes.oneOfType([
            PropTypes.func,
            PropTypes.shape({
                function: PropTypes.string.isRequired,
                options: PropTypes.object,
            }),
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
     * Zoom interaction configuration. Controls which interactions are enabled for
     * zooming and panning. Object with:
     * - zoom (array): Zoom interactions - 'wheel', 'pinch', 'tapAndDrag', 'brush', 'doubleTapReset',
     *   or objects with { type, requiredKeys, pointerMode }
     * - pan (array): Pan interactions - 'drag', 'pressAndDrag', 'wheel',
     *   or objects with { type, requiredKeys, pointerMode }
     */
    zoomInteractionConfig: PropTypes.shape({
        zoom: PropTypes.arrayOf(PropTypes.oneOfType([
            PropTypes.string,
            PropTypes.shape({
                type: PropTypes.string,
                requiredKeys: PropTypes.arrayOf(PropTypes.string),
                pointerMode: PropTypes.oneOf(['mouse', 'touch']),
            }),
        ])),
        pan: PropTypes.arrayOf(PropTypes.oneOfType([
            PropTypes.string,
            PropTypes.shape({
                type: PropTypes.string,
                requiredKeys: PropTypes.arrayOf(PropTypes.string),
                pointerMode: PropTypes.oneOf(['mouse', 'touch']),
            }),
        ])),
    }),

    /**
     * Array of reference line configurations. Each reference line can be vertical (x) or horizontal (y).
     * - x (string|number): X-axis value for a vertical reference line
     * - y (number): Y-axis value for a horizontal reference line
     * - axisId (string): The axis ID to use for the reference value
     * - label (string): Label text displayed along the reference line
     * - labelAlign (string): 'start', 'middle', or 'end' alignment
     * - lineStyle (object): CSS style object for the line (e.g. {stroke: 'red', strokeDasharray: '4 4'})
     * - labelStyle (object): CSS style object for the label
     * - spacing (number|object): Space around label in px, or {x, y} object
     */
    referenceLines: PropTypes.arrayOf(PropTypes.shape({
        x: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
        y: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
        axisId: PropTypes.string,
        label: PropTypes.string,
        labelAlign: PropTypes.oneOf(['start', 'middle', 'end']),
        lineStyle: PropTypes.object,
        labelStyle: PropTypes.object,
        spacing: PropTypes.oneOfType([PropTypes.number, PropTypes.object]),
    })),

    /**
     * Brush configuration for range selection. Object with:
     * - enabled (boolean): Whether brush interaction is enabled (default: false)
     * - preventTooltip (boolean): Prevent tooltip during brush (default: true)
     * - preventHighlight (boolean): Prevent highlight during brush (default: true)
     */
    brushConfig: PropTypes.shape({
        enabled: PropTypes.bool,
        preventTooltip: PropTypes.bool,
        preventHighlight: PropTypes.bool,
    }),

    /**
     * Type of brush overlay to display:
     * - 'none': No overlay (default)
     * - 'default': Standard MUI selection rectangle
     * - 'values': Custom overlay showing start/end values with difference and percentage
     */
    brushOverlay: PropTypes.oneOf(['none', 'default', 'values']),

    /**
     * Series ID for the custom 'values' brush overlay to read data from.
     * If not specified, uses the first series.
     */
    brushSeriesId: PropTypes.string,

    /**
     * Current brush selection data. Read-only output property.
     * Contains pixel coordinates of the brush selection.
     */
    brushData: PropTypes.shape({
        start: PropTypes.shape({
            x: PropTypes.number,
            y: PropTypes.number,
        }),
        current: PropTypes.shape({
            x: PropTypes.number,
            y: PropTypes.number,
        }),
        timestamp: PropTypes.string,
    }),

    /**
     * Axis highlight configuration. Controls how axes are highlighted on hover.
     * - x (string): 'none', 'line', or 'band'
     * - y (string): 'none' or 'line'
     */
    axisHighlight: PropTypes.shape({
        x: PropTypes.oneOf(['none', 'line', 'band']),
        y: PropTypes.oneOf(['none', 'line']),
    }),

    /**
     * Controlled axis highlight state. Array of objects specifying which axis values
     * are highlighted. Each object has:
     * - axisId (string|number): The axis identifier
     * - dataIndex (number): The data index to highlight
     * Set to empty array [] to clear highlights.
     */
    highlightedAxis: PropTypes.arrayOf(PropTypes.shape({
        axisId: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
        dataIndex: PropTypes.number.isRequired,
    })),

    /**
     * Controlled item highlight state. Specifies which data point is highlighted.
     * Object with:
     * - seriesId (string): The series identifier
     * - dataIndex (number): The data index within the series (optional)
     * Set to null to clear highlight.
     */
    highlightedItem: PropTypes.shape({
        seriesId: PropTypes.string.isRequired,
        dataIndex: PropTypes.number,
    }),

    /**
     * Show chart toolbar with zoom/export controls. This is a Pro feature
     * that requires a valid licenseKey.
     */
    showToolbar: PropTypes.bool,

    /**
     * Controlled tooltip item state. Used to synchronize tooltips across multiple charts.
     * Object with:
     * - type (string): Chart type ('line', 'bar', 'pie', etc.)
     * - seriesId (string): The series identifier
     * - dataIndex (number): The data index within the series
     * Set to null to hide tooltip.
     */
    tooltipItem: PropTypes.shape({
        type: PropTypes.string,
        seriesId: PropTypes.string,
        dataIndex: PropTypes.number,
    }),

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
