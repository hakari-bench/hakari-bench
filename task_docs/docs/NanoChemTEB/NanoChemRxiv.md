# NanoChemTEB / NanoChemRxiv

## Overview

NanoChemRxiv is an English chemistry-literature retrieval task in NanoChemTEB. It is derived from the ChEmbed and ChemTEB resources, where source documents are paragraphs from ChemRxiv preprints and queries ask for specific information grounded in held-out chemistry paragraphs. The task is intended to test whether a retrieval model can connect a technical research question to the paragraph that contains the necessary experimental, computational, synthetic, or analytical detail.

The benchmark is especially useful for studying retrieval in scientific domains where surface terminology, numerical conditions, material names, catalysts, ligands, measurements, and method names carry a large amount of relevance signal. Unlike broad web QA collections, this task often requires discriminating between paragraphs that are all scientifically plausible and lexically dense. A correct model must not only recognize general chemistry topics, but also preserve the exact local evidence needed by the query.

## Details

### What the Original Data Measures

The original ChemRxiv retrieval data was built for chemistry embedding evaluation. ChEmbed describes a pipeline that processes ChemRxiv manuscripts into paragraph-level passages, filters them, and creates retrieval-style questions from held-out source paragraphs. ChemTEB uses this family of data to evaluate how well models retrieve chemical literature under domain-specific vocabulary and writing conventions.

Each query is paired with one relevant paragraph. The query may ask about a condition, percentage threshold, simulation setup, ligand effect, electrolyte composition, catalyst behavior, spectroscopy observation, or other precise fact stated in the source passage. This makes the task a paragraph retrieval problem rather than a general document discovery problem. The relevant evidence is often surrounded by formulas, abbreviations, units, reaction names, citations, or method descriptions.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 candidate documents, and 200 positive qrels. Every query has exactly one positive passage. The mean query length is 111.71 characters, while the mean document length is 1,079.07 characters, reflecting paragraph-scale scientific prose rather than short snippets.

The observed examples cover molecular dynamics simulations, viral genome filtering, asymmetric cross-coupling, ionic-liquid electrolytes, ligand structural effects, and other chemistry-adjacent research topics. Many passages contain highly specific experimental or computational context. As a result, the dataset is compact but lexically and technically dense.

### BM25 Evaluation Profile

BM25 is very strong on this task: nDCG@10 is 0.9411, hit@10 is 0.9900, and recall@100 is 0.9950 with a top-500 candidate pool. This indicates that query terms and relevant paragraphs usually share distinctive vocabulary. Chemical names, method labels, concentrations, thresholds, ligands, catalysts, and measurement units all provide direct lexical anchors.

This behavior is important for model researchers. NanoChemRxiv is not a task where semantic abstraction alone is enough to dominate. Exact words are often part of the answer. A query about an unknown-letter threshold, a specific ligand, or a simulation condition can be satisfied only if the retrieval model keeps that detail visible in ranking. BM25 can fail when a wrong paragraph shares most technical terms but differs in the exact condition or result, yet its top-100 coverage shows that lexical retrieval is a very reliable candidate generator here.

### Dense Evaluation Profile

The dense baseline with harrier-oss-270m reaches nDCG@10 of 0.9000, hit@10 of 0.9400, and recall@100 of 0.9850. These scores are strong, but below the BM25 baseline. The gap suggests that embedding similarity captures topic and method compatibility well, while still losing some rank precision when exact scientific wording determines relevance.

Dense retrieval is useful for recognizing paraphrased intent. It can connect a question about solvation free energy or ligand steric effects to paragraphs that discuss the same process using different phrasing. However, the task frequently contains near-neighbor distractors from the same scientific area. If the embedding places many paragraphs about the same catalyst, simulation method, or biological sequence filtering close together, the correct evidence paragraph may not remain at the very top unless exact lexical details are also preserved.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid result is the strongest by nDCG@10, reaching 0.9419, with hit@10 of 0.9750 and recall@100 of 1.0000. The candidate set contains exactly 100 items per query, with no qrel safeguard rows needed. This profile shows that combining lexical and dense signals gives the most complete top-100 candidate coverage and slightly improves top-rank quality over BM25 by nDCG.

The hybrid result should be read carefully. BM25 has a higher hit@10, while reranking_hybrid has higher nDCG@10 and perfect recall@100. That means lexical matching alone often finds a relevant paragraph in the first ten ranks, but the hybrid ordering and candidate mixture help stabilize ranking quality and ensure that the positive passage is never lost by rank 100. For chemistry literature search, this is a useful pattern: lexical retrieval supplies exact terminology, while dense retrieval can recover semantically aligned passages when the wording shifts.

### Metric Interpretation for Model Researchers

NanoChemRxiv is a lexical-detail-heavy scientific retrieval task. High scores require robust handling of exact terms and semantic equivalence at the same time. The BM25 and reranking_hybrid results are very close at the top, and both outperform the dense baseline. A model that improves this task should be inspected for whether it raises exact-condition and exact-entity retrieval, not only broad topic similarity.

Recall@100 is particularly informative. BM25 already reaches 0.9950, and reranking_hybrid reaches 1.0000, so most remaining difficulty is rank ordering inside a high-quality candidate pool. nDCG@10 therefore reflects whether the model can move the single correct paragraph above near-miss paragraphs that mention the same molecules, methods, or experimental families.

### Query and Relevance Type Tendencies

Queries tend to be precise English questions about chemistry or chemistry-adjacent scientific content. They often contain one or more anchors such as a method name, compound class, biological sequence property, catalyst, ligand, electrolyte, numerical threshold, or physical measurement.

Relevant documents are paragraph-length scientific passages. They may include long noun phrases, units, formulas, parenthetical abbreviations, citations, and experimental context. Many positives are not isolated answer sentences; the whole paragraph provides enough context to connect the query to the correct fact. This favors retrievers that can handle long technical passages without losing local evidence.

### Representative Failure Modes

A common failure mode is retrieving a paragraph from the same paper or topic area that mentions the same method but not the requested result. Another is over-ranking passages that share a catalyst, ligand, simulation setup, or biological term while omitting the specific threshold or condition in the query.

Dense-only systems may also smooth over important distinctions between related chemical procedures. BM25-like systems may overvalue rare terms when the same rare term appears in multiple non-relevant paragraphs. Hybrid systems reduce both risks, but reranking still needs to identify which candidate contains the exact evidence rather than merely the same research context.

### Training Data That May Help

Useful training data should include non-overlapping ChEmbed-style synthetic query-passage pairs, ChemRxiv paragraphs outside the evaluation split, PubChem and Semantic Scholar chemistry passages, chemistry literature QA data, and hard negatives drawn from the same paper or same method family. It is important to exclude ChemRxiv Retrieval evaluation queries, qrels, and held-out source paragraphs from training.

Synthetic training examples should be grounded in non-evaluation ChemRxiv-style scientific paragraphs. Good queries ask about methods, measurements, compounds, catalysts, thresholds, structural effects, or numerical findings, and the positive passage should contain the exact requested evidence. Hard negatives should look topically close but differ in the condition, entity, result, or paragraph role.

### Model Improvement Notes

For this task, improvements should focus on preserving exact scientific evidence inside dense representations and reranking features. Strong systems need good token-level sensitivity to names, abbreviations, units, and numbers, while still supporting paraphrase between question wording and scientific prose.

Domain adaptation can help, but should be evaluated against lexical baselines. A dense model that increases topic clustering while weakening exact-entity discrimination may look semantically better yet rank worse on NanoChemRxiv. The best target is a model that keeps BM25-like precision for rare terms and adds dense robustness for paraphrased or implicit scientific descriptions.

## Example Data

### Public Sources

The public source references are the ChEmbed paper, the ChemTEB paper, the BASF-AI ChemRxivRetrieval dataset card, and the BASF-AI ChEmbed training-data collection. The NanoChemTEB task metadata records ChEmbed as the primary task paper.

### Source Reference Table

| Source | Role |
| --- | --- |
| [ChEmbed: Enhancing Chemical Literature Search Through Domain-Specific Text Embeddings](https://arxiv.org/abs/2508.01643) | Primary task paper describing chemistry embedding data and evaluation resources. |
| [ChemTEB](https://arxiv.org/abs/2412.00532) | Benchmark context for chemistry text embedding evaluation. |
| [BASF-AI/ChemRxivRetrieval](https://huggingface.co/datasets/BASF-AI/ChemRxivRetrieval) | Public dataset card for the ChemRxiv retrieval resource. |
| [BASF-AI ChEmbed training data collection](https://huggingface.co/collections/BASF-AI/chembed-training-data) | Related training-data collection for chemistry embedding work. |

### Representative Snippets

| Query Pattern | Positive Passage Pattern |
| --- | --- |
| Asks how molecular dynamics equilibrium densities are used to determine solvation free energy in binary mixtures. | The passage describes vapor-liquid equilibrium simulations and mixture setup details used in the solvation-free-energy workflow. |
| Asks what unknown-letter percentage threshold was used to exclude viral genome sequences during alignment. | The passage states that genome sequences above a specific unknown-letter threshold were removed before alignment. |
| Asks how steric bulk in ligand substituents affects enantioselectivity in a cross-coupling reaction. | The passage discusses ligand structure in a cross-coupling setting and relates steric effects to the selectivity outcome. |
| Asks how water content in an ionic-liquid electrolyte changes methanol formation rate and Faradaic efficiency. | The passage reports electrolyte composition and methanol production behavior under the relevant catalyst condition. |
| Asks why a ligand with particular structural features caused longer simulation times. | The passage describes binding free-energy simulations and explains the equilibration or sampling difficulty associated with the ligand structure. |
