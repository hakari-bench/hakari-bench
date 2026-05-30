# NanoFaMTEB-v2

## Overview

NanoFaMTEB-v2 is the compact Persian retrieval group for FaMTEB. It covers
seventeen Persian natural-language retrieval tasks, including argument
retrieval, fact-verification evidence, finance QA, multi-hop QA, MIRACL and
Natural Questions style passage retrieval, MS MARCO-style search, NeuCLIR news
retrieval, Persian web search, duplicate-question retrieval, scientific and
biomedical search, synthetic QA, chatbot RAG FAQ retrieval, WebFAQ, and
Wikipedia QA.

The group is useful because Persian retrieval is not treated as a single
uniform problem. Some tasks have short web-like queries, some have paragraph or
dialogue queries, and several have many relevant documents per query. A model
must handle Persian script, morphology, translated benchmark artifacts, native
web material, synthetic Persian data, and domain vocabulary from finance,
medicine, science, news, and Wikipedia. BM25, dense retrieval, and
`reranking_hybrid` separate lexical anchoring, semantic matching, and candidate
complementarity across this mix.

## What This Group Measures

[FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571)
introduces a Persian embedding benchmark in the MTEB style. NanoFaMTEB-v2 is
the compact retrieval subset of that broader benchmark. It combines native
Persian resources, translated benchmark tasks, synthetic Persian QA, and
domain-specific retrieval sources.

The group measures Persian retrieval robustness across task definitions. A
relevant item can be a duplicate question, a FAQ answer, a Wikipedia evidence
passage, a finance answer, a scientific abstract, a biomedical COVID document,
a news article, or a chatbot knowledge-base entry. This diversity makes
single-score interpretation risky: researchers should read the group by task
family and retrieval profile.

## Task Families

- **Argument and duplicate retrieval:** `argu_ana_fa` and `quora_fa` test
  counterargument-style pairing and duplicate-question intent.
- **Open-domain QA and evidence retrieval:** `fever_fa`, `hotpot_qa_fa`,
  `miracl_fa`, `nq_fa`, `msmarco_fa`, `syn_per_qa`, and
  `wikipedia_multilingual_fa` retrieve answer or evidence passages.
- **Domain retrieval:** `fi_qa2018_fa`, `sci_fact_fa`, `scidocs_fa`, and
  `treccovid_fa` cover finance, scientific evidence, related papers, and
  biomedical COVID literature.
- **News, web, and FAQ retrieval:** `neu_clir2023_fas`,
  `persian_web_document`, `web_faq_fas`, and `syn_per_chatbot_ragfaq` cover
  news/web documents, FAQ entries, and conversational RAG targets.

## Dataset Shape

NanoFaMTEB-v2 contains 17 task pages, 2,966 queries, 161,314 split-local
documents, and 17,925 positive qrel rows. Query counts vary: most tasks have
200 queries, while MS MARCO has 43, NeuCLIR has 74, and TREC-COVID has 50.
Several tasks are single-positive, but MS MARCO, NeuCLIR, Persian web retrieval,
TREC-COVID, SCIDOCS, and other tasks are strongly multi-positive.

Lengths vary widely. `persian_web_document` uses very short web queries,
whereas `argu_ana_fa` and `syn_per_chatbot_ragfaq` use long argument or
conversation-like queries. Documents range from short duplicate questions and
FAQ answers to long NeuCLIR news documents and scientific or biomedical
abstracts. The group therefore tests Persian retrieval across both terse search
intent and rich context matching.

## Retrieval Behavior

### BM25 Profile

BM25 is strongest when Persian query terms, named entities, or domain words
appear directly in the positive document. `quora_fa`, `syn_per_qa`,
`web_faq_fas`, `wikipedia_multilingual_fa`, `fever_fa`, `hotpot_qa_fa`, and
`persian_web_document` all have substantial sparse signal. These tasks either
preserve short search terms, contain repeated question wording, or have clear
Wikipedia/FAQ lexical anchors.

BM25 is weaker on stance-sensitive, conversational, and related-paper tasks.
`argu_ana_fa`, `syn_per_chatbot_ragfaq`, `scidocs_fa`, and some finance or
biomedical tasks require matching the retrieval relation rather than repeated
words. Multi-positive tasks can also hide difficulty: BM25 may find one
positive while still ranking the relevant set poorly.

### Dense Profile

Dense retrieval is the best profile for most tasks in the current metadata. It
improves Persian QA, MIRACL, MS MARCO, NeuCLIR, web retrieval, chatbot RAG, and
many evidence tasks by connecting paraphrase, answerability, and intent across
different wording. It is especially important for long conversational or
argument-style queries.

Dense retrieval should still be checked for exact Persian anchors. Named
entities, transliterations, domain terminology, and short web queries can be
lost if embedding similarity smooths them away. The best dense gains are those
that improve semantic matching without damaging entity and term recall.

### Reranking Hybrid Profile

`reranking_hybrid` is strongest where sparse and dense candidates are
complementary. It leads on `fi_qa2018_fa`, `hotpot_qa_fa`, `scidocs_fa`,
`treccovid_fa`, and `web_faq_fas` in the current metadata. These tasks combine
domain terms or exact FAQ/QA cues with semantic answerability.

For reranker experiments, hybrid is particularly useful on multi-positive
tasks. MS MARCO, NeuCLIR, Persian web retrieval, and TREC-COVID can have many
valid positives, so Recall@100 and candidate diversity matter as much as
top-rank nDCG.

## Task Summary

| Task | Retrieval focus | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [argu_ana_fa](argu_ana_fa.md) | argument to paired counterargument | 199 | 8,669 | 199 | 0.2860 | 0.3287 | 0.3128 | Dense |
| [fever_fa](fever_fa.md) | claim to evidence | 200 | 10,000 | 229 | 0.8025 | 0.8972 | 0.8396 | Dense |
| [fi_qa2018_fa](fi_qa2018_fa.md) | finance question to answer passage | 200 | 10,000 | 534 | 0.2923 | 0.3525 | 0.3722 | Reranking hybrid |
| [hotpot_qa_fa](hotpot_qa_fa.md) | multi-hop QA to evidence | 200 | 10,000 | 400 | 0.7735 | 0.8060 | 0.8366 | Reranking hybrid |
| [miracl_fa](miracl_fa.md) | MIRACL question to Wikipedia passage | 200 | 10,000 | 427 | 0.4929 | 0.6318 | 0.5931 | Dense |
| [msmarco_fa](msmarco_fa.md) | web query to passage answer | 43 | 8,766 | 2,826 | 0.4737 | 0.6139 | 0.6119 | Dense |
| [neu_clir2023_fas](neu_clir2023_fas.md) | information need to news documents | 74 | 10,000 | 3,669 | 0.4336 | 0.5766 | 0.5595 | Dense |
| [nq_fa](nq_fa.md) | natural question to evidence | 200 | 10,000 | 251 | 0.4470 | 0.5817 | 0.5274 | Dense |
| [persian_web_document](persian_web_document.md) | short web query to document | 200 | 10,000 | 2,186 | 0.6990 | 0.7780 | 0.7703 | Dense |
| [quora_fa](quora_fa.md) | duplicate question retrieval | 200 | 10,000 | 570 | 0.8393 | 0.9122 | 0.8861 | Dense |
| [sci_fact_fa](sci_fact_fa.md) | scientific claim evidence | 200 | 5,183 | 225 | 0.6294 | 0.5610 | 0.6100 | BM25 |
| [scidocs_fa](scidocs_fa.md) | related scientific documents | 200 | 10,000 | 986 | 0.1745 | 0.1937 | 0.2143 | Reranking hybrid |
| [syn_per_chatbot_ragfaq](syn_per_chatbot_ragfaq.md) | conversation to FAQ entry | 200 | 8,696 | 200 | 0.2882 | 0.4304 | 0.3826 | Dense |
| [syn_per_qa](syn_per_qa.md) | synthetic Persian QA evidence | 200 | 10,000 | 200 | 0.8609 | 0.9204 | 0.9173 | Dense |
| [treccovid_fa](treccovid_fa.md) | COVID topic to biomedical literature | 50 | 10,000 | 4,623 | 0.3519 | 0.3594 | 0.4161 | Reranking hybrid |
| [web_faq_fas](web_faq_fas.md) | web FAQ query to answer | 200 | 10,000 | 200 | 0.8680 | 0.8756 | 0.9029 | Reranking hybrid |
| [wikipedia_multilingual_fa](wikipedia_multilingual_fa.md) | Wikipedia question to answer passage | 200 | 10,000 | 200 | 0.8934 | 0.9007 | 0.8958 | Dense |

## Interpretation Notes for Model Researchers

NanoFaMTEB-v2 is best interpreted as a Persian retrieval coverage benchmark.
High performance on short FAQ or Wikipedia-style tasks does not guarantee
strength on argument retrieval, chatbot RAG, NeuCLIR, or scientific relatedness.
Compare models by task family and by whether the task is native, translated, or
synthetic.

Profile changes are especially informative. BM25-competitive tasks expose
strong lexical anchors in Persian. Dense-led tasks show paraphrase and
answerability gains. Hybrid-led tasks suggest candidate complementarity,
usually when domain terms and semantic relevance both matter.

## Training and Leakage Notes

Useful training data includes Persian web search logs, MIRACL-style
question-passage pairs, Persian FAQ retrieval, claim-evidence data,
conversation-to-knowledge-base pairs, finance and scientific retrieval, and
biomedical COVID literature search. Multi-positive tasks should preserve their
qrel structure during training.

Exclude NanoFaMTEB-v2 evaluation queries, positives, qrels, translated test
items, synthetic seeds, FAQ entries, news documents, and scientific abstracts.
Synthetic data should preserve Persian script, morphology, right-to-left
punctuation, named entities, and domain terminology, with hard negatives that
share surface terms but fail the task relation.

## Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571), 2025.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2022.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | https://arxiv.org/abs/2210.07316 |
