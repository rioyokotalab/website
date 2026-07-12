# T-8 — 8-GPU RTX 6000 Ada node status

Queried 2026-07-12 using only the allowed read-only Slurm commands (`sinfo`, `scontrol show node`). No job submission command was used.

## Raw Slurm evidence

`sinfo -N -h -o '%N|%P|%t|%G|%c|%m|%f'` matching line:

```text
rtx6000-ada|rtx6000-ada|down*|gpu:8(S:0-1)|56|500000|(null)
```

`scontrol show node rtx6000-ada`:

```text
NodeName=rtx6000-ada CoresPerSocket=28
   CPUAlloc=0 CPUEfctv=56 CPUTot=56 CPULoad=0.00
   AvailableFeatures=(null)
   ActiveFeatures=(null)
   Gres=gpu:8(S:0-1)
   NodeAddr=rtx6000-ada.yokota NodeHostName=rtx6000-ada
   RealMemory=500000 AllocMem=0 FreeMem=N/A Sockets=2 Boards=1
   State=DOWN+NOT_RESPONDING ThreadsPerCore=1 TmpDisk=0 Weight=20 Owner=N/A MCS_label=N/A
   Partitions=rtx6000-ada
   BootTime=None SlurmdStartTime=None
   LastBusyTime=2026-06-11T16:16:23 ResumeAfterTime=None
   CfgTRES=cpu=56,mem=500000M,billing=56,gres/gpu=8
   AllocTRES=
   CurrentWatts=0 AveWatts=0
   Reason=Not responding [root@2026-06-11T16:16:23]
```

## Decision

The 512GB, 8-GPU node is still down (`DOWN+NOT_RESPONDING`). Its CPU model remains unknown: Slurm's core/socket counts are not enough to identify it, and no hardware guess is permitted. Therefore the computers pages remain unchanged.

## Structured result

- status: completed
- summary: The 8-GPU RTX 6000 Ada node `rtx6000-ada` remains down; updated factual status only, with no page edit.
- changed_files: tools/out/t8-cluster-status.md; tools/state/facts.md (pending dated status update); tools/state/session.md
- commands: `sinfo -N -h -o '%N|%P|%t|%G|%c|%m|%f'`; `scontrol show node rtx6000-ada`.
- verification: raw read-only Slurm output above identifies 8 GPUs and state `DOWN+NOT_RESPONDING`.
- evidence:
  - confirmed: `rtx6000-ada` has 8 configured GPUs, 500000 MB configured memory, and is DOWN+NOT_RESPONDING.
  - confirmed: its Slurm record has no CPU model field; CPU identity is not inferred.
  - hypotheses: none.
- remaining: update the dated computers-node fact and close T-8; no site change is appropriate while it remains down.

## Ledger update

- Updated `tools/state/facts.md` with the 2026-07-12 read-only Slurm status. Neither computers page was changed.

## Structured result

- status: completed
- summary: The 8-GPU RTX 6000 Ada node `rtx6000-ada` remains down; recorded its current status in facts.md and made no page edit.
- changed_files: tools/state/facts.md; tools/out/t8-cluster-status.md; tools/state/session.md
- commands: `sinfo -N -h -o '%N|%P|%t|%G|%c|%m|%f'`; `scontrol show node rtx6000-ada`.
- verification: raw read-only Slurm output above identifies 8 GPUs and state `DOWN+NOT_RESPONDING`; computers-page table still has CPU “-”.
- evidence:
  - confirmed: `rtx6000-ada` has 8 configured GPUs, 500000 MB configured memory, and is DOWN+NOT_RESPONDING.
  - confirmed: its Slurm record has no CPU model field; CPU identity is not inferred.
  - hypotheses: none.
- remaining: none for T-8; reopen only after a fresh cluster status or an authorized hardware-model probe.
