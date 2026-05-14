/**
 * RangeBarChart — Dash wrapper for MUI X BarChartPremium with rangeBar series
 *
 * Requires Premium license. Data format: {start, end} per data point.
 * This is a STUB — Claude Code should implement the full component.
 */
import React, {useCallback, useEffect} from 'react';
import PropTypes from 'prop-types';

const RangeBarChart = (props) => {
    const {
        id,
        series,
        dataset,
        xAxis,
        yAxis,
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
        axisHighlight,
        highlightedItem,
        licenseKey,
        initialZoom,
        showSlider,
        showToolbar,
        setProps,
    } = props;

    useEffect(() => {
        if (licenseKey) {
            // TODO: LicenseInfo.setLicenseKey(licenseKey);
        }
    }, [licenseKey]);

    // Ensure all series have type: 'rangeBar'
    const processedSeries = (series || []).map(s => ({
        ...s,
        type: 'rangeBar',
    }));

    const handleItemClick = useCallback(
        (event, identifier) => {
            if (setProps) {
                setProps({
                    clickData: {
                        seriesId: identifier.seriesId,
                        dataIndex: identifier.dataIndex,
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
                setProps({axisClickData: {axisValue: data.axisValue, event_timestamp: Date.now()}});
            }
        },
        [setProps]
    );

    // TODO: Import BarChartPremium from '@mui/x-charts-premium/BarChartPremium'
    // and render with processedSeries and all other props.
    //
    // const { BarChartPremium } = require('@mui/x-charts-premium/BarChartPremium');
    // return (
    //     <div id={id}>
    //         <BarChartPremium
    //             series={processedSeries}
    //             dataset={dataset}
    //             xAxis={xAxis}
    //             yAxis={yAxis}
    //             layout={layout}
    //             borderRadius={borderRadius}
    //             height={height || 300}
    //             width={width}
    //             margin={margin}
    //             grid={grid}
    //             colors={colors}
    //             skipAnimation={skipAnimation}
    //             loading={loading}
    //             hideLegend={hideLegend}
    //             axisHighlight={axisHighlight}
    //             highlightedItem={highlightedItem}
    //             onItemClick={handleItemClick}
    //             onAxisClick={handleAxisClick}
    //             {...(showToolbar && {showToolbar})}
    //             {...(initialZoom && {initialZoom})}
    //         />
    //     </div>
    // );

    return <div id={id}>RangeBarChart placeholder</div>;
};

RangeBarChart.defaultProps = {
    series: [],
    layout: 'vertical',
    height: 300,
    loading: false,
    licenseKey: '',
};

RangeBarChart.propTypes = {
    id: PropTypes.string,

    /** Range bar series. Each: {data: [{start, end}, ...], label, color}. type:'rangeBar' is auto-set. */
    series: PropTypes.arrayOf(PropTypes.object),

    /** Dataset for dataKey mode. */
    dataset: PropTypes.arrayOf(PropTypes.object),

    xAxis: PropTypes.arrayOf(PropTypes.object),
    yAxis: PropTypes.arrayOf(PropTypes.object),

    layout: PropTypes.oneOf(['vertical', 'horizontal']),
    borderRadius: PropTypes.number,
    height: PropTypes.number,
    width: PropTypes.number,
    margin: PropTypes.oneOfType([PropTypes.number, PropTypes.object]),
    grid: PropTypes.object,
    colors: PropTypes.arrayOf(PropTypes.string),
    skipAnimation: PropTypes.bool,
    loading: PropTypes.bool,
    hideLegend: PropTypes.bool,
    axisHighlight: PropTypes.object,
    highlightedItem: PropTypes.object,

    /** Premium license key. REQUIRED. */
    licenseKey: PropTypes.string,

    initialZoom: PropTypes.arrayOf(PropTypes.object),
    showSlider: PropTypes.bool,
    showToolbar: PropTypes.bool,

    // Output
    clickData: PropTypes.object,
    axisClickData: PropTypes.object,

    setProps: PropTypes.func,
};

export default RangeBarChart;
