#!/usr/bin/python


class SlicerOptions:
    def __init__(self):
        self.pta = 'fi'
        self.criterion = '__assert_fail,__VERIFIER_error'
        self.repeat_num = 1
        self.params = []

class SymbioticOptions(object):
    def __init__(self, symbiotic_dir=None):
        if symbiotic_dir is None:
            from . utils.utils import get_symbiotic_dir
            symbiotic_dir = get_symbiotic_dir()

        self.slicer = SlicerOptions()

        self.tool_name = 'klee'
        self.is32bit = False
        # properties as we get then on input
        self.orig_prp = []
        # properties mapped to our names
        self.prp = []
        self.prpfile = None
        self.malloc_never_fails = False
        self.noprepare = False
        self.explicit_symbolic = False
        self.undef_retval_nosym = False
        self.undefined_are_pure = False
        # link all that we have by default
        self.linkundef = ['verifier', 'libc', 'posix', 'kernel']
        self.timeout = 0
        self.add_libc = False
        self.no_lib = False
        self.no_optimize = False
        self.noslice = False
        self.no_verification = False
        self.final_output = None
        self.witness_output = '{0}/witness.graphml'.format(symbiotic_dir)
        self.source_is_bc = False
        self.optlevel = ["before-O3", "after-O3"]
        self.memsafety_config_file = 'config.json'
        self.dont_exit_on_error = False
        # these files will be linked unconditionally
        self.link_files = []
        # additional parameters that can be passed right
        # to the slicer and symbolic executor
        self.tool_params = []
        # these llvm passes will not be run in the optimization phase
        self.disabled_optimizations = []
        self.CFLAGS = []
        self.CPPFLAGS = []
        self.devel_mode = False
        self.instrumentation_files_path = None

