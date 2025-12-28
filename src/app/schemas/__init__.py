from .Class import Class, InputClassData  # noqa: F401
from .Role import Role  # noqa: F401
from .User import User, InputUserData  # noqa: F401
from .Exercise import Exercise, InputExerciseData  # noqa: F401
from .ExerciseHistory import ExerciseHistory, InputExerciseHistoryData  # noqa: F401

# import glob
# from importlib import import_module
# import os
# from typing import List
# from fastapi import logger

# excluded_files: List[str] = ["__init__.py", "example.py"]
# functions_to_import = ["{}", "Input{}Data"]
# import_path = "src.app.schemas"
# path = import_path.replace(".", os.sep)


# for module in glob.glob(os.path.join(path, "*.py")):
#     file = os.path.split(module)[-1]
#     if file in excluded_files:
#         continue

#     for fname in functions_to_import:
#         fname = fname.format(file[:-3])
#         print(fname)
#         try:
#             globals()[fname] = import_module(f"{import_path}.{file[:-3]}", fname)

#         except AttributeError as e:
#             logger.logger.error(f"Failed to import {file} module's router. - <{e}>")

# print(globals().keys())
