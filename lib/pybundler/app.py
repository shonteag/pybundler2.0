#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from os.path import join, abspath, dirname, basename, isdir, isfile
import argparse

#------------------------------------------------------------------------------
# pybundler
# Copyright 2015 Shonte Amato-Grill
# MIT License
#------------------------------------------------------------------------------
def setup_bundle(args):
    """
    step 1
    outputs a .bundle file used as config for building
    """
    from pybundler.build import bundle
    from pybundler.build import build

    # fix --name
    if args.name == "":
        args.name = basename(args.target_path)
    # fix --toplevel
    if args.toplevel == "":
        args.toplevel = args.name

    bundle_file = join(args.workdir, args.name) + ".bundle"
    if isfile(bundle_file):
        if args.clean:
            os.remove(bundle_file)
        else:
            ans = raw_input("pybundler detected a previous bundle. overwrite? (Y/n) ")
            if str(ans).lower() == "y":
                os.remove(bundle_file)
            else:
                print "build terminated."
                sys.exit(0)

    build_config = bundle(args.target_path,
                          bundle_file, args.toplevel,
                          args.name, args.workdir,
                          args.exn, args.ext, args.exf)

    if args.build:
        build(build_config, args.workdir)


def setup_build(args):
    """
    step 2
    outputs a .sh/.bash file to be distributed
    """
    from pybundler.build import build


def main_bundle():
    # entry for BUILD ONLY!
    # utf8 support
    reload(sys)
    sys.setdefaultencoding("utf-8")

    def parse_name(inv):
        return list(inv.replace(" ", "").split(","))
    def parse_ext(inv):
        return list(inv.replace(" ", "").replace(".", "").split(","))

    parser = argparse.ArgumentParser(
        description = "STEP 1: shell tool for pre-building a packaged environment",
        epilog = """Entry point into pybundler module which provides 'building'
functionality to user.  Creates a '.bundle' file, which is a json of all the 
details needed to create an bundled 'installer' for the targeted environment.

This is usually considered STEP 1."""
    )

    dircontrol = parser.add_argument_group('directory control')
    dircontrol.add_argument('--workdir',
                            action="store", default=abspath(join(os.getcwd(), 'pybundler.work')),
                            help="specify the work/output directory. defaults to `%(default)s` (CWD)")
    dircontrol.add_argument('--clean',
                            action="store_true", default=False,
                            help="direct pybundler to overwrite .bundle and distribution files of matching names.\
                                  defaults to %(default)s")
    dircontrol.add_argument('--toplevel',
                            action="store", default="",
                            help="after bundling, rename top level directory")

    projectcontrol = parser.add_argument_group('bundle control')
    projectcontrol.add_argument('-n', '--name',
                                action="store", default="",
                                help="set the name of this bundle. defaults to basename of target")
    projectcontrol.add_argument('--exn',
                                type=parse_name, default=[],
                                help="file names to excude from bundle. if more than one, use quotations\
                                and separate with a comma. \n--exn=\"f1, f2\"")
    projectcontrol.add_argument('--exf',
                                type=parse_name, default=[],
                                help="folder names to exclude from bundle. if more than one, use quotations\
                                and separate with a comma. \n--exf=\".git, temp, env\"")
    projectcontrol.add_argument('--ext',
                                type=parse_ext, default=[],
                                help="file extensions to exclude from bundle. if more than one, use quotations\
                                and separate with a comma. \n--ext=\".txt, .log\"")

    actioncontrol = parser.add_argument_group('action control')
    actioncontrol.add_argument('--build',
                               action="store_true", default=False,
                               help="tell pybundler to automatically begin building after bundle \
                               operation is complete. defaults to %(default)s")

    parser.add_argument('target_path',
                        action="store",
                        help="tell pybundler to bundle this path as the target")


    args = parser.parse_args()
    setup_bundle(args)


def main_build():
    # entry for BUNDLE ONLY!

    # utf8 support
    reload(sys)
    sys.setdefaultencoding("utf-8")

    parser = argparse.ArgumentParser(
        description = "STEP 2: shell tool for bundling a pre-built environment",
        epilog = """Entry point into pybundler module which provides 'bundling'
functionality to user.  Takes a '.bundle' file as input (generated by 'pybundler-build'
command), and generates the desired executable script for recreation of the environment.

This is usually considered STEP 2."""
    )

    args = parser.parse_args()



# Application start
def main():
    # main entry point
    reload(sys)
    sys.setdefaultencoding("utf-8")

    from pybundler import settings

    parser = argparse.ArgumentParser(
        description = "A python module for creating 'installation' scripts for\
                       bundled project directories.",
        epilog = """To use, please see entry-points: `pybundler-bundle` and
`pybundler-build` (step 1 and 2, respectively)."""
    )

    parser.add_argument("--version",
                        action="version", version="{0} {1}.{2}.{3}".format(
                            settings.app_name,
                            settings.major_version,
                            settings.minor_version,
                            settings.patch_version))

    args = parser.parse_args()
    sys.exit(0)

if __name__ == '__main__':
    main()