# MUI X Charts Styling Guide

## Tooltip Customization

### Key Insight: Portal Rendering

MUI Charts tooltips render in a **portal** attached to `document.body`, NOT inside the chart container. This means:

- CSS selectors like `.my-container .MuiChartsTooltip-*` won't work by default
- The chart's `sx` prop does NOT affect tooltip styling

### Solutions

#### Option 1: Disable Portal (Recommended for CSS styling)

```python
SparklineChart(
    slotProps={
        'tooltip': {'disablePortal': True}
    }
)
```

This renders the tooltip inside the chart container, enabling standard CSS inheritance.

#### Option 2: Use slotProps.tooltip.sx

```javascript
slotProps={{
  tooltip: {
    sx: {
      [`&.${chartsTooltipClasses.root} .${chartsTooltipClasses.valueCell}`]: {
        color: 'red',
      },
    },
  },
}}
```

### Tooltip CSS Classes

| Class | Description |
|-------|-------------|
| `.MuiChartsTooltip-root` | Main tooltip container |
| `.MuiChartsTooltip-paper` | Paper/card surface |
| `.MuiChartsTooltip-table` | Data table |
| `.MuiChartsTooltip-row` | Table row |
| `.MuiChartsTooltip-cell` | General cell |
| `.MuiChartsTooltip-labelCell` | Label text |
| `.MuiChartsTooltip-valueCell` | Value display |
| `.MuiChartsTooltip-axisValueCell` | **Axis value/index** (axis tooltip only) |
| `.MuiChartsTooltip-markCell` | Mark indicator cell |
| `.MuiChartsTooltip-mark` | Color indicator mark |

### MUI v8 DOM Structure Changes

- Label cells are now `<th>` elements instead of `<td>`
- Axis data moved from header to table `<caption>`
- Mark and label combined into single `<th>` element

### Mark Element Sizing

The `.MuiChartsTooltip-mark` color indicator may appear undersized by default. To properly size it:

```css
/* Mark cell container */
.sparkline-container .MuiChartsTooltip-markCell {
    padding: 12px 8px 12px 16px !important;
    vertical-align: middle !important;
}

/* Mark indicator - explicit sizing */
.sparkline-container .MuiChartsTooltip-mark {
    width: 14px !important;
    height: 14px !important;
    border-radius: 4px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 0 8px rgba(79, 195, 247, 0.6) !important;
    display: inline-block !important;
}
```

### Complete Tooltip Styling Example

```css
/* Target ALL tooltip text elements */
.sparkline-container .MuiChartsTooltip-cell,
.sparkline-container .MuiChartsTooltip-labelCell,
.sparkline-container .MuiChartsTooltip-valueCell,
.sparkline-container .MuiChartsTooltip-axisValueCell,
.sparkline-container .MuiChartsTooltip-markCell,
.sparkline-container [class*="MuiChartsTooltip"] td,
.sparkline-container [class*="MuiChartsTooltip"] th,
.sparkline-container [class*="MuiChartsTooltip"] caption {
    color: #ffffff !important;
}

/* Glassmorphism tooltip background */
.sparkline-container .MuiChartsTooltip-paper,
.sparkline-container .MuiPaper-root {
    backdrop-filter: blur(24px) saturate(200%) !important;
    background: linear-gradient(
        135deg,
        rgba(15, 25, 45, 0.95) 0%,
        rgba(10, 20, 40, 0.92) 100%
    ) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 14px !important;
}
```

---

## CSS Mask Effects

### Problem: Masks Affect All Children

When using `mask-image` for opacity effects, the mask affects ALL child elements including tooltips.

```css
/* BAD: Affects tooltip too */
.container.hovering {
    mask-image: linear-gradient(...);
}

/* GOOD: Only affects SVG chart */
.container.hovering svg {
    mask-image: linear-gradient(...);
}
```

### Dynamic Hover Opacity Effect

```css
/* CSS custom property for dynamic mask position */
.sparkline-container.hovering svg {
    mask-image: linear-gradient(
        to right,
        rgba(0, 0, 0, 1) 0%,
        rgba(0, 0, 0, 1) var(--hover-percent, 50%),
        rgba(0, 0, 0, 0.4) var(--hover-percent, 50%),
        rgba(0, 0, 0, 0.4) 100%
    );
}
```

Update `--hover-percent` via Dash callback to create interactive effects.

---

## X-Axis Highlight Line

### Show Only on Hover

```css
/* Hide by default */
.sparkline-container .MuiChartsAxisHighlight-root,
.sparkline-container svg line[class*="AxisHighlight"] {
    opacity: 0;
    transition: opacity 0.2s ease;
}

/* Show when hovering */
.sparkline-container.hovering .MuiChartsAxisHighlight-root,
.sparkline-container.hovering svg line[class*="AxisHighlight"] {
    opacity: 1;
}
```

---

## Glassmorphism / Liquid Glass Design

### Card Container

```css
.glass-card {
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.25) 0%,
        rgba(255, 255, 255, 0.10) 100%
    );
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 24px;
    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.15),
        inset 0 1px 0 0 rgba(255, 255, 255, 0.4);
}
```

### Animated Floating Orbs (Background Depth)

```css
.background::before {
    content: '';
    position: absolute;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(79, 195, 247, 0.4) 0%, transparent 70%);
    border-radius: 50%;
    filter: blur(60px);
    animation: floatOrb 8s ease-in-out infinite;
}

@keyframes floatOrb {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(-30px, 30px) scale(1.1); }
}
```

### Left-to-Right Reveal Animation

```css
@keyframes revealLeftToRight {
    from {
        clip-path: inset(0 100% 0 0);
        opacity: 0;
    }
    to {
        clip-path: inset(0 0 0 0);
        opacity: 1;
    }
}

.chart-container {
    animation: revealLeftToRight 1.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
```

---

## SparklineChart Props for Styling

```python
SparklineChart(
    color='rgba(79, 195, 247, 1)',  # Single color (pass directly, not as array)
    strokeWidth=2,                   # Line thickness
    area=True,                       # Fill under line
    curve='monotoneX',               # Smooth curve
    showTooltip=True,
    showHighlight=True,
    axisHighlight={'x': 'line'},     # Vertical highlight line
    xAxis={'id': 'x-axis'},          # Required for controlled highlighting
    baseline='min',                  # Area fill from minimum
    slotProps={
        'lineHighlight': {'r': 6},   # Highlight dot radius
        'tooltip': {'disablePortal': True},  # Enable CSS styling
    },
    clipAreaOffset={'top': 10, 'right': 10, 'bottom': 10, 'left': 10},
)
```

---

## References

- [MUI X Charts Tooltip](https://mui.com/x/react-charts/tooltip/)
- [ChartsTooltip API](https://mui.com/x/api/charts/charts-tooltip/)
- [MUI X Charts Styling](https://mui.com/x/react-charts/styling/)