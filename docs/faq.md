# The solution of some problems you may face

## Training
1. **ValueError: empty range for randrange() (0,-12, -12)**

    Your LR image may be smaller than the patch size `"LR_size"` in the training config. You can use [get_patch_size.py](../utils/get_patch_size.py) to get the right patch size for your data.
2. Learning rate drop from 0.0001 to 0.000006 after the first epoch

    Check your Pytorch version. If your pytorch version is newer, you should change `self.scheduler.step(epoch)` to `self.scheduler.step()` in [SRSolver.py](../SRFBN_CVPR19/solvers/SRSolver.py), vice versa.

## Validation and Testing
**RuntimeError: invalid argument 0: Sizes of tensors must match except in dimension 0. Got 1 and 18 in dimension 3 at /opt/conda/conda-bld/pytorch_1579022060824/work/aten/src/THC/generic/THCTensorMath.cu:71**

Set `"use_chop"` in the testing config to `false`

