# WIP Dataset And Task Rename Candidates

Status: implemented for the Hakari-Bench dataset YAML registry, result JSON
migration, and upload-staging dataset directories. This document intentionally
keeps the old-to-new mapping for audit and review.

Date: 2026-05-07

## Adopted Naming Policy

The NanoMTEB family follows the official MTEB benchmark-family provenance
instead of broad language buckets.

- Dedicated official-family Nano datasets use the family name when one exists:
  `NanoCMTEB`, `NanoJMTEB`, `NanoFaMTEB`, `NanoRuMTEB`, and `NanoVNMTEB`.
- `NanoMTEB-{language}` names remain only when the content maps to the
  corresponding official language MTEB family, such as Dutch, French, German,
  Korean, Scandinavian, Spanish, and Thai.
- Retrieval tasks from separate benchmarks or mixed task families are grouped
  under `NanoMTEB-Misc`, even when their detected text language is clear.
- Backward-compatible aliases are not provided. Historical results should be
  migrated forward to the canonical dataset names and paths.

This keeps dataset names tied to benchmark source, not merely query/document
language.

## Canonical NanoMTEB Family Datasets

The canonical Hugging Face datasets are:

| Dataset | Provenance rule |
|---|---|
| `NanoMTEB` | Generic English MTEB retrieval Nano tasks. |
| `NanoCMTEB` | C-MTEB / Chinese MTEB retrieval Nano tasks. |
| `NanoMTEB-Dutch` | Official Dutch MTEB-family retrieval Nano tasks. |
| `NanoMTEB-French` | Official French MTEB-family retrieval Nano tasks. |
| `NanoMTEB-German` | Official German MTEB-family retrieval Nano tasks. |
| `NanoJMTEB` | JMTEB and JMTEB-lite retrieval Nano tasks. |
| `NanoMTEB-Korean` | Official Korean MTEB-family retrieval Nano tasks available in this repository. |
| `NanoFaMTEB` | FaMTEB retrieval Nano tasks. |
| `NanoRuMTEB` | ruMTEB retrieval Nano tasks. |
| `NanoMTEB-Scandinavian` | Scandinavian MTEB retrieval Nano tasks. |
| `NanoMTEB-Spanish` | Spanish MTEB retrieval Nano tasks. |
| `NanoMTEB-Thai` | Thai MTEB retrieval Nano tasks. |
| `NanoVNMTEB` | VN-MTEB full retrieval Nano tasks. |
| `NanoMTEB-Misc` | Mixed, separate-source, or non-family retrieval Nano tasks. |

## Dataset Mapping

| Historical dataset | Canonical dataset | Split handling |
|---|---|---|
| `NanoMTEB-Chinese` | `NanoCMTEB` | All splits move unchanged. |
| `NanoMTEB-Japanese` | `NanoJMTEB` | All splits move unchanged. |
| `NanoMTEB-Xlingual` | `NanoMTEB-Misc` | All splits move unchanged. The historical name was too broad for its mixed contents. |
| `NanoMTEB-Polish` | `NanoMTEB-Misc` | All splits move unchanged because `MTEB(pol, v1)` does not provide retrieval tasks. |
| `NanoMTEB-Persian` | `NanoFaMTEB` plus `NanoMTEB-Misc` | FaMTEB-family splits move to `NanoFaMTEB`; NeuCLIR splits move to `NanoMTEB-Misc`. |
| `NanoMTEB-Russian` | `NanoRuMTEB` plus `NanoMTEB-Misc` | ruMTEB-family splits move to `NanoRuMTEB`; RuSciBench splits move to `NanoMTEB-Misc`. |
| `NanoMTEB-Vietnamese` | `NanoVNMTEB` plus `NanoMTEB-Misc` | VN-MTEB full retrieval splits move to `NanoVNMTEB`; nested MTEB task-level nano variants move to `NanoMTEB-Misc`. |
| `NanoMTEB-Dutch` | `NanoMTEB-Dutch` plus `NanoMTEB-Misc` | Dutch MTEB-family splits stay; BEIR-NL-only splits move to `NanoMTEB-Misc`. |
| `NanoMTEB-French` | `NanoMTEB-French` plus `NanoMTEB-Misc` | French MTEB-family splits stay; `NanoFQuAD` moves to `NanoMTEB-Misc`. |
| `NanoMTEB-German` | `NanoMTEB-German` plus `NanoMTEB-Misc` | German MTEB-family splits stay; `NanoGermanGovService` moves to `NanoMTEB-Misc`. |
| `NanoMTEB-Korean` | `NanoMTEB-Korean` plus `NanoMTEB-Misc` | `NanoKoStrategyQA` stays; `NanoAutoRAG`, `NanoLawIRKo`, and `NanoSQuADKorV1` move to `NanoMTEB-Misc`. |

## Split-Level Moves To `NanoMTEB-Misc`

| Historical dataset | Moved splits |
|---|---|
| `NanoMTEB-Dutch` | `NanoCQADupstackAndroidNL`, `NanoCQADupstackEnglishNL`, `NanoCQADupstackGisNL`, `NanoCQADupstackMathematicaNL`, `NanoCQADupstackPhysicsNL`, `NanoCQADupstackProgrammersNL`, `NanoCQADupstackStatsNL`, `NanoCQADupstackTexNL`, `NanoCQADupstackWebmastersNL`, `NanoCQADupstackWordpressNL`, `NanoFEVERNL`, `NanoNQNL`, `NanoQuoraNL` |
| `NanoMTEB-French` | `NanoFQuAD` |
| `NanoMTEB-German` | `NanoGermanGovService` |
| `NanoMTEB-Korean` | `NanoAutoRAG`, `NanoLawIRKo`, `NanoSQuADKorV1` |
| `NanoMTEB-Persian` | `NanoNeuCLIR2023`, `NanoNeuCLIR2023HardNegatives` |
| `NanoMTEB-Russian` | `NanoRuSciBenchCite`, `NanoRuSciBenchCocite` |
| `NanoMTEB-Vietnamese` | `NanoNanoFEVERVN`, `NanoNanoNQVN` |

## Result Migration

Existing evaluation JSON files are converted forward rather than accepted
through old registry names.

Primary result files remain under:

```text
output/hakari-results/{model_id}/{huggingface_dataset_name}/{split}.json.xz
```

For every moved split, the migration:

1. Moves the file into the new Hugging Face dataset directory, for example
   `hakari-bench__NanoMTEB-Misc`.
2. Rewrites `target.dataset_name` and `target.dataset_id`.
3. Keeps `target.split_name`, `target.task_name`, metrics, runtime metadata,
   model metadata, resolved dataset revision, and timestamps unchanged.
4. Rewrites old dataset text in `target.metadata.description` when present.
5. Refuses to overwrite a divergent destination file.

Uploadable canonical Nano dataset directories are staged separately under:

```text
output/NanoMTEB_Family/{canonical_dataset}/
```

Each child directory follows the Hugging Face dataset repo layout used by the
Nano datasets: `corpus`, `queries`, `qrels`, and `bm25` configs plus
`README.md`, `manifest.json`, `nano_bm25_subset_config.json`, and per-split
metadata. `NanoMTEB_Family` is an upload staging directory, not a
HAKARI-Bench dataset collection.

## Deferred Split Rename Candidates

The current implementation changes dataset placement only. The following split
renames remain candidates because they would require matching remote dataset
configuration changes:

| Current split name | Candidate name | Rationale |
|---|---|---|
| `NanoNanoFEVERVN` | `NanoFEVERVNSmall` | Avoids the confusing double `NanoNano` prefix while preserving distinction from full `NanoFEVERVN`. |
| `NanoNanoNQVN` | `NanoNQVNSmall` | Same nested nano-variant naming issue as `NanoNanoFEVERVN`. |
| `NanoWMT19DeFr` | `NanoCLSDWMT19DeFr` | Would make the CrossLingualSemanticDiscrimination source task clearer. |
| `NanoWMT19FrDe` | `NanoCLSDWMT19FrDe` | Same WMT source-family clarification. |
| `NanoWMT21DeFr` | `NanoCLSDWMT21DeFr` | Same WMT source-family clarification. |
| `NanoWMT21FrDe` | `NanoCLSDWMT21FrDe` | Same WMT source-family clarification. |
| `NanoMIRACL` in `NanoJMTEB` | `NanoMIRACLJa` | Optional disambiguation when aggregating split names across datasets. |
| `NanoBSARDV2` | `NanoBSARDRetrievalV2` | Optional closer alignment with the MTEB task class name. |
