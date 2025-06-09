# Flet Object Inspector

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![TestPyPI Version](https://img.shields.io/badge/TestPyPI-v0.1.3-orange.svg)](https://test.pypi.org/project/flet-object-inspector/)


A utility for visualizing and analyzing the structure of [Flet framework](https://flet.dev) objects. Allows easy viewing of complex nested interface structures in a readable format.

## 🚀 Features

- **Tree-like display** of Flet object structures with indentation
- **Display of control properties** (text, width, height, bgcolor, etc.)
- **Handling of special elements** (appbar, drawer, navigation_bar)
- **JSON export** for further processing
- **Conversion to Python dictionaries** for programmatic analysis
- **Customizable recursion depth** and formatting


## 📦 Installation

```bash
# From PyPI
pip install flet-object-inspector

# From test.pypi (for test versions)
pip install -i https://test.pypi.org/simple/ flet-object-inspector

# From source code
git clone https://github.com/yourusername/flet-object-inspector.git
cd flet-object-inspector
pip install -e .
```

## 🛠 Quick Start

```python
import flet as ft
from flet_object_inspector import inspect_flet, flet_to_json, flet_to_dict

# Create a Flet structure
view = ft.View(
    route="/home",
    appbar=ft.AppBar(
        title=ft.Text("My Application"),
        bgcolor=ft.colors.BLUE
    ),
    controls=[
        ft.Container(
            content=ft.Row([
                ft.IconButton(ft.icons.HOME, tooltip="Home"),
                ft.IconButton(ft.icons.SETTINGS, tooltip="Settings"),
                ft.ElevatedButton("Button", width=200)
            ]),
            padding=20,
            bgcolor=ft.colors.GREY_100
        ),
        ft.Text("Welcome!", size=24),
        ft.Column([
            ft.TextField(label="Name", width=300),
            ft.TextField(label="Email", width=300),
        ])
    ]
)

# View the structure
inspect_flet(view)
```

### Output:
```
View (route='/home', visible=True, disabled=False) {
  appbar: AppBar (bgcolor='Colors.BLUE', visible=True, disabled=False) {
    title: Text (value='My Application', visible=True, disabled=False)
  }
  [0] Container (bgcolor='Colors.GREY_100', padding=20, visible=True, disabled=False) {
    Row (visible=True, disabled=False) {
      [0] IconButton (visible=True, disabled=False, tooltip='Home'),
      [1] IconButton (visible=True, disabled=False, tooltip='Settings'),
      [2] ElevatedButton (text='Button', width=200, visible=True, disabled=False)
    }
  },
  [1] Text (value='Welcome!', visible=True, disabled=False),
  [2] Column (visible=True, disabled=False) {
    [0] TextField (width=300, visible=True, disabled=False),
    [1] TextField (width=300, visible=True, disabled=False)
  }
}
```

## 📖 Detailed Usage

### Core Functions

#### `inspect_flet(obj, show_properties=True, indent_size=2, max_depth=10)`

Prints the object structure to the console.

**Parameters:**
- `obj`: Flet object to analyze
- `show_properties`: Whether to display control properties (default: True)
- `indent_size`: Indentation size in spaces (default: 2)
- `max_depth`: Maximum recursion depth (default: 10)

```python
# Structure only, without properties
inspect_flet(view, show_properties=False)

# With larger indentation
inspect_flet(view, indent_size=4)

# Limited depth
inspect_flet(view, max_depth=3)
```

#### `flet_to_dict(obj)`

Converts a Flet object to a Python dictionary.

```python
data = flet_to_dict(view)
print(data['type'])  # 'View'
print(data['properties'])  # {'route': '/home', 'visible': True, ...}
print(len(data['children']))  # Number of child elements
```

#### `flet_to_json(obj, indent=2)`

Exports the structure to JSON format.

```python
# Pretty JSON with indentation
json_str = flet_to_json(view, indent=2)
print(json_str)

# Compact JSON
json_str = flet_to_json(view, indent=None)

# Save to file
with open('structure.json', 'w', encoding='utf-8') as f:
    f.write(flet_to_json(view))
```

### Using the FletInspector Class

For finer control, use the class directly:

```python
from flet_object_inspector import FletInspector

inspector = FletInspector(indent_size=4, max_depth=5)

# Get string representation
structure_str = inspector.inspect(view, show_properties=True)
print(structure_str)

# Convert to dictionary
data_dict = inspector.to_dict(view)
```

## 🔧 Supported Controls

The inspector automatically recognizes and processes all Flet controls:

### Core Controls
- `View`, `Page`, `AppBar`, `NavigationBar`
- `Container`, `Row`, `Column`, `Stack`
- `Text`, `TextField`, `ElevatedButton`, `IconButton`
- `ListView`, `GridView`, `DataTable`

### Special Elements
- `appbar` - application bar
- `drawer` - side menu
- `bottom_navigation_bar` - bottom navigation

### Displayed Properties
- `text`, `value`, `width`, `height`
- `bgcolor`, `color`, `visible`, `disabled`
- `tooltip`, `route`, `title`, `label`
- `padding`, `margin`, `hint_text`

## 💡 Usage Examples

### Analyzing a Complex Form

```python
form = ft.Column([
    ft.Text("Registration", size=30, weight=ft.FontWeight.BOLD),
    ft.Divider(),
    ft.Row([
        ft.TextField(label="First Name", expand=1),
        ft.TextField(label="Last Name", expand=1),
    ]),
    ft.TextField(label="Email", width=400),
    ft.TextField(label="Password", password=True, width=400),
    ft.Row([
        ft.Checkbox(label="Agree to terms"),
        ft.ElevatedButton("Register", bgcolor=ft.colors.BLUE),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
])

inspect_flet(form)
```

### Comparing Structures

```python
# Create two interface versions
version1 = create_interface_v1()
version2 = create_interface_v2()

# Export to JSON for comparison
import json

v1_json = json.loads(flet_to_json(version1))
v2_json = json.loads(flet_to_json(version2))

# Use any JSON comparison library
```

### Debugging Interface Issues

```python
def debug_page_structure(page):
    """Function to debug page structure"""
    print("=== PAGE STRUCTURE ===")
    inspect_flet(page, show_properties=True)
    
    print("\n=== BRIEF STRUCTURE ===")
    inspect_flet(page, show_properties=False)
    
    print(f"\n=== TOTAL CONTROLS: {count_controls(page)} ===")

def count_controls(obj):
    """Count total number of controls"""
    data = flet_to_dict(obj)
    
    def count_recursive(item):
        count = 1 if isinstance(item, dict) and 'type' in item else 0
        
        if isinstance(item, dict):
            for value in item.values():
                count += count_recursive(value)
        elif isinstance(item, list):
            for value in item:
                count += count_recursive(value)
        
        return count
    
    return count_recursive(data)

# Usage
debug_page_structure(my_page)
```

## 🛡️ Error Handling

The inspector is resilient to errors and handles:

- Circular references (with depth limitation)
- Missing attributes
- Non-standard data types
- Corrupted objects

```python
try:
    inspect_flet(potentially_broken_object)
except Exception as e:
    print(f"Error analyzing object: {e}")
    # The inspector will continue with remaining objects
```

## 🔄 Compatibility

- **Python**: 3.7+
- **Flet**: All versions
- **Platforms**: Windows, macOS, Linux

## 🤝 Contributing

We welcome contributions to the project!

```bash
# Clone the repository
git clone https://github.com/yourusername/flet-object-inspector.git
cd flet-object-inspector

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Run examples
python examples/basic_usage.py
```

### Project Structure

```
flet-object-inspector/
├── flet_object_inspector/
│   ├── __init__.py
│   └── inspector.py
├── tests/
│   ├── test_basic.py
│   └── test_advanced.py
├── examples/
│   ├── basic_usage.py
│   └── advanced_usage.py
├── README.md
├── setup.py
└── requirements.txt
```

## 📝 License

The project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

