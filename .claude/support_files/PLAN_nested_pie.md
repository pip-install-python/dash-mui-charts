# Nested Pie Chart Implementation Plan

## Goal
Enhance PieChart component to support multi-series/nested pie charts with inner and outer rings, like the MUI X Charts examples showing hierarchical data visualization.

---

## Analysis of MUI Examples

### Key Pattern: `series` prop accepts array of layer configs
```javascript
series={[
  {
    innerRadius: 0,
    outerRadius: 80,
    data: innerData,
    highlightScope: { fade: 'global', highlight: 'item' },
  },
  {
    innerRadius: 100,  // Gap between rings
    outerRadius: 120,
    data: outerData,
    highlightScope: { fade: 'global', highlight: 'item' },
  },
]}
```

### Key Features to Support:
1. **Multiple series** with different data arrays
2. **Per-series geometry**: innerRadius, outerRadius, cornerRadius, paddingAngle
3. **Per-series styling**: highlightScope, arcLabel, arcLabelMinAngle
4. **Color with opacity**: `#fa938e80` (hex + alpha) for variations
5. **View toggle**: Switch between different data perspectives

---

## Implementation Steps

### Step 1: Modify React Component

**File:** `src/lib/components/PieChart.react.js`

**Changes:**
```javascript
// Add new prop
series: PropTypes.arrayOf(PropTypes.shape({
    data: PropTypes.array.isRequired,
    innerRadius: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    outerRadius: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    paddingAngle: PropTypes.number,
    cornerRadius: PropTypes.number,
    startAngle: PropTypes.number,
    endAngle: PropTypes.number,
    arcLabel: PropTypes.oneOf(['value', 'label', 'formattedValue']),
    arcLabelMinAngle: PropTypes.number,
    arcLabelRadius: PropTypes.number,
    highlightScope: PropTypes.object,
    id: PropTypes.string,
})),

// Logic change:
// If `series` prop provided → use directly
// If only `data` prop → wrap in single series (backward compat)
```

### Step 2: Rebuild Component
```bash
npm run build
```

### Step 3: Update `pages/pie_props.py`

**New Data Structures:**

```python
# Titanic data
TITANIC_RAW = [
    {'Class': '1st', 'Survived': 'No', 'Count': 123},
    {'Class': '1st', 'Survived': 'Yes', 'Count': 202},
    # ... etc
]

# Inner ring - Class totals
CLASS_DATA = [
    {'id': '1st', 'label': '1st Class', 'value': 325, 'color': '#fa938e'},
    {'id': '2nd', 'label': '2nd Class', 'value': 285, 'color': '#98bf45'},
    {'id': '3rd', 'label': '3rd Class', 'value': 706, 'color': '#51cbcf'},
    {'id': 'Crew', 'label': 'Crew', 'value': 908, 'color': '#d397ff'},
]

# Outer ring - Survival within each class
CLASS_SURVIVAL_DATA = [
    # 1st class breakdown
    {'id': '1st-Yes', 'label': 'Survived', 'value': 202, 'color': '#fa938e'},
    {'id': '1st-No', 'label': 'Did not survive', 'value': 123, 'color': '#fa938e80'},
    # 2nd class breakdown
    {'id': '2nd-Yes', 'label': 'Survived', 'value': 118, 'color': '#98bf45'},
    {'id': '2nd-No', 'label': 'Did not survive', 'value': 167, 'color': '#98bf4580'},
    # ... etc
]

# Alternative view - by Survival status
SURVIVAL_DATA = [
    {'id': 'Yes', 'label': 'Survived', 'value': 710, 'color': '#51cbcf'},
    {'id': 'No', 'label': 'Did not survive', 'value': 1514, 'color': '#fa938e'},
]

SURVIVAL_CLASS_DATA = [
    # Survivors by class
    {'id': '1st-Yes', 'label': '1st Class', 'value': 202, 'color': 'rgba(81,203,207,0.9)'},
    {'id': '2nd-Yes', 'label': '2nd Class', 'value': 118, 'color': 'rgba(81,203,207,0.7)'},
    # ... etc
]
```

**New UI Features:**

1. **View Toggle** (SegmentedControl):
   - "View by Class" - inner=class totals, outer=survival breakdown
   - "View by Survival" - inner=survived/not, outer=class breakdown

2. **Ring Configuration Cards**:
   - Inner Ring: innerRadius, outerRadius, cornerRadius
   - Outer Ring: innerRadius, outerRadius, cornerRadius, gap control

3. **Series-specific Controls**:
   - Arc labels per series
   - Highlight behavior per series

4. **Live Preview** showing nested pie with both rings

---

## File Changes Summary

| File | Change |
|------|--------|
| `src/lib/components/PieChart.react.js` | Add `series` prop support |
| `dash_mui_charts/PieChart.py` | Auto-generated after build |
| `pages/pie_props.py` | Complete rewrite with nested demo |

---

## Example Usage After Implementation

```python
from dash_mui_charts import PieChart

# Nested pie chart with two rings
PieChart(
    series=[
        {
            'data': CLASS_DATA,
            'innerRadius': 50,
            'outerRadius': 100,
            'cornerRadius': 3,
            'highlightScope': {'fade': 'global', 'highlight': 'item'},
        },
        {
            'data': CLASS_SURVIVAL_DATA,
            'innerRadius': 110,
            'outerRadius': 140,
            'cornerRadius': 3,
            'highlightScope': {'fade': 'global', 'highlight': 'item'},
        },
    ],
    height=400,
    hideLegend=True,
)
```

---

## Backward Compatibility

Existing code continues to work:
```python
# Old way (still works)
PieChart(
    data=[...],
    innerRadius=50,
    outerRadius=100,
)

# New way (multi-series)
PieChart(
    series=[
        {'data': [...], 'innerRadius': 50, 'outerRadius': 100},
        {'data': [...], 'innerRadius': 110, 'outerRadius': 140},
    ],
)
```
