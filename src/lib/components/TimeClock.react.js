/**
 * TimeClock — Dash wrapper for MUI X TimeClock (@mui/x-date-pickers, Community)
 *
 * An inline time selector (no input / popper / modal). The user drags the clock
 * hand or clicks the numbers to pick hours, minutes, and optionally seconds.
 *
 * Dash boundary contract
 * ----------------------
 * dayjs objects cannot cross the Dash <-> Python boundary, so `value` and
 * `defaultValue` are exchanged as plain strings:
 *   - Full wall-time ISO    : "2022-04-17T15:30:00"
 *   - Time-only             : "15:30" or "15:30:45"
 * On every change the component pushes back `value` (full wall-time ISO string),
 * the current `view`, and a convenience `timeData` object — so a callback can use
 * the parsed parts without re-parsing the string.
 *
 * MUI components inside this wrapper follow the Mantine color scheme on <html>,
 * so the clock re-skins automatically in dark mode (same approach as TreeViewPro).
 */
import React, {useCallback, useEffect, useMemo, useState} from 'react';
import PropTypes from 'prop-types';
import dayjs from 'dayjs';
import {LocalizationProvider} from '@mui/x-date-pickers/LocalizationProvider';
import {AdapterDayjs} from '@mui/x-date-pickers/AdapterDayjs';
import {TimeClock as MuiTimeClock} from '@mui/x-date-pickers/TimeClock';
import {ThemeProvider, createTheme} from '@mui/material/styles';

// --- Color scheme: watch <html data-mantine-color-scheme="..."> ---------------
const readMantineScheme = () => {
    if (typeof document === 'undefined') return 'light';
    const v = document.documentElement.getAttribute('data-mantine-color-scheme');
    return v === 'dark' ? 'dark' : 'light';
};

const useMantineColorScheme = () => {
    const [scheme, setScheme] = useState(readMantineScheme);
    useEffect(() => {
        if (typeof document === 'undefined') return undefined;
        const html = document.documentElement;
        const sync = () => setScheme(readMantineScheme());
        const obs = new MutationObserver(sync);
        obs.observe(html, {
            attributes: true,
            attributeFilter: ['data-mantine-color-scheme'],
        });
        sync();
        return () => obs.disconnect();
    }, []);
    return scheme;
};

const lightTheme = createTheme({palette: {mode: 'light'}});
const darkTheme = createTheme({palette: {mode: 'dark'}});

// --- String <-> dayjs at the Dash boundary ----------------------------------
const TIME_ONLY_RE = /^(\d{1,2}):(\d{2})(:(\d{2}))?$/;

/** Parse a Dash string value into a dayjs object (or null). */
const parseToDayjs = (val) => {
    if (val === null || val === undefined || val === '') return null;
    if (typeof val !== 'string') return null;
    const m = val.match(TIME_ONLY_RE);
    if (m) {
        // Time-only string: anchor it to today's date so the clock has a date part.
        const base = dayjs().startOf('day');
        const withTime = base
            .hour(parseInt(m[1], 10))
            .minute(parseInt(m[2], 10))
            .second(m[4] ? parseInt(m[4], 10) : 0);
        return withTime.isValid() ? withTime : null;
    }
    const d = dayjs(val);
    return d.isValid() ? d : null;
};

/**
 * TimeClock lets the user pick a time on an inline clock face (hours, minutes,
 * and optionally seconds) without any input, popper, or modal. Values are
 * exchanged with Dash as strings; on change it emits `value` (wall-time ISO),
 * the current `view`, and a parsed `timeData` convenience object.
 */
const TimeClock = (props) => {
    const {
        id,
        value,
        defaultValue,
        views,
        view,
        openTo,
        ampm,
        disabled,
        readOnly,
        autoFocus,
        minutesStep,
        minTime,
        maxTime,
        disableFuture,
        disablePast,
        disableIgnoringDatePartForTimeValidation,
        showViewSwitcher,
        className,
        sx,
        setProps,
    } = props;

    const scheme = useMantineColorScheme();
    const theme = scheme === 'dark' ? darkTheme : lightTheme;

    // --- Parse incoming string props to dayjs -------------------------------
    const dValue = useMemo(() => parseToDayjs(value), [value]);
    const dDefault = useMemo(() => parseToDayjs(defaultValue), [defaultValue]);
    const dMinTime = useMemo(() => parseToDayjs(minTime), [minTime]);
    const dMaxTime = useMemo(() => parseToDayjs(maxTime), [maxTime]);

    // --- Change handlers -> Dash outputs ------------------------------------
    const handleChange = useCallback(
        (newVal) => {
            if (!setProps) return;
            if (!newVal || typeof newVal.isValid !== 'function' || !newVal.isValid()) {
                setProps({
                    value: null,
                    timeData: {
                        hours: null,
                        minutes: null,
                        seconds: null,
                        formatted: null,
                        event_timestamp: Date.now(),
                    },
                });
                return;
            }
            setProps({
                value: newVal.format('YYYY-MM-DDTHH:mm:ss'),
                timeData: {
                    hours: newVal.hour(),
                    minutes: newVal.minute(),
                    seconds: newVal.second(),
                    formatted: newVal.format('HH:mm:ss'),
                    event_timestamp: Date.now(),
                },
            });
        },
        [setProps]
    );

    const handleViewChange = useCallback(
        (newView) => {
            if (setProps) setProps({view: newView});
        },
        [setProps]
    );

    // --- Assemble the controlled/uncontrolled value -------------------------
    const clockProps = {};
    if (value !== undefined && value !== null) {
        clockProps.value = dValue; // controlled
    } else if (defaultValue !== undefined && defaultValue !== null) {
        clockProps.defaultValue = dDefault; // uncontrolled initial
    }
    if (view !== undefined && view !== null) clockProps.view = view;

    return (
        <div id={id} className={className}>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
                <ThemeProvider theme={theme}>
                    <MuiTimeClock
                        {...clockProps}
                        views={views}
                        openTo={openTo}
                        ampm={ampm}
                        disabled={disabled}
                        readOnly={readOnly}
                        autoFocus={autoFocus}
                        minutesStep={minutesStep}
                        minTime={dMinTime}
                        maxTime={dMaxTime}
                        disableFuture={disableFuture}
                        disablePast={disablePast}
                        disableIgnoringDatePartForTimeValidation={
                            disableIgnoringDatePartForTimeValidation
                        }
                        showViewSwitcher={showViewSwitcher}
                        sx={sx}
                        onChange={handleChange}
                        onViewChange={handleViewChange}
                    />
                </ThemeProvider>
            </LocalizationProvider>
        </div>
    );
};

TimeClock.defaultProps = {
    views: ['hours', 'minutes'],
    disabled: false,
    readOnly: false,
    autoFocus: false,
    disableFuture: false,
    disablePast: false,
    disableIgnoringDatePartForTimeValidation: false,
    showViewSwitcher: false,
};

TimeClock.propTypes = {
    /** Dash component id */
    id: PropTypes.string,

    // --- Value (string <-> dayjs at the boundary) ---------------------------
    /**
     * Controlled value. Full wall-time ISO ("2022-04-17T15:30:00") or time-only
     * ("15:30" / "15:30:45"). Also an OUTPUT: updated on every change with a
     * full wall-time ISO string.
     */
    value: PropTypes.string,

    /** Uncontrolled initial value (same string formats as `value`). */
    defaultValue: PropTypes.string,

    // --- Views --------------------------------------------------------------
    /** Which views to render, in order. Default ["hours", "minutes"]. */
    views: PropTypes.arrayOf(PropTypes.oneOf(['hours', 'minutes', 'seconds'])),

    /** Controlled visible view. Also an OUTPUT — updated when the view changes. */
    view: PropTypes.oneOf(['hours', 'minutes', 'seconds']),

    /** Which view to open first (uncontrolled). */
    openTo: PropTypes.oneOf(['hours', 'minutes', 'seconds']),

    // --- Format -------------------------------------------------------------
    /** Force 12h (true) or 24h (false). Omit to use the locale default. */
    ampm: PropTypes.bool,

    // --- Form props ---------------------------------------------------------
    /** Disable the whole clock. */
    disabled: PropTypes.bool,

    /** Make the clock read-only (no editing). */
    readOnly: PropTypes.bool,

    /** Auto-focus the clock on mount. */
    autoFocus: PropTypes.bool,

    // --- Constraints --------------------------------------------------------
    /** Step (in minutes) between selectable minute values. */
    minutesStep: PropTypes.number,

    /** Minimum selectable time (ISO or time-only string). */
    minTime: PropTypes.string,

    /** Maximum selectable time (ISO or time-only string). */
    maxTime: PropTypes.string,

    /** Disable times in the future (relative to now). */
    disableFuture: PropTypes.bool,

    /** Disable times in the past (relative to now). */
    disablePast: PropTypes.bool,

    /**
     * When true, min/max time comparisons include the date part. When false
     * (default), only the time-of-day is compared.
     */
    disableIgnoringDatePartForTimeValidation: PropTypes.bool,

    /** Show the hours/minutes/seconds view-switch arrow buttons. */
    showViewSwitcher: PropTypes.bool,

    // --- Appearance ---------------------------------------------------------
    /** CSS class applied to the wrapping div. */
    className: PropTypes.string,

    /** MUI sx styling object applied to the TimeClock. */
    sx: PropTypes.object,

    // --- Output props -------------------------------------------------------
    /**
     * Parsed convenience output, updated on every change:
     * { hours, minutes, seconds, formatted ("HH:mm:ss"), event_timestamp }.
     */
    timeData: PropTypes.exact({
        hours: PropTypes.number,
        minutes: PropTypes.number,
        seconds: PropTypes.number,
        formatted: PropTypes.string,
        event_timestamp: PropTypes.number,
    }),

    /** Dash setProps callback */
    setProps: PropTypes.func,
};

export default TimeClock;
