/**
 * CandlestickChart — Dash wrapper for MUI X CandlestickChart (Premium Preview)
 *
 * Static OHLC candlestick chart. NOT the same as LiveTradingChart (which is a
 * real-time client-side simulation). This wraps MUI's native candlestick component.
 *
 * Requires Premium license.
 * This is a STUB — Claude Code should implement the full component.
 */
import React, {useCallback, useEffect} from 'react';
import PropTypes from 'prop-types';

const CandlestickChart = (props) => {
    const {
        id,
        series,
        dataset,
        xAxis,
        yAxis,
        height,
        width,
        margin,
        grid,
        skipAnimation,
        showToolbar,
        licenseKey,
        setProps,
    } = props;

    useEffect(() => {
        if (licenseKey) {
            // TODO: LicenseInfo.setLicenseKey(licenseKey);
        }
    }, [licenseKey]);

    const handleItemClick = useCallback(
        (event, identifier) => {
            if (setProps) {
                setProps({
                    clickData: {
                        dataIndex: identifier.dataIndex,
                        event_timestamp: Date.now(),
                    },
                });
            }
        },
        [setProps]
    );

    // TODO: Import CandlestickChart from '@mui/x-charts-premium'
    // Note: CandlestickPlot uses WebGL — renders in ChartsWebGLLayer
    //
    // const { CandlestickChart: MuiCandlestickChart } = require('@mui/x-charts-premium');
    // return (
    //     <div id={id}>
    //         <MuiCandlestickChart
    //             series={series || []}
    //             dataset={dataset}
    //             xAxis={xAxis}
    //             yAxis={yAxis}
    //             height={height || 400}
    //             width={width}
    //             margin={margin}
    //             grid={grid}
    //             skipAnimation={skipAnimation}
    //             {...(showToolbar && {showToolbar})}
    //             onItemClick={handleItemClick}
    //         />
    //     </div>
    // );

    return <div id={id}>CandlestickChart placeholder</div>;
};

CandlestickChart.defaultProps = {
    series: [],
    height: 400,
    licenseKey: '',
};

CandlestickChart.propTypes = {
    id: PropTypes.string,

    /**
     * OHLC series. Two formats:
     * 1. Array: {data: [[open, high, low, close], ...], upColor, downColor}
     * 2. Dataset: {datasetKeys: {open, high, low, close}, upColor, downColor}
     */
    series: PropTypes.arrayOf(PropTypes.object),

    /** Dataset for datasetKeys mode. [{date, open, high, low, close, volume?}, ...] */
    dataset: PropTypes.arrayOf(PropTypes.object),

    /** X-axis config. Band scale with dates/labels. Supports zoom. */
    xAxis: PropTypes.arrayOf(PropTypes.object),

    /** Y-axis config. [{label, valueFormatter}] */
    yAxis: PropTypes.arrayOf(PropTypes.object),

    /** Chart height in pixels. */
    height: PropTypes.number,

    /** Chart width in pixels. */
    width: PropTypes.number,

    /** Chart margins {top, bottom, left, right}. */
    margin: PropTypes.object,

    /** Grid lines: {horizontal, vertical}. */
    grid: PropTypes.object,

    /** Disable animations. */
    skipAnimation: PropTypes.bool,

    /** Show toolbar. */
    showToolbar: PropTypes.bool,

    /** Premium license key. REQUIRED. */
    licenseKey: PropTypes.string,

    // Output
    /** Fired on candle click. {dataIndex, event_timestamp} */
    clickData: PropTypes.object,

    setProps: PropTypes.func,
};

export default CandlestickChart;
