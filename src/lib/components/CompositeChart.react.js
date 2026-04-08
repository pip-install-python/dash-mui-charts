import React, { useId, useMemo, useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { LicenseInfo } from '@mui/x-license';
import { ChartDataProviderPro } from '@mui/x-charts-pro/ChartDataProviderPro';
import { ChartsSurface } from '@mui/x-charts-pro/ChartsSurface';
import { LinePlot, AreaPlot, MarkPlot } from '@mui/x-charts-pro/LineChart';
import { ScatterPlot } from '@mui/x-charts/ScatterChart';
import { ChartsXAxis } from '@mui/x-charts-pro/ChartsXAxis';
import { ChartsYAxis } from '@mui/x-charts-pro/ChartsYAxis';
import { ChartsGrid } from '@mui/x-charts-pro/ChartsGrid';
import { ChartsTooltip } from '@mui/x-charts-pro/ChartsTooltip';
import { ChartsTooltipContainer, useAxesTooltip } from '@mui/x-charts/ChartsTooltip';
import { ChartsAxisHighlight } from '@mui/x-charts-pro/ChartsAxisHighlight';
import { ChartsLegend } from '@mui/x-charts-pro/ChartsLegend';
import { ChartsClipPath } from '@mui/x-charts-pro/ChartsClipPath';
import { ChartsReferenceLine } from '@mui/x-charts-pro/ChartsReferenceLine';
import { ChartZoomSlider } from '@mui/x-charts-pro/ChartZoomSlider';
import { ChartsToolbarPro } from '@mui/x-charts-pro/ChartsToolbarPro';

// Track if license key has been set globally
let licenseKeySet = false;

/**
 * Resolve a function-as-prop value from a {function, options} descriptor.
 * Mirrors Dash Mantine Components' dashMantineFunctions pattern.
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
 * Tokens: YYYY, MMM, MM, M, dd, d, HH, mm
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
 * Custom axis tooltip content that also shows nearby scatter data points.
 * Rendered inside ChartsTooltipContainer for proper positioning.
 */
function CompositeAxisTooltipContent({ scatterSeries, proximity }) {
    const tooltipAxes = useAxesTooltip();
    if (!tooltipAxes || tooltipAxes.length === 0) return null;

    // Use the first axis tooltip data
    const tooltipData = tooltipAxes[0];
    const { axisValue, axisFormattedValue, seriesItems } = tooltipData;

    // Format Date axis values as readable date/time strings.
    // axisValue may be a Date (if time scale converted it) or a large number (epoch ms).
    let displayAxisValue = axisFormattedValue;
    if (axisValue instanceof Date) {
        displayAxisValue = axisValue.toLocaleString(undefined, {
            month: 'short', day: 'numeric', year: 'numeric',
            hour: 'numeric', minute: '2-digit',
        });
    } else if (typeof axisValue === 'number' && axisValue > 1e12) {
        // Likely epoch ms — format as date
        displayAxisValue = new Date(axisValue).toLocaleString(undefined, {
            month: 'short', day: 'numeric', year: 'numeric',
            hour: 'numeric', minute: '2-digit',
        });
    }

    // Build set of scatter series IDs so we can filter them from MUI's seriesItems.
    // MUI's axis tooltip handles scatter data poorly in composite charts
    // (wrong dataIndex mapping, raw (x,y) formatting), so we handle scatter ourselves.
    const scatterSeriesIds = new Set(
        (scatterSeries || []).map(s => s.id)
    );

    // Only keep line/area entries from MUI's axis tooltip
    const lineEntries = (seriesItems || []).filter(
        entry => !scatterSeriesIds.has(entry.seriesId)
    );

    // Find ALL scatter points near the hovered axis value via proximity search.
    // Each matching point gets its own row (handles multiple points at same x).
    const scatterEntries = [];
    if (scatterSeries && axisValue != null) {
        const numericValue = axisValue instanceof Date ? axisValue.getTime() : Number(axisValue);
        for (const s of scatterSeries) {
            if (!s.data) continue;
            for (const point of s.data) {
                const dist = Math.abs(point.x - numericValue);
                if (dist <= proximity) {
                    const yVal = point.y;
                    scatterEntries.push({
                        seriesId: s.id,
                        color: s.color || '#666',
                        formattedLabel: s.label || s.id,
                        formattedValue: typeof yVal === 'number'
                            ? yVal.toLocaleString(undefined, { maximumFractionDigits: 2 })
                            : String(yVal),
                    });
                }
            }
        }
    }

    // Combine: line entries first, then scatter matches
    const allEntries = [...lineEntries, ...scatterEntries];
    if (allEntries.length === 0) return null;

    const rowStyle = { display: 'flex', alignItems: 'center', gap: 6, padding: '2px 0' };
    const dotStyle = (color) => ({
        display: 'inline-block',
        width: 10,
        height: 10,
        borderRadius: '50%',
        backgroundColor: color,
        flexShrink: 0,
    });

    return (
        <div style={{
            backgroundColor: 'white',
            border: '1px solid #e0e0e0',
            borderRadius: 4,
            padding: '8px 12px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            fontSize: 13,
        }}>
            <div style={{ marginBottom: 4, fontWeight: 500 }}>
                {displayAxisValue}
            </div>
            {allEntries.map((entry, idx) => (
                <div key={`${entry.seriesId}-${idx}`} style={rowStyle}>
                    <span style={dotStyle(entry.color)} />
                    <span>{entry.formattedLabel || entry.seriesId}:</span>
                    <span style={{ fontWeight: 500 }}>{entry.formattedValue}</span>
                </div>
            ))}
        </div>
    );
}

/**
 * CompositeChart component for layering multiple chart types together.
 * Uses MUI X Charts composition API to render scatter, line, and area plots
 * on a single chart surface. Each series must specify its type ('scatter' or 'line').
 * Supports Pro features like zoom/pan with a license key.
 */
export default function CompositeChart(props) {
    const {
        id,
        licenseKey,
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
        slotProps,
        referenceLines,
        // Pro features
        initialZoom,
        showToolbar = false,
        showSlider = false,
        zoomInteractionConfig,
        // Dash output props
        highlightedItem,
        clickData,
        n_clicks = 0,
        zoomData,
        setProps,
    } = props;

    // Set license key once globally
    if (licenseKey && !licenseKeySet) {
        LicenseInfo.setLicenseKey(licenseKey);
        licenseKeySet = true;
    }

    const chartId = useId();
    const clipPathId = `${chartId}-clip`;

    // Track zoom for controlled remount
    const [chartKey, setChartKey] = useState(0);
    const lastZoomPropRef = useRef(JSON.stringify(initialZoom));

    useEffect(() => {
        const currentStr = JSON.stringify(initialZoom);
        if (currentStr !== lastZoomPropRef.current) {
            lastZoomPropRef.current = currentStr;
            setChartKey(prev => prev + 1);
        }
    }, [initialZoom]);

    // Controlled highlight state
    const [controlledHighlightedItem, setControlledHighlightedItem] = useState(highlightedItem || null);
    const lastHighlightPropRef = useRef(JSON.stringify(highlightedItem));

    useEffect(() => {
        const currentStr = JSON.stringify(highlightedItem);
        if (currentStr !== lastHighlightPropRef.current) {
            lastHighlightPropRef.current = currentStr;
            setControlledHighlightedItem(highlightedItem || null);
        }
    }, [highlightedItem]);

    // Process series - ensure IDs
    const processedSeries = useMemo(() => {
        if (!series || series.length === 0) return [];
        return series.map((s, index) => ({
            ...s,
            id: s.id || `series-${index}`,
        }));
    }, [series]);

    // Determine which plot types are present
    const hasScatter = useMemo(() => processedSeries.some(s => s.type === 'scatter'), [processedSeries]);
    const hasLine = useMemo(() => processedSeries.some(s => s.type === 'line'), [processedSeries]);
    const hasArea = useMemo(() => processedSeries.some(s => s.type === 'line' && s.area), [processedSeries]);
    const hasMarks = useMemo(() => processedSeries.some(s => s.type === 'line' && s.showMark !== false), [processedSeries]);

    // Extract scatter series data for custom tooltip
    const scatterSeriesData = useMemo(() =>
        processedSeries.filter(s => s.type === 'scatter'),
        [processedSeries]);

    // Handle zoom change
    const handleZoomChange = (newZoom) => {
        if (setProps) {
            setProps({ zoomData: newZoom });
        }
    };

    // Handle scatter item click
    const handleScatterClick = (event, params) => {
        if (setProps && params) {
            const seriesConfig = processedSeries.find(s => s.id === params.seriesId);
            const dataPoint = seriesConfig?.data?.[params.dataIndex];

            setProps({
                clickData: {
                    type: 'scatter',
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

    // Handle line/mark click
    const handleLineClick = (event, params) => {
        if (setProps && params) {
            setProps({
                clickData: {
                    type: 'line',
                    seriesId: params.seriesId,
                    dataIndex: params.dataIndex,
                    timestamp: new Date().toISOString(),
                },
                n_clicks: (n_clicks || 0) + 1,
            });
        }
    };

    // Handle highlight change
    const handleHighlightChange = (item) => {
        setControlledHighlightedItem(item);
        lastHighlightPropRef.current = JSON.stringify(item);
        if (setProps) {
            setProps({ highlightedItem: item });
        }
    };

    // Detect slider in axis config
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

    // Process xAxis: resolve valueFormatter/dateFormat, convert epoch ms to Date objects, add slider
    const processedXAxis = useMemo(() => {
        if (!xAxis) return undefined;

        return xAxis.map(axis => {
            let result = { ...axis };

            // Built-in dateFormat: creates a valueFormatter from format strings
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

            // Convert numeric timestamps to Date objects for time scale axes
            if (result.scaleType === 'time' && result.data) {
                result.data = result.data.map(v => typeof v === 'number' ? new Date(v) : v);
            }

            // Inject slider config when showSlider is true
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

    // Auto-compute proximity threshold from x-axis data spacing (must be after processedXAxis)
    const scatterProximity = useMemo(() => {
        const resolvedXAxis = processedXAxis || xAxis;
        if (!resolvedXAxis || !resolvedXAxis[0]?.data || resolvedXAxis[0].data.length < 2) return 0;
        const data = resolvedXAxis[0].data;
        let minStep = Infinity;
        for (let i = 1; i < Math.min(data.length, 100); i++) {
            const a = data[i] instanceof Date ? data[i].getTime() : data[i];
            const b = data[i - 1] instanceof Date ? data[i - 1].getTime() : data[i - 1];
            const step = Math.abs(a - b);
            if (step > 0 && step < minStep) minStep = step;
        }
        return minStep * 0.6;
    }, [processedXAxis, xAxis]);

    // Whether to use custom tooltip that includes scatter data
    const tooltipTrigger = tooltip?.trigger || 'axis';
    const useCustomTooltip = hasScatter && tooltipTrigger === 'axis';

    // Axis render props extraction (same pattern as LineChart)
    const AXIS_RENDER_PROPS = [
        'tickSize', 'disableLine', 'disableTicks', 'tickLabelStyle', 'labelStyle',
        'tickLabelPlacement', 'tickPlacement', 'tickLabelMinGap', 'tickSpacing',
        'tickInterval', 'tickLabelInterval',
    ];

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

    const xAxisConfigs = useMemo(() => {
        const resolvedXAxis = processedXAxis || xAxis;
        if (!resolvedXAxis || resolvedXAxis.length === 0) return [{ renderProps: {} }];
        return resolvedXAxis.map(axis => ({
            axisId: axis.id,
            renderProps: extractRenderProps(axis),
        }));
    }, [processedXAxis, xAxis]);

    const yAxisConfigs = useMemo(() => {
        if (!yAxis) return [{ renderProps: {} }];
        return yAxis.map(axis => ({
            axisId: axis.id,
            renderProps: extractRenderProps(axis),
        }));
    }, [yAxis]);

    // Build provider props
    const providerProps = {
        height,
        series: processedSeries,
        onZoomChange: handleZoomChange,
        skipAnimation,
    };

    if (processedXAxis) providerProps.xAxis = processedXAxis;
    else if (xAxis) providerProps.xAxis = xAxis;
    if (yAxis) providerProps.yAxis = yAxis;
    if (zAxis) providerProps.zAxis = zAxis;
    if (dataset) providerProps.dataset = dataset;
    if (width) providerProps.width = width;
    if (margin) providerProps.margin = margin;
    if (colors) providerProps.colors = colors;
    if (voronoiMaxRadius !== undefined) providerProps.voronoiMaxRadius = voronoiMaxRadius;
    if (disableVoronoi) providerProps.disableVoronoi = disableVoronoi;
    if (zoomInteractionConfig) providerProps.zoomInteractionConfig = zoomInteractionConfig;

    if (initialZoom && initialZoom.length > 0) {
        providerProps.initialZoom = initialZoom;
    }

    // Controlled highlight
    providerProps.highlightedItem = controlledHighlightedItem;
    providerProps.onHighlightChange = handleHighlightChange;

    return (
        <div id={id}>
            <ChartDataProviderPro key={chartKey} {...providerProps}>
                {/* Toolbar (Pro) */}
                {showToolbar && <ChartsToolbarPro />}

                {/* Legend */}
                {!hideLegend && (
                    <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 8 }}>
                        <ChartsLegend />
                    </div>
                )}

                <ChartsSurface>
                    {/* Grid */}
                    {grid && <ChartsGrid horizontal={grid.horizontal} vertical={grid.vertical} />}

                    {/* Clip path for plot area */}
                    <ChartsClipPath id={clipPathId} />

                    {/* Clipped plot area */}
                    <g clipPath={`url(#${clipPathId})`}>
                        {/* Area plots (render first, behind lines) */}
                        {hasArea && <AreaPlot skipAnimation={skipAnimation} />}

                        {/* Line plots */}
                        {hasLine && <LinePlot onItemClick={handleLineClick} skipAnimation={skipAnimation} />}

                        {/* Scatter plots */}
                        {hasScatter && <ScatterPlot onItemClick={handleScatterClick} />}
                    </g>

                    {/* Mark plots (on top, not clipped for visibility) */}
                    {hasMarks && <MarkPlot onItemClick={handleLineClick} skipAnimation={skipAnimation} />}

                    {/* Axes */}
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

                    {/* Axis highlight - default to x='line' when line series are present */}
                    <ChartsAxisHighlight
                        x={axisHighlight?.x ?? (hasLine ? 'line' : 'none')}
                        y={axisHighlight?.y ?? 'none'}
                    />

                    {/* Reference lines */}
                    {referenceLines && referenceLines.map((ref, idx) => (
                        <ChartsReferenceLine key={`ref-${idx}`} {...ref} />
                    ))}

                    {/* Zoom slider */}
                    {(showSlider || hasSliderInAxisConfig) && <ChartZoomSlider />}
                </ChartsSurface>

                {/* Tooltip - use custom composite tooltip when scatter+line, else default */}
                {tooltipTrigger !== 'none' && (
                    useCustomTooltip ? (
                        <ChartsTooltipContainer trigger="axis">
                            <CompositeAxisTooltipContent
                                scatterSeries={scatterSeriesData}
                                proximity={scatterProximity}
                            />
                        </ChartsTooltipContainer>
                    ) : (
                        <ChartsTooltip trigger={tooltipTrigger} />
                    )
                )}
            </ChartDataProviderPro>
        </div>
    );
}

CompositeChart.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * MUI X Pro license key. Required for zoom/pan/toolbar features.
     */
    licenseKey: PropTypes.string,

    /**
     * Array of series to display. Each series MUST include a 'type' field.
     *
     * Scatter series:
     * {type: 'scatter', id, label, color, markerSize, data: [{x, y, id}], highlightScope}
     *
     * Line series:
     * {type: 'line', id, label, color, data: [...], area, curve, showMark, highlightScope, yAxisId}
     */
    series: PropTypes.arrayOf(PropTypes.shape({
        type: PropTypes.oneOf(['scatter', 'line']).isRequired,
        id: PropTypes.string,
        label: PropTypes.string,
        color: PropTypes.string,
        data: PropTypes.oneOfType([
            PropTypes.arrayOf(PropTypes.number),
            PropTypes.arrayOf(PropTypes.shape({
                x: PropTypes.number,
                y: PropTypes.number,
                id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
            })),
        ]),
        datasetKeys: PropTypes.shape({
            x: PropTypes.string,
            y: PropTypes.string,
        }),
        markerSize: PropTypes.number,
        preview: PropTypes.shape({
            markerSize: PropTypes.number,
        }),
        area: PropTypes.bool,
        curve: PropTypes.oneOf([
            'linear', 'monotoneX', 'monotoneY', 'natural',
            'step', 'stepBefore', 'stepAfter',
            'catmullRom', 'bumpX', 'bumpY',
        ]),
        showMark: PropTypes.bool,
        yAxisId: PropTypes.string,
        xAxisId: PropTypes.string,
        highlightScope: PropTypes.shape({
            highlight: PropTypes.oneOf(['item', 'series', 'none']),
            fade: PropTypes.oneOf(['global', 'series', 'none']),
        }),
        stack: PropTypes.string,
        connectNulls: PropTypes.bool,
    })),

    /**
     * X-axis configuration. Array of axis config objects.
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
        zoom: PropTypes.oneOfType([PropTypes.bool, PropTypes.object]),
        dateFormat: PropTypes.string,
        dateTickFormat: PropTypes.string,
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
        zoom: PropTypes.oneOfType([PropTypes.bool, PropTypes.object]),
        valueFormatter: PropTypes.oneOfType([
            PropTypes.func,
            PropTypes.shape({
                function: PropTypes.string.isRequired,
                options: PropTypes.object,
            }),
        ]),
    })),

    /**
     * Z-axis configuration for color mapping scatter points.
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
     * Chart margins in pixels.
     */
    margin: PropTypes.shape({
        top: PropTypes.number,
        right: PropTypes.number,
        bottom: PropTypes.number,
        left: PropTypes.number,
    }),

    /**
     * Grid configuration.
     */
    grid: PropTypes.shape({
        horizontal: PropTypes.bool,
        vertical: PropTypes.bool,
    }),

    /**
     * Color palette array.
     */
    colors: PropTypes.arrayOf(PropTypes.string),

    /**
     * Maximum distance for Voronoi scatter interaction.
     */
    voronoiMaxRadius: PropTypes.oneOfType([
        PropTypes.number,
        PropTypes.oneOf(['item']),
    ]),

    /**
     * If true, disables Voronoi cell interaction.
     */
    disableVoronoi: PropTypes.bool,

    /**
     * Axis highlight configuration.
     */
    axisHighlight: PropTypes.shape({
        x: PropTypes.oneOf(['none', 'line', 'band']),
        y: PropTypes.oneOf(['none', 'line', 'band']),
    }),

    /**
     * Tooltip configuration.
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
     * Props passed to internal slot components.
     */
    slotProps: PropTypes.object,

    /**
     * Reference lines to display on the chart.
     * Array of objects with:
     * - x (number|string): Vertical reference line at x value
     * - y (number): Horizontal reference line at y value
     * - label (string): Label text
     * - lineStyle (object): CSS for line element
     * - labelStyle (object): CSS for label text
     * - labelAlign (string): 'start', 'middle', 'end'
     */
    referenceLines: PropTypes.arrayOf(PropTypes.shape({
        x: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
        y: PropTypes.number,
        label: PropTypes.string,
        lineStyle: PropTypes.object,
        labelStyle: PropTypes.object,
        labelAlign: PropTypes.oneOf(['start', 'middle', 'end']),
        spacing: PropTypes.object,
    })),

    /**
     * Initial zoom configuration (Pro). Array of {axisId, start, end} objects.
     * start/end are percentages (0-100) of the axis range.
     */
    initialZoom: PropTypes.arrayOf(PropTypes.shape({
        axisId: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
        start: PropTypes.number,
        end: PropTypes.number,
    })),

    /**
     * If true, shows the Pro toolbar for zoom/export controls.
     */
    showToolbar: PropTypes.bool,

    /**
     * If true, shows the zoom slider below the chart.
     * Injects zoom.slider.enabled into x-axis config.
     */
    showSlider: PropTypes.bool,

    /**
     * Fine-grained control over zoom/pan interactions (Pro).
     * - zoom: Array of interaction types ['wheel', 'pinch', 'brush', 'tapAndDrag', 'doubleTapReset']
     * - pan: Array of interaction types ['drag', 'pressAndDrag', 'wheel']
     */
    zoomInteractionConfig: PropTypes.shape({
        zoom: PropTypes.array,
        pan: PropTypes.array,
    }),

    /**
     * Currently highlighted item (controlled input/output).
     */
    highlightedItem: PropTypes.object,

    /**
     * Data from the most recent click event.
     * Contains type ('scatter'|'line'), seriesId, dataIndex, and timestamp.
     */
    clickData: PropTypes.object,

    /**
     * Number of times the chart has been clicked.
     */
    n_clicks: PropTypes.number,

    /**
     * Current zoom state. Read-only output updated on zoom/pan.
     * Array of {axisId, start, end} objects.
     */
    zoomData: PropTypes.arrayOf(PropTypes.shape({
        axisId: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
        start: PropTypes.number,
        end: PropTypes.number,
    })),

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func,
};