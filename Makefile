# 3D-print models Makefile
#
# Usage:
#   make                              - build everything
#   make out/toys/foo.stl             - build single file
#   make stl / make 3mf / make pdf    - build by type
#   make clean / make list
#
# Pattern rules (the Make way):
#   out/%.stl: %.scad          OpenSCAD -> STL
#   out/%.3mf: %.scad          OpenSCAD -> 3MF
#   out/%.stl: %.py            CadQuery Python -> STL
#   out/%.pdf: %.py            ReportLab Python -> PDF
#
# Output mirrors source: ./toys/foo.scad -> ./out/toys/foo.stl

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
OPENSCAD := openscad
PYTHON   := .venv/bin/python3

# ---------------------------------------------------------------------------
# Source discovery (content-based for Python)
# ---------------------------------------------------------------------------
EXCLUDE  := -not -path './.git/*' -not -path './.venv/*' -not -name 'common.py'

SCAD_SRCS := $(shell find . -name '*.scad' $(EXCLUDE))
ALL_PY    := $(shell find . -name '*.py' $(EXCLUDE))

PY3D_SRCS := $(foreach f,$(ALL_PY),$(shell grep -ql 'cadquery' $(f) && echo $(f)))
PY2D_SRCS := $(foreach f,$(ALL_PY),$(shell grep -ql 'reportlab' $(f) && echo $(f)))

# Build output lists
SCAD_STLS := $(SCAD_SRCS:.scad=.stl)
SCAD_3MFS := $(SCAD_SRCS:.scad=.3mf)
PY3D_STLS := $(PY3D_SRCS:.py=.stl)
PY2D_PDFS := $(PY2D_SRCS:.py=.pdf)

# Prepend out/ to all outputs
SCAD_STLS := $(patsubst ./%,out/%,$(SCAD_STLS))
SCAD_3MFS := $(patsubst ./%,out/%,$(SCAD_3MFS))
PY3D_STLS := $(patsubst ./%,out/%,$(PY3D_STLS))
PY2D_PDFS := $(patsubst ./%,out/%,$(PY2D_PDFS))

# ---------------------------------------------------------------------------
# Pattern rules
# ---------------------------------------------------------------------------

# OpenSCAD -> STL
out/%.stl: %.scad
	@mkdir -p $(dir $@)
	$(OPENSCAD) -o $@ $<

# OpenSCAD -> 3MF
out/%.3mf: %.scad
	@mkdir -p $(dir $@)
	$(OPENSCAD) -o $@ $<

# CadQuery Python -> STL (script self-renders via common.py)
out/%.stl: %.py
	@mkdir -p $(dir $@)
	$(PYTHON) $<

# ReportLab Python -> PDF (run script, move PDF to out/)
out/%.pdf: %.py
	@mkdir -p $(dir $@)
	$(PYTHON) $<
	@mv $(dir $<)$(notdir $@) $(dir $@) 2>/dev/null || true

# ---------------------------------------------------------------------------
# Aggregate targets
# ---------------------------------------------------------------------------
.PHONY: all stl 3mf pdf clean list

all: stl 3mf pdf

stl: $(SCAD_STLS) $(PY3D_STLS)

3mf: $(SCAD_3MFS)

pdf: $(PY2D_PDFS)

clean:
	rm -rf out

list:
	@echo "=== OpenSCAD -> STL ==="
	@for f in $(SCAD_SRCS); do echo "  out/$${f#./}"  | sed 's/\.scad/.stl/'; done
	@echo ""
	@echo "=== OpenSCAD -> 3MF ==="
	@for f in $(SCAD_SRCS); do echo "  out/$${f#./}"  | sed 's/\.scad/.3mf/'; done
	@echo ""
	@echo "=== CadQuery Python -> STL ==="
	@for f in $(PY3D_SRCS); do echo "  out/$${f#./}" | sed 's/\.py/.stl/'; done
	@echo ""
	@echo "=== 2D Template -> PDF ==="
	@for f in $(PY2D_SRCS); do echo "  out/$${f#./}" | sed 's/\.py/.pdf/'; done
