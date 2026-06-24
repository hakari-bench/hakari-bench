# MNanoBEIR / NanoBEIR-sv / NanoSCIDOCS

## Overview

NanoSCIDOCS in the Swedish NanoBEIR slice is a scientific-document retrieval task derived from SCIDOCS and the SPECTER evaluation setting. The queries are Swedish translated paper titles or short descriptions, and the corpus contains Swedish translated scientific abstracts. The task asks a retriever to find scientifically related papers, often through topical, methodological, or citation-style similarity. It is a compact benchmark for multilingual academic search and paper recommendation behavior.

## Details

### What the Original Data Measures

SCIDOCS measures scientific document relatedness, with evaluation rooted in relationships between papers rather than direct answer support. A relevant abstract may share a research field, method, problem setting, or contribution type with the query paper. This makes the task different from ordinary fact lookup: the model must retrieve related research, not a single passage containing an answer.

The Swedish translated version adds multilingual pressure on technical terms, academic phrasing, and translated scientific abstracts. Many domain terms remain recognizable across languages, while the surrounding syntax and morphology change. A strong retriever must combine lexical technical anchors with semantic understanding of paper topics and contributions.

### Observed Data Profile

The task contains 50 queries, 2,210 documents, and 244 relevance judgments. Every query has multiple positives, with an average of 4.88 positives per query. The minimum is 3, the median is 5.0, and the maximum is 5, so the task consistently evaluates relevant-set ranking rather than single-target retrieval.

Queries average 74.74 characters, while documents average 941.30 characters. The query is usually a compact scientific title, and the document is a longer abstract. This creates a title-to-abstract retrieval problem where the model must infer topic and contribution from a short academic phrase.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.1892, hit@10 of 0.6800, and recall@100 of 0.4221 using the top-500 BM25 candidate subset. This is a weak lexical profile compared with many entity or QA tasks. Scientific terms help find some related abstracts, but exact term overlap does not cover the full set of relevant papers.

The low recall@100 is especially important because every query has several positives. BM25 may retrieve one abstract with the same technical vocabulary while missing other related papers that use different terminology. It may also over-rank documents that share domain words but describe a different contribution.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3472, hit@10 of 0.8200, and recall@100 of 0.6557. Dense retrieval substantially improves over BM25 on every metric. This indicates that embedding similarity is better at capturing scientific relatedness than exact title-term matching alone.

The dense gain is large because scientific relatedness often depends on concept, method, or task rather than identical wording. A dense model can connect abstracts about the same research area even when translated titles and abstracts use different surface forms. Remaining errors likely involve adjacent subfields, generic technical words, or fine-grained distinctions in contribution type.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.2844, hit@10 of 0.8000, and recall@100 of 0.6393. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 1 safeguard row and a mean of 100.02 candidates. The hybrid profile is stronger than BM25 but weaker than dense retrieval on all three main metrics.

This suggests that lexical evidence helps candidate diversity but does not improve the first-stage ordering for Swedish SCIDOCS. Dense similarity is the most aligned signal for scientific relatedness in this slice. The hybrid pool may still be useful for a later reranker, but the current ordering does not outperform dense retrieval.

### Metric Interpretation for Model Researchers

Because every query has multiple positives, recall@100 is a key measure of candidate-generation quality. hit@10 only tells whether at least one related paper appears early, while nDCG@10 shows whether several relevant abstracts are ranked well. A system that finds one obvious paper but misses the rest remains weak for scientific recommendation.

The profile is clear: BM25 struggles with title-to-abstract vocabulary mismatch, dense retrieval is strongest, and reranking_hybrid is intermediate. Researchers can use this task to evaluate scientific semantic retrieval, domain transfer, and whether hybrid scoring improves or disrupts paper-relatedness ranking.

### Query and Relevance Type Tendencies

Queries are scientific titles such as a new DC-DC multi-level boost converter, fast learning of sparse Gaussian Markov random fields, texture synthesis with convolutional neural networks, a broadband circularly polarized RFID antenna, and a digital heart monitor design. Relevant documents are abstracts from related scientific papers.

The task rewards models that understand scientific terminology at the phrase level. Method names, devices, architectures, and application settings all matter. A passage from the same broad field may still be irrelevant if it describes a different method or contribution.

### Representative Failure Modes

Likely failures include retrieving abstracts that share a field but not the contribution, over-ranking documents with repeated technical acronyms, missing related papers that use different translated terminology, and failing to recover all positives for a query. BM25 is brittle to vocabulary variation, while dense models can blur closely related subfields.

### Training Data That May Help

Useful training data includes scientific-paper retrieval, citation and co-citation ranking, paper recommendation data, multilingual academic abstracts, and hard negatives from the same field but different contribution. Swedish scientific text can help with language-specific phrasing, while broader multilingual scientific retrieval can improve semantic transfer.

### Model Improvement Notes

A model targeting this task should improve scientific relatedness rather than answer matching. Dense retrievers are the strongest baseline and should be refined with domain-specific hard negatives. Sparse systems need terminology normalization and expansion but must preserve technical specificity. Hybrid systems should be tuned carefully so lexical matches do not displace semantically stronger related papers.

## Example Data

| Query | Positive document |
| --- | --- |
| Ny DC-DC flernivåspänningshöjande omvandlare [44 chars] | Multinivåspänningsomvandlare är på väg att bli en ny typ av kraftomvandlare för högspänningsapplikationer. Multinivåspänningsomvandlare syntetiserar vanligtvis en trappformad spänningsvåg från flera nivåer av likspänningskondensatorer. En av de största begränsningarna med multinivåomvandlare är spänningsobalansen mellan olika nivåer. Teknikerna för att balansera spänningen mellan olika nivåer involverar vanligtvis spänningsklämning eller kondensatorladdningskontroll. Det finns flera sätt att implementera spänningsbalans i multinivåomvandlare. Utan att ta hänsyn till traditionella magnetiskt kopplade omvandlare presenterar denna artikel tre nyligen utvecklade multinivåspänningsomvandlare: 1) diodklämning, 2) flygkondensatorer, och 3) kaskaderade växelriktare med separata likspänningskällor. Driftsprincipen, egenskaperna, begränsningarna och potentiella applikationerna för dessa omvandlare kommer att diskuteras. [923 chars] |
| Snabb inlärning av glesa gaussiska Markovfält baserat på Cholesky-faktorisering [79 chars] | Sure, please provide the English document text that you need translated into Swedish. [85 chars] |
| Textursyntes med konvolutiva neurala nätverk [44 chars] | I detta arbete undersöker vi effekten av djupet i ett konvolutivt nätverk på dess noggrannhet i en stor skala bildigenkänningsinställning. Vår huvudsakliga bidrag är en grundlig utvärdering av nätverk med ökande djup, vilket visar att en betydande förbättring av tidigare konfigurationer kan uppnås genom att öka djupet till 16–19 viktskikt. Dessa resultat låg till grund för vårt bidrag till ImageNet Challenge 2014, där vårt team tog förstaplatsen och andraplatsen i lokaliserings- och klassificeringsbanorna respektive. Vi visar också att våra representationer fungerar bra på andra datamängder, där vi uppnår toppresultat. Viktigt att nämna är att vi har gjort våra två bästa ConvNet-modeller tillgängliga för allmänheten för att underlätta vidare forskning om användningen av djupa visuella representationer inom datorseende. [830 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original task context | [SPECTER](https://arxiv.org/abs/2004.07180) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sv dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |

Representative query and positive abstract snippets:

| Query | Positive document snippet |
| --- | --- |
| Ny DC-DC flernivåspänningshöjande omvandlare | Multinivåspänningsomvandlare är på väg att bli en ny typ av kraftomvandlare... |
| Snabb inlärning av glesa gaussiska Markovfält baserat på Cholesky-faktorisering | Sure, please provide the English document text that you need translated into Swedish. |
| Textursyntes med konvolutiva neurala nätverk | I detta arbete undersöker vi effekten av djupet i ett konvolutivt nätverk på dess noggrannhet... |
| Planär bredbandsringantenn med cirkulär polarisering för RFID-system | I denna artikel föreslås en teknik med horisontellt meanderande strimma... |
| Design av en avancerad digital hjärtmonitor med grundläggande elektroniska komponenter | I denna artikel presenterar vi designen och utvecklingen av en ny integrerad enhet för att mäta hjärtfrekvens... |
