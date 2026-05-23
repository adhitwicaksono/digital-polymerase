# Prototype 001B RNA → HNA Run Summary

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 001B
Full-template-guided RNA → HNA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-8mer.pdb
HNA template: /mnt/data/481d-HNA8nt.pdb
Output PDB: /mnt/data/hna_prototype_001B_outputs/converted_hna_RNA-8mer_001B.pdb
Report: /mnt/data/hna_prototype_001B_outputs/conversion_report_RNA-8mer_001B.md
Source sequence: CUAGGCUC
Template base classes: GUGUACAC
Converted residues: 8
Mean anchor RMSD: 0.2454 Å
Max anchor RMSD: 0.2642 Å
--------------------------------------------------------------------------------
O3′(i)→P(i+1): PASS (measured=7, failed=0, mean=1.591 Å)
C1′→glycosidic N: PASS (measured=8, failed=0, mean=1.337 Å)
================================================================================
```

```text
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
