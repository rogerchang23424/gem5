# Copyright (c) 2022 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os

from testlib import *
from testlib.configuration import constants
from testlib.helper import (
    diff_out_file,
    joinpath,
)

if config.bin_path:
    resource_path = config.bin_path
else:
    resource_path = joinpath(absdirpath(__file__), "..", "resources")


class MatchExitCode(verifier.Verifier):
    """
    Looking for a match between a regex pattern and the content of a list
    of files. Verifier will pass as long as the pattern is found in at least
    one of the files.
    """

    def __init__(self):
        super().__init__()
        self.exit_code = 0

    def parse_file(self, fname):
        if not os.path.exists(fname):
            return False

        with open(fname, "rb") as file_:
            code = ord(file_.read(1))
            return code == self.exit_code

    def test(self, params):
        fixtures = params.fixtures
        # Get the file from the tempdir of the test.
        tempdir = fixtures[constants.tempdir_fixture_name].path

        fname = "exitcode"
        if self.parse_file(joinpath(tempdir, fname)):
            return  # Success

        test_util.fail("Could not match exit code.")


# The following lists the RISCV binaries. Those commented out presently result
# in a test failure. This is outlined in the following Jira issue:
# https://gem5.atlassian.net/browse/GEM5-496
rv64_binaries = (
    "rv64samt-ps-sysclone_d",
    "rv64samt-ps-sysfutex1_d",
    #    'rv64samt-ps-sysfutex2_d',
    "rv64samt-ps-sysfutex3_d",
    #    'rv64samt-ps-sysfutex_d',
    "rv64ua-ps-amoadd_d",
    "rv64ua-ps-amoadd_w",
    "rv64ua-ps-amoand_d",
    "rv64ua-ps-amoand_w",
    "rv64ua-ps-amomax_d",
    "rv64ua-ps-amomax_w",
    "rv64ua-ps-amomaxu_d",
    "rv64ua-ps-amomaxu_w",
    "rv64ua-ps-amomin_d",
    "rv64ua-ps-amomin_w",
    "rv64ua-ps-amominu_d",
    "rv64ua-ps-amominu_w",
    "rv64ua-ps-amoor_d",
    "rv64ua-ps-amoor_w",
    "rv64ua-ps-amoswap_d",
    "rv64ua-ps-amoswap_w",
    "rv64ua-ps-amoxor_d",
    "rv64ua-ps-amoxor_w",
    "rv64ua-ps-lrsc",
    "rv64uamt-ps-amoadd_d",
    "rv64uamt-ps-amoand_d",
    "rv64uamt-ps-amomax_d",
    "rv64uamt-ps-amomaxu_d",
    "rv64uamt-ps-amomin_d",
    "rv64uamt-ps-amominu_d",
    "rv64uamt-ps-amoor_d",
    "rv64uamt-ps-amoswap_d",
    "rv64uamt-ps-amoxor_d",
    "rv64uamt-ps-lrsc_d",
    "rv64ub-ps-add_uw",
    "rv64ub-ps-andn",
    "rv64ub-ps-bclr",
    "rv64ub-ps-bclri",
    "rv64ub-ps-bext",
    "rv64ub-ps-bexti",
    "rv64ub-ps-binv",
    "rv64ub-ps-binvi",
    "rv64ub-ps-bset",
    "rv64ub-ps-bseti",
    "rv64ub-ps-clmul",
    "rv64ub-ps-clmulh",
    "rv64ub-ps-clmulr",
    "rv64ub-ps-clz",
    "rv64ub-ps-clzw",
    "rv64ub-ps-cpop",
    "rv64ub-ps-cpopw",
    "rv64ub-ps-ctz",
    "rv64ub-ps-ctzw",
    "rv64ub-ps-max",
    "rv64ub-ps-maxu",
    "rv64ub-ps-min",
    "rv64ub-ps-minu",
    "rv64ub-ps-orc_b",
    "rv64ub-ps-orn",
    "rv64ub-ps-rev8",
    "rv64ub-ps-rol",
    "rv64ub-ps-rolw",
    "rv64ub-ps-ror",
    "rv64ub-ps-rori",
    "rv64ub-ps-roriw",
    "rv64ub-ps-rorw",
    "rv64ub-ps-sext_b",
    "rv64ub-ps-sext_h",
    "rv64ub-ps-sh1add",
    "rv64ub-ps-sh1add_uw",
    "rv64ub-ps-sh2add",
    "rv64ub-ps-sh2add_uw",
    "rv64ub-ps-sh3add",
    "rv64ub-ps-sh3add_uw",
    "rv64ub-ps-slli_uw",
    "rv64ub-ps-xnor",
    "rv64ub-ps-zext_h",
    "rv64uc-ps-rvc",
    "rv64ud-ps-fadd",
    "rv64ud-ps-fclass",
    "rv64ud-ps-fcmp",
    "rv64ud-ps-fcvt",
    "rv64ud-ps-fcvt_w",
    "rv64ud-ps-fdiv",
    "rv64ud-ps-fmadd",
    "rv64ud-ps-fmin",
    "rv64ud-ps-ldst",
    "rv64ud-ps-move",
    "rv64ud-ps-recoding",
    "rv64ud-ps-structural",
    "rv64uf-ps-fadd",
    "rv64uf-ps-fclass",
    "rv64uf-ps-fcmp",
    "rv64uf-ps-fcvt",
    "rv64uf-ps-fcvt_w",
    "rv64uf-ps-fdiv",
    "rv64uf-ps-fmadd",
    "rv64uf-ps-fmin",
    "rv64uf-ps-ldst",
    "rv64uf-ps-move",
    "rv64uf-ps-recoding",
    "rv64ui-ps-add",
    "rv64ui-ps-addi",
    "rv64ui-ps-addiw",
    "rv64ui-ps-addw",
    "rv64ui-ps-and",
    "rv64ui-ps-andi",
    "rv64ui-ps-auipc",
    "rv64ui-ps-beq",
    "rv64ui-ps-bge",
    "rv64ui-ps-bgeu",
    "rv64ui-ps-blt",
    "rv64ui-ps-bltu",
    "rv64ui-ps-bne",
    "rv64ui-ps-fence_i",
    "rv64ui-ps-jal",
    "rv64ui-ps-jalr",
    "rv64ui-ps-lb",
    "rv64ui-ps-lbu",
    "rv64ui-ps-ld",
    "rv64ui-ps-lh",
    "rv64ui-ps-lhu",
    "rv64ui-ps-lui",
    "rv64ui-ps-lw",
    "rv64ui-ps-lwu",
    "rv64ui-ps-or",
    "rv64ui-ps-ori",
    "rv64ui-ps-sb",
    "rv64ui-ps-sd",
    "rv64ui-ps-sh",
    "rv64ui-ps-simple",
    "rv64ui-ps-sll",
    "rv64ui-ps-slli",
    "rv64ui-ps-slliw",
    "rv64ui-ps-sllw",
    "rv64ui-ps-slt",
    "rv64ui-ps-slti",
    "rv64ui-ps-sltiu",
    "rv64ui-ps-sltu",
    "rv64ui-ps-sra",
    "rv64ui-ps-srai",
    "rv64ui-ps-sraiw",
    "rv64ui-ps-sraw",
    "rv64ui-ps-srl",
    "rv64ui-ps-srli",
    "rv64ui-ps-srliw",
    "rv64ui-ps-srlw",
    "rv64ui-ps-sub",
    "rv64ui-ps-subw",
    "rv64ui-ps-sw",
    "rv64ui-ps-xor",
    "rv64ui-ps-xori",
    "rv64um-ps-div",
    "rv64um-ps-divu",
    "rv64um-ps-divuw",
    "rv64um-ps-divw",
    "rv64um-ps-mul",
    "rv64um-ps-mulh",
    "rv64um-ps-mulhsu",
    "rv64um-ps-mulhu",
    "rv64um-ps-mulw",
    "rv64um-ps-rem",
    "rv64um-ps-remu",
    "rv64um-ps-remuw",
    "rv64um-ps-remw",
    "rv64uzfh-ps-fadd",
    "rv64uzfh-ps-fclass",
    "rv64uzfh-ps-fcmp",
    "rv64uzfh-ps-fcvt",
    "rv64uzfh-ps-fcvt_w",
    "rv64uzfh-ps-fdiv",
    "rv64uzfh-ps-fmadd",
    "rv64uzfh-ps-fmin",
    "rv64uzfh-ps-ldst",
    "rv64uzfh-ps-move",
    "rv64uzfh-ps-recoding",
)

rv32_binaries = (
    "rv32ua-ps-amoadd_w",
    "rv32ua-ps-amoand_w",
    "rv32ua-ps-amomaxu_w",
    "rv32ua-ps-amomax_w",
    "rv32ua-ps-amominu_w",
    "rv32ua-ps-amomin_w",
    "rv32ua-ps-amoor_w",
    "rv32ua-ps-amoswap_w",
    "rv32ua-ps-amoxor_w",
    "rv32ua-ps-lrsc",
    "rv32uamt-ps-amoadd_w",
    "rv32uamt-ps-amoand_w",
    "rv32uamt-ps-amomaxu_w",
    "rv32uamt-ps-amomax_w",
    "rv32uamt-ps-amominu_w",
    "rv32uamt-ps-amomin_w",
    "rv32uamt-ps-amoor_w",
    "rv32uamt-ps-amoswap_w",
    "rv32uamt-ps-amoxor_w",
    "rv32uamt-ps-lrsc_w",
    "rv32ub-ps-andn",
    "rv32ub-ps-bclr",
    "rv32ub-ps-bclri",
    "rv32ub-ps-bext",
    "rv32ub-ps-bexti",
    "rv32ub-ps-binv",
    "rv32ub-ps-binvi",
    "rv32ub-ps-bset",
    "rv32ub-ps-bseti",
    "rv32ub-ps-clmul",
    "rv32ub-ps-clmulh",
    "rv32ub-ps-clmulr",
    "rv32ub-ps-clz",
    "rv32ub-ps-cpop",
    "rv32ub-ps-ctz",
    "rv32ub-ps-max",
    "rv32ub-ps-maxu",
    "rv32ub-ps-min",
    "rv32ub-ps-minu",
    "rv32ub-ps-orc_b",
    "rv32ub-ps-orn",
    "rv32ub-ps-rev8",
    "rv32ub-ps-rol",
    "rv32ub-ps-ror",
    "rv32ub-ps-rori",
    "rv32ub-ps-sext_b",
    "rv32ub-ps-sext_h",
    "rv32ub-ps-sh1add",
    "rv32ub-ps-sh2add",
    "rv32ub-ps-sh3add",
    "rv32ub-ps-xnor",
    "rv32ub-ps-zext_h",
    "rv32uc-ps-rvc",
    "rv32ud-ps-fadd",
    "rv32ud-ps-fclass",
    "rv32ud-ps-fcmp",
    "rv32ud-ps-fcvt",
    "rv32ud-ps-fcvt_w",
    "rv32ud-ps-fdiv",
    "rv32ud-ps-fmadd",
    "rv32ud-ps-fmin",
    "rv32ud-ps-ldst",
    "rv32ud-ps-recoding",
    "rv32uf-ps-fadd",
    "rv32uf-ps-fclass",
    "rv32uf-ps-fcmp",
    "rv32uf-ps-fcvt",
    "rv32uf-ps-fcvt_w",
    "rv32uf-ps-fdiv",
    "rv32uf-ps-fmadd",
    "rv32uf-ps-fmin",
    "rv32uf-ps-ldst",
    "rv32uf-ps-move",
    "rv32uf-ps-recoding",
    "rv32ui-ps-add",
    "rv32ui-ps-addi",
    "rv32ui-ps-and",
    "rv32ui-ps-andi",
    "rv32ui-ps-auipc",
    "rv32ui-ps-beq",
    "rv32ui-ps-bge",
    "rv32ui-ps-bgeu",
    "rv32ui-ps-blt",
    "rv32ui-ps-bltu",
    "rv32ui-ps-bne",
    "rv32ui-ps-fence_i",
    "rv32ui-ps-jal",
    "rv32ui-ps-jalr",
    "rv32ui-ps-lb",
    "rv32ui-ps-lbu",
    "rv32ui-ps-lh",
    "rv32ui-ps-lhu",
    "rv32ui-ps-lui",
    "rv32ui-ps-lw",
    "rv32ui-ps-or",
    "rv32ui-ps-ori",
    "rv32ui-ps-sb",
    "rv32ui-ps-sh",
    "rv32ui-ps-simple",
    "rv32ui-ps-sll",
    "rv32ui-ps-slli",
    "rv32ui-ps-slt",
    "rv32ui-ps-slti",
    "rv32ui-ps-sltiu",
    "rv32ui-ps-sltu",
    "rv32ui-ps-sra",
    "rv32ui-ps-srai",
    "rv32ui-ps-srl",
    "rv32ui-ps-srli",
    "rv32ui-ps-sub",
    "rv32ui-ps-sw",
    "rv32ui-ps-xor",
    "rv32ui-ps-xori",
    "rv32um-ps-div",
    "rv32um-ps-divu",
    "rv32um-ps-mul",
    "rv32um-ps-mulh",
    "rv32um-ps-mulhsu",
    "rv32um-ps-mulhu",
    "rv32um-ps-rem",
    "rv32um-ps-remu",
    "rv32uzfh-ps-fadd",
    "rv32uzfh-ps-fclass",
    "rv32uzfh-ps-fcmp",
    "rv32uzfh-ps-fcvt",
    "rv32uzfh-ps-fcvt_w",
    "rv32uzfh-ps-fdiv",
    "rv32uzfh-ps-fmadd",
    "rv32uzfh-ps-fmin",
    "rv32uzfh-ps-ldst",
    "rv32uzfh-ps-move",
    "rv32uzfh-ps-recoding",
)

bare_biaries = (
    "rv64mi-p-csr",
    # "rv64mi-p-illegal",
)

cpu_types = ("atomic", "timing", "minor", "o3")

for cpu_type in cpu_types:
    for binary in rv64_binaries:
        gem5_verify_config(
            name=f"asm-riscv-{binary}-{cpu_type}",
            verifiers=(),
            config=joinpath(
                config.base_dir,
                "tests",
                "gem5",
                "asmtest",
                "configs",
                "riscv_asmtest.py",
            ),
            config_args=[
                binary,
                cpu_type,
                "--num-cores",
                "4",
                "--resource-directory",
                resource_path,
            ],
            valid_isas=(constants.all_compiled_tag,),
            valid_hosts=constants.supported_hosts,
        )
    for binary in rv32_binaries:
        gem5_verify_config(
            name=f"asm-riscv-{binary}-{cpu_type}",
            verifiers=(),
            config=joinpath(
                config.base_dir,
                "tests",
                "gem5",
                "asmtest",
                "configs",
                "riscv_asmtest.py",
            ),
            config_args=[
                binary,
                cpu_type,
                "--num-cores",
                "4",
                "--riscv-32bits",
                "--resource-directory",
                resource_path,
            ],
            valid_isas=(constants.all_compiled_tag,),
            valid_hosts=constants.supported_hosts,
        )
