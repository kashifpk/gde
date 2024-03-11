"Dynamic imports related utility code"

import importlib


# A function to dynamically import a module where the full package and module
# path is given as a string argument to the function.
# Returns the actual module
def import_module(module_path):
    module_name = module_path.rsplit(".", 1)[0]
    class_name = module_path.rsplit(".", 1)[1]
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
