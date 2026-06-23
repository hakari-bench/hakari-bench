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
| My objective is to devise a methodology for constructing intelligent robots that mimic human-like behavior. These robots would be capable of operating in real-world environments and executing a range of complex tasks. Such a robotic agent would interact with its surroundings, making decisions and performing actions. More importantly, it would continuously adapt to its environment by learning from signals and cues it receives. I aim to create a unified framework that can integrate a large number... [500 / 1,172 chars] | In this paper, we propose a novel task, Manipulation Question Answering (MQA), where the robot performs manipulation actions to change the environment in order to answer a given question. To solve this problem, a framework consisting of a QA module and a manipulation module is proposed. For the QA module, we adopt the method for the Visual Question Answering (VQA) task. For the manipulation module, a Deep Q Network (DQN) model is designed to generate manipulation actions for the robot to interact with the environment. We consider the situation where the robot continuously manipulating objects inside a bin until the answer to the question is found. Besides, a novel dataset that contains a variety of object models, scenarios and corresponding question-answer pairs is established in a simulation environment. Extensive experiments have been conducted to validate the effectiveness of the proposed framework. [915 chars] |
| I want to build a healthcare decision support system that will recommend treatment plans for patients. In order to make the prediction process transparent and interpretable, I believe I could use reinforcement learning. Given the patient’s past medical history, I will spawn many processes, in each process an artificial or digital twin for the patient is spawned to mimic the patient’s health trajectories. In each process, the patient will receive many treatments, prescriptions, surgeries, and wil... [500 / 1,255 chars] | Although reinforcement learning (RL) has tremendous success in many fields, applying RL to real-world settings such as healthcare is challenging when the reward is hard to specify and no exploration is allowed. In this work, we focus on recovering clinicians' rewards in treating patients. We incorporate the what-if reasoning to explain the clinician's treatments based on their potential future outcomes. We use generalized additive models (GAMs) - a class of accurate, interpretable models - to recover the reward. In both simulation and a real-world hospital dataset, we show our model outperforms baselines. Finally, our model's explanations match several clinical guidelines when treating patients while we found the commonly-used linear model often contradicts them. [773 chars] |
| I am working on a project analyzing customer feedback for a new product launch, so I need a method that can effectively identify the topics and segments in each feedback. Since the feedback we received is very complicated and contains a lot of noise words that digress from main topics, I need a method that is able to remove noise and simplify these feedbacks. Using this method, I hope our system could provide insights into the most common issues customers are facing and help us improve the produ... [500 / 730 chars] | With the evolution of the cloud and customer centric culture, we inherently accumulate huge repositories of textual reviews, feedback, and support data.This has driven enterprises to seek and research engagement patterns, user network analysis, topic detections, etc.However, huge manual work is still necessary to mine data to be able to mine actionable outcomes. In this paper, we proposed and developed an innovative Semi-Supervised Learning approach by utilizing Deep Learning and Topic Modeling to have a better understanding of the user voice.This approach combines a BERT-based multiclassification algorithm through supervised learning combined with a novel Probabilistic and Semantic Hybrid Topic Inference (PSHTI) Model through unsupervised learning, aiming at automating the process of better identifying the main topics or areas as well as the sub-topics from the textual feedback and support.There are three major break-through: 1. As the advancement of deep learning technology, there ha... [1,000 / 1,906 chars] |

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
