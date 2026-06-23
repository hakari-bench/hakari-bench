# NanoBIRCO / NanoBIRCODorisMae

## Overview

NanoBIRCODorisMae is a compact Nano task derived from BIRCO's DORIS-MAE scientific literature search setting. Each query is a paragraph-length first-person research need, and the corpus contains scientific abstracts, mostly from computer science and adjacent areas. The retrieval goal is to find abstracts that satisfy the user's methodological, application, data, evaluation, and constraint requirements. This makes the task useful for evaluating complex scientific search and multi-facet query understanding.

## Details

### What the Original Data Measures

BIRCO frames DORIS-MAE as retrieval for complex research questions from computer scientists. The objective is to identify abstracts that effectively meet the user's needs, which may include several facets such as task, method, modality, scalability, domain, and evaluation setting.

This differs from paper-title relatedness or ordinary keyword search. The query is a long request written by a researcher, not a citation title. A relevant abstract may satisfy several constraints at once, and some abstracts may be partial matches. The task therefore tests holistic fit to a research objective.

### Observed Data Profile

The task contains 60 queries, 5,544 documents, and 1,569 relevance judgments. The average number of positives is 26.15 per query, but the distribution is skewed: the median is 1.0, the minimum is 1, the maximum is 100, and 16 queries are multi-positive, or 26.67% of the set.

Queries average 995.53 characters, while documents average 1,220.27 characters. Queries often describe a project goal, desired method, domain constraints, and evaluation needs. Documents are scientific abstracts containing methods, datasets, tasks, results, or applications.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3866, hit@10 of 0.5500, and recall@100 of 0.5940 using the top-500 BM25 candidate subset. Lexical matching can help when a research need names specific methods, datasets, domains, or technical terms. It also provides good recall on some broad topics.

The main weakness is facet matching. BM25 may rank papers that share a few terms while missing the full research intent. A query about transparent healthcare decision support, customer-feedback segmentation, or autonomous-driving risk may require method and application fit, not just shared vocabulary.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4140, hit@10 of 0.5167, and recall@100 of 0.5322. Dense retrieval has the best nDCG@10, indicating better top-rank alignment with the complex research objective. It is weaker than BM25 on hit@10 and recall@100.

This pattern suggests that embedding similarity helps rank the best-fitting abstracts when it finds them, but sparse lexical coverage still matters for broad candidate retrieval. The long multi-facet queries create a tension between holistic semantic matching and exact technical anchors.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4012, hit@10 of 0.5167, and recall@100 of 0.6424. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 6 safeguard rows, candidate counts from 100 to 101, and a mean of 100.10 candidates. Hybrid has the best recall@100, while dense has the best nDCG@10.

This makes reranking_hybrid the strongest candidate pool for downstream ranking. It combines BM25's technical term coverage with dense retrieval's research-intent matching. A reranker can then judge which abstracts satisfy the greatest number of query facets.

### Metric Interpretation for Model Researchers

Because the positive distribution is skewed, both single-positive and broad multi-positive cases matter. hit@10 reflects whether at least one relevant abstract is visible, nDCG@10 reflects top-rank fit, and recall@100 measures whether the candidate pool covers the broader relevant set for high-positive queries.

The comparison shows that BM25 provides coverage, dense retrieval improves top-fit quality, and reranking_hybrid is strongest for candidate completeness. This task is useful for evaluating long, multi-facet research search rather than simple topic matching.

### Query and Relevance Type Tendencies

Queries ask for papers on intelligent robots with human-like behavior, healthcare decision support with interpretable reinforcement learning, customer feedback topic segmentation, human causal logic models, neurodegenerative disease detection from brain scans, and other research goals. Relevant abstracts may satisfy method, domain, data, or evaluation constraints.

The task rewards matching multiple facets simultaneously. A paper can be on the same broad topic but fail the requested method or application, while another paper with less lexical overlap may better satisfy the research need.

### Representative Failure Modes

Likely failures include over-ranking same-topic abstracts that miss a key method, ignoring application constraints, matching isolated keywords instead of holistic fit, and missing useful abstracts because the query uses different terminology from the paper. BM25 may be too term-driven, while dense retrieval may compress away rare technical requirements.

### Training Data That May Help

Useful training data includes non-overlapping DORIS-MAE-style research-need retrieval pairs, paper recommendation datasets with expert-written needs, citation intent retrieval, abstract search logs, and hard negatives from the same research area that miss one or more query facets. Multi-facet labels or graded relevance are especially helpful.

### Model Improvement Notes

A model targeting this task should represent individual query facets and then score holistic fit. Sparse systems need field-aware indexing for methods, datasets, and applications. Dense systems need training on long research needs and facet-aware hard negatives. Hybrid systems are useful candidate pools because they show the best recall@100.

## Example Data

| Query | Positive document |
| --- | --- |
| My objective is to devise a methodology for constructing intelligent robots that mimic human-like be... [100 / 1,172 chars] | In this paper, we propose a novel task, Manipulation Question Answering (MQA), where the robot performs manipulation actions to change the environment in order to answer a given question. To solve thi... [200 / 915 chars] |
| I want to build a healthcare decision support system that will recommend treatment plans for patient... [100 / 1,255 chars] | Although reinforcement learning (RL) has tremendous success in many fields, applying RL to real-world settings such as healthcare is challenging when the reward is hard to specify and no exploration i... [200 / 773 chars] |
| I am working on a project analyzing customer feedback for a new product launch, so I need a method t... [100 / 730 chars] | With the evolution of the cloud and customer centric culture, we inherently accumulate huge repositories of textual reviews, feedback, and support data.This has driven enterprises to seek and research... [200 / 1,906 chars] |
| I am interested in understanding how modern computer programs can emulate human causal logic. To ach... [100 / 749 chars] | Research in Cognitive Science suggests that humans understand and represent knowledge of the world through causal relationships. In addition to observations, they can rely on experimenting and counter... [200 / 1,606 chars] |
| As a data scientist, I am currently developing an early detection system designed to identify the on... [100 / 1,196 chars] | Deep learning is attracting significant interest in the neuroimaging community as a means to diagnose psychiatric and neurological disorders from structural magnetic resonance images. However, there i... [200 / 1,359 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BIRCO](https://arxiv.org/abs/2402.14151) |
| Project repository | [BIRCO GitHub repository](https://github.com/BIRCO-benchmark/BIRCO) |
| NanoBIRCO dataset | [hakari-bench/NanoBIRCO](https://huggingface.co/datasets/hakari-bench/NanoBIRCO) |

Representative query and positive abstract snippets:

| Query | Positive document snippet |
| --- | --- |
| A research need for intelligent robots that mimic human-like behavior in real-world environments. | A paper proposes Manipulation Question Answering, where a robot changes the environment to answer a question. |
| A healthcare decision support system using interpretable reinforcement learning. | A paper discusses applying reinforcement learning in healthcare when rewards are hard to specify and exploration is not allowed. |
| A project on segmenting complicated customer feedback for a product launch. | A paper discusses large repositories of textual reviews, feedback, and support data. |
| A need to understand computational models of human causal logic. | A paper discusses causal relationships, experimentation, and counterfactual reasoning in cognitive science. |
| A system to detect neurodegenerative disease onset from brain scans. | A paper examines deep learning for diagnosing psychiatric and neurological disorders from structural MRI. |
