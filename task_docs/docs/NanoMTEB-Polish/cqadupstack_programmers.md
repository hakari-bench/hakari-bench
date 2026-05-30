# NanoMTEB-Polish / cqadupstack_programmers

## Overview

`cqadupstack_programmers` is the Polish NanoMTEB version of the Programmers subset from CQADupStack. Unlike code-only retrieval tasks, this split focuses on software engineering practice: architecture, testing, licensing, frameworks, methodology, project process, developer roles, and conceptual programming explanations. A short Polish query must retrieve longer forum questions that ask the same practical or conceptual software-engineering issue.

The Nano split contains 200 queries, 10,000 documents, and 634 positive relevance judgments. Queries average about 59 characters and documents about 1,075 characters, so the task often requires matching compact titles to long discussion-style posts. Duplicate clusters are common: 84 queries have more than one positive, the average number of positives per query is 3.17, and one query has 100 positives. This makes the task useful for studying retrieval over broad engineering concerns where many users ask similar questions in different professional contexts.

## Details

### What the Original Data Measures

CQADupStack evaluates duplicate-question retrieval in community QA data. In the Programmers subset, relevance means that two questions ask the same engineering decision or conceptual issue, not merely that they mention the same language, framework, methodology, or career role. A question about learning Django from examples is relevant to another question about understanding Django as a framework, but not to every Django-related post.

This differs from implementation-focused code retrieval. The central signal is often the user's decision or concern: whether to invest in data structures and algorithms, how to validate software licenses, whether using .NET requires payment, how to explain pointers, or how to organize solo Scrum. Models must represent practical intent across long discussions and varied wording.

### Observed Data Profile

The documents are long because Programmers-style posts often include background, constraints, opinions, examples, and tradeoffs. Many candidate documents share broad terms such as software, architecture, testing, framework, license, developer, Scrum, or UML. These terms are informative but not enough to identify duplicates.

The Polish translation preserves many English technical names and acronyms. Terms such as Django, .NET, UML, Scrum, C#, and framework remain important lexical anchors, while Polish prose expresses the decision being asked. Strong retrieval therefore requires both exact recognition of technical terms and semantic modeling of the underlying software-engineering question.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3191, hit@10 of 0.4650, and recall@100 of 0.3549. Lexical matching works when queries contain distinctive terms such as .NET, Django, UML, Scrum, or "unit test." It is also helpful for licensing and framework questions where specific product names define the topic.

BM25 struggles when multiple posts share the same broad vocabulary but ask different decisions. Software architecture, testing, and project-process questions often reuse common phrases while differing in the practical problem. Term frequency can therefore retrieve same-topic posts that are not duplicates, especially in long documents where many engineering terms appear.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run improves to nDCG@10 of 0.3275, hit@10 of 0.5550, and recall@100 of 0.4227. The hit-rate gain is substantial, indicating that embedding similarity better captures the practical intent behind many queries. Dense retrieval can connect questions about investing in algorithms, understanding a framework, validating licenses, or explaining pointers even when the wording differs.

At the same time, dense nDCG@10 is only slightly above BM25. This suggests that dense retrieval finds more relevant material somewhere near the top, but it still has trouble ordering true duplicates above related engineering discussions. In this domain, many posts are semantically close without being duplicates.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is strongest, with nDCG@10 of 0.3607, hit@10 of 0.5600, and recall@100 of 0.4637. Candidate lists contain 100 to 101 items, and 41 rows use the positive safeguard. The hybrid run combines BM25's exact technical anchors with dense retrieval's broader intent matching, producing the best top-10 quality and the best candidate coverage.

This profile fits the task well. Software-engineering questions often have both named technologies and abstract decisions. A good candidate set needs to preserve specific names such as .NET or Django while also finding paraphrases of the same decision. The hybrid result indicates that neither lexical nor dense retrieval alone covers the task as well as their combination.

### Metric Interpretation for Model Researchers

This split is hybrid-favorable. BM25 provides a reasonable base because product names and methodology terms matter. Dense retrieval improves hit@10 and recall@100 by capturing practical intent. `reranking_hybrid` performs best overall, suggesting that production-style retrieval for this domain should combine exact and semantic signals.

The large duplicate clusters also matter. Some broad software-engineering questions attract many near-identical posts, while others are isolated. A model should be judged by both nDCG@10 and recall@100: high nDCG shows that the top results are good, while high recall indicates that the system preserves enough duplicates for downstream reranking or analysis.

### Query and Relevance Type Tendencies

Representative queries ask whether to keep investing in data structures and algorithms, how to learn Django from examples, how to validate a license while calling home, whether using .NET requires payment to Microsoft, and how to explain pointers clearly. These are not simply keyword topics; they are practical questions with user intent, constraints, and context.

Relevant documents may use different examples or professional framing. A licensing question may appear as a trial-subscription product story. A framework-learning question may be framed as difficulty understanding documentation. A pointer question may be conceptual rather than language-specific. This variety makes semantic modeling important.

### Representative Failure Modes

BM25 may over-rank posts that share a technology or methodology but ask a different question. For example, many posts mention Scrum, but only some ask about the same team-process issue. Dense retrieval may over-rank semantically similar career or architecture discussions that are not duplicates because they involve different tradeoffs.

Long documents create another failure mode: a candidate post may mention several technologies and processes in background text. If the model does not identify the main question, it may match on incidental terms. Rerankers need to focus on the actual decision being asked rather than all vocabulary in the post.

### Training Data That May Help

Useful training data includes software-engineering QA duplicate pairs, Polish developer forum questions, translated Stack Exchange posts, and hard negatives from the same methodology or technology area. Data should include both conceptual programming questions and professional decision questions.

Hard negatives are especially valuable when they share the same named entity but differ in intent: several .NET licensing posts with different legal questions, several Django learning posts with different goals, or several testing posts about different testing levels. These teach a model not to treat topical overlap as duplicate relevance.

### Model Improvement Notes

Dense models can improve by representing practical software-engineering intent in long posts. Sparse systems can improve through handling acronyms, framework names, and Polish technical phrases, but they will still confuse same-topic non-duplicates. Hybrid systems are well matched to this task because exact names and abstract decisions both matter.

For reranking research, this split is a useful bridge between natural-language retrieval and technical-domain retrieval. The best model should identify the user's decision, preserve named technology constraints, and rank true duplicates above broadly related engineering discussions.

## Example Data

### Public Sources

- CQADupStack original paper: https://ir.webis.de/anthology/2015.adcs_conference-2015.3/
- MTEB benchmark paper: https://arxiv.org/abs/2210.07316
- CLARIN-KNEXT Polish dataset card: https://huggingface.co/datasets/clarin-knext/cqadupstack-programmers-pl
- Source task dataset card: https://huggingface.co/datasets/mteb/CQADupstack-Programmers-PL

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| CQADupStack paper | Original community QA duplicate-retrieval construction. |
| MTEB paper | Benchmark context for retrieval evaluation. |
| CLARIN-KNEXT dataset card | Polish translated Programmers subset. |
| MTEB task card | Task packaging and retrieval interface. |

### Representative Snippets

- A query asks whether to keep investing in data structures and algorithms; relevant documents discuss whether implementing algorithms improves programming skill.
- A query asks how to learn Django by example; relevant posts discuss understanding Django and framework internals.
- A query asks about license validation and calling home; relevant documents describe secure validation for subscription software.
- A query asks whether using .NET requires payment to Microsoft; relevant posts discuss selling a C# desktop application and licensing constraints.
- A query asks for a clear explanation of pointers; relevant documents discuss conceptual definitions of pointers in programming languages.
