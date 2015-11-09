#!/usr/bin/env python
# encoding: utf-8

import os
from os.path import join, abspath, dirname, isdir, isfile, basename
import sys
import time
import base64
import json

reload(sys)
sys.setdefaultencoding("utf-8")


# minor helper methods
def _write(msg, newline=True):
    sys.stdout.write(msg)
    if newline:
        sys.stdout.write("\n")
    sys.stdout.flush()


def _build_directory_structure_string(structure):
    """
    builds and returns a formatted string of pre-built
    project directory structure
    """
    def _recurse_dic(dic, level, prefix, buf):
        idx = 0
        for key, value in dic.items():
            idc = "┣━"
            if idx == len(dic.keys()) - 1:
                idc = "┗━"
            if level == 0:
                idc = ""

            if isinstance(value, dict):
                buf.append("{0}{1}[{2}]".format(prefix, idc, key))
                if len(dic.keys()) > 1 and idx != len(dic.keys()) - 1:
                    tmp_prefix = prefix + "┃  "
                else:
                    tmp_prefix = prefix + "    "
                _recurse_dic(value, level + 1, tmp_prefix, buf)
            else:
                buf.append("{0}{1}{2}".format(prefix, idc, key))

            idx += 1

    buf = []
    _recurse_dic(structure, 0, "", buf)
    return "\n".join(buf)


# main methods
def bundle(target_path,
           bundle_path,
           toplevel,
           name, workdir,
           exn, ext, exf,
           showtree=True):
    """
    step 1
    create the .bundle file (json format)
    """
    _start_time = time.time()

    def _build_directory_structure(project_root, exn, ext, exf):
        """
        STEP 1.1: Walk the target directory. Build file/dir
        list excluding exn, ext, and exf entries where applicable.
        """
        structure = {}
        num_file = 0
        num_dir = 0

        num_file_exc = 0
        num_dir_exc = 0

        total_size = 0

        root = project_root.rstrip(os.sep)
        start = root.rfind(os.sep) + 1
        for path, dirs, files in os.walk(root):
            # excludes
            for dn in dirs:
                if dn in exf:
                    dirs.remove(dn)
                    num_dir_exc += 1
            for fn in files:
                if fn in exn:
                    files.remove(fn)
                    num_file_exc += 1
            for fn in files:
                extension = fn.split('.')[-1]
                if extension in ext:
                    files.remove(fn)
                    num_file_exc += 1

            folders = path[start:].split(os.sep)
            subdir = dict.fromkeys(files)

            num_file += len(files)
            num_dir += len(dirs)

            # coalate data on files
            for fn in files:
                full_path = os.path.join(path, fn)
                total_size += os.stat(full_path).st_size
                with open(full_path, 'rb') as f:
                    # get byte data
                    _tmp_data = f.read()
                    # get md5 checksum
                    # encode byte-stream to base64. installer will decode.
                    subdir[fn] = base64.b64encode(_tmp_data)

            # add to structure dict
            parent = reduce(dict.get, folders[:-1], structure)
            parent[folders[-1]] = subdir

        return structure, num_dir, num_file, (num_dir_exc, num_file_exc), total_size

    _write("build")
    _write("  directory structure ... ", False)
    structure, num_dir, num_file, exc, size = _build_directory_structure(target_path, exn, ext, exf)
    _write("ok.")
    _write("    found {0} directories, {1} files; {2:.2f}Mb ({3} bytes)".format(num_dir, num_file, float(size)/1000.0, size))
    _write("    (excluded {0} dir, {1} files)".format(exc[0], exc[1]))

    # rename the toplevel
    structure[toplevel] = structure[basename(target_path)]
    del structure[basename(target_path)]

    # write out the tree
    if showtree:
        _write("structure:")
        _write("{0}".format(_build_directory_structure_string(structure)))

    # construc the config dict
    build_config = {
        "project_root": abspath(target_path),
        "toplevel_rename": toplevel,
        "project_name": name,
        "excludes": {
            "exn": exn,
            "ext": ext,
            "exf": exf
        },
        "num_file": num_file,
        "num_dir": num_dir,
        "bytesize": size,
        "structure": structure
    }

    # dump the .bundle file as a json config
    _write("  writing project config to {0} ... ".format(bundle_path), False)
    with open(bundle_path, 'w') as f:
        json.dump(build_config, f,
                  sort_keys=True,
                  ensure_ascii=False,
                  indent=4)
    _write("ok")
    _write("build completed, {0:.2f} seconds".format(time.time() - _start_time))

    return build_config


def build(build_config,
          workdir):
    """
    step 2
    """
    pass