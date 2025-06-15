from typing_extensions import deprecated as deprecated
import warnings
from datetime import date

DEPRECATION_MESSAGE_TEMPLATE = "Deprecated: {reason} | Removal scheduled: {expires_on} (v{version})"

def deprecation_deadline (*, expires_on: date, version: str):
    """Indicate date and version of removal for a deprecated object
    
    This decorator is applied on top of the `deprecated` decorator
    defined in PEP 702 to set deadlines for a compulsory deprecation
    The information thus added is included in the error messages, and
    is also extracted by the deprecation management tooling of the
    codebase.
    
    Usage:

    @deprecation_deadline (expires_on = date (2025, 11, 12), version = "1.29");
    @deprecated ("use class B instead")
    class A: pass

    @deprecation_deadline (expires_on = date (2026, 11, 12), version = "1.30");
    @deprecated ("Use function f instead")
    def g (): pass
    """
    def w (f):
        if not f.__deprecated__:
            raise Exception ('this function is not marked as deprecated')
        err = DEPRECATION_MESSAGE_TEMPLATE.format (f.__deprecated__, expires_on, version)
        f.__deprecated__ = err

        # modifying the displayed deprecation messages
        free_var_names = f.__code__.co_freevars
        free_var_cells = [c for c in f.__closure__]
        msg_cell = free_var_cells [free_var_names.index ('msg')]
        msg_cell.cell_contents = f.__deprecated__ = err
        return f
    return w

def enable_deprecation_warnings():
    warnings.simplefilter('default', DeprecationWarning)

def disable_deprecation_warnings():
    warnings.simplefilter('ignore', DeprecationWarning)
