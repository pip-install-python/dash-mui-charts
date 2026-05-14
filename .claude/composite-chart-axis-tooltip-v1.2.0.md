# dash-mui-charts v1.2.0: CompositeChart Axis Tooltip Enhancement

## Issue Summary

**Component**: `CompositeChart`
**Current version**: 1.1.0
**Target version**: 1.2.0
**Priority**: High — this is the primary barrier to consistent tooltip behavior across chart types

### Problem

When `CompositeChart` has **mixed series types** (line + scatter) and `tooltip={'trigger': 'axis'}` is set, the tooltip only appears when the user hovers **directly over a data mark** (line point or scatter dot). It does NOT show when hovering at arbitrary x-positions like `LineChart` does with `trigger: 'axis'`.

This breaks the expected UX where `trigger: 'axis'` means "show tooltip data for all series at the current x-axis position, regardless of proximity to data marks."

### Expected Behavior (matches LineChart)

With `trigger: 'axis'`:
- Tooltip should appear at **any x-position** within the chart area
- Tooltip should display values for **all series** (both line and scatter) at that x-position
- Scatter series should use proximity matching (nearest point within a configurable radius)
- The `highlightedAxis` callback prop should fire at any x-position (not only near marks)

### Actual Behavior (v1.1.0)

- Tooltip only appears when mouse is near/on a data mark
- Hovering in empty space between data points shows no tooltip
- The `axisHighlight` visual (e.g., `{x: 'line'}`) correctly renders a vertical line at the mouse position — but no tooltip accompanies it
- `highlightedAxis` does fire from the chart, but the built-in tooltip doesn't render

---

## Root Cause Analysis

### How LineChart handles `trigger: 'axis'` (correct behavior)

In `LineChart` (function `yT`), the tooltip is rendered as:

```jsx
// LineChart tooltip rendering (simplified from minified source)
{tooltip?.trigger !== 'none' && (
  <ChartsTooltip trigger={tooltip?.trigger || 'axis'} />
)}
```

`ChartsTooltip` (`mM`) with `trigger='axis'` renders `ChartsAxisTooltipContent` (`lM`), which uses MUI's `useAxesTooltip()` hook. This hook reads the internal axis interaction state maintained by `ChartContainerPro`, which tracks mouse position across the entire chart area and maps it to the nearest axis data index — regardless of whether a data mark exists there.

### How CompositeChart handles `trigger: 'axis'` (broken path)

In `CompositeChart` (function `G$`), there is special-case logic:

```jsx
// CompositeChart tooltip rendering (simplified from minified source)
const ae = tooltip?.trigger || 'axis';           // trigger mode
const Z = series.some(s => s.type === 'scatter'); // has scatter series
const se = Z && ae === 'axis';                    // special case flag

{ae !== 'none' && (
  se
    ? <ChartsTooltipContainer trigger="axis">
        <CompositeAxisTooltipContent scatterSeries={scatterSeries} proximity={oe} />
      </ChartsTooltipContainer>
    : <ChartsTooltip trigger={ae} />
)}
```

**The branching logic**: When the chart has scatter series AND trigger is `'axis'`, it bypasses the standard `ChartsTooltip` and instead uses `ChartsTooltipContainer` with a custom `CompositeAxisTooltipContent` (`H$`).

### Why the custom tooltip fails

`CompositeAxisTooltipContent` (`H$`) uses `useAxesTooltip()` (`sM`) to get axis hover data:

```jsx
function CompositeAxisTooltipContent({ scatterSeries, proximity }) {
  const axisData = useAxesTooltip(); // sM()
  if (!axisData || axisData.length === 0) return null;
  
  const { axisValue, axisFormattedValue, seriesItems } = axisData[0];
  
  // Filter out scatter series from the line-based seriesItems
  const scatterIds = new Set(scatterSeries.map(s => s.id));
  const lineItems = seriesItems.filter(item => !scatterIds.has(item.seriesId));
  
  // Proximity-match scatter data points near the current axis value
  const scatterItems = [];
  for (const series of scatterSeries) {
    for (const point of series.data) {
      if (Math.abs(point.x - axisValue) <= proximity) {
        scatterItems.push({ seriesId: series.id, color: series.color, ... });
      }
    }
  }
  
  // Render combined line + scatter tooltip
  return <div>...</div>;
}
```

**The issue**: `useAxesTooltip()` returns data based on the **internal interaction state** of the chart. In CompositeChart, the interaction state tracking differs from standalone LineChart because CompositeChart uses the composition API (`ChartDataProviderPro` + `ChartsSurface`) rather than the high-level `LineChartPro` component. The composition API may not fully wire up the axis interaction tracking needed for `useAxesTooltip()` to return data at every x-position.

Additionally, `ChartsTooltipContainer` (`fM`) controls the Popper open/close state. Its open condition depends on whether `useAxesTooltip()` returns non-empty data. If the hook doesn't fire at arbitrary positions, the container stays closed.

### Key difference from LineChart

LineChart uses `ChartContainerPro` internally, which has full axis interaction wiring built in. CompositeChart uses the lower-level composition API (`ChartDataProviderPro` + raw plot components), which may not automatically set up the same axis interaction tracking.

---

## Proposed Fix for v1.2.0

### Option A: Fix axis interaction tracking in CompositeChart (Recommended)

Ensure the composition API setup in CompositeChart includes the same axis interaction tracking that `ChartContainerPro` provides to LineChart.

**In the CompositeChart React component (`G$`):**

1. The component currently uses `ChartDataProviderPro` (`gb`) as its provider. Verify that this provider includes `ChartsAxisHighlight` interaction state tracking for the x-axis.

2. The `ChartsAxisHighlight` component (`wM`) is already rendered:
   ```jsx
   <ChartsAxisHighlight 
     x={axisHighlight?.x ?? (hasLines ? 'line' : 'none')} 
     y={axisHighlight?.y ?? 'none'} 
   />
   ```
   This handles the visual highlight line but may not be sufficient to drive tooltip data.

3. **Key change**: When `trigger === 'axis'`, ensure the tooltip container receives axis hover data even when the mouse is not directly over a mark. This likely requires:
   - Using `ChartsAxisHighlight` interaction tracking to feed `useAxesTooltip()`
   - OR switching to `ChartsTooltip` (standard, `mM`) instead of the custom `CompositeAxisTooltipContent` when `trigger === 'axis'`, and handling scatter data display separately

**Simplest implementation:**

```jsx
// BEFORE (v1.1.0):
{ae !== 'none' && (
  se 
    ? <ChartsTooltipContainer trigger="axis">
        <CompositeAxisTooltipContent scatterSeries={te} proximity={oe} />
      </ChartsTooltipContainer>
    : <ChartsTooltip trigger={ae} />
)}

// AFTER (v1.2.0):
// Always use the standard ChartsTooltip for axis trigger,
// with scatter proximity data injected into the content
{ae !== 'none' && (
  <ChartsTooltip trigger={ae} />
)}
```

If the standard `ChartsTooltip` with `trigger='axis'` works in the composition API context (i.e., `useAxesTooltip()` returns data at any x-position), this is the simplest fix. The trade-off is that scatter series won't get proximity-based matching in the tooltip — they'd need `connectNulls` or data alignment to appear in the axis tooltip.

### Option B: Use `ChartsTooltipContainer` with corrected open state

If `useAxesTooltip()` doesn't work in the composition API context, the `ChartsTooltipContainer` needs its open state driven by axis position rather than by hook data:

```jsx
// Use the pointer position directly to control tooltip open state
<ChartsTooltipContainer trigger="axis" anchor="pointer">
  <CompositeAxisTooltipContent scatterSeries={te} proximity={oe} />
</ChartsTooltipContainer>
```

The `anchor: 'pointer'` might help, but the core issue is whether `useAxesTooltip()` returns data. If not, the internal `ChartsTooltipContainer` will render `null` children and the Popper won't open.

### Option C: Add `highlightedAxis` as a controlled prop (like LineChart)

Add `highlightedAxis` and `tooltipAxis` props to CompositeChart, matching LineChart's API:

```python
# New props for CompositeChart (matching LineChart)
class CompositeChart(Component):
    highlightedAxis: list[dict]   # Controlled axis highlight state
    tooltipAxis: list[dict]       # Controlled tooltip axis state
```

**React implementation:**

```jsx
// In CompositeChart (G$):
const highlightedAxis = t.highlightedAxis;
const tooltipAxis = t.tooltipAxis;

// Pass to ChartDataProviderPro
pe.highlightedAxis = highlightedAxis;
pe.onHighlightedAxisChange = (newAxis) => {
  setProps({ highlightedAxis: newAxis });
};

// For tooltip sync
pe.tooltipAxis = tooltipAxis;
pe.onTooltipAxisChange = (newAxis) => {
  setProps({ tooltipAxis: newAxis });
};
```

This would enable Dash callbacks to:
1. Read `highlightedAxis` from one CompositeChart
2. Write it to other CompositeCharts
3. Sync tooltip display across multiple charts

**This option is recommended in addition to Option A**, as it gives Dash users full control over cross-chart synchronization.

---

## Additional Props to Add

### `highlightedAxis` (input/output)

```python
highlightedAxis: list[dict]  # [{axisId: str, dataIndex: int}]
```

- Fires when user hovers at any x-position (like LineChart already does)
- Can be set programmatically to highlight a specific axis position
- Enables cross-chart sync via Dash callbacks

### `tooltipAxis` (input/output)

```python
tooltipAxis: list[dict]  # [{axisId: str, dataIndex: int}]
```

- Controls which axis tooltip is shown (like LineChart `tooltipAxis`)
- When set externally, shows tooltip at that position even without mouse hover
- Enables tooltip sync across multiple CompositeCharts

### `tooltipItem` (input/output)

```python
tooltipItem: dict  # {type: str, seriesId: str, dataIndex: int}
```

- Controls which item tooltip is shown
- Already exists in LineChart but missing from CompositeChart

---

## Use Case: Multi-Chart Synced Tooltips

The Martin OnSite Dashboard displays 3 stacked time-series CompositeCharts (Discharge Time, Pressure, Temperature) for air cannon equipment. Requirements:

1. User hovers over **any** chart at **any** x-position
2. All 3 charts show a vertical crosshair line at that position
3. All 3 charts show a tooltip with series values at that position
4. Scatter event markers (alerts/warnings) are overlaid on the line data

**Current workaround** (v1.1.0): Uses `tooltip={'trigger': 'none'}` with custom Python-rendered tooltip divs positioned via CSS `calc()`. The `highlightedAxis` callback fires from CompositeChart and drives the custom tooltip system. This works but:
- Requires complex Python callback logic for tooltip rendering
- Tooltip positioning via CSS `calc()` is fragile and breaks with zoom
- Cannot use MUI's built-in tooltip formatting/styling

**With v1.2.0 fix**: `tooltip={'trigger': 'axis'}` would work natively, and `tooltipAxis`/`highlightedAxis` controlled props would enable sync across charts without custom tooltip rendering.

---

## Testing Checklist

### Axis Tooltip Trigger
- [ ] `CompositeChart` with line-only series: `trigger: 'axis'` shows tooltip at any x-position
- [ ] `CompositeChart` with scatter-only series: `trigger: 'axis'` shows tooltip at any x-position
- [ ] `CompositeChart` with line + scatter series: `trigger: 'axis'` shows tooltip at any x-position
- [ ] Tooltip shows values for ALL series (line and scatter) at the hovered position
- [ ] Scatter values use proximity matching for non-aligned data points
- [ ] `trigger: 'item'` still works (tooltip only on mark hover)
- [ ] `trigger: 'none'` still works (no tooltip)

### Controlled Props
- [ ] `highlightedAxis` fires on any x-position hover (not just near marks)
- [ ] Setting `highlightedAxis` programmatically highlights that position
- [ ] `tooltipAxis` shows tooltip at the specified position
- [ ] Setting `tooltipAxis` from another chart syncs tooltip display
- [ ] `tooltipItem` works for item-level tooltip control

### Axis Highlight
- [ ] `axisHighlight: {x: 'line', y: 'line'}` shows crosshair lines
- [ ] `axisHighlight: {x: 'band'}` shows band highlight (point/band scale only)
- [ ] Axis highlight fires at any x-position (drives `highlightedAxis` callback)

### Zoom Interaction
- [ ] Tooltip works correctly when chart is zoomed in
- [ ] Tooltip position accounts for zoom offset
- [ ] `highlightedAxis` dataIndex is correct within zoomed range

### Backward Compatibility
- [ ] Existing `tooltip: {trigger: 'none'}` + custom tooltip pattern still works
- [ ] `highlightedItem` still works for item-level sync
- [ ] No breaking changes to existing CompositeChart props

---

## Migration Guide (for consumers)

### Before (v1.1.0 workaround)

```python
# Disable native tooltip, use custom Python tooltips
CompositeChart(
    tooltip={'trigger': 'none'},
    axisHighlight={'x': 'line', 'y': 'line'},
)

# Complex callback listening to highlightedAxis/highlightedItem
# to render custom tooltip divs positioned with CSS calc()
@callback(
    Output('custom-tooltip', 'style'),
    Output('custom-tooltip', 'children'),
    Input('chart', 'highlightedAxis'),
    Input('chart', 'highlightedItem'),
)
def render_tooltip(axis, item):
    # ~100 lines of tooltip positioning and rendering logic
    ...
```

### After (v1.2.0)

```python
# Native axis tooltip works on CompositeChart
CompositeChart(
    tooltip={'trigger': 'axis'},
    axisHighlight={'x': 'line', 'y': 'line'},
)

# For multi-chart sync, use controlled tooltipAxis
@callback(
    Output('chart-2', 'tooltipAxis'),
    Output('chart-3', 'tooltipAxis'),
    Input('chart-1', 'tooltipAxis'),
)
def sync_tooltips(axis):
    return axis, axis
```
