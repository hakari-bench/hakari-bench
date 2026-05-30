# MNanoBEIR / NanoBEIR-de / NanoNFCorpus

## Overview

This task is the German NanoBEIR version of NFCorpus, a medical information retrieval benchmark built from health and nutrition information needs linked to biomedical articles. The original NFCorpus dataset was introduced as a full-text learning-to-rank resource where queries are derived from consumer-facing NutritionFacts.org topics and relevance links connect those needs to PubMed or medical evidence. In this NanoBEIR slice, 50 short German health queries are matched against 2,953 German biomedical or medical-information documents, with 1,651 positive relevance judgments. Unlike single-answer QA tasks, most queries have many positives: the average is 33.02 positives per query and 47 of 50 queries are multi-positive. This makes the task a compact but demanding test of consumer-health vocabulary, biomedical terminology, and the ability to rank many valid evidence documents for the same information need.

## Details

### What the Original Data Measures

NFCorpus measures the retrieval gap between lay health topics and professional biomedical literature. Queries may mention foods, diets, diseases, supplements, interventions, or broad medical concerns in short consumer language, while relevant documents use abstract-style terminology, study designs, outcomes, and mechanistic descriptions. In BEIR and NanoBEIR, the task evaluates whether a retriever can surface medically relevant evidence documents rather than merely documents that share a visible disease or diet keyword.

### Observed Data Profile

The German Nano task has 50 queries, 2,953 documents, and 1,651 positive qrel rows. Query text is short, averaging about 29 characters, while documents are much longer, averaging about 1,732 characters. Positives per query range from 1 to 100, with a median of 23.5. This creates a very different ranking problem from web QA: a model must retrieve a cluster of relevant biomedical documents, not just find one answer passage. Example queries include chicken nuggets, medical ethics, fava beans, saturated fats, adenovirus 36, and probiotics for cold prevention.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.200, Hit@10 of 0.560, and Recall@100 of 0.125. The low recall is especially meaningful because many queries have dozens of positives, yet sparse matching retrieves only a small fraction in the top 100. BM25 can find exact lexical matches for terms such as food names, disease labels, or intervention names, but it struggles when consumer phrasing and biomedical terminology diverge. It may also over-focus on a repeated term while missing documents that discuss the same health concept through outcomes, mechanisms, population descriptions, or study language.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline performs better, with nDCG@10 of 0.252, Hit@10 of 0.680, and Recall@100 of 0.173. This suggests that semantic similarity is useful for bridging lay German queries to longer medical abstracts. Dense retrieval can connect a short topic label to documents that use scientific phrasing, and it can rank evidence documents that do not repeat the query wording exactly. However, recall remains low relative to the number of positives, showing that this task remains difficult even for embedding-based retrieval. The model must identify medically relevant evidence across many possible positive documents, not only a single semantically close passage.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.229, Hit@10 of 0.620, and Recall@100 of 0.172, with five safeguard rows at 101 candidates. It is close to dense on Recall@100 but below dense on nDCG@10 and Hit@10. This indicates that hybrid search improves coverage over BM25 but does not fully solve top-rank ordering for biomedical evidence. Lexical signals help preserve exact medical terms, while dense signals recover paraphrased or terminology-shifted documents. The remaining gap shows that medical relevance is not identical to either keyword overlap or broad semantic similarity; models must learn domain-specific evidence matching.

### Metric Interpretation for Model Researchers

For NFCorpus, nDCG@10 and Recall@100 must be interpreted in a multi-positive setting. Hit@10 only tells whether at least one relevant document appears, and therefore hides much of the ranking difficulty. Recall@100 is low for all three profiles because each query may have many relevant abstracts; a model can retrieve one good document and still miss most of the evidence set. Researchers should examine whether improvements increase the diversity and coverage of relevant medical evidence, not only the first positive hit.

### Query and Relevance Type Tendencies

Queries are often short topic labels or consumer-health questions. Relevant documents are long biomedical abstracts, clinical summaries, or evidence passages that may mention interventions, cohorts, outcomes, risks, and mechanisms. A single query can map to many article types, including dietary studies, clinical interventions, epidemiological findings, and mechanistic research. This makes the task sensitive to domain vocabulary, medical synonymy, and cross-register matching between lay and scientific German.

### Representative Failure Modes

Sparse systems can miss positives when the query uses consumer language and the document uses biomedical terminology. Dense systems can retrieve medically adjacent documents that are topically close but not actually relevant to the specific intervention or outcome. Hybrid systems can improve coverage but still rank generic medical passages above more directly relevant evidence. Because many positives exist per query, failure analysis should inspect both missing evidence clusters and top-ranked false positives.

### Training and Leakage Considerations

Training should exclude NFCorpus, BEIR, NanoBEIR, and translated NutritionFacts-linked records likely to overlap with the evaluation queries or linked medical documents. Useful non-overlapping data includes biomedical IR benchmarks, German or multilingual consumer-health QA retrieval pairs, PubMed ranking data, and terminology-rich paraphrase pairs. Multi-positive training is recommended because the benchmark rewards retrieving multiple evidence documents for a single health topic.

### Model Improvement Signals

Improvements should come from better biomedical German representations, lay-to-technical terminology mapping, and hard negatives that share disease or diet terms but do not support the same health claim. Strong models should retrieve a range of relevant evidence documents, including abstracts that phrase the same health concept through mechanisms, population groups, or outcomes. Hybrid systems should preserve exact medical terms while allowing dense signals to bridge vocabulary gaps.

## Example Data

| Query | Positive Document |
|---|---|
| Gesunde Schokoladen-Milchshakes | Ziel: Untersuchung der Beziehung zwischen dem Verzehr von Kirschen und dem Risiko von wiederkehrenden Gichtanfällen bei Personen mit Gicht... |
| Medizinische Ethik | HINTERGRUND: Ein Hauptproblem bei der Kontrolle des Serumcholesterins durch diätetische Maßnahmen scheint die Notwendigkeit zu sein... |
| Saubohnen | In den letzten 20 Jahren hat das wachsende Interesse an der Biochemie, Ernährung und Pharmakologie von L-Arginin... |
| Was steckt eigentlich in Chicken Nuggets? | ZIEL: Untersuchung der Inhaltsstoffe von Hähnchen-Nuggets zweier nationaler Fast-Food-Ketten... |
| gesättigte Fette | Das Interesse an der Möglichkeit, dass die Ernährung der Mutter während der Schwangerschaft die Entwicklung von Allergien bei Kindern beeinflussen könnte... |

## Public Sources

- [NFCorpus paper](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
- [NFCorpus project page](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| NFCorpus paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| NFCorpus project page | https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/ |
| BEIR benchmark | https://github.com/beir-cellar/beir |
| MMTEB benchmark | https://arxiv.org/abs/2502.13595 |
| NanoBEIR dataset | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
