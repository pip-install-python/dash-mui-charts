
> Dash Mantine Components v2.7.0 Documentation for debounce prop
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt  
> All relative links in this file should be resolved against https://www.dash-mantine-components.com
> Based on [Mantine v8](https://v8.mantine.dev/). Do not use Mantine v9 docs for API reference.




## debounce prop  
Learn how to use the debounce prop in Dash Mantine Components to control when input values update. Reduce callback load and improve performance in text inputs, dropdowns, pickers, and more.  
Category: Dash  

### About the debounce prop


The `debounce` prop delays the update of a component's value until the user stops interacting, reducing callback
frequency for inputs.


To control how often the input's value is updated while the user is typing, use the `debounce` prop:

- `debounce=False` Is the default and it will update as the user interacts with the input.
- Set `debounce=True` to update the value only when the user finishes typing and moves focus away (i.e. on blur).
- Set `debounce=<milliseconds>` to update the value after a specified delay from the user's last keystroke. For example,
`debounce=300` will wait 300 milliseconds after the user stops typing before updating the value.


####  debounce=False
```python
import dash_mantine_components as dmc
from dash import callback, Input, Output


component = dmc.Group(
    gap=50,
    children=[
        dmc.TimePicker(label="Enter a time", id="timepicker-usage"),
        dmc.Text(id="out-timepicker")
    ],
)

@callback(
    Output("out-timepicker", "children"),
    Input("timepicker-usage", "value")
)
def update(value):
    return f"You entered: {value}"
```
####  debounce=True
```python
import dash_mantine_components as dmc
from dash import callback, Input, Output


component = dmc.Group(
    gap=50,
    children=[
        dmc.TimePicker(
            label="Enter a time",
            debounce=True,
            id="timepicker-debounce"
        ),
        dmc.Text(id="out-timepicker-debounce")
    ],
)

@callback(
    Output("out-timepicker-debounce", "children"),
    Input("timepicker-debounce", "value")
)
def update(value):
    return f"You entered: {value}"
```
#### debounce=1000
```python
import dash_mantine_components as dmc
from dash import callback, Input, Output


component = dmc.Group(
    gap=50,
    children=[
        dmc.TimePicker(
            label="Enter a time",
            debounce=1000,
            id="timepicker-debounce-ms"
        ),
        dmc.Text(id="out-timepicker-debounce-ms")
    ],
)

@callback(
    Output("out-timepicker-debounce-ms", "children"),
    Input("timepicker-debounce-ms", "value")
)
def update(value):
    return f"You entered: {value}"
```
### Example with TextInput

This example uses `debounce=True`.  Note that the comments are updated only after the user has
finished entering data.

```python
import dash_mantine_components as dmc
from dash import  callback, Input, Output

component = dmc.Stack(

    [
        dmc.TextInput(
            id="debounce-text",
            label="Enter your comments",
            debounce=True
        ),
        dmc.Text(id="debounce-text-output"),
    ],
)


@callback(
    Output("debounce-text-output", "children"),
    Input("debounce-text", "value"),
)
def update_output(comments):
    if not comments:
        return ""
    return f"Thank you for your feedback: {comments}"
```
### Supported Components
The `debounce` prop is supported by many DMC input components, including:

- TextInput

- Textarea

- NumberInput

- PasswordInput

- JsonInput

- Select, MultiSelect, Autocomplete

- DateInput, DateTimePicker, DatePickerInput

- MonthPickerInput, YearPickerInput, TimeInput, TimePicker

- RichTextEditor


For the `Slider` and `RangeSlider`  use [updatemode](/components/slider#update-mode)

### Usage Tips

- Use `debounce=True` for forms where you only care about the final value after the user finishes typing, for example, email fields, names, comments.

- Use `debounce=300` or higher for search boxes or filters that trigger live updates (for example,  querying a table or filtering a plot). This prevents the app from firing a callback on every keystroke and keeps things responsive.

- Combine with `n_submit` or `n_blur` if you want finer control over when inputs send updates.