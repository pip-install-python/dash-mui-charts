import React, { useId, useMemo, useState, useEffect, useRef, useCallback } from 'react';
import PropTypes from 'prop-types';
import { LicenseInfo } from '@mui/x-license';
import { ChartDataProviderPro } from '@mui/x-charts-pro/ChartDataProviderPro';
import { ChartsSurface } from '@mui/x-charts-pro/ChartsSurface';
import { ChartsXAxis } from '@mui/x-charts-pro/ChartsXAxis';
import { ChartsYAxis } from '@mui/x-charts-pro/ChartsYAxis';
import { ChartsGrid } from '@mui/x-charts-pro/ChartsGrid';
import { ChartsAxisHighlight } from '@mui/x-charts-pro/ChartsAxisHighlight';
import { ChartsLegend } from '@mui/x-charts-pro/ChartsLegend';
import { ChartsClipPath } from '@mui/x-charts-pro/ChartsClipPath';
import { ChartsReferenceLine } from '@mui/x-charts-pro/ChartsReferenceLine';
import { ChartZoomSlider } from '@mui/x-charts-pro/ChartZoomSlider';
import { ChartsToolbarPro } from '@mui/x-charts-pro/ChartsToolbarPro';
import { useXScale, useYScale, useDrawingArea } from '@mui/x-charts/hooks';

// Track if license key has been set globally
let licenseKeySet = false;

/**
 * Custom CandlePlot renders OHLC candles inside ChartsSurface using
 * MUI's scale hooks. Each candle is an SVG rect (body) + line (wick).
 */
function CandlePlot({ ohlcData, labels, upColor, downColor, bodyWidthRatio, wickWidth, onCandleClick }) {
    const xScale = useXScale();
    const yScale = useYScale();
    const { left, top, width, height } = useDrawingArea();

    if (!xScale || !yScale || !ohlcData || ohlcData.length === 0) return null;

    const bandwidth = xScale.bandwidth ? xScale.bandwidth() : (width / ohlcData.length);
    const bodyWidth = bandwidth * (bodyWidthRatio || 0.6);

    return (
        <g>
            {ohlcData.map((d, i) => {
                const label = labels[i];
                const xBase = xScale(label);
                if (xBase === undefined) return null;

                const cx = xBase + bandwidth / 2;
                const isUp = d.close >= d.open;
                const color = isUp ? (upColor || '#4caf50') : (downColor || '#f44336');

                const bodyTop = yScale(Math.max(d.open, d.close));
                const bodyBottom = yScale(Math.min(d.open, d.close));
                const wickTop = yScale(d.high);
                const wickBottom = yScale(d.low);

                const bodyHeight = Math.max(1, bodyBottom - bodyTop);

                return (
                    <g key={i}
                       style={{ cursor: onCandleClick ? 'pointer' : 'default' }}
                       onClick={onCandleClick ? (e) => onCandleClick(e, i, d) : undefined}
                    >
                        {/* Upper wick */}
                        <line
                            x1={cx} y1={wickTop}
                            x2={cx} y2={bodyTop}
                            stroke={color}
                            strokeWidth={wickWidth || 2}
                        />
                        {/* Lower wick */}
                        <line
                            x1={cx} y1={bodyBottom}
                            x2={cx} y2={wickBottom}
                            stroke={color}
                            strokeWidth={wickWidth || 2}
                        />
                        {/* Body */}
                        <rect
                            x={cx - bodyWidth / 2}
                            y={bodyTop}
                            width={bodyWidth}
                            height={bodyHeight}
                            fill={isUp ? color : color}
                            stroke={color}
                            strokeWidth={1}
                            rx={1}
                        />
                    </g>
                );
            })}
        </g>
    );
}

/**
 * Overlay plot for volume bars below candles (optional).
 * Renders semi-transparent bars scaled to a fraction of the chart height.
 */
function VolumePlot({ volumeData, labels, ohlcData, upColor, downColor, maxHeightRatio }) {
    const xScale = useXScale();
    const { left, top, width, height } = useDrawingArea();

    if (!xScale || !volumeData || volumeData.length === 0) return null;

    const bandwidth = xScale.bandwidth ? xScale.bandwidth() : (width / volumeData.length);
    const barWidth = bandwidth * 0.5;
    const maxVol = Math.max(...volumeData);
    if (maxVol === 0) return null;

    const volumeHeight = height * (maxHeightRatio || 0.2);
    const baseY = top + height;

    return (
        <g opacity={0.3}>
            {volumeData.map((vol, i) => {
                const label = labels[i];
                const xBase = xScale(label);
                if (xBase === undefined || vol === 0) return null;

                const cx = xBase + bandwidth / 2;
                const barH = (vol / maxVol) * volumeHeight;
                const isUp = ohlcData[i] && ohlcData[i].close >= ohlcData[i].open;
                const color = isUp ? (upColor || '#4caf50') : (downColor || '#f44336');

                return (
                    <rect
                        key={i}
                        x={cx - barWidth / 2}
                        y={baseY - barH}
                        width={barWidth}
                        height={barH}
                        fill={color}
                        rx={1}
                    />
                );
            })}
        </g>
    );
}

/**
 * Simple OHLC tooltip that tracks mouse position over candles.
 */
function CandleTooltip({ ohlcData, labels, tooltipEnabled }) {
    const xScale = useXScale();
    const yScale = useYScale();
    const { left, top, width, height } = useDrawingArea();
    const [hoverIndex, setHoverIndex] = useState(null);
    const tooltipRef = useRef(null);

    if (!tooltipEnabled || !xScale || !ohlcData || ohlcData.length === 0) return null;

    const bandwidth = xScale.bandwidth ? xScale.bandwidth() : (width / ohlcData.length);

    const handleMouseMove = (e) => {
        const svg = e.currentTarget.ownerSVGElement || e.currentTarget.closest('svg');
        if (!svg) return;
        const pt = svg.createSVGPoint();
        pt.x = e.clientX;
        pt.y = e.clientY;
        const svgPt = pt.matrixTransform(svg.getScreenCTM().inverse());

        if (svgPt.x < left || svgPt.x > left + width || svgPt.y < top || svgPt.y > top + height) {
            setHoverIndex(null);
            return;
        }

        // Find which band the mouse is in
        for (let i = 0; i < labels.length; i++) {
            const xBase = xScale(labels[i]);
            if (xBase !== undefined && svgPt.x >= xBase && svgPt.x < xBase + bandwidth) {
                setHoverIndex(i);
                return;
            }
        }
        setHoverIndex(null);
    };

    const handleMouseLeave = () => setHoverIndex(null);

    const d = hoverIndex !== null ? ohlcData[hoverIndex] : null;

    return (
        <>
            {/* Invisible overlay to capture mouse events */}
            <rect
                x={left} y={top} width={width} height={height}
                fill="transparent"
                onMouseMove={handleMouseMove}
                onMouseLeave={handleMouseLeave}
                style={{ pointerEvents: 'all' }}
            />
            {/* Vertical highlight line */}
            {hoverIndex !== null && (
                <line
                    x1={xScale(labels[hoverIndex]) + bandwidth / 2}
                    y1={top}
                    x2={xScale(labels[hoverIndex]) + bandwidth / 2}
                    y2={top + height}
                    stroke="rgba(128,128,128,0.4)"
                    strokeWidth={1}
                    strokeDasharray="4,4"
                    pointerEvents="none"
                />
            )}
            {/* Tooltip box */}
            {d && hoverIndex !== null && (
                <g pointerEvents="none">
                    <foreignObject
                        x={Math.min(xScale(labels[hoverIndex]) + bandwidth, left + width - 160)}
                        y={top + 8}
                        width={150}
                        height={110}
                    >
                        <div
                            ref={tooltipRef}
                            style={{
                                background: 'rgba(30,30,30,0.92)',
                                color: '#fff',
                                padding: '8px 10px',
                                borderRadius: 6,
                                fontSize: 12,
                                lineHeight: '18px',
                                fontFamily: 'system-ui, sans-serif',
                                boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
                            }}
                        >
                            <div style={{ fontWeight: 600, marginBottom: 4 }}>{labels[hoverIndex]}</div>
                            <div>O: <span style={{ color: '#90caf9' }}>{d.open}</span></div>
                            <div>H: <span style={{ color: '#81c784' }}>{d.high}</span></div>
                            <div>L: <span style={{ color: '#ef9a9a' }}>{d.low}</span></div>
                            <div>C: <span style={{ color: d.close >= d.open ? '#4caf50' : '#f44336' }}>{d.close}</span></div>
                        </div>
                    </foreignObject>
                </g>
            )}
        </>
    );
}


/**
 * CandlestickChart — Dash wrapper that renders OHLC candlestick charts
 * using MUI X Charts Pro composition API with custom SVG candle rendering.
 *
 * Supports:
 * - Array format: series[0].data = [[open, high, low, close], ...]
 * - Dataset format: dataset + series[0].datasetKeys = {open, high, low, close}
 * - Volume overlay (optional)
 * - Reference lines
 * - Grid, axes, zoom (Pro), toolbar (Pro)
 * - Click events
 */
export default function CandlestickChart(props) {
    const {
        id,
        series = [],
        dataset,
        xAxis,
        yAxis,
        height = 400,
        width,
        margin,
        grid,
        skipAnimation = false,
        hideLegend = true,
        tooltip,
        referenceLines = [],
        // Candle appearance
        bodyWidthRatio,
        wickWidth,
        // Volume
        showVolume = false,
        volumeHeightRatio,
        // Pro features
        licenseKey,
        initialZoom,
        showSlider = false,
        showToolbar = false,
        zoomInteractionConfig,
        // Dash output props
        clickData,
        hoverData,
        zoomData,
        setProps,
    } = props;

    const clipPathId = useId();

    // Set license key once globally
    if (licenseKey && !licenseKeySet) {
        LicenseInfo.setLicenseKey(licenseKey);
        licenseKeySet = true;
    }

    // --- Parse OHLC data from series/dataset ---
    const { ohlcData, labels, volumeData, upColor, downColor } = useMemo(() => {
        const seriesDef = series[0] || {};
        let parsed = [];
        let cats = [];
        let vols = [];
        const up = seriesDef.upColor || '#4caf50';
        const down = seriesDef.downColor || '#f44336';

        if (seriesDef.data && Array.isArray(seriesDef.data)) {
            // Array format: [[open, high, low, close], ...] or [{open, high, low, close}, ...]
            parsed = seriesDef.data.map(d => {
                if (Array.isArray(d)) {
                    return { open: d[0], high: d[1], low: d[2], close: d[3] };
                }
                return d;
            });
        } else if (dataset && seriesDef.datasetKeys) {
            // Dataset format
            const keys = seriesDef.datasetKeys;
            parsed = dataset.map(row => ({
                open: row[keys.open || 'open'],
                high: row[keys.high || 'high'],
                low: row[keys.low || 'low'],
                close: row[keys.close || 'close'],
            }));
        }

        // Extract labels from xAxis data, dataset, or generate indices
        if (xAxis && xAxis[0]) {
            if (xAxis[0].data) {
                cats = xAxis[0].data;
            } else if (xAxis[0].dataKey && dataset) {
                cats = dataset.map(row => row[xAxis[0].dataKey]);
            }
        }
        if (cats.length === 0) {
            cats = parsed.map((_, i) => String(i));
        }

        // Extract volume if available
        if (seriesDef.volumeKey && dataset) {
            vols = dataset.map(row => row[seriesDef.volumeKey] || 0);
        } else if (seriesDef.volume && Array.isArray(seriesDef.volume)) {
            vols = seriesDef.volume;
        }

        return { ohlcData: parsed, labels: cats, volumeData: vols, upColor: up, downColor: down };
    }, [series, dataset, xAxis]);

    // --- Compute Y-axis domain from OHLC data ---
    const computedYDomain = useMemo(() => {
        if (ohlcData.length === 0) return { min: 0, max: 100 };
        const allLows = ohlcData.map(d => d.low);
        const allHighs = ohlcData.map(d => d.high);
        const dataMin = Math.min(...allLows);
        const dataMax = Math.max(...allHighs);
        const padding = (dataMax - dataMin) * 0.05;
        return { min: dataMin - padding, max: dataMax + padding };
    }, [ohlcData]);

    // --- Zoom State (Pro) ---
    const [controlledZoom, setControlledZoom] = useState(() =>
        initialZoom && Array.isArray(initialZoom) ? initialZoom : []
    );
    const lastKnownZoomRef = useRef(JSON.stringify(initialZoom || []));

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

    // --- Click handler ---
    const handleCandleClick = useCallback((event, index, ohlc) => {
        if (setProps) {
            setProps({
                clickData: {
                    dataIndex: index,
                    label: labels[index],
                    open: ohlc.open,
                    high: ohlc.high,
                    low: ohlc.low,
                    close: ohlc.close,
                    timestamp: new Date().toISOString(),
                },
            });
        }
    }, [setProps, labels]);

    // --- Build provider props ---
    // We need a hidden bar series for MUI to correctly set up the band scale
    // and y-axis domain. The candles are rendered separately as custom SVG.
    const hiddenSeries = useMemo(() => [{
        type: 'bar',
        id: '__candle_placeholder',
        data: ohlcData.map(d => d.close),
        color: 'transparent',
        highlightScope: { highlight: 'none', fade: 'none' },
    }], [ohlcData]);

    // Build xAxis config
    const processedXAxis = useMemo(() => {
        const baseAxis = (xAxis && xAxis[0]) ? { ...xAxis[0] } : {};
        const result = {
            id: baseAxis.id || 'x-axis-candle',
            scaleType: 'band',
            data: labels,
            ...baseAxis,
        };

        if (showSlider) {
            const existingZoom = result.zoom || {};
            const zoomConfig = existingZoom === true ? {} : (typeof existingZoom === 'object' ? existingZoom : {});
            result.zoom = {
                ...zoomConfig,
                slider: { ...zoomConfig.slider, enabled: true },
            };
        }

        return [result];
    }, [xAxis, labels, showSlider]);

    // Build yAxis config with computed domain
    const processedYAxis = useMemo(() => {
        const baseAxis = (yAxis && yAxis[0]) ? { ...yAxis[0] } : {};
        return [{
            id: baseAxis.id || 'y-axis-candle',
            min: computedYDomain.min,
            max: computedYDomain.max,
            ...baseAxis,
            // User-provided min/max override computed values
            ...(baseAxis.min !== undefined ? { min: baseAxis.min } : { min: computedYDomain.min }),
            ...(baseAxis.max !== undefined ? { max: baseAxis.max } : { max: computedYDomain.max }),
        }];
    }, [yAxis, computedYDomain]);

    const providerProps = {
        height,
        series: hiddenSeries,
        xAxis: processedXAxis,
        yAxis: processedYAxis,
        onZoomChange: handleZoomChange,
    };

    if (width) providerProps.width = width;
    if (margin) providerProps.margin = margin;
    if (skipAnimation) providerProps.skipAnimation = skipAnimation;
    if (zoomInteractionConfig) providerProps.zoomInteractionConfig = zoomInteractionConfig;
    if (controlledZoom && controlledZoom.length > 0) {
        providerProps.initialZoom = controlledZoom;
    }

    const tooltipEnabled = !tooltip || tooltip.trigger !== 'none';

    return (
        <div id={id}>
            <ChartDataProviderPro {...providerProps}>
                {showToolbar && <ChartsToolbarPro />}

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

                    {/* Clipped candle area */}
                    <g clipPath={`url(#${clipPathId})`}>
                        {/* Volume bars (behind candles) */}
                        {showVolume && volumeData.length > 0 && (
                            <VolumePlot
                                volumeData={volumeData}
                                labels={labels}
                                ohlcData={ohlcData}
                                upColor={upColor}
                                downColor={downColor}
                                maxHeightRatio={volumeHeightRatio}
                            />
                        )}

                        {/* Candlestick bodies and wicks */}
                        <CandlePlot
                            ohlcData={ohlcData}
                            labels={labels}
                            upColor={upColor}
                            downColor={downColor}
                            bodyWidthRatio={bodyWidthRatio}
                            wickWidth={wickWidth}
                            onCandleClick={handleCandleClick}
                        />
                    </g>

                    {/* Axes */}
                    <ChartsXAxis />
                    <ChartsYAxis />

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

                    {/* OHLC Tooltip */}
                    <CandleTooltip
                        ohlcData={ohlcData}
                        labels={labels}
                        tooltipEnabled={tooltipEnabled}
                    />

                    {/* Zoom slider */}
                    {showSlider && <ChartZoomSlider />}
                </ChartsSurface>
            </ChartDataProviderPro>
        </div>
    );
}

CandlestickChart.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * OHLC candlestick series. Typically a single series with two data formats:
     *
     * Array format:
     *   series=[{data: [[open,high,low,close], ...], upColor: '#4caf50', downColor: '#f44336'}]
     *
     * Dataset format (use with dataset prop):
     *   series=[{datasetKeys: {open:'open', high:'high', low:'low', close:'close'},
     *            upColor: '#4caf50', downColor: '#f44336'}]
     *
     * Optional volume:
     *   series=[{..., volume: [100, 200, ...]}]  (array format)
     *   series=[{..., volumeKey: 'volume'}]       (dataset format)
     *
     * Series properties:
     * - data (array): Array of [open, high, low, close] tuples or {open, high, low, close} objects
     * - datasetKeys (object): {open, high, low, close} mapping to dataset columns
     * - upColor (string): Color when close >= open (default: '#4caf50')
     * - downColor (string): Color when close < open (default: '#f44336')
     * - volume (array): Volume values for each candle
     * - volumeKey (string): Dataset column name for volume data
     */
    series: PropTypes.arrayOf(PropTypes.object),

    /**
     * Dataset for datasetKeys mode. Array of row objects.
     * Example: [{date: '2025-01-02', open: 100, high: 110, low: 95, close: 105, volume: 1000}, ...]
     */
    dataset: PropTypes.arrayOf(PropTypes.object),

    /**
     * X-axis configuration. Typically band scale with dates/labels.
     * - data (array): Category labels (dates, day names, etc.)
     * - dataKey (string): Column from dataset for labels
     * - label (string): Axis label text
     * - scaleType (string): Always 'band' for candlestick (set automatically)
     * - zoom (object): Zoom config for Pro features
     * - tickLabelStyle (object): CSS for tick labels
     * - tickPlacement (string): 'start', 'end', 'middle', 'extremities'
     */
    xAxis: PropTypes.arrayOf(PropTypes.object),

    /**
     * Y-axis configuration for price values.
     * - label (string): Axis label (e.g., 'Price ($)')
     * - min/max (number): Override auto-computed domain from OHLC data
     * - position (string): 'left' or 'right'
     */
    yAxis: PropTypes.arrayOf(PropTypes.object),

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
     * Disable animations.
     */
    skipAnimation: PropTypes.bool,

    /**
     * Hide the legend (default: true for candlestick).
     */
    hideLegend: PropTypes.bool,

    /**
     * Tooltip configuration: {trigger: 'item'|'none'}.
     * Set trigger to 'none' to disable the OHLC tooltip.
     */
    tooltip: PropTypes.exact({
        trigger: PropTypes.oneOf(['item', 'none']),
    }),

    /**
     * Candle body width as a ratio of the band width (0-1). Default: 0.6.
     */
    bodyWidthRatio: PropTypes.number,

    /**
     * Wick (shadow) line width in pixels. Default: 2.
     */
    wickWidth: PropTypes.number,

    /**
     * Show volume bars below candles. Requires volume data in series.
     */
    showVolume: PropTypes.bool,

    /**
     * Volume bars maximum height as ratio of chart height (0-1). Default: 0.2.
     */
    volumeHeightRatio: PropTypes.number,

    /**
     * Reference lines array. Same format as BarChart/LineChart.
     */
    referenceLines: PropTypes.arrayOf(PropTypes.object),

    // --- Pro Features ---

    /**
     * MUI X Pro license key. Required for zoom, slider, and toolbar.
     */
    licenseKey: PropTypes.string,

    /**
     * Initial zoom state (Pro). Array of {axisId, start, end}.
     */
    initialZoom: PropTypes.arrayOf(PropTypes.object),

    /**
     * Show zoom range slider (Pro).
     */
    showSlider: PropTypes.bool,

    /**
     * Show toolbar (Pro).
     */
    showToolbar: PropTypes.bool,

    /**
     * Zoom interaction configuration (Pro).
     */
    zoomInteractionConfig: PropTypes.object,

    // --- Output Props ---

    /**
     * Fires on candle click. Contains: {dataIndex, label, open, high, low, close, timestamp}.
     */
    clickData: PropTypes.object,

    /**
     * Hover data output (reserved for future use).
     */
    hoverData: PropTypes.object,

    /**
     * Zoom state output (Pro).
     */
    zoomData: PropTypes.arrayOf(PropTypes.object),

    /**
     * Dash callback function.
     */
    setProps: PropTypes.func,
};
