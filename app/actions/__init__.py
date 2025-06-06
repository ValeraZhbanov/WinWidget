import inspect
from importlib import import_module
from pathlib import Path
from app.core.base_action import BaseAction


actions = [
    obj
    for module_name in [
        f.stem 
        for f in Path(__file__).parent.glob("*.py") 
        if f.is_file() and f.stem != "__init__"
    ]
    for _, obj in inspect.getmembers(import_module(f".{module_name}", package=__package__), inspect.isclass)
    if issubclass(obj, BaseAction) and obj is not BaseAction
]
