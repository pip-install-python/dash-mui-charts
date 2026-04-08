/**
 * Functions-as-props registry for dash-mui-charts.
 * Mirrors the Dash Mantine Components pattern (dashMantineFunctions).
 *
 * Usage from Python:
 *   xAxis=[{
 *       'scaleType': 'time',
 *       'valueFormatter': {
 *           'function': 'formatDate',
 *           'options': {'format': 'M/d HH:mm', 'tickFormat': 'M/d'},
 *       },
 *   }]
 *
 * Options:
 *   format     - Format for tooltips (default: 'M/d')
 *   tickFormat - Shorter format for axis tick labels (default: same as format)
 *
 * Supported tokens:
 *   YYYY - 4-digit year        (2025)
 *   MMM  - abbreviated month   (Jan, Feb, ...)
 *   MM   - 2-digit month       (01-12)
 *   M    - month               (1-12)
 *   dd   - 2-digit day         (01-31)
 *   d    - day                 (1-31)
 *   HH   - 2-digit hour 24h   (00-23)
 *   mm   - 2-digit minute      (00-59)
 */
var dmcf = window.dashMuiChartsFunctions = window.dashMuiChartsFunctions || {};

dmcf.formatDate = function(value, context, options) {
    var dt = value instanceof Date ? value : new Date(value);
    var pad = function(n) { return n < 10 ? '0' + n : '' + n; };
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

    // Use tickFormat for tick labels, full format for tooltips
    var fmt;
    if (context && context.location === 'tick' && options && options.tickFormat) {
        fmt = options.tickFormat;
    } else {
        fmt = (options && options.format) || 'M/d';
    }

    return fmt.replace(/YYYY|MMM|MM|dd|HH|mm|M|d/g, function(token) {
        switch(token) {
            case 'YYYY': return dt.getFullYear();
            case 'MMM':  return months[dt.getMonth()];
            case 'MM':   return pad(dt.getMonth() + 1);
            case 'M':    return dt.getMonth() + 1;
            case 'dd':   return pad(dt.getDate());
            case 'd':    return dt.getDate();
            case 'HH':   return pad(dt.getHours());
            case 'mm':   return pad(dt.getMinutes());
            default:     return token;
        }
    });
};

// ---------------------------------------------------------------------------
// swingAlertFilter — detect swing high/low points in live candle data
// ---------------------------------------------------------------------------
// Usage from Python:
//   alertFilter={'function': 'swingAlertFilter', 'options': {'lookback': 7}}
//
// Called with (candles, candidateIndex, context, options) where:
//   candles        - full candle buffer array [{open, high, low, close, volume}, ...]
//   candidateIndex - index of the candle being evaluated
//   context        - {lookback: N} from the component
//   options        - user-supplied options from Python
//
// Returns 'up' for swing high, 'down' for swing low, null otherwise.
dmcf.swingAlertFilter = function(candles, candidateIndex, context, options) {
    var lookback = (options && options.lookback) || (context && context.lookback) || 5;
    var candidate = candles[candidateIndex];
    if (!candidate) return null;

    var rangeStart = Math.max(0, candidateIndex - lookback);
    var rangeEnd = Math.min(candles.length - 1, candidateIndex + lookback);
    var isHigh = true;
    var isLow = true;

    for (var j = rangeStart; j <= rangeEnd; j++) {
        if (j === candidateIndex) continue;
        if (candles[j].high > candidate.high) isHigh = false;
        if (candles[j].low < candidate.low) isLow = false;
        if (!isHigh && !isLow) break;
    }

    if (isHigh && isLow) {
        // Rare: candle is both highest and lowest — pick by body direction
        return candidate.close >= candidate.open ? 'up' : 'down';
    }
    if (isHigh) return 'up';
    if (isLow) return 'down';
    return null;
};

// ---------------------------------------------------------------------------
// priceAlertFormatter — format alert labels as price instead of percentage
// ---------------------------------------------------------------------------
// Usage from Python:
//   alertFormatter={'function': 'priceAlertFormatter', 'options': {'decimals': 2}}
//
// Called with (alert, context, options) where:
//   alert   - {tick, price, type, pctChange, message}
//   context - {index: i} rendering context
//   options - user-supplied options from Python
//
// Returns a formatted label string like "▲ $102.45" or "▼ $97.80".
dmcf.priceAlertFormatter = function(alert, context, options) {
    var prefix = alert.type === 'up' ? '\u25B2 ' : '\u25BC ';
    var decimals = (options && options.decimals) || 2;
    return prefix + '$' + alert.price.toFixed(decimals);
};