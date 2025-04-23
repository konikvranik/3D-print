import cadquery as cq


def render(object, fname, tolerance=0.0001, angularTolerance=0.1):
    # Check if show_object is available (for CQ-editor)
    if 'show_object' not in globals():
        def show_object(*args, **kwargs):
            pass

    show_object(object)

    # Export the model to STL
    cq.exporters.export(object, fname, None, tolerance, angularTolerance)
