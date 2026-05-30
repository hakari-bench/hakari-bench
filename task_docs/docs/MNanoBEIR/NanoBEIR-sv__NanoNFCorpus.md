# MNanoBEIR / NanoBEIR-sv / NanoNFCorpus

## Overview

NanoNFCorpus in the Swedish NanoBEIR slice is a biomedical and nutrition retrieval task derived from NFCorpus. The queries are Swedish translated health and nutrition information needs, and the corpus contains Swedish translated scientific or medical passages. The task measures whether a retriever can connect short health-related queries to long domain passages that discuss relevant conditions, interventions, ingredients, outcomes, or medical concepts. It is a compact diagnostic for domain-specific retrieval where broad topical similarity is often not enough.

## Details

### What the Original Data Measures

NFCorpus was built for medical information retrieval with health and nutrition needs and relevance judgments over scientific text. In retrieval form, a query may be a short keyword phrase, a symptom, a food item, a health concern, or a question about a medical concept. Relevant documents can include abstracts or passages that discuss the same condition, intervention, or outcome.

The Swedish translated version tests multilingual biomedical retrieval under a difficult short-query setting. Many queries are only one or two terms, while the relevant passages are long and technical. A model must identify biomedical relevance from sparse query evidence, handle translated terminology, and rank many relevant passages rather than only finding one obvious match.

### Observed Data Profile

The task contains 50 queries, 2,953 documents, and 1,651 relevance judgments. It is highly multi-positive, with an average of 33.02 positives per query. The minimum is 1, the median is 23.5, the maximum is 100, and 47 queries are multi-positive, or 94.0% of the query set. This makes the task a broad relevant-set retrieval benchmark.

Queries average 23.16 characters, while documents average 1,493.97 characters. The query-document length gap is large. A query such as a nutrient, food, or condition name may correspond to many long biomedical passages, and the relevant evidence may be only one part of the document. This makes recall and ranking coverage difficult.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2383, hit@10 of 0.6000, and recall@100 of 0.1224 using the top-500 BM25 candidate subset. Lexical matching can find some relevant passages because biomedical terms are often distinctive, but the recall is very low relative to the large number of positives. This shows that exact term overlap is not enough to cover the evidence set.

The low recall@100 is particularly important. Since many queries have dozens of positives, retrieving a few passages with the most obvious term overlap still leaves most relevant documents outside the candidate window. BM25 is useful for precise terminology, but it is brittle when Swedish translation, synonyms, or broader biomedical concepts change the surface form.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.2315, hit@10 of 0.5600, and recall@100 of 0.1757. Dense retrieval improves recall@100 over BM25 but slightly trails BM25 in nDCG@10 and hit@10. This suggests that embedding similarity broadens the candidate set but does not consistently place the best passages in the first page.

This is a common challenge in biomedical retrieval. General dense models may recognize that passages are medically related, but they can blur conditions, interventions, outcomes, or study populations. Short queries provide little context, so dense embeddings may retrieve semantically adjacent material that is not judged relevant, while BM25 can still benefit from exact technical terms.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.2519, hit@10 of 0.5600, and recall@100 of 0.1799. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 9 safeguard rows and a mean of 100.18 candidates. The hybrid profile has the best nDCG@10 and recall@100, while BM25 has the best hit@10.

The hybrid result indicates that combining lexical and dense evidence helps this task, but the overall recall remains low because the relevant sets are very large. The top-10 gain suggests that lexical biomedical anchors and dense semantic coverage complement one another. Still, the benchmark remains difficult for all three retrieval modes, especially as a candidate-generation task for broad biomedical relevance.

### Metric Interpretation for Model Researchers

For NanoNFCorpus-sv, recall@100 is essential because most queries have many positives. A model that finds one relevant passage can achieve a hit, but it may still fail to represent the medical evidence landscape. nDCG@10 measures whether the first page contains strong relevant material, while recall@100 shows whether the candidate pool is broad enough for downstream reranking or review.

The current profiles show no simple winner across every metric. BM25 is competitive at finding at least one lexically obvious result. Dense retrieval expands coverage but weakens first-page precision. reranking_hybrid gives the best graded top-10 ranking and recall, though the recall is still modest. This makes the task useful for testing biomedical hard negatives and multi-positive retrieval coverage.

### Query and Relevance Type Tendencies

Queries include short health phrases such as healthy chocolate milkshakes, medical ethics, fava beans, what is really in chicken nuggets, and saturated fat. Relevant documents are long scientific or medical passages, often describing studies, objectives, methods, associations, or health outcomes.

The task rewards models that understand biomedical and nutrition concepts, including foods, nutrients, diseases, interventions, risks, and study outcomes. It also requires tolerance for broad relevance: a query may have many relevant passages that discuss the same condition or topic from different angles. Ranking only the most literal matches is not enough.

### Representative Failure Modes

Likely failures include retrieving passages with the same food or medical term but the wrong outcome, missing relevant documents that use synonyms or broader terminology, over-ranking general health text, and failing to cover multiple positive passages. BM25 can be too narrow, while dense retrieval can be too broad. Hybrid systems must balance exact terminology with semantic expansion.

### Training Data That May Help

Useful training data includes biomedical retrieval, medical QA, nutrition search, scientific abstract ranking, and hard negatives from the same condition or intervention but different outcomes. Swedish medical text and terminology resources can help with language-specific phrasing. For rerankers, multi-positive supervision is important because the task is about coverage over a large relevant set.

### Model Improvement Notes

A model targeting this task should improve biomedical concept normalization and multi-positive recall. Sparse systems need synonym expansion and morphology-aware matching for Swedish medical terms. Dense systems need domain-specific training to separate closely related biomedical concepts. Hybrid systems are promising, but they should be evaluated for relevant-set coverage, not only first positive discovery.

## Example Data

### Public Sources

The original task is based on NFCorpus, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact multilingual dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sv dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |

Representative query and positive passage snippets:

| Query | Positive document snippet |
| --- | --- |
| Hälsosamma chokladmjölkshakes | Syfte: Att undersöka sambandet mellan intag av körsbär och risken för återkommande giktattacker... |
| medicinsk etik | Bakgrund: En av de stora utmaningarna med att kontrollera serumkolesterol genom dietintervention verkar vara behovet... |
| favabönor | De senaste 20 åren har intresset för L-arginins biokemi, näring och farmakologi ökat... |
| Vad finns egentligen i kycklingbitar? | SYFTE: Att bestämma innehållet i kycklingbitar från 2 nationella matkedjor... |
| mättat fett | Intresset har ökat för möjligheten att moderns kostintag under graviditeten kan påverka utvecklingen av allergiska sjukdomar... |
