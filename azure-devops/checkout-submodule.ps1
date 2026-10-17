# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

[CmdletBinding(PositionalBinding=$false)]
Param(
  [Parameter(Mandatory)][ValidateSet('llvm-project', 'boost-math', 'benchmarks/google-benchmark')][String]$submodule
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

git submodule update --init --force --no-fetch --filter=tree:0 --depth=1 -- $submodule
git -C $submodule clean --quiet -x -d -f -f
