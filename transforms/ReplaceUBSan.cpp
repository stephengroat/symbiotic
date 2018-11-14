//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.

#include <cassert>
#include <vector>
#include <set>

#include "llvm/IR/DataLayout.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/GlobalVariable.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/Module.h"
#include "llvm/Pass.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/TypeBuilder.h"
#if LLVM_VERSION_MAJOR >= 4 || (LLVM_VERSION_MAJOR == 3 && LLVM_VERSION_MINOR >= 5)
  #include "llvm/IR/InstIterator.h"
#else
  #include "llvm/Support/InstIterator.h"
#endif
#include "llvm/Support/raw_ostream.h"
#include "llvm/Transforms/Utils/BasicBlockUtils.h"
#include <llvm/IR/DebugInfoMetadata.h>

using namespace llvm;

namespace {

/** Clone metadata from one instruction to another.
 * If i1 does not contain any metadata, then the instruction
 * that is closest to i1 is picked (we prefer the one that is after
 * and if there is none, then use the closest one before).
 *
 * @param i1 the first instruction
 * @param i2 the second instruction without any metadata
 */
static void CloneMetadata(const llvm::Instruction *i1, llvm::Instruction *i2) {
    if (i1->hasMetadata()) {
        i2->setDebugLoc(i1->getDebugLoc());
        return;
    }

    const llvm::Instruction *metadataI = nullptr;
    bool after = false;
    for (const llvm::Instruction& I : *i1->getParent()) {
        if (&I == i1) {
            after = true;
            continue;
        }

        if (I.hasMetadata()) {
            // store every "last" instruction with metadata,
            // so that in the case that we won't find anything
            // after i1, we can use metadata that are the closest
            // "before" i1
            metadataI = &I;
            if (after)
                break;
        }
    }

    assert(metadataI && "Did not find dbg in any instruction of a block");
    i2->setDebugLoc(metadataI->getDebugLoc());
}


class ReplaceUBSan : public FunctionPass {
  public:
    static char ID;

    ReplaceUBSan() : FunctionPass(ID) {}

    virtual bool runOnFunction(Function &F);
};

bool ReplaceUBSan::runOnFunction(Function &F)
{
  bool modified = false;
  Module *M = F.getParent();
  Constant *ver_err = nullptr;

  for (inst_iterator I = inst_begin(F), E = inst_end(F); I != E;) {
    Instruction *ins = &*I;
    ++I;
    if (CallInst *CI = dyn_cast<CallInst>(ins)) {
      if (CI->isInlineAsm())
        continue;

      const Value *val = CI->getCalledValue()->stripPointerCasts();
      const Function *callee = dyn_cast<Function>(val);
      if (!callee || callee->isIntrinsic())
        continue;

      assert(callee->hasName());
      StringRef name = callee->getName();

      if (!name.startswith("__ubsan_handle"))
        continue;

      if (callee->isDeclaration()) {
        if (!ver_err) {
          LLVMContext& Ctx = M->getContext();
          ver_err = M->getOrInsertFunction("__VERIFIER_error",
                                           Type::getVoidTy(Ctx),
                                           nullptr);
        }

        auto CI2 = CallInst::Create(ver_err);
        CloneMetadata(CI, CI2);

        CI2->insertAfter(CI);
        CI->eraseFromParent();

        modified = true;
      }
    }
  }
  return modified;
}

} // namespace

static RegisterPass<ReplaceUBSan> RUBS("replace-ubsan",
                                       "Replace ubsan calls with calls to __VERIFIER_error");
char ReplaceUBSan::ID;

class ReplaceAsserts : public FunctionPass {
  public:
    static char ID;

    ReplaceAsserts() : FunctionPass(ID) {}

    virtual bool runOnFunction(Function &F);
};

bool ReplaceAsserts::runOnFunction(Function &F)
{
  bool modified = false;
  Module *M = F.getParent();
  Constant *ver_err = nullptr;

  for (inst_iterator I = inst_begin(F), E = inst_end(F); I != E;) {
    Instruction *ins = &*I;
    ++I;
    if (CallInst *CI = dyn_cast<CallInst>(ins)) {
      if (CI->isInlineAsm())
        continue;

      const Value *val = CI->getCalledValue()->stripPointerCasts();
      const Function *callee = dyn_cast<Function>(val);
      if (!callee || callee->isIntrinsic())
        continue;

      if (!callee->isDeclaration())
        continue;

      assert(callee->hasName());
      StringRef name = callee->getName();
      if (!name.equals("__assert_fail"))
        continue;

      if (!ver_err) {
        LLVMContext& Ctx = M->getContext();
        ver_err = M->getOrInsertFunction("__VERIFIER_error",
                                         Type::getVoidTy(Ctx),
                                         nullptr);
      }

      auto CI2 = CallInst::Create(ver_err);
      CloneMetadata(CI, CI2);

      CI2->insertAfter(CI);
      CI->eraseFromParent();

      modified = true;
    }
  }
  return modified;
}

static RegisterPass<ReplaceAsserts> RASS("replace-asserts",
                                         "Replace assert calls with calls to __VERIFIER_error");
char ReplaceAsserts::ID;

