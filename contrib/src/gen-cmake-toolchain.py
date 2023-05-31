#!/usr/bin/env python3
import os
import argparse

# Argument parsing
parser = argparse.ArgumentParser(
    description="Generate a CMake crossfile based on environment variables")
parser.add_argument('file', type=argparse.FileType('w', encoding='UTF-8'),
    help="output file")
args = parser.parse_args()

# Helper to add env variable value to crossfile
def _add_environ_val(meson_key, env_key):
    env_value = os.environ.get(env_key)
    if env_value != None:
        if " " in env_value:
            args.file.write("set({} \"{}\")\n".format(meson_key, env_value))
        else:
            args.file.write("set({} {})\n".format(meson_key, env_value))

def _add_environ_val_not_empty(meson_key, env_key):
    env_value = os.environ.get(env_key)
    if env_value != None and env_value != '':
        args.file.write("set({} {})\n".format(meson_key, env_value))


# Generate meson crossfile
args.file.write("# CMake toolchain automatically generated by contrib makefile\n")

# Binaries section
_add_environ_val('CMAKE_BUILD_TYPE', 'BUILD_TYPE')
_add_environ_val('CMAKE_SYSTEM_PROCESSOR', 'HOST_ARCH')
_add_environ_val_not_empty('CMAKE_SYSTEM_NAME', 'SYSTEM_NAME')
_add_environ_val('CMAKE_RC_COMPILER', 'RC_COMPILER')
_add_environ_val('CMAKE_RANLIB', 'RANLIB')
_add_environ_val('CMAKE_AR', 'AR')

_add_environ_val('CMAKE_OSX_SYSROOT', 'OSX_SYSROOT')

# we should not have to set this
_add_environ_val('_CMAKE_TOOLCHAIN_PREFIX', 'TOOLCHAIN_PREFIX')

_add_environ_val('CMAKE_C_COMPILER', 'CC')
_add_environ_val('CMAKE_CXX_COMPILER', 'CXX')

_add_environ_val('CMAKE_C_SYSROOT_FLAG', 'C_SYSROOT_FLAG')
_add_environ_val('CMAKE_CXX_SYSROOT_FLAG', 'CXX_SYSROOT_FLAG')


_add_environ_val('CMAKE_FIND_ROOT_PATH', 'PREFIX')

_add_environ_val('CMAKE_FIND_ROOT_PATH', 'FIND_ROOT_PATH')
args.file.write("set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)\n")
_add_environ_val('CMAKE_FIND_ROOT_PATH_MODE_LIBRARY', 'PATH_MODE_LIBRARY')
_add_environ_val('CMAKE_FIND_ROOT_PATH_MODE_INCLUDE', 'PATH_MODE_INCLUDE')

# final includes
env_value = os.environ.get('EXTRA_INCLUDE')
if env_value != None and env_value != '':
    args.file.write("include({})\n".format(env_value))

