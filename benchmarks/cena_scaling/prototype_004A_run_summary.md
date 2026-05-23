# Prototype 004A RNA → CeNA Run Summary

## RNA-8mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 004A
RNA → CeNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-8mer.pdb
CeNA template: /mnt/data/2H0N_CeNA_8mer_clean_ss.pdb
Output PDB: /mnt/data/cena_prototype_004A_outputs/converted_cena_RNA-8mer_auto_004A.pdb
Report: /mnt/data/cena_prototype_004A_outputs/conversion_report_RNA-8mer_auto_004A.md
Requested mode: auto
Actual mode: full-template
Source sequence: CUAGGCUC
Template base classes: GUGUACAC
Converted residues: 8
Mean template/local anchor RMSD: 0.5160 Å
Max template/local anchor RMSD: 0.5421 Å
--------------------------------------------------------------------------------
O3′(i)→P(i+1): PASS (measured=7, failed=0, mean=1.603 Å)
C1′→glycosidic N: PASS (measured=8, failed=0, mean=1.487 Å)
C4′→C6′: PASS (measured=8, failed=0, mean=1.458 Å)
C6′→C7′: PASS (measured=8, failed=0, mean=1.322 Å)
C7′→C1′: PASS (measured=8, failed=0, mean=1.559 Å)
================================================================================

STDERR:
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
```

## RNA-12mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 004A
RNA → CeNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-12mer.pdb
CeNA template: /mnt/data/2H0N_CeNA_8mer_clean_ss.pdb
Output PDB: /mnt/data/cena_prototype_004A_outputs/converted_cena_RNA-12mer_auto_004A.pdb
Report: /mnt/data/cena_prototype_004A_outputs/conversion_report_RNA-12mer_auto_004A.md
Requested mode: auto
Actual mode: chain-preserving
Source sequence: CUAGGCUCGAAA
Template base classes: GUGUACAC
Converted residues: 12
Mean template/local anchor RMSD: 0.8029 Å
Max template/local anchor RMSD: 0.9289 Å
Mean base anchor RMSD: 0.4679 Å
Max base anchor RMSD: 0.7588 Å
--------------------------------------------------------------------------------
O3′(i)→P(i+1): PASS (measured=11, failed=0, mean=1.607 Å)
C1′→glycosidic N: PASS (measured=12, failed=0, mean=1.494 Å)
C4′→C6′: FAIL (measured=12, failed=8, mean=1.735 Å)
C6′→C7′: PASS (measured=12, failed=0, mean=1.320 Å)
C7′→C1′: PASS (measured=12, failed=0, mean=1.559 Å)
================================================================================

STDERR:
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
```

## RNA-16mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 004A
RNA → CeNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-16mer.pdb
CeNA template: /mnt/data/2H0N_CeNA_8mer_clean_ss.pdb
Output PDB: /mnt/data/cena_prototype_004A_outputs/converted_cena_RNA-16mer_auto_004A.pdb
Report: /mnt/data/cena_prototype_004A_outputs/conversion_report_RNA-16mer_auto_004A.md
Requested mode: auto
Actual mode: chain-preserving
Source sequence: ACCACCUAGGCUCGAA
Template base classes: GUGUACAC
Converted residues: 16
Mean template/local anchor RMSD: 0.8256 Å
Max template/local anchor RMSD: 0.9389 Å
Mean base anchor RMSD: 0.5180 Å
Max base anchor RMSD: 0.7531 Å
--------------------------------------------------------------------------------
O3′(i)→P(i+1): PASS (measured=15, failed=0, mean=1.606 Å)
C1′→glycosidic N: PASS (measured=16, failed=0, mean=1.493 Å)
C4′→C6′: FAIL (measured=16, failed=12, mean=1.744 Å)
C6′→C7′: PASS (measured=16, failed=0, mean=1.321 Å)
C7′→C1′: PASS (measured=16, failed=0, mean=1.558 Å)
================================================================================

STDERR:
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
```

## RNA-22mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 004A
RNA → CeNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-22mer.pdb
CeNA template: /mnt/data/2H0N_CeNA_8mer_clean_ss.pdb
Output PDB: /mnt/data/cena_prototype_004A_outputs/converted_cena_RNA-22mer_auto_004A.pdb
Report: /mnt/data/cena_prototype_004A_outputs/conversion_report_RNA-22mer_auto_004A.md
Requested mode: auto
Actual mode: chain-preserving
Source sequence: AUACGACCACCUAGGCUCGAAA
Template base classes: GUGUACAC
Converted residues: 22
Mean template/local anchor RMSD: 0.8373 Å
Max template/local anchor RMSD: 0.9435 Å
Mean base anchor RMSD: 0.5788 Å
Max base anchor RMSD: 0.7589 Å
--------------------------------------------------------------------------------
O3′(i)→P(i+1): PASS (measured=21, failed=0, mean=1.606 Å)
C1′→glycosidic N: PASS (measured=22, failed=0, mean=1.493 Å)
C4′→C6′: FAIL (measured=22, failed=18, mean=1.856 Å)
C6′→C7′: PASS (measured=22, failed=0, mean=1.321 Å)
C7′→C1′: PASS (measured=22, failed=0, mean=1.559 Å)
================================================================================

STDERR:
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
```

## RNA-34mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 004A
RNA → CeNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-34mer.pdb
CeNA template: /mnt/data/2H0N_CeNA_8mer_clean_ss.pdb
Output PDB: /mnt/data/cena_prototype_004A_outputs/converted_cena_RNA-34mer_auto_004A.pdb
Report: /mnt/data/cena_prototype_004A_outputs/conversion_report_RNA-34mer_auto_004A.md
Requested mode: auto
Actual mode: chain-preserving
Source sequence: GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC
Template base classes: GUGUACAC
Converted residues: 34
Mean template/local anchor RMSD: 0.8255 Å
Max template/local anchor RMSD: 0.9435 Å
Mean base anchor RMSD: 0.5651 Å
Max base anchor RMSD: 0.7666 Å
--------------------------------------------------------------------------------
O3′(i)→P(i+1): PASS (measured=33, failed=0, mean=1.606 Å)
C1′→glycosidic N: PASS (measured=34, failed=0, mean=1.493 Å)
C4′→C6′: FAIL (measured=34, failed=28, mean=1.835 Å)
C6′→C7′: PASS (measured=34, failed=0, mean=1.321 Å)
C7′→C1′: PASS (measured=34, failed=0, mean=1.560 Å)
================================================================================

STDERR:
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
```

## 8t5o-HH-typeI-111mer-full

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 004A
RNA → CeNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/8t5o-HH-typeI-111mer-full.pdb
CeNA template: /mnt/data/2H0N_CeNA_8mer_clean_ss.pdb
Output PDB: /mnt/data/cena_prototype_004A_outputs/converted_cena_8t5o-HH-typeI-111mer-full_auto_004A.pdb
Report: /mnt/data/cena_prototype_004A_outputs/conversion_report_8t5o-HH-typeI-111mer-full_auto_004A.md
Requested mode: auto
Actual mode: chain-preserving
Source sequence: GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC
Template base classes: GUGUACAC
Converted residues: 111
Mean template/local anchor RMSD: 0.7988 Å
Max template/local anchor RMSD: 0.9389 Å
Mean base anchor RMSD: 0.5186 Å
Max base anchor RMSD: 0.7666 Å
--------------------------------------------------------------------------------
O3′(i)→P(i+1): PASS (measured=109, failed=0, mean=1.606 Å)
C1′→glycosidic N: PASS (measured=111, failed=0, mean=1.493 Å)
C4′→C6′: FAIL (measured=111, failed=87, mean=1.835 Å)
C6′→C7′: PASS (measured=111, failed=0, mean=1.321 Å)
C7′→C1′: PASS (measured=111, failed=0, mean=1.559 Å)
================================================================================

STDERR:
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
```
