# MNanoBEIR / NanoBEIR-sv / NanoSciFact

## Overview

NanoSciFact in the Swedish NanoBEIR slice is a scientific evidence retrieval task derived from SciFact. The queries are Swedish translated scientific claims, and the corpus contains Swedish translated scientific abstracts. The retrieval goal is to find abstracts that provide evidence for the claim, not merely papers that discuss the same broad topic. This makes the task a compact benchmark for scientific fact-checking retrieval, biomedical terminology handling, and evidence-sensitive ranking in Swedish.

## Details

### What the Original Data Measures

SciFact evaluates verification of scientific claims against research abstracts. In retrieval form, a claim must be matched to an abstract that contains the evidence needed to assess it. The relevant abstract may support or contextualize the claim through a specific experimental result, biomedical mechanism, clinical finding, or methodological statement.

The Swedish translated version tests this evidence retrieval behavior with long technical claims and long abstracts. Many queries contain biomedical entities, diseases, genes, therapies, or measurement concepts. A strong retriever must preserve exact scientific anchors while also recognizing when an abstract expresses the same evidence relation in different wording.

### Observed Data Profile

The task contains 50 queries, 2,919 documents, and 56 relevance judgments. Most queries have one positive abstract, with an average of 1.12 positives per query. The minimum is 1, the median is 1.0, the maximum is 4, and 4 queries are multi-positive, or 8.0% of the query set. This is therefore mostly a single-evidence retrieval task.

Queries average 95.12 characters, while documents average 1,429.10 characters. Both sides are scientifically dense, but the abstract is much longer and may contain background, methods, results, and conclusions. The retrieval challenge is to identify the evidence-bearing abstract, not simply the abstract with the most shared biomedical words.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6539, hit@10 of 0.8200, and recall@100 of 0.8929 using the top-500 BM25 candidate subset. This is a strong lexical baseline. Scientific claims often contain distinctive terminology such as gene names, diseases, treatment names, or biological processes, and BM25 can use those terms effectively.

The score is not perfect because evidence retrieval requires more than matching terminology. A same-entity abstract may fail to support the claim, while a more relevant abstract may express the finding through different phrasing. BM25 is therefore good at candidate discovery, but still needs help distinguishing evidence from related background.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.6730, hit@10 of 0.8400, and recall@100 of 0.9286. Dense retrieval improves over BM25 across all three metrics. This indicates that embedding similarity adds value beyond exact scientific term overlap, especially for paraphrased evidence and claim-to-abstract semantic matching.

The dense improvement is moderate rather than dramatic because lexical anchors already carry substantial signal in scientific claims. Dense retrieval appears to help when the evidence relation is expressed in a less literal way or when the relevant abstract contains broader context around the claim. Remaining errors likely involve very close biomedical distractors or claims whose truth depends on fine-grained causal or experimental details.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7181, hit@10 of 0.8800, and recall@100 of 0.9286. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 4 safeguard rows and a mean of 100.08 candidates. This is the strongest top-rank profile among the three modes, while recall@100 matches dense retrieval.

The hybrid profile is well aligned with Swedish SciFact. BM25 contributes precise biomedical terminology, and dense retrieval contributes semantic evidence matching. The result improves nDCG@10 and hit@10, showing that the combination is not just broader but also better ordered near the top. For a scientific verification pipeline, this candidate set is a strong first-stage retrieval option.

### Metric Interpretation for Model Researchers

nDCG@10 is the key ranking metric because an evidence retrieval system must surface the correct abstract in the first page. hit@10 measures whether at least one evidence abstract is visible, while recall@100 measures whether a later reranker or verifier has access to the evidence. Since most queries have one positive, the top-rank metrics are especially direct.

The comparison shows a useful progression. BM25 is already strong due to exact scientific terminology. Dense retrieval improves candidate coverage and top-rank quality through semantic matching. reranking_hybrid is strongest at the top, demonstrating that this task benefits from combining lexical anchors with dense claim-evidence similarity.

### Query and Relevance Type Tendencies

Queries are long scientific claims, often biomedical. Examples mention Ly49Q and neutrophil migration, antiretroviral therapy and tuberculosis, interferon-induced genes and West Nile virus, HPV detection for cervical cancer screening, and TDP-43 interactions in neuronal loss. Relevant documents are abstracts that contain the experimental or clinical evidence related to the claim.

The task rewards models that preserve technical detail. Small changes in a gene, treatment, disease, or causal relation can change relevance. A retriever must distinguish a true evidence abstract from a merely related abstract in the same biomedical area.

### Representative Failure Modes

Likely failures include retrieving abstracts that mention the same entity but not the claim outcome, confusing support evidence with background, over-ranking broad biomedical context, and missing evidence when translated terminology differs from the claim. BM25 may overvalue exact terms, while dense models may retrieve semantically adjacent but non-evidential abstracts.

### Training Data That May Help

Useful training data includes scientific claim verification, biomedical evidence retrieval, PubMed-style abstract search, multilingual scientific QA, and hard negatives that share entities but do not evidence the claim. Swedish scientific text can help with terminology and phrasing. For rerankers, close non-evidence abstracts are the most useful negatives.

### Model Improvement Notes

A model targeting this task should combine biomedical term precision with evidence-aware semantic matching. Sparse systems need strong tokenization and normalization for scientific names. Dense systems should improve factual relation sensitivity through hard-negative training. Hybrid systems are well suited here, especially when followed by a reranker that compares the claim with the full abstract.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q styr organiseringen av neutrofilmigration till inflammationsställen genom att reglera membranr... [100 / 115 chars] | Neutrofilerna genomgår snabbt polarisering och riktad rörelse för att tränga in i infektions- och inflammationsställen. Vi visar här att en inhiberande MHC I-receptor, Ly49Q, var avgörande för den sna... [200 / 1,025 chars] |
| Antiretroviral behandling minskar förekomsten av tuberkulos över ett brett spektrum av CD4-strata. [98 chars] | BAKGRUND Infektion med humant immunbristvirus (HIV) är den starkaste riskfaktorn för att utveckla tuberkulos och har drivit på dess återkomst, särskilt i subsahariska Afrika. År 2010 uppskattades det... [200 / 2,152 chars] |
| Snabb uppreglering och högre basala uttryck av interferoninducerade gener minskar överlevnaden hos g... [100 / 160 chars] | Neuronernas känslighet i hjärnan för mikrobiella infektioner är en avgörande faktor för klinisk utfall. Det finns lite kunskap om de molekylära faktorer som styr denna sårbarhet. Vi visar här att två... [200 / 1,092 chars] |
| Primär screening för livmoderhalscancer med HPV-detektion har högre longitudinell känslighet än konv... [100 / 177 chars] | Bakgrund: Screening för livmoderhalscancer baserat på testning för humant papillomavirus (HPV) ökar känsligheten för upptäckt av höggradig (grad 2 eller 3) livmoderhalscancerprekancerösa förändringar,... [200 / 2,333 chars] |
| Hinderar interaktionen mellan TDP-43 och komplex I-proteiner ND3 och ND6 resulterar i ökad TDP-43-in... [100 / 125 chars] | Genetiska mutationer i TAR DNA-bindande protein 43 (TARDBP, även känt som TDP-43) orsakar amyotrofisk lateral skleros (ALS), och en ökning av TDP-43 (kodat av TARDBP) i cytoplasman är en framträdande... [200 / 1,263 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [SciFact](https://arxiv.org/abs/2004.14974) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sv dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |

Representative query and positive abstract snippets:

| Query | Positive document snippet |
| --- | --- |
| Ly49Q styr organiseringen av neutrofilmigration till inflammationsställen genom att reglera membranraftsfunktioner. | Neutrofilerna genomgår snabbt polarisering och riktad rörelse för att tränga in i infektions- och inflammationsställen... |
| Antiretroviral behandling minskar förekomsten av tuberkulos över ett brett spektrum av CD4-strata. | BAKGRUND Infektion med humant immunbristvirus (HIV) är den starkaste riskfaktorn för att utveckla tuberkulos... |
| Snabb uppreglering och högre basala uttryck av interferoninducerade gener minskar överlevnaden hos granulära cellneuroner som är infekterade av West Nile-virus. | Neuronernas känslighet i hjärnan för mikrobiella infektioner är en avgörande faktor för klinisk utfall... |
| Primär screening för livmoderhalscancer med HPV-detektion har högre longitudinell känslighet än konventionell cytologi för att upptäcka cervikal intraepithelial neoplasi grad 2. | Bakgrund: Screening för livmoderhalscancer baserat på testning för humant papillomavirus (HPV) ökar känsligheten... |
| Hinderar interaktionen mellan TDP-43 och komplex I-proteiner ND3 och ND6 resulterar i ökad TDP-43-inducerad neuronal förlust. | Genetiska mutationer i TAR DNA-bindande protein 43 orsakar amyotrofisk lateral skleros... |
