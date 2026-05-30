# NanoMTEB-Thai / mkqa_th

## Overview

`NanoMTEB-Thai / mkqa_th` is a Thai MKQA-derived retrieval task where Thai questions retrieve short answer strings rather than explanatory passages. The original MKQA benchmark was built from Natural Questions queries and supplies language-specific, passage-independent answers across many languages. In this retrieval formulation, the "documents" are answer labels such as entity names, dates, numbers, or short phrases. The result is a deliberately difficult benchmark for models that must connect a natural-language Thai question to the correct answer string even when that string has little or no lexical overlap with the query.

## Details

### What the Original Data Measures

MKQA measures multilingual open-domain question answering with aligned answers across languages. The retrieval version converts that setting into answer-label retrieval: the query is a question, and the candidate collection consists of short possible answers. This differs sharply from passage retrieval because the correct document often does not contain explanatory context.

For this Thai split, queries are primarily Thai, while answer strings may be Thai labels, English names, dates, numeric values, or compact multilingual forms. Models therefore need both Thai question understanding and robust entity or fact association.

### Observed Data Profile

The Nano split contains 200 queries, 6,652 documents, and 300 positive qrel rows. Each query has 1.5 positives on average, with a median of 1 and a maximum of 6. There are 49 multi-positive queries, or 24.5% of the query set. Queries average 40.20 characters, while documents average only 13.40 characters.

This very short document length is the defining feature of the task. A relevant document may be a number such as `82.0`, an English person name such as `Edwin Encarnación`, or a Thai transliterated name. The model cannot rely on passage context to bridge the query and answer.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0182, hit@10 of 0.0450, and recall@100 of 0.0567. This is extremely low compared with Thai passage retrieval tasks, and the reason is structural: the correct answer label is usually absent from the question.

BM25 can help only when the query repeats part of the answer, contains a recognizable title, or asks for a value that happens to share a lexical clue with the candidate answer. For most questions, however, sparse term frequency cannot infer that a Thai question about an NBA season should retrieve `82.0`, or that a question about a television role should retrieve an actor's name.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.0359, hit@10 of 0.0750, and recall@100 of 0.1433. Dense retrieval is better than BM25 on every reported metric, but the absolute values remain low. This shows that embedding similarity helps map Thai questions toward plausible answer labels, yet the answer-label format is still difficult for a general retriever.

The task stresses parametric and multilingual knowledge inside the embedding model. To succeed, a model must represent question intent, entity type, and factual association in a space where very short answers can be ranked directly.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 168 queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.0272, hit@10 of 0.0550, and recall@100 of 0.1267. The hybrid candidate set improves substantially over BM25 recall but does not surpass dense retrieval in the top ranks.

This pattern suggests that sparse candidates add some complementary coverage, but the decisive signal for this task is semantic and factual rather than lexical. The large number of safeguard rows is also important: many positives need explicit inclusion beyond the ordinary top-100 candidate window, which confirms that candidate generation is itself a major bottleneck.

### Metric Interpretation for Model Researchers

Low scores should not be read as simple model failure on Thai text. They reflect a harder retrieval formulation where the document is only the answer string. nDCG@10 and hit@10 measure whether the retriever can place the answer label near the top without supporting context. Recall@100 measures whether a reranker would even see the correct answer.

Dense retrieval being strongest is expected for this setting, but its low absolute recall indicates room for models trained specifically on multilingual answer-label retrieval, entity linking, and factual QA.

### Query and Relevance Type Tendencies

Queries ask factual questions about people, places, organizations, quantities, dates, and entertainment or sports facts. Relevant documents are compact answer labels. Some questions allow multiple equivalent answer forms, which explains the multi-positive queries.

The relevance relation is exact-answer oriented. A semantically related entity, a plausible number, or a topical phrase is not relevant unless it is an accepted answer string.

### Representative Failure Modes

Sparse systems fail when the answer is not mentioned in the query. Dense systems may retrieve an answer of the right type but wrong entity, confuse multilingual aliases, or rank popular entities above the specific requested answer. Numeric and date questions are especially brittle because embeddings may capture the question category without selecting the exact value.

### Training Data That May Help

Useful data includes Thai open-domain QA, multilingual question-answer pairs, Wikidata-linked entity questions, answer-label contrastive pairs, and hard negatives grouped by answer type. Training should include cases where the answer string has no lexical overlap with the question and should represent numeric, date, person, location, and organization answers separately.

### Model Improvement Notes

This task benefits from retrieval models that combine Thai question understanding with entity memory and answer-type calibration. For candidate generation, dense retrieval is the main baseline to beat. For reranking, the model should be trained on short answer labels, not only on passages, because there is little document-side context to interpret.

## Example Data

### Public Sources

- [MKQA: A Linguistically Diverse Benchmark for Multilingual Open Domain Question Answering](https://arxiv.org/abs/2007.15207), 2020.
- [apple/ml-mkqa](https://github.com/apple/ml-mkqa), source repository.
- [mteb/MKQARetrieval](https://huggingface.co/datasets/mteb/MKQARetrieval), MTEB dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MKQA: A Linguistically Diverse Benchmark for Multilingual Open Domain Question Answering | 2020 | paper | https://arxiv.org/abs/2007.15207 |
| apple/ml-mkqa | 2020 | repository | https://github.com/apple/ml-mkqa |
| mteb/MKQARetrieval |  | dataset card | https://huggingface.co/datasets/mteb/MKQARetrieval |

### Representative Snippets

| Query | Relevant answer label |
| --- | --- |
| อายุจำกัดสำหรับลูกเสือหญิงคือเท่าไหร่ | `5.0 18.0 ปี` |
| ใครเป็นผู้เล่นเบสหนึ่งของแยงกีส์ | `Edwin Encarnación` |
| เมืองแอลบูเคอร์คีในรัฐนิวเม็กซิโกมีประชากรเท่าไหร่ | `558545.0` |
| ใครแสดงบทแม่ในเรื่อง That '70s Show | `เดบร้า โจ รัปป์` |
| แต่ละทีมเล่นในเอ็นบีเอกี่เกมส์ | `82.0` |
