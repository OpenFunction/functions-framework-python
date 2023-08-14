# Copyright 2023 The OpenFunction Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import importlib.util
import inspect
import json
import os
import sys
import types

from functions_framework.context.function_context import FunctionContext
from functions_framework.context.user_context import UserContext
from functions_framework.exceptions import (
    InvalidConfigurationException,
    InvalidFunctionSignatureException,
    InvalidTargetTypeException,
    MissingTargetException,
)

DEFAULT_SOURCE = os.path.realpath("./main.py")

FUNCTION_SIGNATURE_TYPE = "FUNCTION_SIGNATURE_TYPE"
FUNC_CONTEXT = "FUNC_CONTEXT"
HTTP_SIGNATURE_TYPE = "http"
CLOUDEVENT_SIGNATURE_TYPE = "cloudevent"
BACKGROUNDEVENT_SIGNATURE_TYPE = "event"

# REGISTRY_MAP stores the registered functions.
# Keys are user function names, values are user function signature types.
REGISTRY_MAP = {}


# Default function signature rule.
def __function_signature_rule__(context: UserContext):
    pass


FUNCTION_SIGNATURE_RULE = inspect.signature(__function_signature_rule__)


def get_user_function(source, source_module, target):
    """Returns user function, raises exception for invalid function."""
    # Extract the target function from the source file
    if not hasattr(source_module, target):
        raise MissingTargetException(
            "File {source} is expected to contain a function named {target}".format(
                source=source, target=target
            )
        )
    function = getattr(source_module, target)
    # Check that it is a function
    if not isinstance(function, types.FunctionType):
        raise InvalidTargetTypeException(
            "The function defined in file {source} as {target} needs to be of "
            "type function. Got: invalid type {target_type}".format(
                source=source, target=target, target_type=type(function)
            )
        )

    if FUNCTION_SIGNATURE_RULE != inspect.signature(function):
        raise InvalidFunctionSignatureException(
            "The function defined in file {source} as {target} needs to be of "
            "function signature {signature}, but got {target_signature}".format(
                source=source,
                target=target,
                signature=FUNCTION_SIGNATURE_RULE,
                target_signature=inspect.signature(function),
            )
        )

    return function


def load_function_module(source):
    """Load user function source file."""
    # 1. Extract the module name from the source path
    realpath = os.path.realpath(source)
    directory, filename = os.path.split(realpath)
    name, extension = os.path.splitext(filename)
    # 2. Create a new module
    spec = importlib.util.spec_from_file_location(
        name, realpath, submodule_search_locations=[directory]
    )
    source_module = importlib.util.module_from_spec(spec)
    # 3. Add the directory of the source to sys.path to allow the function to
    # load modules relative to its location
    sys.path.append(directory)
    # 4. Add the module to sys.modules
    sys.modules[name] = source_module
    return source_module, spec


def get_function_source(source):
    """Get the configured function source."""
    source = source or os.environ.get("FUNCTION_SOURCE", DEFAULT_SOURCE)
    # Python 3.5: os.path.exist does not support PosixPath
    source = str(source)
    return source


def get_function_target(target):
    """Get the configured function target."""
    target = target or os.environ.get("FUNCTION_TARGET", "")
    # Set the environment variable if it wasn't already
    os.environ["FUNCTION_TARGET"] = target
    if not target:
        raise InvalidConfigurationException(
            "Target is not specified (FUNCTION_TARGET environment variable not set)"
        )
    return target


def get_func_signature_type(func_name: str, signature_type: str) -> str:
    """Get user function's signature type.

    Signature type is searched in the following order:
        1. Decorator user used to register their function
        2. --signature-type flag
        3. environment variable FUNCTION_SIGNATURE_TYPE
    If none of the above is set, signature type defaults to be "http".
    """
    registered_type = REGISTRY_MAP[func_name] if func_name in REGISTRY_MAP else ""
    sig_type = (
        registered_type
        or signature_type
        or os.environ.get(FUNCTION_SIGNATURE_TYPE, HTTP_SIGNATURE_TYPE)
    )
    # Set the environment variable if it wasn't already
    os.environ[FUNCTION_SIGNATURE_TYPE] = sig_type
    # Update signature type for legacy GCF Python 3.7
    if os.environ.get("ENTRY_POINT"):
        os.environ["FUNCTION_TRIGGER_TYPE"] = sig_type
    return sig_type


def get_openfunction_context(func_context: str) -> FunctionContext:
    """Get openfunction context"""
    context_str = func_context or os.environ.get(FUNC_CONTEXT)

    if context_str:
        context = FunctionContext.from_json(json.loads(context_str))
        return context

    return None
