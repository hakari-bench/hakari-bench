# NanoMTEB-Scandinavian / dan_fever

## Overview

`dan_fever` is the Danish NanoMTEB-Scandinavian retrieval adaptation of DanFEVER. DanFEVER was introduced as a Danish FEVER-style fact-verification dataset for misinformation research, using claims paired with evidence from Danish Wikipedia and Den Store Danske. In the retrieval form used here, the query is a Danish factual claim and the relevant document is the evidence snippet that supports or refutes that claim. The task therefore evaluates claim-to-evidence retrieval, not ordinary question answering.

The Nano split contains 200 queries, 2,522 documents, and exactly 200 positive relevance judgments. Every query has one positive evidence snippet. Queries average about 59 characters, while documents average about 312 characters. The corpus is compact and encyclopedic, and the observed claims cover albums, plants, top-level domains, British nobility, minor planets, sports, institutions, science terms, and television facts. This makes named entities, dates, titles, and places strong retrieval cues.

## Details

### What the Original Data Measures

DanFEVER follows the FEVER fact-verification setup: a claim is labeled as supported, refuted, or not enough information based on evidence. The original task is about deciding factual consistency. The Scandinavian benchmark reuses the claim-evidence structure as a retrieval problem, asking whether a model can find the evidence text for a claim.

This conversion changes the evaluation target. The model is not asked to classify the claim's truth value. It is asked to retrieve the evidence snippet that would allow such a verification decision. A relevant document may repeat many claim terms, but it must also contain the specific fact needed to verify or contradict the claim.

### Observed Data Profile

The corpus is small compared with many Nano tasks, and the documents are concise encyclopedia snippets. Each query has exactly one positive, so the ranking problem is straightforward to interpret: the evidence either appears near the top or it does not. There is no multi-positive clustering.

Many claims are lexically close to their evidence. For example, claims about `Blood Mountain`, `almindelig perlebusk`, `.my`, British nobility, or `(944) Hidalgo` preserve distinctive names from the evidence. This gives lexical systems a strong advantage, though some cases still require Danish paraphrase handling or recognition of equivalent factual wording.

### BM25 Evaluation Profile

BM25 is the strongest top-rank profile, with nDCG@10 of 0.8856, hit@10 of 0.9900, and recall@100 of 1.0000. This is a highly lexically favorable task. The claim often shares named entities, dates, titles, and descriptive phrases with the evidence snippet. In a compact corpus, those repeated terms are enough to retrieve nearly every positive in the top 10 and all positives in the top 100.

This does not mean the task is trivial for all systems. The remaining errors are likely cases where the claim paraphrases the evidence, changes a fact, or uses wording that does not align exactly with the snippet. But relative to most retrieval tasks, BM25 has an unusually strong position here.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run reports nDCG@10 of 0.8630, hit@10 of 0.9700, and recall@100 of 0.9700. Dense retrieval is also strong, but slightly below BM25. This suggests that semantic similarity captures most claim-evidence relations, while exact lexical evidence remains especially valuable for Danish encyclopedia facts.

Dense retrieval may help when the claim and evidence differ in phrasing, but it can also rank semantically similar snippets about the same entity class above the exact evidence. In a single-positive setup, even small ordering differences matter.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.8832, hit@10 of 0.9750, and recall@100 of 1.0000. Candidate lists contain exactly 100 items, with no safeguard rows. Hybrid retrieval matches BM25 on recall@100 and is almost tied on nDCG@10, but it does not exceed BM25's top-10 quality.

This profile shows that hybrid retrieval is safe for candidate generation on this task. It preserves all positives at top 100 while keeping top-10 ranking close to the lexical baseline. However, because BM25 is already near ceiling, hybrid search has little room to improve direct ranking.

### Metric Interpretation for Model Researchers

This split is BM25-favorable. It is a useful counterexample to tasks where dense retrieval dominates. The reason is structural: short Danish claims and concise encyclopedia evidence often share the same exact entities and facts. A model that underperforms BM25 here may be losing important lexical precision.

Researchers should also note the ceiling effect. With BM25 hit@10 at 0.9900 and recall@100 at 1.0000, improvements are hard to observe. This task is more useful as a sanity check for lexical grounding and Danish entity handling than as a challenging semantic-retrieval benchmark.

### Query and Relevance Type Tendencies

Representative claims state that the album `Blood Mountain` has a coherent story and recurring theme, that the pearl bush develops pearl-shaped buds and white flowers, that `.my` is the Malaysian top-level domain, that British nobility is the upper class in Britain, and that `(944) Hidalgo` was discovered on 31 October 1920. The relevant snippets are short encyclopedia statements that verify those facts.

Most retrieval signals are concrete: names, dates, object types, countries, and titles. The model should preserve these terms while also recognizing small paraphrases around the factual relation.

### Representative Failure Modes

Dense systems may retrieve a semantically related encyclopedia snippet about the same entity type but not the exact evidence. BM25 may fail when a claim uses different wording from the evidence or when multiple snippets share the same entity name. Hybrid systems can inherit both risks, though the compact corpus and strong lexical cues make failures rare.

Another failure mode is treating refuted-style claims as if topical relatedness were enough. The evidence snippet must allow verification of the exact claim, including the detail that is supported or contradicted.

### Training Data That May Help

Useful training data includes non-overlapping DanFEVER claim-evidence pairs, Danish Wikipedia retrieval pairs, Danish fact-verification hard negatives, and same-entity encyclopedia negatives. Training data should exclude the Nano claims, qrels, and evidence snippets used in this split.

Hard negatives should share the same entity, title, date range, or category but fail to verify the exact claim. These examples teach the model to retrieve evidence rather than merely related encyclopedia text.

### Model Improvement Notes

Sparse systems are naturally strong here, so improvements should focus on Danish tokenization, entity preservation, and exact fact grounding. Dense models should avoid over-smoothing named entities and dates. Hybrid systems are useful as robust candidate generators but are unlikely to show large gains unless paired with a reranker that can handle the few ambiguous cases.

For evaluation, nDCG@10 mainly measures how close the system is to lexical ceiling. Recall@100 is already saturated for BM25 and hybrid, so remaining progress depends on top-rank ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| Albummet Blood Mountain har en sammenhængde historie og et gennemgående tema. [77 chars] | Blood Mountain er et konceptalbum af heavy metal-gruppen Mastodon. Det er Mastodons tredje studiealbum og blev udgivet i september 2006. Som det foregående album Leviathan er Blood Mountain et konceptalbum med en sammenhængende historie og et gennemgående tema. [261 chars] |
| Den almindelige perlebusk får perleformede knopper og derefter hvide blomster på dens busk. [91 chars] | Almindelig perlebusk ("Exochorda racemosa") er en mellemstor, løvfældende busk med en opret vækst og iøjnefaldende klaser af hvide, perleformede knopper og senere hvide blomster. Busken er fuldt hårdfør og bruges som prydbusk i haverne. [236 chars] |
| .my er det malaysiske topdomæne. [32 chars] | .my er et nationalt topdomæne der er reserveret til Malaysia. [61 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| Scandinavian Embedding Benchmarks | Benchmark framing for Scandinavian retrieval tasks. |
| DanFEVER paper | Original Danish claim-verification dataset description. |
| DanFEVER dataset card | Source data packaging and dataset access. |

### Representative Snippets

- A claim says `Blood Mountain` has a coherent story and recurring theme; the evidence describes it as a Mastodon concept album.
- A claim says the pearl bush develops pearl-shaped buds and white flowers; the evidence describes `Exochorda racemosa`.
- A claim says `.my` is the Malaysian top-level domain; the evidence states that `.my` is reserved for Malaysia.
- A claim says British nobility is the upper class in Britain; the evidence describes the social class and its privileges.
- A claim says `(944) Hidalgo` was discovered on 31 October 1920; the evidence identifies the object and discovery details.
