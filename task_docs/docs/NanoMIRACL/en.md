# NanoMIRACL / en

## Overview

`NanoMIRACL / en` is the English split of the MIRACL-style multilingual
monolingual retrieval benchmark. English queries retrieve English Wikipedia
passages, not translated evidence or answer strings. The Nano split has 200
queries, 10,000 documents, and 560 positive qrel rows. This is a high-resource
English passage-retrieval setting, but it still tests whether a model can select
the passage that contains the requested evidence rather than any passage about
the same topic. Current diagnostics show dense retrieval as the strongest
nDCG@10 profile, BM25 as extremely strong for hit@10 and recall@100, and
`reranking_hybrid` as the best overall coverage profile.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual: English queries retrieve English
passages from English Wikipedia. The benchmark emphasizes natural questions,
passage-level evidence, and human relevance judgments.

The English MIRACL split inherits the same retrieval-first framing as the other
languages. Native-language questions are judged against candidate passages, so
the relevant item is an evidence-bearing passage, not a direct short answer.
The task therefore measures open-domain passage retrieval over a broad
encyclopedic corpus.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 560 positive qrel
rows. Positives per query average 2.80, with a minimum of 1, a median of 2, and
a maximum of 11. There are 137 multi-positive queries, representing 68.5 percent
of the split. Queries average 39.91 characters, while documents average 471.76
characters.

The examples are short English information needs using forms such as `When`,
`What`, `How`, `Who`, `Where`, `Is`, `Does`, `Do`, and `Why`. Topics cover
people, places, organizations, politics, science, demography, religion,
philosophy, software, companies, sports entertainment, history, and definitions.
Several questions ask about facts that should be interpreted against the
Wikipedia snapshot rather than current real-world state.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.6774, hit@10 = 0.9950, and recall@100 = 0.9929. BM25 is
exceptionally strong on this English split because many questions contain
distinctive names and topical phrases, such as organizations, political
entities, game studios, countries, people, or technical terms.

The BM25 profile shows that exact lexical matching remains highly competitive
for English Wikipedia retrieval. Its hit@10 is higher than dense retrieval, and
its recall@100 is close to the hybrid ceiling. The main limitation is top-rank
ordering: BM25 can retrieve many relevant or near-relevant passages but rank a
topic-overlap passage above the passage that best states the requested relation.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7721, hit@10 = 0.9550, and recall@100 = 0.9482.
Dense retrieval is the strongest observed profile by nDCG@10. It ranks
answer-bearing passages higher than BM25 when the important signal is semantic
relation matching rather than repeated terms.

The tradeoff is visible in recall and hit rate. Dense retrieval improves the
quality of the top-ranked evidence, but it misses some positives that BM25
keeps in the candidate pool. This makes the English split useful for separating
semantic ranking quality from candidate coverage. A dense model can look best
at nDCG@10 while still being weaker than lexical retrieval at preserving the
full judged positive set.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.7474, hit@10 = 0.9850,
and recall@100 = 0.9964. Hybrid retrieval is slightly below dense retrieval by
nDCG@10, but it has the strongest recall@100 and a hit@10 score close to BM25.

This profile emulates the benefit of combining lexical and semantic search.
BM25 contributes exact English entity names, titles, and rare phrases, while
dense retrieval contributes relation-sensitive evidence matching. The result is
a candidate set that retains almost all judged positives and still has strong
top-10 quality, making it a natural input for cross-encoder or late-interaction
reranking.

### Metric Interpretation for Model Researchers

This task is multi-positive for 68.5 percent of queries. Hit@10 measures whether
at least one relevant passage appears near the top. nDCG@10 rewards ranking
relevant passages high, and recall@100 measures how much of the positive set is
available for reranking.

The metric pattern is especially useful because each method has a different
strength. Dense retrieval is best for top-rank ordering, BM25 is extremely
strong at finding at least one positive and preserving positives, and
`reranking_hybrid` provides the best candidate coverage. Researchers should not
interpret English MIRACL as a pure dense-retrieval win or a pure lexical win;
the split distinguishes ranking quality from retrieval coverage.

### Query and Relevance Type Tendencies

Queries are concise English questions about dates, definitions, people,
organizations, places, quantities, causal or yes/no relations, and historical or
scientific facts. Relevant documents are English Wikipedia passages with
article-title context and evidence-bearing prose.

The task rewards exact entity handling, relation recognition, and passage-level
answer evidence. A passage about the same broad article is not necessarily
relevant if it does not contain the requested date, location, person, definition,
or factual relation.

### Representative Failure Modes

BM25 can over-rank passages that share entity names or generic question terms
but do not answer the question. For example, a question about dualism may
retrieve passages about property dualism or cognitive dissonance before the
passage that names the relevant philosophical source. A question about the CEO
of WWE can retrieve generic CEO-related pages before the passage containing the
specific executive. A question about Antarctica's size can be affected by common
geographic wording and high-overlap distractors.

Dense retrieval can fail by choosing a semantically plausible passage that lacks
the exact evidence. Hybrid retrieval reduces this missing-positive problem but
still needs reranking to prefer the passage that directly supports the answer.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL English training data,
English Wikipedia question-to-passage retrieval pairs, English open-domain QA
evidence retrieval datasets, and entity-attribute retrieval supervision.
Training should emphasize passage-level evidence rather than only answer-string
prediction or paraphrase similarity.

Synthetic data can help when it creates English Wikipedia-style passages with
titles, dates, offices, places, population figures, definitions, and factual
relations. Generated questions should vary `when`, `what`, `who`, `where`, `how
many`, `how much`, `is`, and `does` forms. Comparable evaluation should exclude
upstream development/test data or other MIRACL-derived examples likely to
overlap with this Nano split.

### Model Improvement Notes

Dense retrievers should preserve the semantic ranking gains while recovering
more of BM25's exact-match coverage. Sparse systems can improve by
down-weighting generic question words and better recognizing relation-bearing
phrases. Rerankers should combine exact entity evidence with semantic answer
relation matching and should treat topic overlap as insufficient unless the
passage contains the requested fact.

For hybrid systems, `NanoMIRACL / en` is a clear candidate-generation benchmark:
`reranking_hybrid` has the best positive coverage, but dense retrieval shows
the strongest top-rank quality. A strong system should use both signals and
then rerank aggressively for evidence specificity.

## Example Data

| Query | Positive document |
| --- | --- |
| How many people visit the Eiffel Tower each year? [49 chars] | Tourism in Paris The Eiffel Tower is acknowledged as the universal symbol of Paris and France. It was originally designed by Émile Nouguier and Maurice Koechlin. In March 1885 Gustave Eiffel, known primarily as a successful iron engineer, submitted a plan for a tower to the French Ministre du Commerce et de l'Industrie. He entered a competition for students studying at the university. The winning proposal would stand as the centerpiece of the 1889 Exposition. Eiffel's was one of over 100 submissions. Eiffel's proposal was finally chosen in June 1886. Even before its construction, the Tower's uniqueness was noticed. The Eiffel Tower was finally inaugurated on March 31, 1889. Currently about 6.9 million people visit the Eiffel tower each year. [752 chars] |
| How long is the Omo River? [26 chars] | Omo River Its course is generally to the south, however with a major bend to the west at about 7° N 37° 30' E to about 36° E where it turns south until 5° 30' N where it makes a large S- bend then resumes its southerly course to Lake Turkana. According to materials published by the Ethiopian Central Statistical Agency, the Omo-Bottego River is 760 kilometers long. [367 chars] |
| Where did Sun Yat-sen study medicine? [37 chars] | Sun Yat Sen Memorial House Whilst studying at the Hong Kong College of Medicine for Chinese, the young Dr. Sun constantly travelled between Hong Kong and Macau to criticise the corruption of the Qing regime and agitated for revolution to save the country. He, along with Chan Siu-bak, Yau Lit and Yeung Hok-ling, were known as the "Si Da Kou" (Four Bandits). During this period, Sun Yat-Sen made many revolutionary statements and his first great essay—"Letter to Zheng Zaoru"—in his anthology was published by a Macau newspaper in 1890. [537 chars] |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984),
  2022.
- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/),
  2023.
- [MIRACL GitHub repository](https://github.com/project-miracl/miracl).
- [miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus),
  source corpus dataset.
- [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | [https://arxiv.org/abs/2210.09984](https://arxiv.org/abs/2210.09984) |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | [https://aclanthology.org/2023.tacl-1.63/](https://aclanthology.org/2023.tacl-1.63/) |
| MIRACL GitHub repository |  | project repository | [https://github.com/project-miracl/miracl](https://github.com/project-miracl/miracl) |
| miracl/miracl-corpus |  | dataset card | [https://huggingface.co/datasets/miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A question asking how many people visit the Eiffel Tower each year. | A passage about Paris tourism or the Eiffel Tower containing the visitor statistic. |
| A question asking how long the Omo River is. | A passage about the Omo River's course and length. |
| A question asking where Sun Yat-sen studied medicine. | A passage about Sun Yat-sen and his medical education. |
| A question asking for the population of a city or region. | A passage with the relevant population or colonial/geographic context. |
| A question asking when an ideology, organization, or event developed. | A passage that states the historical date or development context. |
