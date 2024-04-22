/*
 * Copyright (c) 2011,2017-2019 ARM Limited
 * All rights reserved
 *
 * The license below extends only to copyright in the software and shall
 * not be construed as granting a license to any other intellectual
 * property including but not limited to intellectual property relating
 * to a hardware implementation of the functionality of the software
 * licensed hereunder.  You may use the software subject to the license
 * terms below provided that you ensure that this notice is replicated
 * unmodified and in its entirety in all distributions of the software,
 * modified or unmodified, in source code or in binary form.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * @file This module implements a bridge between TARMAC traces, as generated by
 * other models, and gem5 (AtomicCPU model). Its goal is to detect possible
 * inconsistencies between the two models as soon as they occur.  The module
 * takes a TARMAC trace as input, which is used to compare the architectural
 * state of the two models after each simulated instruction.
 */

#ifndef __ARCH_ARM_TRACERS_TARMAC_PARSER_HH__
#define __ARCH_ARM_TRACERS_TARMAC_PARSER_HH__

#include <fstream>
#include <memory>
#include <unordered_map>

#include "base/trace.hh"
#include "base/types.hh"
#include "cpu/static_inst.hh"
#include "cpu/thread_context.hh"
#include "mem/request.hh"
#include "params/TarmacParser.hh"
#include "sim/insttracer.hh"
#include "tarmac_base.hh"

namespace gem5
{

namespace trace
{

class TarmacParserRecord : public TarmacBaseRecord
{
  public:
    /**
     * Event triggered to check the value of the destination registers.  Needed
     * to handle some cases where registers are modified after the trace record
     * has been dumped.  E.g., the SVC instruction updates the CPSR and SPSR as
     * part of the fault handling routine.
     */
    struct TarmacParserRecordEvent : public Event
    {
        /**
         * Reference to the TARMAC trace object to which this record belongs.
         */
        TarmacParser &parent;
        /** Current thread context. */
        ThreadContext *thread;
        /** Current instruction. */
        const StaticInstPtr inst;
        /** PC of the current instruction. */
        std::unique_ptr<PCStateBase> pc;
        /** True if a mismatch has been detected for this instruction. */
        bool mismatch;
        /**
         * True if a mismatch has been detected for this instruction on PC or
         * opcode.
         */
        bool mismatchOnPcOrOpcode;

        TarmacParserRecordEvent(TarmacParser &_parent, ThreadContext *_thread,
                                const StaticInstPtr _inst,
                                const PCStateBase &_pc, bool _mismatch,
                                bool _mismatch_on_pc_or_opcode)
            : parent(_parent),
              thread(_thread),
              inst(_inst),
              pc(_pc.clone()),
              mismatch(_mismatch),
              mismatchOnPcOrOpcode(_mismatch_on_pc_or_opcode)
        {}

        void process();
        const char *description() const;
    };

    struct ParserInstEntry : public InstEntry
    {
      public:
        uint64_t seq_num;
    };

    struct ParserRegEntry : public RegEntry
    {
      public:
        char repr[16];
    };

    struct ParserMemEntry : public MemEntry
    {
    };

    static const int MaxLineLength = 256;

    /**
     * Print a mismatch header containing the instruction fields as reported
     * by gem5.
     */
    static void printMismatchHeader(const StaticInstPtr inst,
                                    const PCStateBase &pc);

    TarmacParserRecord(Tick _when, ThreadContext *_thread,
                       const StaticInstPtr _staticInst, const PCStateBase &_pc,
                       TarmacParser &_parent,
                       const StaticInstPtr _macroStaticInst = NULL);

    void dump() override;

    /**
     * Performs a memory access to read the value written by a previous write.
     * @return False if the result of the memory access should be ignored
     * (faulty memory access, etc.).
     */
    bool readMemNoEffect(Addr addr, uint8_t *data, unsigned size,
                         unsigned flags);

  private:
    /**
     * Advances the TARMAC trace up to the next instruction,
     * register, or memory access record. The collected data is stored
     * in one of {inst/reg/mem}_record.
     * @return False if EOF is reached.
     */
    bool advanceTrace();

    /** Returns the string representation of an instruction set state. */
    const char *iSetStateToStr(ISetState isetstate) const;

    /** Buffer for instruction trace records. */
    static ParserInstEntry instRecord;

    /** Buffer for register trace records. */
    static ParserRegEntry regRecord;

    /** Buffer for memory access trace records (stores only). */
    static ParserMemEntry memRecord;

    /** Type of last parsed record. */
    static TarmacRecordType currRecordType;

    /** Buffer used for trace file parsing. */
    static char buf[MaxLineLength];

    /** List of records of destination registers. */
    static std::list<ParserRegEntry> destRegRecords;

    /** Map from misc. register names to indexes. */
    using MiscRegMap = std::unordered_map<std::string, RegIndex>;
    static MiscRegMap miscRegMap;

    /**
     * True if a TARMAC instruction record has already been parsed for this
     * instruction.
     */
    bool parsingStarted;

    /** True if a mismatch has been detected for this instruction. */
    bool mismatch;

    /**
     * True if a mismatch has been detected for this instruction on PC or
     * opcode.
     */
    bool mismatchOnPcOrOpcode;

    /** Request for memory write checks. */
    RequestPtr memReq;

    /** Max. vector length (SVE). */
    static int8_t maxVectorLength;

  protected:
    TarmacParser &parent;
};

/**
 * Tarmac Parser: this tracer parses an existing Tarmac trace and it
 * diffs it with gem5 simulation status, comparing results and
 * reporting architectural mismatches if any.
 */
class TarmacParser : public InstTracer
{
    friend class TarmacParserRecord;

  public:
    typedef TarmacParserParams Params;

    TarmacParser(const Params &p)
        : InstTracer(p),
          startPc(p.start_pc),
          exitOnDiff(p.exit_on_diff),
          exitOnInsnDiff(p.exit_on_insn_diff),
          memWrCheck(p.mem_wr_check),
          ignoredAddrRange(p.ignore_mem_addr),
          cpuId(p.cpu_id),
          macroopInProgress(false)
    {
        assert(!(exitOnDiff && exitOnInsnDiff));

        trace.open(p.path_to_trace.c_str());
        if (startPc == 0x0) {
            started = true;
        } else {
            advanceTraceToStartPc();
            started = false;
        }
    }

    virtual ~TarmacParser() { trace.close(); }

    InstRecord *
    getInstRecord(Tick when, ThreadContext *tc, const StaticInstPtr staticInst,
                  const PCStateBase &pc,
                  const StaticInstPtr macroStaticInst = nullptr) override
    {
        if (!started && pc.instAddr() == startPc)
            started = true;

        if (started) {
            return new TarmacParserRecord(when, tc, staticInst, pc, *this,
                                          macroStaticInst);
        } else {
            return nullptr;
        }
    }

  private:
    /** Helper function to advance the trace up to startPc. */
    void advanceTraceToStartPc();

    /** TARMAC trace file. */
    std::ifstream trace;

    /**
     * Tracing starts when the PC gets this value for the first time (ignored
     * if 0x0).
     */
    Addr startPc;

    /**
     * If true, the simulation is stopped as the first mismatch is detected.
     */
    bool exitOnDiff;

    /**
     * If true, the simulation is stopped as the first mismatch is detected on
     * PC or opcode.
     */
    bool exitOnInsnDiff;

    /** If true, memory write accesses are checked. */
    bool memWrCheck;

    /** Ignored addresses (ignored if empty). */
    AddrRange ignoredAddrRange;

    /** If true, the trace format includes the CPU id. */
    bool cpuId;

    /** True if tracing has started. */
    bool started;

    /** True if a macroop is currently in progress. */
    bool macroopInProgress;
};

} // namespace trace
} // namespace gem5

#endif // __ARCH_ARM_TRACERS_TARMAC_PARSER_HH__
