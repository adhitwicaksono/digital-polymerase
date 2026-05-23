# Prototype 005A RNA → XyNA Run Summary

## RNA-8mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 005A
RNA → XyNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-8mer.pdb
XyNA template: /mnt/data/2n4j_XyNA-8nt.pdb
Output PDB: /mnt/data/xyna_prototype_005A_outputs/converted_xyna_RNA-8mer_auto_005A.pdb
Report: /mnt/data/xyna_prototype_005A_outputs/conversion_report_RNA-8mer_auto_005A.md
Requested mode: auto
Actual mode: chain-preserving
Source sequence: CUAGGCUC
Template base classes: GUGUACAC
Converted residues: 8
Mean local/template RMSD: 0.0923 Å
Max local/template RMSD: 0.1275 Å
--------------------------------------------------------------------------------
O3'(i)→P(i+1): PASS (measured=7, failed=0, mean=1.606 Å)
C1'→glycosidic N: PASS (measured=8, failed=0, mean=1.477 Å)
C2'→O2': PASS (measured=8, failed=0, mean=1.433 Å)
C1'→O4': PASS (measured=8, failed=0, mean=1.412 Å)
C4'→O4': PASS (measured=8, failed=0, mean=1.452 Å)
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
Digital Polymerase Prototype 005A
RNA → XyNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-12mer.pdb
XyNA template: /mnt/data/2n4j_XyNA-8nt.pdb
Output PDB: /mnt/data/xyna_prototype_005A_outputs/converted_xyna_RNA-12mer_auto_005A.pdb
Report: /mnt/data/xyna_prototype_005A_outputs/conversion_report_RNA-12mer_auto_005A.md
Requested mode: auto
Actual mode: chain-preserving
Source sequence: CUAGGCUCGAAA
Template base classes: GUGUACAC
Converted residues: 12
Mean local/template RMSD: 0.0830 Å
Max local/template RMSD: 0.1275 Å
--------------------------------------------------------------------------------
O3'(i)→P(i+1): PASS (measured=11, failed=0, mean=1.607 Å)
C1'→glycosidic N: PASS (measured=12, failed=0, mean=1.476 Å)
C2'→O2': PASS (measured=12, failed=0, mean=1.433 Å)
C1'→O4': PASS (measured=12, failed=0, mean=1.412 Å)
C4'→O4': PASS (measured=12, failed=0, mean=1.452 Å)
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
Digital Polymerase Prototype 005A
RNA → XyNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-16mer.pdb
XyNA template: /mnt/data/2n4j_XyNA-8nt.pdb
Output PDB: /mnt/data/xyna_prototype_005A_outputs/converted_xyna_RNA-16mer_auto_005A.pdb
Report: /mnt/data/xyna_prototype_005A_outputs/conversion_report_RNA-16mer_auto_005A.md
Requested mode: auto
Actual mode: chain-preserving
Source sequence: ACCACCUAGGCUCGAA
Template base classes: GUGUACAC
Converted residues: 16
Mean local/template RMSD: 0.0864 Å
Max local/template RMSD: 0.1285 Å
--------------------------------------------------------------------------------
O3'(i)→P(i+1): PASS (measured=15, failed=0, mean=1.606 Å)
C1'→glycosidic N: PASS (measured=16, failed=0, mean=1.476 Å)
C2'→O2': PASS (measured=16, failed=0, mean=1.433 Å)
C1'→O4': PASS (measured=16, failed=0, mean=1.412 Å)
C4'→O4': PASS (measured=16, failed=0, mean=1.452 Å)
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
Digital Polymerase Prototype 005A
RNA → XyNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-22mer.pdb
XyNA template: /mnt/data/2n4j_XyNA-8nt.pdb
Output PDB: /mnt/data/xyna_prototype_005A_outputs/converted_xyna_RNA-22mer_auto_005A.pdb
Report: /mnt/data/xyna_prototype_005A_outputs/conversion_report_RNA-22mer_auto_005A.md
Requested mode: auto
Actual mode: chain-preserving
Source sequence: AUACGACCACCUAGGCUCGAAA
Template base classes: GUGUACAC
Converted residues: 22
Mean local/template RMSD: 0.0766 Å
Max local/template RMSD: 0.1275 Å
--------------------------------------------------------------------------------
O3'(i)→P(i+1): PASS (measured=21, failed=0, mean=1.606 Å)
C1'→glycosidic N: PASS (measured=22, failed=0, mean=1.474 Å)
C2'→O2': PASS (measured=22, failed=0, mean=1.433 Å)
C1'→O4': PASS (measured=22, failed=0, mean=1.412 Å)
C4'→O4': PASS (measured=22, failed=0, mean=1.452 Å)
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
Digital Polymerase Prototype 005A
RNA → XyNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-34mer.pdb
XyNA template: /mnt/data/2n4j_XyNA-8nt.pdb
Output PDB: /mnt/data/xyna_prototype_005A_outputs/converted_xyna_RNA-34mer_auto_005A.pdb
Report: /mnt/data/xyna_prototype_005A_outputs/conversion_report_RNA-34mer_auto_005A.md
Requested mode: auto
Actual mode: chain-preserving
Source sequence: GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC
Template base classes: GUGUACAC
Converted residues: 34
Mean local/template RMSD: 0.0760 Å
Max local/template RMSD: 0.1275 Å
--------------------------------------------------------------------------------
O3'(i)→P(i+1): PASS (measured=33, failed=0, mean=1.606 Å)
C1'→glycosidic N: PASS (measured=34, failed=0, mean=1.474 Å)
C2'→O2': PASS (measured=34, failed=0, mean=1.433 Å)
C1'→O4': PASS (measured=34, failed=0, mean=1.412 Å)
C4'→O4': PASS (measured=34, failed=0, mean=1.452 Å)
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
Digital Polymerase Prototype 005A
RNA → XyNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/8t5o-HH-typeI-111mer-full.pdb
XyNA template: /mnt/data/2n4j_XyNA-8nt.pdb
Output PDB: /mnt/data/xyna_prototype_005A_outputs/converted_xyna_8t5o-HH-typeI-111mer-full_auto_005A.pdb
Report: /mnt/data/xyna_prototype_005A_outputs/conversion_report_8t5o-HH-typeI-111mer-full_auto_005A.md
Requested mode: auto
Actual mode: chain-preserving
Source sequence: GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC
Template base classes: GUGUACAC
Converted residues: 111
Mean local/template RMSD: 0.0781 Å
Max local/template RMSD: 0.1285 Å
--------------------------------------------------------------------------------
O3'(i)→P(i+1): PASS (measured=109, failed=0, mean=1.606 Å)
C1'→glycosidic N: PASS (measured=111, failed=0, mean=1.474 Å)
C2'→O2': PASS (measured=111, failed=0, mean=1.433 Å)
C1'→O4': PASS (measured=111, failed=0, mean=1.412 Å)
C4'→O4': PASS (measured=111, failed=0, mean=1.451 Å)
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

## RNA-8mer-full-template

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 005A
RNA → XyNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-8mer.pdb
XyNA template: /mnt/data/2n4j_XyNA-8nt.pdb
Output PDB: /mnt/data/xyna_prototype_005A_outputs/converted_xyna_RNA-8mer_full_template_005A.pdb
Report: /mnt/data/xyna_prototype_005A_outputs/conversion_report_RNA-8mer_full_template_005A.md
Requested mode: full-template
Actual mode: full-template
Source sequence: CUAGGCUC
Template base classes: GUGUACAC
Converted residues: 8
Mean local/template RMSD: 0.0637 Å
Max local/template RMSD: 0.1019 Å
--------------------------------------------------------------------------------
O3'(i)→P(i+1): PASS (measured=7, failed=0, mean=1.615 Å)
C1'→glycosidic N: PASS (measured=8, failed=0, mean=1.474 Å)
C2'→O2': PASS (measured=8, failed=0, mean=1.433 Å)
C1'→O4': PASS (measured=8, failed=0, mean=1.422 Å)
C4'→O4': PASS (measured=8, failed=0, mean=1.424 Å)
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
