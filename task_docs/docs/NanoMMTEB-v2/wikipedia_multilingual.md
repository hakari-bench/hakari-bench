# NanoMMTEB-v2 / wikipedia_multilingual

## Overview

`NanoMMTEB-v2 / wikipedia_multilingual` is a multilingual Wikipedia retrieval
task with synthetically generated questions. Queries ask about facts from
Wikipedia passages across several languages, and the retriever must return the
answer-bearing passage. The Nano split has 200 queries, 10,000 documents, and
200 positive qrel rows, with exactly one positive document per query. Current
diagnostics show all three retrieval profiles as very strong: dense retrieval
has the best nDCG@10, `reranking_hybrid` has the best hit@10 and recall@100,
and BM25 is also near ceiling because generated questions preserve distinctive
passage terms.

## Details

### What the Original Data Measures

The WikipediaRetrievalMultilingual dataset is derived from a multilingual
Wikipedia corpus with synthetically generated retrieval queries. MMTEB includes
multilingual retrieval tasks like this to broaden evaluation beyond English and
to test multilingual passage retrieval over factual encyclopedia text.

The task measures native-language factual passage retrieval. A model must
connect a generated question to the passage that directly contains the answer
evidence.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel
rows. Every query has exactly one positive document. Queries average 59.16
characters, while documents average 383.29 characters.

Observed examples include Portuguese, Czech, Bulgarian, Swedish, English,
Italian, Romanian, Finnish, and other language passages. Questions target
explicit facts, entities, definitions, quantities, causes, or historical
significance.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.9425, hit@10 = 0.9700, and recall@100 = 0.9850. BM25 is
near ceiling.

This strong lexical result likely reflects the synthetic query generation
process: questions often preserve distinctive entities, places, terms, or
phrasing from the positive passage. Exact matching is highly effective, and
remaining errors probably involve similar entities, same-article passages, or
language-specific tokenization issues.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.9624, hit@10 = 0.9700, and recall@100 = 0.9700.
Dense retrieval has the strongest nDCG@10.

This shows that multilingual embedding similarity handles these generated
questions very well. Dense retrieval can match paraphrase and factual meaning
while preserving enough entity information to rank the positive passage at or
near the top.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 candidates per query and
achieves nDCG@10 = 0.9452, hit@10 = 0.9850, and recall@100 = 1.0000. Hybrid
retrieval has perfect recall@100 and the best hit@10, while dense retrieval has
slightly better nDCG@10.

This is a strong hybrid candidate-generation case. BM25 contributes exact
entity and phrase anchors, while dense retrieval contributes multilingual
semantic matching. A reranker could use the perfect top-100 coverage to improve
fine-grained ordering among near-matches.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has one answer-bearing Wikipedia
passage. Hit@10 measures whether that passage appears near the top. nDCG@10 is
sensitive to its exact rank, and recall@100 measures candidate coverage for
reranking.

The near-ceiling scores mean this task is less about broad retrieval failure and
more about small rank-order differences among strong systems. It is useful for
testing multilingual factual retrieval consistency and hybrid coverage.

### Query and Relevance Type Tendencies

Queries are native-language questions about explicit facts in Wikipedia-style
passages. Relevant documents are short factual passages that contain the answer
evidence. Topics include genetics of bean varieties, urban development,
habitats, sacred mountains, and food-additive safety.

The task rewards entity preservation, native-language passage matching, and
robust multilingual semantic alignment.

### Representative Failure Modes

BM25 can fail when generated questions paraphrase the passage or when related
Wikipedia passages share the same entity. Dense retrieval can fail when
multiple passages are semantically similar and the answer depends on a precise
quantity, cause, or named relation. Hybrid retrieval can retain all positives
but still rank a near-duplicate passage above the target.

Rerankers should verify that the passage directly answers the question rather
than merely mentioning the same entity or topic.

### Training Data That May Help

Useful training data includes multilingual Wikipedia question-passage pairs,
native-language QA retrieval, synthetic query generation over non-overlapping
Wikipedia passages, and same-article or same-entity hard negatives. The Nano
split's generated queries, qrels, and positive Wikipedia passages should be
excluded from training.

Synthetic data can generate native-language questions from non-evaluation
Wikipedia passages. Questions should target explicit facts, entities,
definitions, quantities, or causes. Hard negatives should come from the same
article, entity family, or topic neighborhood.

### Model Improvement Notes

Dense retrievers should preserve factual entity detail while maintaining
multilingual semantic alignment. Sparse systems should use language-aware
tokenization and normalization. Rerankers should compare the requested fact
against the candidate passage rather than only scoring topic similarity.

For hybrid systems, `NanoMMTEB-v2 / wikipedia_multilingual` is a high-coverage
success case: `reranking_hybrid` reaches perfect recall@100. The remaining
improvement opportunity is top-rank ordering among already strong candidates.

## Example Data

| Query | Positive document |
| --- | --- |
| Quais são as origens genéticas das variedades de feijão típicas de Portugal? [76 chars] | Com base num estudo publicado na US National Library of Medicine National Institutes of Health, em 2017, as variedades de feijão típicas de Portugal exibem proximidade genética com as variedades próprias dos Andes, pelo que se depreende que os feijões que se vieram a fixar e a usar mais comummente em Portugal terão sido aqueles que provieram originalmente dessa região da América do Sul. [389 chars] |
| Jaký vliv mělo zřízení zvláštní hospodářské zóny Pchu-tung na rozvoj Šanghaje? [78 chars] | Od 27. května 1949 je Šanghaj pod komunistickou vládou. Třebaže po roce 1949 přesídlila řada západních firem do Hongkongu, který tak vystřídal Šanghaj v roli obchodní metropole Dálného východu, výsadní hospodářské postavení Šanghaje v rámci Číny zůstalo neotřeseno. I dnes je, nepočítáme-li Hongkong, regionem se suverénně nejvyšším HDP na hlavu v ČLR. Zatímco v 60. až 80. letech město spíše stagnovalo, velký rozmach přišel po zřízení zvláštní hospodářské zóny Pchu-tung v roce 1990, kde vyrostly velkolepé mrakodrapy a nové mezinárodní letiště. Velkým problémem zůstává těžko kontrolovatelný příliv přistěhovalců z venkovských oblastí, především z provincií An‑chuej, Ťiang‑su a Če‑ťiang. [691 chars] |
| Какви местообитания предпочита рисът? [37 chars] | Рисът е представителят на семейство Коткови, който обитава най-разнообразни хабитати от всичките му представители. Предпочита тъмни гори, тайга, планински, хвойнови и широколистни гори с гъст подлес, лесостеп и лесотундра. По северните склонове на Хималаите достигат на надморска височина от 2500 метра, където е характерна алпийска тундра и скалисти райони, а в района на Тибетското плато местообитанията имат пустинен характер. Обикновено тези райони са обитавани от Lynx lynx isabellinus, който е единствения подвид пригоден за живот в по-открити пространства. Въпреки че е потайно животно рисът не се страхува от човека. Той може да обитава и вторично залесени гори и сечища, а в години през които гладува е възможно да влезе в села и дори големи градове. [759 chars] |

### Public Sources

- [mteb/WikipediaRetrievalMultilingual](https://huggingface.co/datasets/mteb/WikipediaRetrievalMultilingual).
- [ellamind/wikipedia-2023-11-retrieval-multilingual-queries](https://huggingface.co/datasets/ellamind/wikipedia-2023-11-retrieval-multilingual-queries).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595),
  2025.
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| mteb/WikipediaRetrievalMultilingual | 2024 | dataset card | [https://huggingface.co/datasets/mteb/WikipediaRetrievalMultilingual](https://huggingface.co/datasets/mteb/WikipediaRetrievalMultilingual) |
| ellamind/wikipedia-2023-11-retrieval-multilingual-queries | 2024 | dataset card | [https://huggingface.co/datasets/ellamind/wikipedia-2023-11-retrieval-multilingual-queries](https://huggingface.co/datasets/ellamind/wikipedia-2023-11-retrieval-multilingual-queries) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Portuguese question about genetic origins of typical bean varieties. | A Portuguese passage about Andean genetic proximity of bean varieties. |
| A Czech question about how the Pudong economic zone affected Shanghai. | A Czech passage about Shanghai's post-1949 development and Pudong. |
| A Bulgarian question about lynx habitat preferences. | A Bulgarian passage describing forests, taiga, and mountain habitats. |
| A Swedish question about Aconcagua's significance under the Inca Empire. | A Swedish passage describing Aconcagua as a sacred mountain. |
| An English question about acceptable daily intake for aspartame. | An English passage defining ADI and health-organization values. |
