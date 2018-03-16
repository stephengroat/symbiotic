#!/usr/bin/python

import argparse

class SymbioticOptions(argparse.Namespace):
    def __init__(self, symbiotic_dir=None):
        if symbiotic_dir is None:
            from . utils.utils import get_symbiotic_dir
            symbiotic_dir = get_symbiotic_dir()

       ## properties as we get then on input
       #self.orig_prp = []
       ## properties mapped to our names
       #self.prp = []
       #self.prpfile = None
       #self.noprepare = False
       #self.undef_retval_nosym = False
       ## link all that we have by default
       #self.linkundef = ['verifier', 'libc', 'posix', 'kernel']

       ## KLEE specific
       #self.add_libc = False
       #self.no_lib = False
       #self.source_is_bc = False
       #self.optlevel = ["before-O3", "after-O3"]
       #self.dont_exit_on_error = False
       ## these files will be linked unconditionally
       #self.link_files = []
       ## additional parameters that can be passed right
       ## to the slicer and symbolic executor
       #self.tool_params = []
       ## these llvm passes will not be run in the optimization phase
       #self.disabled_optimizations = []

       #self.devel_mode = False
       ## properties as we get then on input
       #self.orig_prp = []
       ## properties mapped to our names
       #self.prp = []
       #self.prpfile = None
       #self.undef_retval_nosym = False
       #self.undefined_are_pure = False
       ## link all that we have by default
       #self.linkundef = ['verifier', 'libc', 'posix', 'kernel']


def add_compile_opts(parser):
    parser.add_argument("--cppflags", action="append",
                        default=[], dest="CPPFLAGS")
    parser.add_argument("--cflags", action="append",
                        default=[], dest="CFLAGS")

    parser.add_argument("--bc", action="store_true",
                        dest="source_is_bc",
                        help="The (only) input source is already bitcode")


def add_generic_opts(parser):
    parser.add_argument('--timeout', metavar='T', type=int,
                        default=0)

    parser.add_argument("--malloc-never-fails", action="store_true",
                        help="Assume that dynamic memory allocation never fails")

    #FIXME: rename this option
    parser.add_argument("--no-prepare", action="store_true", dest="noprepare",
                        help="Do not run prepare phase")

    parser.add_argument("--32", action="store_true", dest="is32bit",
                        help="Do not run prepare phase")

    parser.add_argument("--explicit-symbolic", action="store_true",
                        help="Do not make uninitialized data symbolic")

    parser.add_argument("--no-optimize", action="store_true",
                        help="Do not optimize the bitcode")

    parser.add_argument("--undefined-are-pure", action="store_true",
                        default=True,
                        help="Assume that undefined functions are pure")

    parser.add_argument("--no-verification", action="store_true",
                        help="Only apply transformations do not run verifier")

    parser.add_argument("--verifier", default="klee", dest="tool_name",
                        help="Verifier to use, default=klee")

    parser.add_argument("--output", dest="final_output",
                        help="The output name of the file after all transformations")

    parser.add_argument('--witness', dest="witness_output",
                        default='{0}/witness.graphml'.format(symbiotic_dir))








def add_slicer_opts(parser):
    parser.add_argument('--no-slice', action='store_true', dest='noslice',
                        help='Do not slice the code')
    parser.add_argument('--pta', choices=['fi', 'fs'], dest='pta',
                        default='fi', help='Pointer analysis to use: fs, fi')

    parser.add_argument('--slicing-criterion', dest='criteria',
                        action='append',
                        default=['__assert_fail', '__VERIFIER_error'],
                        help='Slicing criterion (a function call-site), can be used multiple times. Default={__VERIFIER_error, __assert_fail}')

    parser.add_argument('--repeat-slicing', metavar='N', type=int, dest='repeat_num',
                        default=1,
                        help='Repeat slicing N times, default=1')

    parser.add_argument('--slicer-params', dest='params',
                        action='append',
                        #default=[],
                        help='Extra parameters passed to slicer')


def add_instr_opts(parser):
       parser.add_argument('--memsafety-config-file', default="config.json",
                           help="Configuration file for memsafety instrumentation")
       parser.add_argument("--instrumentation-files-path")


descr =\
"""
Symbiotic
"""
class SymbioticOptionsParser:
    def __init__(self):
        self._argparser = argparse.ArgumentParser(descr)

        # register arguments
        add_generic_opts(self._argparser)
        add_slicer_opts(self._argparser)
        add_instr_opts(self._argparser)
        add_compile_opts(self._argparser)

    def parse_env(self, options):
        pass

    def parse(self):
        nmspace = SymbioticOptions()
        options = self._argparser.parse_args(namespace=nmspace)
        self.parse_env(options)

        return options
