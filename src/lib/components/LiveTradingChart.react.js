import React, { useId, useMemo, useState, useEffect, useRef, useCallback } from 'react';
import PropTypes from 'prop-types';
import { LicenseInfo } from '@mui/x-license';
import { ChartDataProviderPro } from '@mui/x-charts-pro/ChartDataProviderPro';
import { ChartsSurface } from '@mui/x-charts-pro/ChartsSurface';
import { ChartsXAxis } from '@mui/x-charts-pro/ChartsXAxis';
import { ChartsYAxis } from '@mui/x-charts-pro/ChartsYAxis';
import { ChartsGrid } from '@mui/x-charts-pro/ChartsGrid';
import { ChartsTooltip } from '@mui/x-charts-pro/ChartsTooltip';
import { ChartsAxisHighlight } from '@mui/x-charts-pro/ChartsAxisHighlight';
import { ChartsClipPath } from '@mui/x-charts-pro/ChartsClipPath';
import { ChartsReferenceLine } from '@mui/x-charts-pro/ChartsReferenceLine';
import { ChartZoomSlider } from '@mui/x-charts-pro/ChartZoomSlider';
import { useDrawingArea, useXScale, useYScale } from '@mui/x-charts/hooks';

let licenseKeySet = false;

// ---------------------------------------------------------------------------
// resolveFunctionProp — DMC-pattern function-as-prop resolver
// ---------------------------------------------------------------------------
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

// ---------------------------------------------------------------------------
// Seeded PRNG (mulberry32)
// ---------------------------------------------------------------------------
function createSeededRng(seed) {
    let state = seed | 0;
    return {
        next() {
            state = (state + 0x6D2B79F5) | 0;
            let t = Math.imul(state ^ (state >>> 15), 1 | state);
            t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
            return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
        },
        nextGaussian() {
            const u1 = this.next() || 0.0001;
            const u2 = this.next();
            return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
        },
    };
}

// ---------------------------------------------------------------------------
// Generate one OHLCV candle from previous close
// ---------------------------------------------------------------------------
function generateCandle(prevClose, rng, vol, dft) {
    const open = prevClose;
    const r1 = rng.nextGaussian() * vol;
    const r2 = rng.nextGaussian() * vol;
    const r3 = rng.nextGaussian() * vol;
    const close = Math.max(0.01, open * Math.exp(dft + r1));
    const high = Math.max(open, close) * (1 + Math.abs(r2) * 0.4);
    const low = Math.min(open, close) * (1 - Math.abs(r3) * 0.4);
    const volume = Math.max(50, Math.round(800 + rng.nextGaussian() * 400 + Math.abs(r1) * 3000));
    return { open, high, low, close, volume };
}

// ---------------------------------------------------------------------------
// CandlestickPlot — renders candle bodies + wicks using MUI hooks
// ---------------------------------------------------------------------------
function CandlestickPlot({ candles, upColor, downColor, totalSlots }) {
    const { width: drawWidth } = useDrawingArea();
    const xScale = useXScale();
    const yScale = useYScale();

    if (!candles || candles.length === 0) return null;

    const slotWidth = drawWidth / Math.max(totalSlots, 1);
    const bodyWidth = Math.max(1, slotWidth * 0.6);
    const wickWidth = Math.max(0.5, slotWidth * 0.06);

    return (
        <g>
            {candles.map((c, i) => {
                const cx = xScale(i);
                if (cx === undefined) return null;
                const isUp = c.close >= c.open;
                const color = isUp ? upColor : downColor;
                const yHigh = yScale(c.high);
                const yLow = yScale(c.low);
                const yOpen = yScale(c.open);
                const yClose = yScale(c.close);
                if ([yHigh, yLow, yOpen, yClose].some(v => v === undefined)) return null;

                const bodyTop = Math.min(yOpen, yClose);
                const bodyHeight = Math.max(1, Math.abs(yOpen - yClose));

                return (
                    <g key={`candle-${i}`}>
                        {/* Wick */}
                        <line
                            x1={cx} y1={yHigh} x2={cx} y2={yLow}
                            stroke={color} strokeWidth={wickWidth}
                        />
                        {/* Body */}
                        <rect
                            x={cx - bodyWidth / 2}
                            y={bodyTop}
                            width={bodyWidth}
                            height={bodyHeight}
                            fill={isUp ? color : color}
                            stroke={color}
                            strokeWidth={0.5}
                        />
                    </g>
                );
            })}
        </g>
    );
}

// ---------------------------------------------------------------------------
// VolumeBars — renders volume bars in the bottom portion of the drawing area
// ---------------------------------------------------------------------------
function VolumeBars({ candles, upColor, downColor, totalSlots, volumeHeightPct }) {
    const { top, height: drawHeight, width: drawWidth } = useDrawingArea();
    const xScale = useXScale();

    if (!candles || candles.length === 0) return null;

    const maxVol = Math.max(...candles.map(c => c.volume), 1);
    const volZoneHeight = drawHeight * (volumeHeightPct / 100);
    const volZoneTop = top + drawHeight - volZoneHeight;
    const slotWidth = drawWidth / Math.max(totalSlots, 1);
    const barWidth = Math.max(1, slotWidth * 0.55);

    return (
        <g opacity={0.35}>
            {candles.map((c, i) => {
                const cx = xScale(i);
                if (cx === undefined) return null;
                const isUp = c.close >= c.open;
                const barH = (c.volume / maxVol) * volZoneHeight;
                return (
                    <rect
                        key={`vol-${i}`}
                        x={cx - barWidth / 2}
                        y={volZoneTop + volZoneHeight - barH}
                        width={barWidth}
                        height={barH}
                        fill={isUp ? upColor : downColor}
                    />
                );
            })}
        </g>
    );
}

// ---------------------------------------------------------------------------
// PriceLabels — shows close price above/below select candles
// ---------------------------------------------------------------------------
function PriceLabels({ candles, labelInterval }) {
    const xScale = useXScale();
    const yScale = useYScale();

    if (!candles || candles.length === 0) return null;

    const interval = labelInterval || Math.max(1, Math.floor(candles.length / 8));

    return (
        <g>
            {candles.map((c, i) => {
                if (i % interval !== 0 && i !== candles.length - 1) return null;
                const cx = xScale(i);
                const cy = yScale(c.close);
                if (cx === undefined || cy === undefined) return null;
                const isUp = c.close >= c.open;
                const color = isUp ? '#4caf50' : '#f44336';

                return (
                    <g key={`label-${i}`}>
                        <circle cx={cx} cy={cy} r={3} fill={color} />
                        <text
                            x={cx}
                            y={cy - 10}
                            textAnchor="middle"
                            fill={color}
                            fontSize={10}
                            fontWeight="bold"
                        >
                            {c.close.toFixed(1)}
                        </text>
                    </g>
                );
            })}
        </g>
    );
}

// ---------------------------------------------------------------------------
// ForecastOverlay — dashed line + shaded uncertainty area
// ---------------------------------------------------------------------------
function ForecastOverlay({ forecastData, upperBound, lowerBound, startIndex, color, opacity }) {
    const xScale = useXScale();
    const yScale = useYScale();

    if (!forecastData || forecastData.length === 0) return null;

    const pts = [];
    for (let i = 0; i < forecastData.length; i++) {
        const x = xScale(startIndex + i);
        const y = yScale(forecastData[i]);
        const yUp = yScale(upperBound[i]);
        const yLo = yScale(lowerBound[i]);
        if (x === undefined || y === undefined) continue;
        pts.push({ x, y, yUp, yLo });
    }
    if (pts.length === 0) return null;

    let linePath = `M ${pts[0].x} ${pts[0].y}`;
    for (let i = 1; i < pts.length; i++) linePath += ` L ${pts[i].x} ${pts[i].y}`;

    let areaPath = `M ${pts[0].x} ${pts[0].yUp}`;
    for (let i = 1; i < pts.length; i++) areaPath += ` L ${pts[i].x} ${pts[i].yUp}`;
    for (let i = pts.length - 1; i >= 0; i--) areaPath += ` L ${pts[i].x} ${pts[i].yLo}`;
    areaPath += ' Z';

    return (
        <g>
            <path d={areaPath} fill={color} fillOpacity={opacity} />
            <path d={linePath} stroke={color} strokeWidth={2} strokeDasharray="6 4" fill="none" />
        </g>
    );
}

// ---------------------------------------------------------------------------
// AlertMarks — badges on significant price moves
// ---------------------------------------------------------------------------
function AlertMarks({ alerts, alertUpColor, alertDownColor, formatterFn }) {
    const xScale = useXScale();
    const yScale = useYScale();

    if (!alerts || alerts.length === 0) return null;

    return (
        <g>
            {alerts.map((alert, i) => {
                const x = xScale(alert.displayIndex);
                const y = yScale(alert.price);
                if (x === undefined || y === undefined) return null;
                const isUp = alert.type === 'up';
                const bgColor = isUp ? alertUpColor : alertDownColor;
                const labelText = formatterFn
                    ? formatterFn(alert, { index: i })
                    : `${isUp ? '+' : ''}${alert.pctChange.toFixed(1)}%`;
                const labelWidth = labelText.length * 7 + 10;

                return (
                    <g key={`alert-${i}`}>
                        <rect
                            x={x - labelWidth / 2}
                            y={isUp ? y - 32 : y + 10}
                            width={labelWidth}
                            height={18}
                            rx={4}
                            fill={bgColor}
                        />
                        <text
                            x={x} y={isUp ? y - 19 : y + 23}
                            textAnchor="middle" fill="white"
                            fontSize={10} fontWeight="bold"
                        >
                            {labelText}
                        </text>
                        <circle cx={x} cy={y} r={4} fill={bgColor} stroke="white" strokeWidth={1.5} />
                    </g>
                );
            })}
        </g>
    );
}

// ---------------------------------------------------------------------------
// ShadedBackground — forecast zone shading
// ---------------------------------------------------------------------------
function ShadedBackground({ startIndex, endIndex }) {
    const { top, bottom, height } = useDrawingArea();
    const xScale = useXScale();

    const x1 = xScale(startIndex);
    const x2 = xScale(endIndex);
    if (x1 === undefined || x2 === undefined) return null;

    return (
        <rect
            x={x1} y={0}
            width={x2 - x1}
            height={top + height + bottom}
            fill="#9e9e9e" opacity={0.08}
        />
    );
}

// ---------------------------------------------------------------------------
// LiveTradingChart component
// ---------------------------------------------------------------------------
/**
 * LiveTradingChart simulates real-time candlestick trading data with volume bars,
 * forecast line with uncertainty bands, alert labels, and optional price labels.
 * Uses an internal React timer for smooth high-speed updates.
 */
export default function LiveTradingChart(props) {
    const {
        id,
        licenseKey,
        height = 500,
        width,
        margin,
        windowSize = 60,
        forecastSize = 15,
        running = false,
        intervalMs = 300,
        seed = 42,
        resetTrigger = 0,
        initialPrice = 100,
        volatility = 0.02,
        drift = 0.001,
        forecastVolatility = 1.5,
        alertProbability = 0.08, // legacy — unused by default swing detection
        alertThresholdPct = 2.0, // legacy — unused by default swing detection
        alertLookback = 5,
        alertMinDistance = 10,
        maxVisibleAlerts = 6,
        alertFilter,
        alertFormatter,
        candleUpColor = '#4caf50',
        candleDownColor = '#f44336',
        forecastColor = '#ff9800',
        alertUpColor = '#4caf50',
        alertDownColor = '#f44336',
        uncertaintyOpacity = 0.15,
        showVolume = true,
        showLabels = false,
        volumeHeightPct = 20,
        showGrid = true,
        showSlider = false,
        hideLegend = true,
        grid,
        xAxisLabel = 'Tick',
        yAxisLabel = 'Price',
        // Dash outputs
        currentPrice,
        tickCount,
        alertHistory,
        zoomData,
        setProps,
    } = props;

    if (licenseKey && !licenseKeySet) {
        LicenseInfo.setLicenseKey(licenseKey);
        licenseKeySet = true;
    }

    const chartId = useId();
    const clipPathId = `${chartId}-clip`;

    // Mutable simulation state
    const rngRef = useRef(createSeededRng(seed));
    const candleBufferRef = useRef([]);
    const alertBufferRef = useRef([]);
    const intervalRef = useRef(null);
    const lastResetRef = useRef(resetTrigger);

    // Initialize with first candle
    useEffect(() => {
        if (candleBufferRef.current.length === 0) {
            candleBufferRef.current = [{
                open: initialPrice, high: initialPrice * 1.005,
                low: initialPrice * 0.995, close: initialPrice,
                volume: 500,
            }];
        }
    }, [initialPrice]);

    // Display state
    const [displayData, setDisplayData] = useState({
        candles: [],
        forecast: [],
        upperBound: [],
        lowerBound: [],
        alerts: [],
        forecastStartIndex: 0,
    });

    // Generate forecast from close price
    const generateForecast = useCallback((lastClose, rng, numPoints) => {
        const forecast = [];
        const upper = [];
        const lower = [];
        let price = lastClose;
        let cumUncertainty = 0;
        for (let i = 0; i < numPoints; i++) {
            const shock = rng.nextGaussian() * volatility * 0.5;
            price = price * Math.exp(drift + shock);
            cumUncertainty += volatility * forecastVolatility * lastClose;
            forecast.push(price);
            upper.push(price + cumUncertainty * 0.5);
            lower.push(price - cumUncertainty * 0.5);
        }
        return { forecast, upper, lower };
    }, [volatility, drift, forecastVolatility]);

    // Reset
    useEffect(() => {
        if (resetTrigger !== lastResetRef.current) {
            lastResetRef.current = resetTrigger;
            rngRef.current = createSeededRng(seed);
            candleBufferRef.current = [{
                open: initialPrice, high: initialPrice * 1.005,
                low: initialPrice * 0.995, close: initialPrice,
                volume: 500,
            }];
            alertBufferRef.current = [];
            setDisplayData({
                candles: candleBufferRef.current.slice(),
                forecast: [], upperBound: [], lowerBound: [],
                alerts: [], forecastStartIndex: 0,
            });
            if (setProps) {
                setProps({ currentPrice: initialPrice, tickCount: 0, alertHistory: [] });
            }
        }
    }, [resetTrigger, seed, initialPrice, setProps]);

    // Main simulation loop
    useEffect(() => {
        if (!running) {
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
                intervalRef.current = null;
            }
            return;
        }

        intervalRef.current = setInterval(() => {
            const buf = candleBufferRef.current;
            const prevClose = buf.length > 0 ? buf[buf.length - 1].close : initialPrice;
            const candle = generateCandle(prevClose, rngRef.current, volatility, drift);
            buf.push(candle);

            // Alert check — deferred swing-point detection
            // Evaluate the candle alertLookback ticks ago (it now has enough
            // future context to confirm whether it's a local extreme)
            const candidateIdx = buf.length - 1 - alertLookback;
            if (candidateIdx >= alertLookback) {
                const candidate = buf[candidateIdx];
                const alertFilterFn = resolveFunctionProp(alertFilter);
                let alertType = null;

                if (alertFilterFn) {
                    // Custom filter via functions-as-props
                    const result = alertFilterFn(buf, candidateIdx, { lookback: alertLookback });
                    if (result === true) {
                        alertType = candidate.close >= candidate.open ? 'up' : 'down';
                    } else if (result === 'up' || result === 'down') {
                        alertType = result;
                    }
                } else {
                    // Built-in swing high/low detection
                    const rangeStart = Math.max(0, candidateIdx - alertLookback);
                    const rangeEnd = Math.min(buf.length - 1, candidateIdx + alertLookback);
                    let isSwingHigh = true;
                    let isSwingLow = true;

                    for (let j = rangeStart; j <= rangeEnd; j++) {
                        if (j === candidateIdx) continue;
                        if (buf[j].high > candidate.high) isSwingHigh = false;
                        if (buf[j].low < candidate.low) isSwingLow = false;
                        if (!isSwingHigh && !isSwingLow) break;
                    }

                    if (isSwingHigh && isSwingLow) {
                        alertType = candidate.close >= candidate.open ? 'up' : 'down';
                    } else if (isSwingHigh) {
                        alertType = 'up';
                    } else if (isSwingLow) {
                        alertType = 'down';
                    }
                }

                // Enforce minimum distance between alerts
                const lastAlertTick = alertBufferRef.current.length > 0
                    ? alertBufferRef.current[alertBufferRef.current.length - 1].tick
                    : -Infinity;

                if (alertType && (candidateIdx - lastAlertTick >= alertMinDistance)) {
                    const pctChange = ((candidate.close - candidate.open) / candidate.open) * 100;
                    alertBufferRef.current.push({
                        tick: candidateIdx,
                        price: alertType === 'up' ? candidate.high : candidate.low,
                        type: alertType,
                        pctChange,
                        message: `${alertType === 'up' ? '+' : ''}${pctChange.toFixed(2)}%`,
                    });
                }
            }

            // Window
            const windowStart = Math.max(0, buf.length - windowSize);
            const windowed = buf.slice(windowStart);

            // Forecast
            const { forecast, upper, lower } = generateForecast(
                candle.close, createSeededRng(seed + buf.length), forecastSize
            );

            // Visible alerts (capped to maxVisibleAlerts, keeping most significant)
            let visibleAlerts = alertBufferRef.current
                .filter(a => a.tick >= windowStart && a.tick < windowStart + windowSize)
                .map(a => ({ ...a, displayIndex: a.tick - windowStart }));

            if (visibleAlerts.length > maxVisibleAlerts) {
                visibleAlerts.sort((a, b) => Math.abs(b.pctChange) - Math.abs(a.pctChange));
                visibleAlerts = visibleAlerts.slice(0, maxVisibleAlerts);
                visibleAlerts.sort((a, b) => a.displayIndex - b.displayIndex);
            }

            setDisplayData({
                candles: windowed,
                forecast, upperBound: upper, lowerBound: lower,
                alerts: visibleAlerts,
                forecastStartIndex: windowed.length - 1,
            });

            if (setProps) {
                const update = {
                    currentPrice: Math.round(candle.close * 100) / 100,
                    tickCount: buf.length,
                };
                if (alertBufferRef.current.length !== (alertHistory || []).length) {
                    update.alertHistory = alertBufferRef.current.slice(-50);
                }
                setProps(update);
            }
        }, intervalMs);

        return () => {
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
                intervalRef.current = null;
            }
        };
    }, [running, intervalMs, volatility, drift, generateForecast, windowSize, forecastSize,
        alertProbability, alertThresholdPct, alertLookback, alertMinDistance, maxVisibleAlerts,
        alertFilter, seed, initialPrice, setProps]);

    // Build axis data and hidden line series for domain/tooltip
    const { series, xAxisData, yDomain, forecastStartIdx } = useMemo(() => {
        const candles = displayData.candles;
        const totalLen = candles.length + displayData.forecast.length;
        const xData = Array.from({ length: totalLen }, (_, i) => i);

        // Close prices for tooltip (actual candles + null for forecast zone)
        const closeData = [
            ...candles.map(c => c.close),
            ...Array(displayData.forecast.length).fill(null),
        ];

        // Compute y domain from candle highs/lows + forecast bounds
        const allValues = [
            ...candles.flatMap(c => [c.high, c.low]),
            ...displayData.forecast,
            ...displayData.upperBound,
            ...displayData.lowerBound,
        ].filter(v => v != null && isFinite(v));

        let yMin = 0, yMax = 200;
        if (allValues.length > 0) {
            yMin = Math.min(...allValues);
            yMax = Math.max(...allValues);
            const pad = (yMax - yMin) * 0.12 || 5;
            yMin -= pad;
            yMax += pad;
        }

        return {
            series: [{
                type: 'line',
                id: 'close',
                label: 'Close',
                data: closeData,
                color: '#9e9e9e',
                showMark: false,
                connectNulls: false,
            }],
            xAxisData: xData,
            yDomain: { min: yMin, max: yMax },
            forecastStartIdx: candles.length - 1,
        };
    }, [displayData]);

    // Zoom change handler
    const handleZoomChange = (newZoom) => {
        if (setProps) {
            setProps({ zoomData: newZoom });
        }
    };

    const xAxisConfig = {
        id: 'x-axis',
        data: xAxisData,
        scaleType: 'linear',
        tickLabelStyle: { fontSize: 11 },
    };
    if (showSlider) {
        xAxisConfig.zoom = {
            minSpan: 10,
            panning: true,
            filterMode: 'discard',
            slider: { enabled: true, preview: true },
        };
    }

    const providerProps = {
        height,
        series,
        skipAnimation: true,
        xAxis: [xAxisConfig],
        yAxis: [{
            id: 'y-axis',
            label: yAxisLabel,
            width: 65,
            min: yDomain.min,
            max: yDomain.max,
            tickLabelStyle: { fontSize: 11 },
        }],
        onZoomChange: handleZoomChange,
    };
    if (width) providerProps.width = width;
    if (margin) providerProps.margin = margin;

    const totalSlots = xAxisData.length;
    const candles = displayData.candles;
    const lastClose = candles.length > 0 ? candles[candles.length - 1].close : initialPrice;

    return (
        <div id={id}>
            <ChartDataProviderPro {...providerProps}>
                <ChartsSurface>
                    {/* Grid */}
                    {(showGrid || grid) && (
                        <ChartsGrid
                            horizontal={grid?.horizontal ?? true}
                            vertical={grid?.vertical ?? false}
                        />
                    )}

                    <ChartsClipPath id={clipPathId} />

                    <g clipPath={`url(#${clipPathId})`}>
                        {/* Forecast zone shading */}
                        {displayData.forecast.length > 0 && (
                            <ShadedBackground
                                startIndex={forecastStartIdx}
                                endIndex={xAxisData.length - 1}
                            />
                        )}

                        {/* Volume bars (behind candles) */}
                        {showVolume && (
                            <VolumeBars
                                candles={candles}
                                upColor={candleUpColor}
                                downColor={candleDownColor}
                                totalSlots={totalSlots}
                                volumeHeightPct={volumeHeightPct}
                            />
                        )}

                        {/* Candlestick plot */}
                        <CandlestickPlot
                            candles={candles}
                            upColor={candleUpColor}
                            downColor={candleDownColor}
                            totalSlots={totalSlots}
                        />

                        {/* Forecast overlay */}
                        {displayData.forecast.length > 0 && (
                            <ForecastOverlay
                                forecastData={[lastClose, ...displayData.forecast]}
                                upperBound={[lastClose, ...displayData.upperBound]}
                                lowerBound={[lastClose, ...displayData.lowerBound]}
                                startIndex={forecastStartIdx}
                                color={forecastColor}
                                opacity={uncertaintyOpacity}
                            />
                        )}
                    </g>

                    {/* Price labels (outside clip so text isn't cut) */}
                    {showLabels && (
                        <PriceLabels candles={candles} />
                    )}

                    {/* Alert marks */}
                    <AlertMarks
                        alerts={displayData.alerts}
                        alertUpColor={alertUpColor}
                        alertDownColor={alertDownColor}
                        formatterFn={resolveFunctionProp(alertFormatter)}
                    />

                    {/* Axes */}
                    <ChartsXAxis axisId="x-axis" label={xAxisLabel} />
                    <ChartsYAxis axisId="y-axis" />

                    <ChartsAxisHighlight x="line" y="none" />

                    {/* Open price reference line */}
                    <ChartsReferenceLine
                        y={initialPrice}
                        label="Open"
                        lineStyle={{ stroke: '#9e9e9e', strokeDasharray: '4 4', strokeWidth: 1 }}
                        labelStyle={{ fill: '#9e9e9e', fontSize: 11 }}
                        labelAlign="start"
                    />
                    {/* Zoom slider */}
                    {showSlider && <ChartZoomSlider />}
                </ChartsSurface>

                <ChartsTooltip trigger="axis" />
            </ChartDataProviderPro>
        </div>
    );
}

LiveTradingChart.propTypes = {
    /** The ID used to identify this component in Dash callbacks. */
    id: PropTypes.string,
    /** MUI X Pro license key. */
    licenseKey: PropTypes.string,
    /** Chart height in pixels. Default 500. */
    height: PropTypes.number,
    /** Chart width in pixels. If not set, fills available space. */
    width: PropTypes.number,
    /** Chart margins. */
    margin: PropTypes.shape({
        top: PropTypes.number,
        right: PropTypes.number,
        bottom: PropTypes.number,
        left: PropTypes.number,
    }),
    /** Number of visible candles in the sliding window. Default 60. */
    windowSize: PropTypes.number,
    /** Number of forecast points beyond the window. Default 15. */
    forecastSize: PropTypes.number,
    /** Whether the simulation is running. Default false. */
    running: PropTypes.bool,
    /** Tick interval in milliseconds. Default 300. */
    intervalMs: PropTypes.number,
    /** RNG seed for reproducible randomness. Default 42. */
    seed: PropTypes.number,
    /** Increment this to reset the simulation. */
    resetTrigger: PropTypes.number,
    /** Starting price. Default 100. */
    initialPrice: PropTypes.number,
    /** Price volatility factor. Default 0.02. */
    volatility: PropTypes.number,
    /** Price drift/trend factor. Default 0.001. */
    drift: PropTypes.number,
    /** Forecast uncertainty multiplier. Default 1.5. */
    forecastVolatility: PropTypes.number,
    /** (Legacy) Probability of alert per tick — unused by default swing detection. */
    alertProbability: PropTypes.number,
    /** (Legacy) Minimum % change to flag as alert — unused by default swing detection. */
    alertThresholdPct: PropTypes.number,
    /** Number of candles on each side to confirm a swing high/low. Default 5. */
    alertLookback: PropTypes.number,
    /** Minimum ticks between consecutive alerts to prevent clustering. Default 10. */
    alertMinDistance: PropTypes.number,
    /** Maximum number of alert labels visible in the window. Default 6. */
    maxVisibleAlerts: PropTypes.number,
    /** Functions-as-props: custom alert detection. {function: 'name', options: {...}} */
    alertFilter: PropTypes.shape({
        function: PropTypes.string.isRequired,
        options: PropTypes.object,
    }),
    /** Functions-as-props: custom alert label formatting. {function: 'name', options: {...}} */
    alertFormatter: PropTypes.shape({
        function: PropTypes.string.isRequired,
        options: PropTypes.object,
    }),
    /** Candle color for upward (close >= open) moves. Default '#4caf50'. */
    candleUpColor: PropTypes.string,
    /** Candle color for downward (close < open) moves. Default '#f44336'. */
    candleDownColor: PropTypes.string,
    /** Forecast line/area color. Default '#ff9800'. */
    forecastColor: PropTypes.string,
    /** Alert label color for upward moves. Default '#4caf50'. */
    alertUpColor: PropTypes.string,
    /** Alert label color for downward moves. Default '#f44336'. */
    alertDownColor: PropTypes.string,
    /** Opacity of the forecast uncertainty shaded area. Default 0.15. */
    uncertaintyOpacity: PropTypes.number,
    /** Show volume bars. Default true. */
    showVolume: PropTypes.bool,
    /** Show price labels on candles. Default false. */
    showLabels: PropTypes.bool,
    /** Volume bars height as percentage of chart area. Default 20. */
    volumeHeightPct: PropTypes.number,
    /** Show grid lines. Default true. */
    showGrid: PropTypes.bool,
    /** Show zoom slider below the chart (Pro). Default false. */
    showSlider: PropTypes.bool,
    /** Hide the legend. Default true. */
    hideLegend: PropTypes.bool,
    /** Grid configuration. */
    grid: PropTypes.shape({
        horizontal: PropTypes.bool,
        vertical: PropTypes.bool,
    }),
    /** X-axis label text. Default 'Tick'. */
    xAxisLabel: PropTypes.string,
    /** Y-axis label text. Default 'Price'. */
    yAxisLabel: PropTypes.string,
    /** Current price (read-only output). */
    currentPrice: PropTypes.number,
    /** Total ticks elapsed (read-only output). */
    tickCount: PropTypes.number,
    /** Recent alert history (read-only output). */
    alertHistory: PropTypes.array,
    /** Current zoom state (read-only output). */
    zoomData: PropTypes.arrayOf(PropTypes.shape({
        axisId: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
        start: PropTypes.number,
        end: PropTypes.number,
    })),
    /** Dash-assigned callback for reporting property changes. */
    setProps: PropTypes.func,
};