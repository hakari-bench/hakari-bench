# MNanoBEIR / NanoBEIR-fr / NanoTouche2020

## Overview

This task is the French NanoBEIR version of Touché 2020, an argument retrieval benchmark for controversial questions. The original CLEF Touché task focuses on retrieving arguments for socially important topics and everyday decision questions, where relevance depends on both topic match and argumentative content. In this NanoBEIR slice, French translated controversial questions must retrieve French translated debate-style argument documents from 5,745 candidates. The task contains 49 queries and 932 positive relevance judgments. Every query has multiple positives, averaging 19.02 relevant arguments. It is a compact benchmark for pro/con coverage, argument relevance, and ranking long argumentative documents rather than short answer passages.

## Details

### What the Original Data Measures

Touché 2020 measures argument retrieval. A relevant document should address the controversial question with a substantive argument, stance, reason, example, or evidence. Topical mention alone is not enough. For queries about homework, prescription drug advertising, child vaccination, abortion, or standardized testing, a good retriever should surface documents that actually argue the issue.

### Observed Data Profile

The French Nano task has 49 queries, 5,745 documents, and 932 positives. Every query is multi-positive, with 6 to 32 positives and a median of 19. Queries average about 60 characters, while documents are long, averaging about 2,488 characters. Example queries ask whether homework is useful, whether prescription drugs should be advertised directly to consumers, which vaccines children should receive, whether abortion should be legal, and whether standardized tests improve education.

### BM25 Evaluation Profile

BM25 is strong, with nDCG@10 of 0.561, Hit@10 of 1.000, and Recall@100 of 0.791. The perfect Hit@10 reflects strong topic terms and many positives per query. Sparse matching is very effective at finding at least one relevant argument for every topic. However, ranking remains meaningful because argument retrieval should prioritize substantive arguments, not only documents that mention the same controversial issue.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline reaches nDCG@10 of 0.473, Hit@10 of 0.959, and Recall@100 of 0.752. Dense retrieval is weaker than BM25 in this French sample, suggesting that exact topic anchoring is especially important. Embedding similarity can retrieve broad opinion text or adjacent policy discussions that are semantically related but not as directly responsive to the query.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile is strongest overall, with nDCG@10 of 0.576, Hit@10 of 1.000, and Recall@100 of 0.827. It preserves BM25's complete first-page coverage while improving both nDCG and recall. This is a clear hybrid-search case: BM25 anchors the central issue, while dense retrieval broadens coverage to arguments that use different wording or stance framing.

### Metric Interpretation for Model Researchers

Hit@10 is saturated for BM25 and hybrid, so nDCG@10 and Recall@100 are more useful. nDCG@10 measures whether strong relevant arguments appear early. Recall@100 measures whether the candidate set covers a broad pro/con space. Because every query has many positives, a system that retrieves only one argument is incomplete even if Hit@10 is high.

### Query and Relevance Type Tendencies

Queries are concise French controversial questions. Relevant documents are long debate arguments, often with claims, reasons, examples, and persuasive framing. Positives can cover different sides of the issue, so retrieval should favor coverage and diversity. Hard negatives may mention the same topic but fail to address the central question argumentatively.

### Representative Failure Modes

BM25 can over-rank long documents that repeat the topic without strong argumentative content. Dense retrieval can retrieve broad opinion pieces that do not answer the specific question. Hybrid retrieval improves coverage but may still underrepresent one side of the debate. Failure analysis should check argument substance and stance coverage, not just topic match.

### Training and Leakage Considerations

Training should exclude Touché 2020, BEIR, NanoBEIR, and translated argument documents likely to overlap with these topics or documents. Useful non-overlapping data includes debate portal argument collections, pro/con retrieval pairs, argument quality ranking data, and French or multilingual controversial-topic retrieval supervision. Multi-positive training is required because every query has many relevant arguments.

### Model Improvement Signals

Strong models should preserve exact issue matching while learning argumentative relevance and stance coverage. Useful signals include same-topic non-argument hard negatives, stance-diverse positives, paired pro/con arguments, and long-document argument ranking. Hybrid systems are well suited because they combine topic anchoring with semantic argument expansion.

## Example Data

| Query | Positive document |
| --- | --- |
| Les devoirs sont-ils utiles ? [29 chars] | Premièrement, voici trois arguments en faveur du maintien des devoirs dans les écoles modernes. 1. Les devoirs aident les apprenants actifs. Il est généralement admis qu'il existe trois types d'apprenants : ceux qui apprennent en écoutant, ceux qui apprennent en voyant et ceux qui apprennent en faisant. Alors que beaucoup se contentent d'entendre ou de voir les instructions sur un sujet donné, certains ont besoin de le faire réellement. Ainsi, les devoirs sont bénéfiques pour ce dernier groupe car l'instruction se fait par l'action. 2. Les devoirs renforcent l'instruction. Bien que beaucoup seraient probablement ravis de ne pas avoir de devoirs, la qualité de l'éducation reçue en souffrirait certainement s'ils étaient supprimés. Que les devoirs soient des lectures imposées, des dissertations, etc., tout est conçu pour renforcer l'instruction dans l'esprit des élèves. Après tout, ceux qui font leurs devoirs sont plus académiquement performants que ceux qui ne le font pas. Je pense que c... [1,000 / 4,176 chars] |
| Les médicaments sur ordonnance doivent-ils être publicisés directement auprès des consommateurs ? [97 chars] | De nombreuses publicités ne fournissent pas suffisamment d'informations sur l'efficacité des médicaments. Par exemple, Lunesta est promu par une chenille volante entrant par la fenêtre d'une chambre, au-dessus d'une personne dormant paisiblement. En réalité, Lunesta aide les patients à s'endormir 15 minutes plus vite après six mois de traitement et leur offre 37 minutes de sommeil supplémentaire par nuit. La majorité des publicités reposent sur des appels émotionnels, mais peu mentionnent les causes de la condition, les facteurs de risque ou les changements de mode de vie importants. Dans une étude de 38 publicités pharmaceutiques, les chercheurs ont constaté que 82 % faisaient une affirmation factuelle et 86 % présentaient des arguments rationnels pour l'utilisation du produit. Seulement 26 % décrivaient les causes de la condition, les facteurs de risque ou la prévalence. Ainsi, les patients ne reçoivent pas une information équilibrée qui les rendrait conscients que prendre un de ces... [1,000 / 1,987 chars] |
| Quels vaccins les enfants doivent-ils recevoir ? [48 chars] | Ce n'est pas encore un dossier complet... Juste quelques points que j'ai rassemblés... Les gouvernements ne devraient pas avoir le droit d'intervenir dans les décisions de santé que les parents prennent pour leurs enfants. Selon un sondage de 2010 réalisé par l'Université du Michigan, 31 % des parents estiment qu'ils devraient avoir le droit de refuser les vaccinations obligatoires à l'entrée à l'école pour leurs enfants. De nombreux parents ont des croyances religieuses contre la vaccination. Forcer de tels parents à vacciner leurs enfants violerait le 1er Amendement, qui garantit aux citoyens le droit à la libre pratique de leur religion. Les vaccins sont souvent inutiles dans de nombreux cas où le risque de décès par maladie est faible. Au début du XIXe siècle, la mortalité due aux maladies infantiles comme la coqueluche, la rougeole et la scarlatine a chuté drastiquement avant que l'immunisation ne soit disponible. Cette diminution de la mortalité a été attribuée à une meilleure hy... [1,000 / 5,341 chars] |

## Public Sources

- [Touché 2020 overview](https://doi.org/10.1007/978-3-030-58219-7_26)
- [Touché 2020 dataset](https://doi.org/10.5281/zenodo.6862281)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| Touché 2020 overview (https://doi.org/10.1007/978-3-030-58219-7_26) |
| Touché 2020 dataset (https://doi.org/10.5281/zenodo.6862281) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
