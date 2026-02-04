# AGENTS.md

This file provides guidance for AI coding agents working with this 3D-print models codebase.

## Project Overview

3D printing models repository using Python and CadQuery for parametric CAD design. Contains models for smart home devices, storage solutions, hydroponics, toys, and various practical items.

- **Language**: Python 3.10+
- **Main Library**: CadQuery (Python-based CAD modeling)
- **Output Formats**: STL, STEP, 3MF, DXF
- **CAD Tool**: OpenSCAD (.scad files) also present

## Running Scripts

### Execute Python Models
```bash
# Run from repository root
python3 script_name.py

# Run specific model
python3 smarthome/reolink_zvonek.py
python3 hydroponie/controller_case.py

# Models auto-generate .stl files in the same directory
```

### Virtual Environment (if present)
```bash
source .venv/bin/activate  # Activate if .venv exists
python script_name.py
deactivate  # When done
```

### OpenSCAD Models
```bash
# Render .scad files using OpenSCAD CLI
openscad -o output.stl input.scad
```

## Code Style Guidelines

### Language & Encoding
- **Language**: English for all code, comments, and documentation
- **Encoding**: UTF-8 (use `# -*- coding: utf-8 -*-` if non-ASCII characters needed)
- **Line length**: 120 characters (enforced by .clang-format)

### Imports
- **Order**: Standard library → Third-party → Local modules
- **CadQuery**: Always `import cadquery as cq`
- **Common utilities**: `from common import render, calculate_pla_bore_diameter`
- **Separate sections**: Blank line between import groups

```python
import os
import sys

import cadquery as cq
from cadquery import Workplane, Assembly

from common import render
```

### Naming Conventions
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `WALL_THICKNESS = 1`)
- **Variables**: `snake_case` (e.g., `screw_hole = 4`)
- **Functions**: `snake_case` (e.g., `def build_case():`)
- **Files**: `snake_case.py` (e.g., `reolink_zvonek.py`)
- **Global workplane**: Use `wp` for CadQuery Workplane objects

### Types & Documentation
- **Type hints**: Use for function parameters and returns
  ```python
  def calculate_pla_bore_diameter(screw_diameter: float) -> float:
  ```
- **Docstrings**: Google style for functions
  ```python
  def function(arg1: type) -> return_type:
      """
      Brief description.

      More detailed explanation if needed.

      Args:
          arg1: Description of argument.

      Returns:
          Description of return value.
      """
  ```

### Code Structure
- **Constants first**: Define all measurements and constants at top of file
- **Helper functions**: Define before main workflow
- **Main pattern**: Use standard Python main pattern
  ```python
  def main():
      """Main workflow."""
      result = build_something()
      render(result, 'output_file.stl')

  if __name__ == "__main__":
      main()
  ```

### CadQuery Patterns
- **Workplane variable**: Commonly use global `wp` or pass as parameter
- **Chaining**: CadQuery uses method chaining extensively
  ```python
  wp = (wp.moveTo(x, y)
        .circle(radius)
        .extrude(height)
        .faces(">Z").workplane()
        .rect(width, height)
        .cutBlind(-depth))
  ```
- **Face selection**: Use `>Z`, `<X`, `>Y[-2]` notation for selecting faces
- **Centered parameters**: Explicit `centered=[True, False, False]` for clarity

### Common Utilities (common.py)
- **render()**: Auto-exports to STL with optional filename
- **calculate_pla_bore_diameter()**: Calculates pilot hole for screws in PLA
- **build_toothed_cylinder()**: Creates gear-like toothed cylinders

### Error Handling
- **No exceptions needed**: Most scripts are simple generators
- **Validation**: Add assertions for critical measurements if needed
- **Comments**: Explain complex geometric operations in Czech or English

### Comments
- **Language**: English preferred, Czech acceptable for domain-specific terms
- **Document intent**: Explain WHY, not WHAT the code does
- **Measurements**: Comment physical dimensions and their source
  ```python
  TTGO_WIDTH = 25.7  # Measured from TTGO board datasheet
  ```

## Project Structure

```
/
├── common.py              # Shared utilities (render, calculations)
├── smarthome/            # Smart home device cases
├── hydroponie/           # Hydroponics components
├── storage/              # Storage and organization
├── toys/                 # Toy parts and accessories
├── 3D_printer_stuff/     # 3D printer accessories
├── mazda6/               # Car parts
└── *.py, *.scad         # Individual model scripts
```

## Testing

No formal test framework is currently used. Models are verified by:
1. Visual inspection in CQ-editor
2. STL file generation without errors
3. Physical print testing

## Output Files

Generated files are gitignored:
- `*.stl` - 3D model output
- `*.step` - CAD exchange format
- `*.3mf` - 3D manufacturing format
- `*.gcode` - Printer instructions

## Best Practices

1. **Measurements**: Define all dimensions as constants at file top
2. **Tolerances**: Add clearance for 3D printing (typically 0.2mm)
3. **Screw holes**: Use `calculate_pla_bore_diameter()` for proper sizing
4. **Wall thickness**: Minimum 1mm for PLA, 1.5mm+ for structural parts
5. **Render always**: Every script should call `render()` to generate output
6. **Descriptive names**: Use clear variable names reflecting physical parts
7. **Comments for math**: Explain geometric calculations and formulas

## Common Pitfalls

- ❌ Forgetting to call `render()` at end of script
- ❌ Using exact screw diameter without bore compensation
- ❌ Insufficient wall thickness (<1mm) causing print failures
- ❌ Not accounting for 3D printer tolerances (±0.1-0.2mm)
- ❌ Over-complex models that are slow to render

## Dependencies

Install CadQuery:
```bash
pip install cadquery
# Or for full development environment
pip install cadquery[dev]
```

## Notes for Agents

- This is a personal hobby project focused on practical 3D printable designs
- Code prioritizes simplicity and clarity over performance
- Physical printability is more important than code elegance
- Test renders before committing to ensure STL generation works
