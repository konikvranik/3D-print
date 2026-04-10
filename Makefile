# 3D-print models Makefile
#
# Usage:
#   make                              - build everything
#   make toys/foo.stl                 - build single file
#   make stl / make 3mf / make pdf    - build by type
#   make clean / make list
#
# Pattern rules (the Make way):
#   %.stl: %.scad              OpenSCAD -> STL
#   %.3mf: %.scad              OpenSCAD -> 3MF
#   %.stl: %.py                CadQuery Python -> STL
#   %.3mf: %.py               CadQuery Python -> 3MF
#   %.pdf: %.py                ReportLab Python -> PDF
#
# Output lands next to source: ./toys/foo.scad -> ./toys/foo.stl

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
# Find OpenSCAD: system first, then local AppImage, then auto-download
OPENSCAD_SYSTEM := $(shell openscad --version >/dev/null 2>&1 && echo openscad)
OPENSCAD_LOCAL  := $(shell test -x tools/openscad && echo tools/openscad)
ifdef OPENSCAD_SYSTEM
  OPENSCAD := $(OPENSCAD_SYSTEM)
else ifdef OPENSCAD_LOCAL
  OPENSCAD := $(OPENSCAD_LOCAL)
else
  OPENSCAD := tools/setup_openscad.sh
endif
PYTHON   := .venv/bin/python3

ifneq ($(OPENSCAD),tools/setup_openscad.sh)
$(info Using OpenSCAD: $(OPENSCAD))
endif

# ---------------------------------------------------------------------------
# Source discovery (content-based for Python)
# ---------------------------------------------------------------------------
EXCLUDE  := -not -path './.git/*' -not -path './.venv/*' -not -name 'common.py'

SCAD_SRCS := $(shell find . -name '*.scad' $(EXCLUDE))
ALL_PY    := $(shell find . -name '*.py' $(EXCLUDE))

PY3D_SRCS := $(foreach f,$(ALL_PY),$(shell grep -ql 'cadquery' $(f) && echo $(f)))
PY2D_SRCS := $(foreach f,$(ALL_PY),$(shell grep -ql 'reportlab' $(f) && echo $(f)))
PY3MF_SRCS := $(foreach f,$(ALL_PY),$(shell grep -ql '.3mf' $(f) && echo $(f)))

# Build output lists (same directory as source)
SCAD_STLS := $(SCAD_SRCS:.scad=.stl)
SCAD_3MFS := $(SCAD_SRCS:.scad=.3mf)
PY3D_STLS := $(PY3D_SRCS:.py=.stl)
PY3MF_3MFS := $(patsubst ./%,%,$(PY3MF_SRCS:.py=.3mf))
PY2D_PDFS := $(PY2D_SRCS:.py=.pdf)

# ---------------------------------------------------------------------------
# Pattern rules
# ---------------------------------------------------------------------------

# OpenSCAD -> STL
%.stl: %.scad
	$(OPENSCAD) -o $@ $<

# OpenSCAD -> 3MF
%.3mf: %.scad
	$(OPENSCAD) -o $@ $<

# CadQuery Python -> STL (script self-renders via common.py)
%.stl: %.py
	$(PYTHON) $<

# CadQuery Python -> 3MF
%.3mf: %.py
	$(PYTHON) $<

# ReportLab Python -> PDF
%.pdf: %.py
	$(PYTHON) $<

# ---------------------------------------------------------------------------
# Aggregate targets
# ---------------------------------------------------------------------------
.PHONY: all stl 3mf pdf clean list

all: stl 3mf pdf

stl: $(SCAD_STLS) $(PY3D_STLS)

3mf: $(SCAD_3MFS) $(PY3MF_3MFS)

pdf: $(PY2D_PDFS)

clean:
	find . -name '*.stl' -not -path './.venv/*' -delete
	find . -name '*.3mf' -not -path './.venv/*' -delete
	find . -name '*.pdf' -not -path './.venv/*' -delete

list:
	@echo "=== OpenSCAD -> STL ==="
	@for f in $(SCAD_SRCS); do echo "  $${f%.scad}.stl  <-  $$f"; done
	@echo ""
	@echo "=== OpenSCAD -> 3MF ==="
	@for f in $(SCAD_SRCS); do echo "  $${f%.scad}.3mf  <-  $$f"; done
	@echo ""
	@echo "=== CadQuery Python -> STL ==="
	@for f in $(PY3D_SRCS); do echo "  $${f%.py}.stl  <-  $$f"; done
	@echo ""
	@echo "=== CadQuery Python -> 3MF ==="
	@for f in $(PY3MF_SRCS); do echo "  $${f%.py}.3mf  <-  $$f"; done
	@echo ""
	@echo "=== 2D Template -> PDF ==="
	@for f in $(PY2D_SRCS); do echo "  $${f%.py}.pdf  <-  $$f"; done
