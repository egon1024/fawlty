import os
import importlib

# Get the current directory
current_dir = os.path.dirname(__file__)

# Get a list of all the Python files in the resources directory
file_list = [f for f in os.listdir(current_dir) if f.endswith('.py')]

# Import each module dynamically
for file in file_list:
    # Remove the file extension to get the module name
    module_name = os.path.splitext(file)[0]

    # Import the module
    module = importlib.import_module(f'fawlty.resources.{module_name}')

    # Add the module to the current namespace
    globals()[module_name] = module
