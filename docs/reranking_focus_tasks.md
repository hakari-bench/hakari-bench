# Reranking-Focused Tasks

This document defines which Overall tasks the leaderboard uses by default in
Reranking mode, and why. The task list itself lives in
`config/viewer/overall_tasks.yaml` as the `reranking_focus_359` manifest, and
`config/viewer/overall.yaml` points both Overall views at it through
`reranking_task_manifest` and `reranking_expected_task_count`.

## Why A Separate Task Set

Reranking mode measures how well a model reorders a fixed top-100 candidate
list (`reranking_hybrid`, see [duckdb_schema.md](duckdb_schema.md)). Cross-encoder
rerankers are built for one job: given a user's information need and a
candidate passage, judge whether the passage satisfies that need. Many of the
550 Overall tasks reuse the retrieval format for something else, such as
finding a counterargument, matching a translation pair, or picking the correct
option of a multiple-choice question. Those tasks are valid retrieval
benchmarks for embeddings, but they reward skills that a search reranker is
not trained for and blur the comparison the Reranking tab is meant to show.

The Reranking tab therefore ranks the Overall views on 359 reranker-oriented
tasks by default. The Reranking settings row below the evaluation tabs has a
`Tasks` switch: `Reranking-focused` (default) or `All tasks`, which sets
`rerank_tasks=all` in the URL and restores the full 550-task Overall. The same
row holds the `Safeguard positives` toggle. Retrieval mode, single Nano-set views, and
Custom scopes always use their normal task sets.

## What Makes A Task Reranker-Oriented

A task is kept when all three conditions hold.

1. **The query is an information need.** A person (or a realistic simulation of
   one) is searching for something, such as a web query, a question, an FAQ
   question, a claim to verify, a patient case, or a developer problem.
2. **The relevant document satisfies that need.** It answers the question,
   provides the evidence, or is the item being searched for. Relevance is not
   defined by a structural relation such as "is the translation of", "is
   cited by", "is the duplicate of", or "is the correct option".
3. **The query is short enough to read as a search request.** The average
   query must be 150 characters or shorter. Documents may be any length.

Two refinements apply to rule 3.

- Benchmarks built specifically for reasoning-heavy or expert retrieval
  (NanoBRIGHT, NanoR2MED, NanoBIRCO, NanoIFIR) are exempt from the query-length
  limit. Their long queries are real problem descriptions, not a sign of a
  non-search task.
- Query length is judged per benchmark where the benchmark is one task in many
  languages. MNanoBEIR uses the English task's average query length for all 14
  languages, and NanoMLDR uses the mean over its 13 languages. Character counts
  differ by script, and the same task should not be kept in one language and
  dropped in another.

Query and document lengths come from `text_stats_chars` in
`task_docs/metadata/**.json`, which are mean character counts over the Nano
split.

### Task Families That Are Excluded

| Family | Examples | Why it is excluded |
| --- | --- | --- |
| Counterargument retrieval | ArguAna and its translations | Relevance is "argues against", not "answers". |
| Citation prediction | SCIDOCS, RuSciBench cite/cocite | Relevance is a citation link between papers. |
| Duplicate-question detection | Quora, CQADupStack | Symmetric paraphrase matching, not answer finding. |
| Document-to-document matching | NanoDAPFAM, AILA, LeCaRDv2, GerDaLIR, NLP Journal abstract-to-article, RELIC | The query is itself a document; this is similarity search rather than answering a need. |
| Summary to source | LegalSummarization | The query is derived from the target document. |
| Multiple-choice reasoning converted to retrieval | NanoRARb, WinoGrande, SpartQA, TempReason | The corpus is a pool of answer options. |
| Synthetic long-context probes and long-context sets | NanoLongEmbed (Passkey, Needle, NarrativeQA, 2WikiMultihopQA, QMSum, SummScreenFD), LEMB Passkey | Built to probe long-context embeddings; documents can be whole books and corpora have only 200 to 800 documents. |
| Bitext discrimination | WMT19/WMT21 cross-lingual semantic discrimination | Relevance is "is the translation of". |
| Code transformation, completion, or SQL generation | CodeTransOcean, CodeSearchNet-CCR, CodeFeedback, SyntheticText2SQL, WikiSQL | The target is a transformed artifact, not an answer to a search. |
| Synthetic query sets | NanoMuPLeR, EuroPIRQ, `syn_per_qa` | Queries are generated to match a passage rather than collected from a need. |

### Borderline Families That Are Kept

These families were reviewed individually and kept because they still pair a
search request with an answering document. Most of them are small.

- Natural-language-to-code search (CosQA, MBPP, CodeRAG programming solutions
  and online tutorials).
- Argument retrieval for a short topic (Touche-2020).
- Headline or title to body (news headline retrieval, Store norske leksikon,
  procurement and bibliography titles, NLP Journal title-to-abstract and
  title-to-introduction).
- Taxonomy mapping with short queries (NanoBuiltBench).
- Short answer strings (`mkqa_th`).

Conversational tasks and NanoSSRB structured-record search are also allowed by
category but are currently removed by the query-length rule.

## Effect On The Leaderboard

Measured on the remote DuckDB at results commit `3e6be26` (87 complete models,
safeguard positives on, base rows, nDCG@10). The top five models keep their
places. Cross-encoder rerankers move up because the removed tasks are mostly
ones that search rerankers were not trained for.

| Model | Rank on 550 tasks | Rank on 359 tasks |
| --- | ---: | ---: |
| nvidia/Nemotron-3.5-Rerank-8B-BF16 | 1 | 1 |
| BAAI/bge-reranker-v2-m3 | 13 | 6 |
| jinaai/jina-reranker-v2-base-multilingual | 19 | 13 |
| Alibaba-NLP/gte-multilingual-reranker-base | 24 | 17 |
| cross-encoder/mmarco-mMiniLMv2-L12-H384-v1 | 48 | 40 |
| openai/text-embedding-3-large | 15 | 22 |
| Qwen/Qwen3-Embedding-0.6B | 26 | 32 |
| BM25 (full-corpus reference) | 63 | 60 |

## Maintaining The Manifest

- `reranking_focus_359` must stay a subset of the Overall manifest. The viewer
  configuration loader rejects a manifest that is not a subset or whose size
  differs from `reranking_expected_task_count`.
- When a Nano-set or task joins `overall_550`, classify each new task with the
  rules above, add the eligible task keys to the reranking manifest, rename the
  manifest and update `reranking_expected_task_count` if the count changes, and
  update the tables below.
- Rebuild the DuckDB after changing the manifest so that the precomputed
  Overall Reranking rows and initial-view snapshots use the new task set. The
  `viewer_leaderboard_rows` mart stores both scopes, keyed by
  `reranking_task_scope` (`focus` and `all`), so `Reranking-focused` and
  `All tasks` are both served from precomputed rows. Until the rebuild, the
  viewer computes any scope whose stored task count no longer matches
  dynamically, which is correct but slower.
- The viewer help text describes the selection loosely (roughly two thirds of
  the tasks) on purpose, so routine manifest updates do not require help-copy
  edits. Exact counts live in this document and in `config/viewer/overall.yaml`.

## Task Tables

### Category Decisions

| Category | Decision | Included / Overall tasks |
| --- | --- | ---: |
| Information retrieval (search, QA, FAQ, fact verification) | Eligible | 292 / 299 |
| Reasoning-heavy or expert retrieval | Eligible | 35 / 35 |
| Natural-language-to-code search | Eligible | 4 / 13 |
| Argument retrieval | Eligible | 16 / 16 |
| Headline or title to body | Eligible | 9 / 9 |
| Conversational query | Eligible | 0 / 2 |
| Taxonomy or structured-record mapping | Eligible | 2 / 8 |
| Short answer string | Eligible | 1 / 1 |
| Duplicate-question detection | Excluded | 0 / 50 |
| Document-to-document matching | Excluded | 0 / 22 |
| Synthetic query set | Excluded | 0 / 18 |
| Counterargument retrieval | Excluded | 0 / 20 |
| Citation prediction | Excluded | 0 / 21 |
| Summary to source | Excluded | 0 / 1 |
| Multiple-choice reasoning converted to retrieval | Excluded | 0 / 17 |
| Synthetic long-context probe | Excluded | 0 / 1 |
| Bitext discrimination | Excluded | 0 / 4 |
| Code transformation, completion, or SQL generation | Excluded | 0 / 7 |
| Long-context evaluation set (NanoLongEmbed) | Excluded | 0 / 6 |

### Per Nano-Set Counts

| Nano-set | Included | Overall tasks |
| --- | ---: | ---: |
| MNanoBEIR | 140 | 182 |
| NanoBIRCO | 3 | 5 |
| NanoBRIGHT | 20 | 20 |
| NanoBuiltBench | 2 | 2 |
| NanoCMTEB | 8 | 8 |
| NanoChemTEB | 3 | 3 |
| NanoCoIR | 1 | 10 |
| NanoCodeRAG | 2 | 4 |
| NanoDAPFAM | 0 | 12 |
| NanoFaMTEB-v2 | 12 | 17 |
| NanoIFIR | 4 | 4 |
| NanoIndicQA | 11 | 11 |
| NanoJMTEB-v2 | 9 | 11 |
| NanoLaw | 2 | 4 |
| NanoLongEmbed | 0 | 6 |
| NanoMIRACL | 18 | 18 |
| NanoMLDR | 13 | 13 |
| NanoMMTEB-v2 | 7 | 18 |
| NanoMTEB-BR | 5 | 6 |
| NanoMTEB-Dutch | 14 | 27 |
| NanoMTEB-French | 7 | 8 |
| NanoMTEB-German | 4 | 5 |
| NanoMTEB-Korean | 5 | 5 |
| NanoMTEB-Misc | 3 | 12 |
| NanoMTEB-Polish | 3 | 14 |
| NanoMTEB-Scandinavian | 6 | 7 |
| NanoMTEB-Spanish | 7 | 7 |
| NanoMTEB-Thai | 9 | 9 |
| NanoMTEB-v2 | 6 | 10 |
| NanoMedical | 7 | 7 |
| NanoMuPLeR | 0 | 14 |
| NanoR2MED | 8 | 8 |
| NanoRARb | 0 | 14 |
| NanoRTEB | 4 | 14 |
| NanoRuMTEB | 3 | 3 |
| NanoSSRB | 0 | 6 |
| NanoVNMTEB | 13 | 26 |
| **Total** | **359** | **550** |

### Excluded Tasks

MNanoBEIR rows are listed once per task and apply to all 14 languages.

| Nano-set | Task | Reason | Judged query chars |
| --- | --- | --- | ---: |
| MNanoBEIR | NanoArguAna | Counterargument retrieval | 1202 |
| MNanoBEIR | NanoQuoraRetrieval | Duplicate-question detection | 48 |
| MNanoBEIR | NanoSCIDOCS | Citation prediction | 73 |
| NanoBIRCO | NanoBIRCOArguAna | Counterargument retrieval | 1124 |
| NanoBIRCO | NanoBIRCORelic | Document-to-document matching | 1016 |
| NanoCoIR | NanoApps | Average query longer than 150 characters | 1675 |
| NanoCoIR | NanoCodeFeedbackMT | Code transformation, completion, or SQL generation | 4469 |
| NanoCoIR | NanoCodeFeedbackST | Code transformation, completion, or SQL generation | 731 |
| NanoCoIR | NanoCodeSearchNet | Average query longer than 150 characters | 636 |
| NanoCoIR | NanoCodeSearchNetCCR | Code transformation, completion, or SQL generation | 373 |
| NanoCoIR | NanoCodeTransOceanContest | Code transformation, completion, or SQL generation | 1010 |
| NanoCoIR | NanoCodeTransOceanDL | Code transformation, completion, or SQL generation | 2154 |
| NanoCoIR | NanoStackOverflowQA | Average query longer than 150 characters | 1362 |
| NanoCoIR | NanoSyntheticText2SQL | Code transformation, completion, or SQL generation | 103 |
| NanoCodeRAG | NanoCodeRAGLibraryDocumentationSolutions | Average query longer than 150 characters | 397 |
| NanoCodeRAG | NanoCodeRAGStackoverflowPosts | Average query longer than 150 characters | 210 |
| NanoDAPFAM | NanoDAPFAMAllTitlAbsClmToTitlAbs | Document-to-document matching | 8339 |
| NanoDAPFAM | NanoDAPFAMAllTitlAbsClmToTitlAbsClm | Document-to-document matching | 8339 |
| NanoDAPFAM | NanoDAPFAMAllTitlAbsToTitlAbs | Document-to-document matching | 776 |
| NanoDAPFAM | NanoDAPFAMAllTitlAbsToTitlAbsClm | Document-to-document matching | 776 |
| NanoDAPFAM | NanoDAPFAMInTitlAbsClmToTitlAbs | Document-to-document matching | 8405 |
| NanoDAPFAM | NanoDAPFAMInTitlAbsClmToTitlAbsClm | Document-to-document matching | 8405 |
| NanoDAPFAM | NanoDAPFAMInTitlAbsToTitlAbs | Document-to-document matching | 771 |
| NanoDAPFAM | NanoDAPFAMInTitlAbsToTitlAbsClm | Document-to-document matching | 771 |
| NanoDAPFAM | NanoDAPFAMOutTitlAbsClmToTitlAbs | Document-to-document matching | 9316 |
| NanoDAPFAM | NanoDAPFAMOutTitlAbsClmToTitlAbsClm | Document-to-document matching | 9316 |
| NanoDAPFAM | NanoDAPFAMOutTitlAbsToTitlAbs | Document-to-document matching | 787 |
| NanoDAPFAM | NanoDAPFAMOutTitlAbsToTitlAbsClm | Document-to-document matching | 787 |
| NanoFaMTEB-v2 | argu_ana_fa | Counterargument retrieval | 1101 |
| NanoFaMTEB-v2 | quora_fa | Duplicate-question detection | 49 |
| NanoFaMTEB-v2 | scidocs_fa | Citation prediction | 62 |
| NanoFaMTEB-v2 | syn_per_chatbot_ragfaq | Average query longer than 150 characters | 597 |
| NanoFaMTEB-v2 | syn_per_qa | Synthetic query set | 60 |
| NanoJMTEB-v2 | nlpjournal_abs_article | Document-to-document matching | 495 |
| NanoJMTEB-v2 | nlpjournal_abs_intro | Document-to-document matching | 495 |
| NanoLaw | NanoGerDaLIRSmall | Document-to-document matching | 890 |
| NanoLaw | NanoLeCaRDv2 | Document-to-document matching | 4259 |
| NanoLongEmbed | Nano2WikiMultihopQA | Long-context evaluation set (NanoLongEmbed) | 68 |
| NanoLongEmbed | NanoNarrativeQA | Long-context evaluation set (NanoLongEmbed) | 49 |
| NanoLongEmbed | NanoNeedle | Long-context evaluation set (NanoLongEmbed) | 59 |
| NanoLongEmbed | NanoPasskey | Long-context evaluation set (NanoLongEmbed) | 38 |
| NanoLongEmbed | NanoQMSum | Long-context evaluation set (NanoLongEmbed) | 446 |
| NanoLongEmbed | NanoSummScreenFD | Long-context evaluation set (NanoLongEmbed) | 601 |
| NanoMMTEB-v2 | ailastatutes | Document-to-document matching | 3038 |
| NanoMMTEB-v2 | argu_ana | Counterargument retrieval | 1200 |
| NanoMMTEB-v2 | legal_bench_corporate_lobbying | Document-to-document matching | 180 |
| NanoMMTEB-v2 | lembpasskey | Synthetic long-context probe | 38 |
| NanoMMTEB-v2 | scidocs | Citation prediction | 70 |
| NanoMMTEB-v2 | spart_qa | Multiple-choice reasoning converted to retrieval | 655 |
| NanoMMTEB-v2 | stack_overflow_qa | Average query longer than 150 characters | 1362 |
| NanoMMTEB-v2 | statcan_dialogue_dataset | Average query longer than 150 characters | 795 |
| NanoMMTEB-v2 | temp_reason_l1 | Multiple-choice reasoning converted to retrieval | 50 |
| NanoMMTEB-v2 | twitter_hjerne | Average query longer than 150 characters | 166 |
| NanoMMTEB-v2 | wino_grande | Multiple-choice reasoning converted to retrieval | 112 |
| NanoMTEB-BR | MedPTRetrieval | Average query longer than 150 characters | 152 |
| NanoMTEB-Dutch | argu_ana_nl | Counterargument retrieval | 1317 |
| NanoMTEB-Dutch | cqadupstack_android | Duplicate-question detection | 59 |
| NanoMTEB-Dutch | cqadupstack_english | Duplicate-question detection | 50 |
| NanoMTEB-Dutch | cqadupstack_gis | Duplicate-question detection | 63 |
| NanoMTEB-Dutch | cqadupstack_mathematica | Duplicate-question detection | 55 |
| NanoMTEB-Dutch | cqadupstack_physics | Duplicate-question detection | 62 |
| NanoMTEB-Dutch | cqadupstack_programmers | Duplicate-question detection | 61 |
| NanoMTEB-Dutch | cqadupstack_stats | Duplicate-question detection | 64 |
| NanoMTEB-Dutch | cqadupstack_tex | Duplicate-question detection | 54 |
| NanoMTEB-Dutch | cqadupstack_webmasters | Duplicate-question detection | 59 |
| NanoMTEB-Dutch | cqadupstack_wordpress | Duplicate-question detection | 57 |
| NanoMTEB-Dutch | quora | Duplicate-question detection | 52 |
| NanoMTEB-Dutch | scidocs_nl | Citation prediction | 78 |
| NanoMTEB-French | alloprof | Average query longer than 150 characters | 179 |
| NanoMTEB-German | ger_da_lir | Document-to-document matching | 880 |
| NanoMTEB-Misc | cite_ru | Citation prediction | 1399 |
| NanoMTEB-Misc | cocite_ru | Citation prediction | 962 |
| NanoMTEB-Misc | en | Synthetic query set | 140 |
| NanoMTEB-Misc | fi | Synthetic query set | 147 |
| NanoMTEB-Misc | pt | Synthetic query set | 150 |
| NanoMTEB-Misc | wmt19_de_fr | Bitext discrimination | 159 |
| NanoMTEB-Misc | wmt19_fr_de | Bitext discrimination | 149 |
| NanoMTEB-Misc | wmt21_de_fr | Bitext discrimination | 170 |
| NanoMTEB-Misc | wmt21_fr_de | Bitext discrimination | 175 |
| NanoMTEB-Polish | cqadupstack_android | Duplicate-question detection | 59 |
| NanoMTEB-Polish | cqadupstack_english | Duplicate-question detection | 47 |
| NanoMTEB-Polish | cqadupstack_gis | Duplicate-question detection | 61 |
| NanoMTEB-Polish | cqadupstack_mathematica | Duplicate-question detection | 50 |
| NanoMTEB-Polish | cqadupstack_physics | Duplicate-question detection | 59 |
| NanoMTEB-Polish | cqadupstack_programmers | Duplicate-question detection | 59 |
| NanoMTEB-Polish | cqadupstack_stats | Duplicate-question detection | 61 |
| NanoMTEB-Polish | cqadupstack_tex | Duplicate-question detection | 50 |
| NanoMTEB-Polish | cqadupstack_webmasters | Duplicate-question detection | 60 |
| NanoMTEB-Polish | cqadupstack_wordpress | Duplicate-question detection | 56 |
| NanoMTEB-Polish | quora | Duplicate-question detection | 53 |
| NanoMTEB-Scandinavian | twitter_hjerne | Average query longer than 150 characters | 166 |
| NanoMTEB-v2 | argu_ana | Counterargument retrieval | 1200 |
| NanoMTEB-v2 | cqadupstack_gaming | Duplicate-question detection | 48 |
| NanoMTEB-v2 | cqadupstack_unix | Duplicate-question detection | 49 |
| NanoMTEB-v2 | scidocs | Citation prediction | 70 |
| NanoMuPLeR | el | Synthetic query set | 141 |
| NanoMuPLeR | en | Synthetic query set | 135 |
| NanoMuPLeR | es | Synthetic query set | 135 |
| NanoMuPLeR | fi | Synthetic query set | 160 |
| NanoMuPLeR | fr | Synthetic query set | 141 |
| NanoMuPLeR | it | Synthetic query set | 141 |
| NanoMuPLeR | lt | Synthetic query set | 143 |
| NanoMuPLeR | lv | Synthetic query set | 140 |
| NanoMuPLeR | nl | Synthetic query set | 148 |
| NanoMuPLeR | pl | Synthetic query set | 144 |
| NanoMuPLeR | pt | Synthetic query set | 135 |
| NanoMuPLeR | sk | Synthetic query set | 136 |
| NanoMuPLeR | sl | Synthetic query set | 136 |
| NanoMuPLeR | sv | Synthetic query set | 144 |
| NanoRARb | NanoARCChallenge | Multiple-choice reasoning converted to retrieval | 127 |
| NanoRARb | NanoAlphaNLI | Multiple-choice reasoning converted to retrieval | 104 |
| NanoRARb | NanoHellaSwag | Multiple-choice reasoning converted to retrieval | 115 |
| NanoRARb | NanoPIQA | Multiple-choice reasoning converted to retrieval | 38 |
| NanoRARb | NanoQuail | Multiple-choice reasoning converted to retrieval | 1814 |
| NanoRARb | NanoRARbCode | Multiple-choice reasoning converted to retrieval | 470 |
| NanoRARb | NanoRARbMath | Multiple-choice reasoning converted to retrieval | 201 |
| NanoRARb | NanoSIQA | Multiple-choice reasoning converted to retrieval | 127 |
| NanoRARb | NanoTempReasonL2Context | Multiple-choice reasoning converted to retrieval | 28755 |
| NanoRARb | NanoTempReasonL2Fact | Multiple-choice reasoning converted to retrieval | 1744 |
| NanoRARb | NanoTempReasonL2Pure | Multiple-choice reasoning converted to retrieval | 53 |
| NanoRARb | NanoTempReasonL3Context | Multiple-choice reasoning converted to retrieval | 31804 |
| NanoRARb | NanoTempReasonL3Fact | Multiple-choice reasoning converted to retrieval | 1981 |
| NanoRARb | NanoTempReasonL3Pure | Multiple-choice reasoning converted to retrieval | 65 |
| NanoRTEB | NanoAILACasedocs | Document-to-document matching | 3038 |
| NanoRTEB | NanoAILAStatutes | Document-to-document matching | 3038 |
| NanoRTEB | NanoApps | Average query longer than 150 characters | 1675 |
| NanoRTEB | NanoChatDoctor | Average query longer than 150 characters | 441 |
| NanoRTEB | NanoDS1000 | Average query longer than 150 characters | 1154 |
| NanoRTEB | NanoFinanceBench | Average query longer than 150 characters | 161 |
| NanoRTEB | NanoFreshStack | Average query longer than 150 characters | 1660 |
| NanoRTEB | NanoHumanEval | Average query longer than 150 characters | 291 |
| NanoRTEB | NanoLegalSummarization | Summary to source | 103 |
| NanoRTEB | NanoWikiSQL | Code transformation, completion, or SQL generation | 1551 |
| NanoSSRB | Academic | Average query longer than 150 characters | 298 |
| NanoSSRB | FinanceAndEconomics | Average query longer than 150 characters | 314 |
| NanoSSRB | HumanResources | Average query longer than 150 characters | 321 |
| NanoSSRB | LLMAgentAndTool | Average query longer than 150 characters | 362 |
| NanoSSRB | ProductSearch | Average query longer than 150 characters | 232 |
| NanoSSRB | ResumeSearch | Average query longer than 150 characters | 443 |
| NanoVNMTEB | argu_ana_vn | Counterargument retrieval | 1184 |
| NanoVNMTEB | cqadupstack_android_vn | Duplicate-question detection | 56 |
| NanoVNMTEB | cqadupstack_gis_vn | Duplicate-question detection | 59 |
| NanoVNMTEB | cqadupstack_mathematica_vn | Duplicate-question detection | 49 |
| NanoVNMTEB | cqadupstack_physics_vn | Duplicate-question detection | 59 |
| NanoVNMTEB | cqadupstack_programmers_vn | Duplicate-question detection | 59 |
| NanoVNMTEB | cqadupstack_stats_vn | Duplicate-question detection | 53 |
| NanoVNMTEB | cqadupstack_tex_vn | Duplicate-question detection | 48 |
| NanoVNMTEB | cqadupstack_unix_vn | Duplicate-question detection | 53 |
| NanoVNMTEB | cqadupstack_webmasters_vn | Duplicate-question detection | 58 |
| NanoVNMTEB | cqadupstack_wordpress_vn | Duplicate-question detection | 52 |
| NanoVNMTEB | quora_vn | Duplicate-question detection | 77 |
| NanoVNMTEB | scidocs_vn | Citation prediction | 73 |
