# Prototype 002A.1 Patch Test Summary

## 8mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 002A.1
Fragment-guided RNA → ANA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-8mer.pdb
ANA template: /mnt/data/1ho6_ANApart.pdb
Output PDB: /mnt/data/ana_patch_002A1_test_outputs/converted_ana_8mer_patched.pdb
Report: /mnt/data/ana_patch_002A1_test_outputs/conversion_report_8mer_patched.md
Converted residues: 8
Source sequence: CUAGGCUC
Mean anchor RMSD: 0.3239 Å
Max anchor RMSD: 0.3562 Å
--------------------------------------------------------------------------------
Chain-continuity validation:
  O3′(i)→P(i+1): FAIL
  measured=7, failed=7, mean=3.203 Å, min=0.935 Å, max=5.302 Å
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

## 12mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 002A.1
Fragment-guided RNA → ANA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-12mer.pdb
ANA template: /mnt/data/1ho6_ANApart.pdb
Output PDB: /mnt/data/ana_patch_002A1_test_outputs/converted_ana_12mer_patched.pdb
Report: /mnt/data/ana_patch_002A1_test_outputs/conversion_report_12mer_patched.md
Converted residues: 12
Source sequence: CUAGGCUCGAAA
Mean anchor RMSD: 0.3249 Å
Max anchor RMSD: 0.3562 Å
--------------------------------------------------------------------------------
Chain-continuity validation:
  O3′(i)→P(i+1): FAIL
  measured=11, failed=11, mean=2.793 Å, min=0.847 Å, max=5.302 Å
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

## 16mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 002A.1
Fragment-guided RNA → ANA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-16mer.pdb
ANA template: /mnt/data/1ho6_ANApart.pdb
Output PDB: /mnt/data/ana_patch_002A1_test_outputs/converted_ana_16mer_patched.pdb
Report: /mnt/data/ana_patch_002A1_test_outputs/conversion_report_16mer_patched.md
Converted residues: 16
Source sequence: ACCACCUAGGCUCGAA
Mean anchor RMSD: 0.3248 Å
Max anchor RMSD: 0.3562 Å
--------------------------------------------------------------------------------
Chain-continuity validation:
  O3′(i)→P(i+1): FAIL
  measured=15, failed=15, mean=2.965 Å, min=0.847 Å, max=5.302 Å
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

## 22mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 002A.1
Fragment-guided RNA → ANA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-22mer.pdb
ANA template: /mnt/data/1ho6_ANApart.pdb
Output PDB: /mnt/data/ana_patch_002A1_test_outputs/converted_ana_22mer_patched.pdb
Report: /mnt/data/ana_patch_002A1_test_outputs/conversion_report_22mer_patched.md
Converted residues: 22
Source sequence: AUACGACCACCUAGGCUCGAAA
Mean anchor RMSD: 0.2950 Å
Max anchor RMSD: 0.3562 Å
--------------------------------------------------------------------------------
Chain-continuity validation:
  O3′(i)→P(i+1): FAIL
  measured=21, failed=19, mean=2.635 Å, min=0.847 Å, max=5.302 Å
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

## 34mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 002A.1
Fragment-guided RNA → ANA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-34mer.pdb
ANA template: /mnt/data/1ho6_ANApart.pdb
Output PDB: /mnt/data/ana_patch_002A1_test_outputs/converted_ana_34mer_patched.pdb
Report: /mnt/data/ana_patch_002A1_test_outputs/conversion_report_34mer_patched.md
Converted residues: 34
Source sequence: GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC
Mean anchor RMSD: 0.3047 Å
Max anchor RMSD: 0.3562 Å
--------------------------------------------------------------------------------
Chain-continuity validation:
  O3′(i)→P(i+1): FAIL
  measured=33, failed=31, mean=2.968 Å, min=0.847 Å, max=6.349 Å
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

## HH_111mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 002A.1
Fragment-guided RNA → ANA candidate reconstruction
================================================================================
Source RNA: /mnt/data/8t5o-HH-typeI-111mer-full.pdb
ANA template: /mnt/data/1ho6_ANApart.pdb
Output PDB: /mnt/data/ana_patch_002A1_test_outputs/converted_ana_HH_111mer_patched.pdb
Report: /mnt/data/ana_patch_002A1_test_outputs/conversion_report_HH_111mer_patched.md
Converted residues: 111
Source sequence: GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC
Mean anchor RMSD: 0.2994 Å
Max anchor RMSD: 0.3562 Å
--------------------------------------------------------------------------------
Chain-continuity validation:
  O3′(i)→P(i+1): FAIL
  measured=109, failed=103, mean=3.045 Å, min=0.847 Å, max=6.349 Å
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
