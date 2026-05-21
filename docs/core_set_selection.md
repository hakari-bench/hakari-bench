# HAKARI Core Set Selection Rationale

Research date: 2026-05-21 JST

## Abstract

The HAKARI Core set is the small, curated leaderboard view intended to answer a
single question: how should a dense retrieval model be compared when the full
HAKARI benchmark inventory is too large to interpret at once? The selected Core
set is:

1. `MNanoBEIR`
2. `NanoMMTEB-v2`
3. `NanoRTEB`
4. `NanoMLDR`
5. `NanoBRIGHT`
6. `NanoLaw`
7. `NanoCoIR`

This document records why these seven Nano sets were selected. The decision was
made by combining external adoption signals, source benchmark quality, task and
language diversity, overlap analysis, lexical baseline difficulty, and actual
dense-model score dispersion from the evaluated DuckDB warehouse. The goal was
not to maximize task count. It was to keep a compact set whose aggregate score
is interpretable, broad, and difficult to game by over-weighting one benchmark
family.

The Core score also uses configured aggregation units rather than blindly
averaging every raw task row. In particular, `MNanoBEIR` is aggregated by
`task_name`: an ArguAna-style task is first averaged across its language
variants and then contributes as one Core scoring unit. This preserves the
multilingual BEIR anchor without allowing the raw language x task matrix to
dominate the Core aggregate.

## Final Core Set

| Position | Nano set | Role in Core | Main reason for inclusion |
| ---: | --- | --- | --- |
| 1 | `MNanoBEIR` | Classical multilingual IR anchor | BEIR-style retrieval remains a common reference point; Core aggregates it by source task name so multilingual coverage does not dominate by raw row count. |
| 2 | `NanoMMTEB-v2` | Broad multilingual MTEB/MMTEB anchor | Represents modern MTEB-style retrieval coverage across many task types and languages. |
| 3 | `NanoRTEB` | Practical retrieval domains | Adds English RTEB-style applied retrieval tasks with strong model separation. |
| 4 | `NanoMLDR` | Multilingual long-document retrieval | Strong external adoption through BGE-M3/MLDR and excellent dense score dispersion across all languages. |
| 5 | `NanoBRIGHT` | Reasoning-heavy retrieval stress test | Hard tasks with high model separation and strong dataset usage signals. |
| 6 | `NanoLaw` | Legal-domain retrieval | A multilingual, multi-source legal retrieval group whose tasks are registered in MTEB and better supported than `NanoBIRCO` as a Core domain representative. |
| 7 | `NanoCoIR` | Code retrieval | Preserves a code-search dimension that is not captured by legal, long-document, or general IR tasks. |

## Pruned or Not Promoted Sets

The Core set was deliberately pruned. These decisions are as important as the
selected set because they prevent the Core score from becoming a second copy of
the `All` view.

| Nano set | Decision | Reason |
| --- | --- | --- |
| `NanoMIRACL` | Removed from Core after review | MIRACL remains a canonical multilingual benchmark, but the analyzed dense results showed substantial saturation and low model separation. Its role is better served by the `All` and benchmark-specific views than by the compact Core score. |
| `NanoLongEmbed` | Removed from the earlier Core proposal | Dense dispersion was good, but the set contains synthetic long-context probes such as passkey/needle-style tasks and has weaker external adoption than `NanoMLDR`. `NanoMLDR` gives a cleaner multilingual long-document retrieval signal. |
| `NanoBIRCO` | Replaced by `NanoLaw` | `NanoBIRCO` is valuable as a complex-objective stress test, but it is small, English-only, and has weaker paper and dataset adoption signals. `NanoLaw` provides a better Core domain slot. |
| `NanoDAPFAM` | Not promoted | Patent retrieval is distinctive, but dense model dispersion was very low and many tasks were floor-like. Better suited to a domain appendix. |
| `NanoMedical` | Not promoted | Useful medical benchmark, but after overlap removal it is less discriminative than `NanoBRIGHT`, `NanoMLDR`, or `NanoRTEB`. |
| `NanoR2MED` | Not promoted | Hard medical reasoning stress test with good dispersion, but newer and less established. Better as an optional stress suite. |
| `NanoMuPLeR` | Not promoted | Good dense dispersion, but high average scores and a narrow multilingual task shape. Keep as a language/domain appendix rather than Core. |
| `NanoJMTEB-v2` and other language-family NanoMTEB groups | Not promoted | Important for language-specific diagnostics, but including them in Core would over-weight MTEB-family language views. |
| `NanoCMTEB` | Deferred | Present in configuration, but the analyzed DuckDB did not contain comparable dense base rows for this set. |

## Selection Criteria

The Core set was chosen using five criteria.

1. External benchmark credibility

   Core tasks should come from benchmarks or datasets that are used outside this
   repository. Signals included paper citations, Hugging Face dataset likes and
   downloads, and whether the source tasks are registered in the official MTEB
   task catalog.

2. Task diversity

   The final set covers classical multilingual IR, broad MTEB/MMTEB retrieval,
   RTEB-style applied retrieval, multilingual long-document retrieval, hard
   reasoning retrieval, legal retrieval, and code retrieval.

3. Language diversity

   The set contains broad multilingual groups (`MNanoBEIR`, `NanoMMTEB-v2`,
   `NanoMLDR`) while avoiding a Core made mostly of language-specific
   MTEB-family views.

4. Low redundancy

   Candidate groups were checked for source-task overlap and for rank
   correlation across evaluated dense models. Some overlap is intentional for
   anchor tasks, but the final set avoids adding multiple groups that primarily
   express the same signal.

5. Empirical model separation

   A benchmark should usually distinguish current dense models. We therefore
   measured per-task score dispersion across ten evaluated dense embedding
   models, using only base dense rows and excluding embedding variants.

## Evidence from Evaluated Dense Results

Dense score evidence came from the evaluated DuckDB warehouse available on
2026-05-21. The analyzed rows used `embedding_variant_name IS NULL`, so int8,
binary, truncate, and rescore variants were excluded. Ten dense embedding
models had complete base results for 514 tasks across 32 benchmark groups.

For each task, we computed score dispersion across the ten models. The table
below reports benchmark-level means over those task-level statistics.

Definitions:

- `avg_mean`: average task mean score across the ten dense models.
- `avg_std`: average within-task standard deviation across the ten models.
- `p90-p10`: average within-task 90th percentile minus 10th percentile.
- `ceiling`: tasks with mean >= 0.90 and std <= 0.05.
- `floor`: tasks with mean <= 0.25 and std <= 0.05.
- `low-var`: tasks with std <= 0.03.
- `healthy`: tasks with 0.25 < mean < 0.85 and std >= 0.05.

| Nano set | Dense analysis task rows | avg_mean | avg_std | p90-p10 | ceiling | floor | low-var | healthy |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `MNanoBEIR` | 182 raw, grouped by `task_name` in Core | 0.5521 | 0.0476 | 0.1042 | 2 | 1 | 16 | 73 |
| `NanoMMTEB-v2` proxy | 18 | 0.5434 | 0.0572 | 0.1206 | 5 | 2 | 5 | 9 |
| `NanoRTEB` | 14 | 0.5954 | 0.0960 | 0.2203 | 0 | 0 | 0 | 11 |
| `NanoMLDR` | 13 | 0.5399 | 0.0844 | 0.1918 | 0 | 0 | 0 | 13 |
| `NanoBRIGHT` | 20 | 0.3289 | 0.1021 | 0.2436 | 0 | 2 | 0 | 14 |
| `NanoLaw` after Core overlap exclusions | 4 | 0.5634 | 0.0686 | 0.1516 | 0 | 0 | 0 | 4 |
| `NanoCoIR` | 10 | 0.7872 | 0.0938 | 0.2115 | 3 | 0 | 0 | 4 |

The analyzed result database still stored the current `NanoMMTEB-v2` family
under the legacy `NanoMMTEB` benchmark label, so the row above is used as the
best available dense-result proxy for `NanoMMTEB-v2`.

This table explains several choices:

- `NanoMLDR` was selected over `NanoLongEmbed` because all 13 `NanoMLDR` tasks
  were healthy and because its external adoption signals are stronger.
- `NanoBRIGHT` and `NanoRTEB` were retained because they show high model
  separation and few saturation artifacts.
- `NanoMIRACL` was removed from Core because its recognition as a multilingual
  benchmark did not offset the low dense-model dispersion observed in this
  result warehouse.
- `NanoLaw` was selected over `NanoBIRCO` after comparing domain coverage,
  MTEB registration, citations, and effective Core overlap.

## Evidence from Pruned Alternatives

| Nano set | Effective tasks | avg_mean | avg_std | p90-p10 | ceiling | floor | low-var | healthy | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `NanoMIRACL` | 18 | 0.7880 | 0.0280 | 0.0597 | 1 | 0 | 12 | 1 | Canonical multilingual benchmark, but too saturated and low-variance for the compact Core score. |
| `NanoLongEmbed` | 6 | 0.6265 | 0.0911 | 0.2049 | 0 | 0 | 0 | 3 | Good dispersion, but weaker external signal and more synthetic long-context overlap than `NanoMLDR`. |
| `NanoBIRCO` | 5 | 0.2890 | 0.0618 | 0.1182 | 0 | 1 | 1 | 3 | Valuable hard benchmark, but smaller, English-only, and weaker external signal than `NanoLaw`. |
| `NanoDAPFAM` | 18 | 0.2870 | 0.0322 | 0.0754 | 0 | 6 | 8 | 0 | Too low-variance for Core, despite being domain-distinct. |
| `NanoMedical` after overlap exclusions | 7 | 0.5323 | 0.0509 | 0.1059 | 0 | 0 | 0 | 4 | Reasonable optional domain set, but not stronger than selected Core candidates. |
| `NanoR2MED` | 8 | 0.2626 | 0.0944 | 0.2264 | 0 | 2 | 0 | 5 | Hard and discriminative, but newer and less established. |
| `NanoMuPLeR` | 14 | 0.8113 | 0.0765 | 0.1848 | 0 | 0 | 0 | 11 | Strong optional language/domain suite, but high-score and narrower than Core needs. |
| `NanoJMTEB-v2` | 11 | 0.8132 | 0.0430 | 0.0945 | 4 | 0 | 5 | 2 | Important Japanese diagnostic set, but too saturated and language-specific for Core. |

## External Adoption and Source Quality

External signals were collected on 2026-05-21. Citation counts were treated as
directional rather than exact because Crossref, OpenAlex, Google Scholar, and
Hugging Face paper pages count different objects and update at different times.
Newer papers are expected to have fewer citations.

| Evidence item | Observed signal | Interpretation |
| --- | --- | --- |
| MTEB paper | Crossref 307 citations, OpenAlex 350 citations | Strong source signal for MTEB-family retrieval tasks and the general evaluation design. |
| MMTEB paper | OpenAlex 11 citations, Hugging Face paper page with 1,072 citing datasets | Newer than MTEB, but already visible through dataset usage. |
| BEIR | Very high external recognition; citation counts vary widely by source | Supports keeping a BEIR-style multilingual anchor through `MNanoBEIR`. |
| MIRACL | Crossref 37 citations, OpenAlex 35 citations | Moderate citation signal, but a canonical multilingual retrieval benchmark. |
| BGE-M3 / MLDR | Crossref 419 citations, OpenAlex 384 citations, Hugging Face paper page with 444 citing models | Strong reason to promote `NanoMLDR` into Core. |
| BRIGHT | OpenAlex 3 citations, but `xlangai/BRIGHT` had 71 HF likes and 17,528 downloads | New benchmark with strong dataset usage and high empirical discrimination. |
| LegalBench | OpenAlex 131 citations | Strong legal benchmark signal within `NanoLaw`. |
| LegalBench plus other NanoLaw source papers | Approximately 208 OpenAlex citations across the inspected legal source papers | `NanoLaw` is not one paper, but its component tasks are better supported than a single weakly cited group. |
| BIRCO | OpenAlex 1 citation | Valuable and difficult, but less established than `NanoLaw` for a Core domain slot. |
| CoIR | ACL 2025-era source with low early citations | Kept because code retrieval is a distinct capability axis and citations are expected to lag for recent work. |

## MTEB Registration Check

Official MTEB registration was checked against
`embeddings-benchmark/mteb` main at commit
`16cc3869619c78499c34bdb59533004899b0f4dc` on 2026-05-21. This matters because
tasks already present in MTEB are more likely to be understood, reproduced, and
compared by external users.

All `NanoLaw` tasks map to MTEB retrieval tasks:

| NanoLaw task | MTEB task name |
| --- | --- |
| `NanoAILACasedocs` | `AILACasedocs` |
| `NanoAILAStatutes` | `AILAStatutes` |
| `NanoGerDaLIRSmall` | `GerDaLIRSmall` |
| `NanoLeCaRDv2` | `LeCaRDv2` |
| `NanoLegalBenchConsumerContractsQA` | `LegalBenchConsumerContractsQA` |
| `NanoLegalBenchCorporateLobbying` | `LegalBenchCorporateLobbying` |
| `NanoLegalQuAD` | `LegalQuAD` |
| `NanoLegalSummarization` | `LegalSummarization` |

All `NanoBIRCO` tasks also map to MTEB retrieval tasks:

| NanoBIRCO task | MTEB task name |
| --- | --- |
| `NanoBIRCOArguAna` | `BIRCO-ArguAna` |
| `NanoBIRCOClinicalTrial` | `BIRCO-ClinicalTrial` |
| `NanoBIRCODorisMae` | `BIRCO-DorisMae` |
| `NanoBIRCORelic` | `BIRCO-Relic` |
| `NanoBIRCOWTB` | `BIRCO-WTB` |

The MTEB check therefore did not disqualify `NanoBIRCO`. The deciding factor
was that `NanoLaw` gives the Core set a clearer, externally supported legal
domain dimension, whereas `NanoBIRCO` is better kept as a specialized hard
complex-objective group in `All` and `Group`.

## NanoLaw versus NanoBIRCO

The final replacement of `NanoBIRCO` with `NanoLaw` was the most important
late-stage decision.

| Property | `NanoLaw` | `NanoBIRCO` |
| --- | ---: | ---: |
| Domain | Legal retrieval | Complex-objective general IR |
| Languages | English, German, Chinese | English |
| Subtasks | 8 | 5 |
| Queries | 1,259 | 408 |
| Split-local documents | 15,142 | 18,789 |
| Positive qrels | 5,488 | 2,909 |
| Query-weighted BM25 nDCG@10 | 0.6275 | 0.1822 |
| Query-weighted BM25 hit@10 | 0.8133 | 0.3750 |
| Effective Core tasks after overlap removal | 4 | 5 |
| Dense healthy tasks | 4 of 4 effective tasks | 3 of 5 tasks |

`NanoBIRCO` is lexically much harder and remains useful for diagnostics. However,
Core should not only be hard. It should also be legible to leaderboard users and
defensible as a representative sample of important retrieval use cases.
`NanoLaw` is stronger on that axis because it bundles multiple legal retrieval
families across jurisdictions, languages, and source papers.

## Dataset Scale and Lexical Baselines

The Core set mixes easy, hard, and lexical-overlap-resistant tasks. Some Core
components have strong BM25 baselines because the source task is lexical by
nature. Others are deliberately hard for BM25.

| Nano set | Subtasks | Queries | Split-local documents | Positive qrels | Query-weighted BM25 nDCG@10 | Query-weighted BM25 hit@10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `NanoMLDR` | 13 | 2,089 | 55,585 | 2,089 | 0.7178 | 0.7946 |
| `NanoBRIGHT` | 20 | 2,245 | 121,771 | 9,287 | 0.2156 | 0.4454 |
| `NanoLaw` | 8 | 1,259 | 15,142 | 5,488 | 0.6275 | 0.8133 |
| `NanoCoIR` | 10 | 1,850 | 76,295 | 1,850 | 0.5965 | 0.6962 |
| `NanoBIRCO` | 5 | 408 | 18,789 | 2,909 | 0.1822 | 0.3750 |

These baselines also explain why Core keeps both domain and reasoning stress
sets. `NanoBRIGHT` provides hard reasoning-heavy retrieval where BM25 is weak.
`NanoLaw` provides legal-domain retrieval where lexical signals can be strong
but not sufficient. `NanoCoIR` keeps a code retrieval axis whose failure modes
are different again.

## Aggregation and Overlap Policy

Core normally uses one scoring unit per raw task row, except for explicitly
configured grouped components. The important exception is `MNanoBEIR`, where
Core uses `group_by: task_name` so that each BEIR source task contributes once
after averaging across language variants.

Some benchmark configurations also define excluded tasks to prevent duplicate
source tasks from being counted twice in benchmark-specific views. For
`NanoLaw`, the following tasks overlap with `NanoRTEB` or `NanoMMTEB-v2` and
are excluded by the viewer configuration when appropriate:

- `NanoAILACasedocs`
- `NanoAILAStatutes`
- `NanoLegalBenchCorporateLobbying`
- `NanoLegalSummarization`

The remaining effective `NanoLaw` contribution is still useful:

- `NanoGerDaLIRSmall`
- `NanoLeCaRDv2`
- `NanoLegalBenchConsumerContractsQA`
- `NanoLegalQuAD`

Those four effective tasks were all healthy in the dense dispersion analysis.

## Limitations

This selection should be revisited when one of the following changes:

- More dense models are evaluated across all Nano groups.
- `NanoCMTEB` receives comparable dense base results in the same DuckDB schema.
- A new domain benchmark achieves both strong external adoption and strong model
  separation.
- MTEB or MMTEB significantly changes the registered task catalog.
- Saturation increases on `NanoCoIR` or `NanoMMTEB-v2` enough to reduce their
  usefulness as Core components.

The Core set is not intended to replace the full `All` view. It is a compact
summary. Domain and language-specific diagnosis should still use `All`,
`Group`, and the individual benchmark views.

## References and Source Pointers

- HAKARI Core configuration: `config/viewer/overall.yaml`.
- HAKARI benchmark metadata and task docs: `docs/benchmark_tasks/`.
- Dense-result warehouse used for the 2026-05-21 analysis:
  `output/results/hakari_bench.duckdb` in the evaluated local worktree.
- Official MTEB repository checked on 2026-05-21:
  <https://github.com/embeddings-benchmark/mteb>.
- BEIR paper: <https://arxiv.org/abs/2104.08663>.
- MTEB paper: <https://aclanthology.org/2023.eacl-main.148/>.
- MMTEB paper: <https://arxiv.org/abs/2502.13595>.
- MIRACL paper: <https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00595/116724/MIRACL-A-Multilingual-Retrieval-Dataset>.
- BGE-M3 / MLDR paper: <https://aclanthology.org/2024.findings-acl.137/>.
- BRIGHT paper: <https://arxiv.org/abs/2407.12883>.
- LegalBench paper: <https://arxiv.org/abs/2308.11462>.
- BIRCO paper: <https://arxiv.org/abs/2402.14151>.
- CoIR paper: <https://aclanthology.org/2025.acl-long.1072/>.
