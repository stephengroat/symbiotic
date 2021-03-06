#!/usr/bin/python

from . property import get_property

class SymbioticOptions(object):
    def __init__(self, env):
        # source codes
        self.sources = []

        self.tool_name = 'klee'
        self.is32bit = False
        self.stats = False
        self.generate_ll = False
        # properties mapped to our names
        self.property = get_property(env.symbiotic_dir, None)
        self.noslice = False
        self.malloc_never_fails = False
        self.noprepare = False
        self.explicit_symbolic = False
        self.undef_retval_nosym = False
        self.undefined_are_pure = False
        # link all that we have by default
        self.linkundef = ['svcomp', 'verifier', 'libc', 'posix', 'kernel']
        self.timeout = 0
        self.add_libc = False
        self.no_lib = False
        self.require_slicer = False
        self.no_optimize = False
        self.no_verification = False
        self.final_output = None
        self.witness_output = '{0}/witness.graphml'.format(env.symbiotic_dir)
        self.source_is_bc = False
        self.optlevel = ["before-O3", "after-O3"]
        self.slicer_pta = 'fi'
        self.slicing_criterion = '__assert_fail,__VERIFIER_error'
        self.memsafety_config_file = 'config.json'
        self.overflow_config_file = 'config.json'
        self.repeat_slicing = 1
        self.dont_exit_on_error = False
        # these files will be linked unconditionally
        self.link_files = []
        # additional parameters that can be passed right
        # to the slicer and symbolic executor
        self.slicer_cmd = ['sbt-slicer']
        self.slicer_params = []
        self.tool_params = []
        # these llvm passes will not be run in the optimization phase
        self.disabled_optimizations = []
        self.CFLAGS = []
        self.CPPFLAGS = []
        self.devel_mode = False
        self.instrumentation_files_path = None
        self.nowitness = False
        # try to automatically find paths with common header files
        self.search_include_paths = False
        # flag for checking overflows with clang sanitizer
        self.overflow_with_clang = False
        # replay error path
        self.replay_error = False
