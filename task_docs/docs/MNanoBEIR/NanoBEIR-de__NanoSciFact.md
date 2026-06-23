# MNanoBEIR / NanoBEIR-de / NanoSciFact

## Overview

This task is the German NanoBEIR version of SciFact, a scientific claim verification retrieval benchmark. The original SciFact dataset contains expert-written scientific claims paired with abstracts that support or refute those claims, with rationale annotations for verification. In retrieval form, the model receives a German translated scientific claim and must retrieve German translated abstracts that contain the evidence needed to verify it. This NanoBEIR slice contains 50 queries, 2,919 documents, and 56 positive relevance judgments. Most claims have one positive abstract, with a small number of multi-positive cases. The task is useful for evaluating whether retrieval models can connect long, terminology-rich scientific claims to evidence-bearing abstracts, while separating retrieval quality from the later support/refute classification step.

## Details

### What the Original Data Measures

SciFact measures scientific evidence retrieval and claim verification. Claims are derived from citation-like scientific assertions and usually describe specific findings, mechanisms, interventions, or observed effects. The retrieval problem is to find the abstract that contains evidence for or against the claim. A model must therefore preserve scientific terminology while recognizing when an abstract actually provides evidential support, not merely when it belongs to the same broad biomedical topic.

### Observed Data Profile

The German Nano task has 50 queries, 2,919 documents, and 56 positives. Positives per query average 1.12, and only four queries have multiple positives. Queries are long for a retrieval benchmark, averaging about 111 characters, while documents average about 1,648 characters. The examples include claims about neutrophil migration, antiretroviral therapy and tuberculosis, West Nile virus, cervical cancer screening, and TDP-43 neuronal damage. Positive documents are long translated scientific abstracts with background, methods, results, and conclusions.

### BM25 Evaluation Profile

BM25 performs strongly, with nDCG@10 of 0.621, Hit@10 of 0.760, and Recall@100 of 0.839. This reflects the lexical structure of scientific claims: claims often repeat distinctive biomedical entities, proteins, diseases, interventions, and measurement terms that also appear in the evidence abstract. Term frequency and rare-token matching are therefore highly informative. BM25 still fails when evidence uses different terminology, abbreviations, or experimental context, but it provides a solid baseline because exact scientific vocabulary matters.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is strongest by top-10 ranking, reaching nDCG@10 of 0.702, Hit@10 of 0.840, and Recall@100 of 0.893. Dense retrieval improves over BM25 by connecting scientific claims to abstracts that express the same finding in less direct wording. It can capture relationships among interventions, outcomes, biological mechanisms, and disease contexts beyond raw lexical overlap. The strong dense result indicates that semantic evidence matching is important even when exact terminology is useful.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.658, Hit@10 of 0.820, and Recall@100 of 0.946, with three safeguard rows at 101 candidates. It has the best Recall@100, while dense retrieval has the best nDCG@10. This is a useful hybrid-search pattern: combining BM25 and dense retrieval improves evidence coverage, but the final top ordering can still benefit from dense semantic ranking. For verification pipelines, the higher hybrid recall may be valuable because missing the evidence abstract cannot be fixed by a downstream verifier.

### Metric Interpretation for Model Researchers

For SciFact, Recall@100 is important because a fact-checking pipeline needs the evidence abstract in the candidate set. nDCG@10 measures how usable the retriever is without a heavy downstream reranker. The dense profile gives the best direct ranking, while reranking_hybrid gives the broadest evidence coverage. Researchers should distinguish retrieval from verification: retrieving a refuting abstract is still a positive retrieval result if it contains the needed evidence.

### Query and Relevance Type Tendencies

Queries are declarative scientific claims, not questions. They often include biomedical entities, abbreviations, causal relationships, and comparative findings. Relevant documents are abstracts that provide evidence for or against the claim. Some negatives may share the same protein, disease, or intervention but discuss a different result, making hard-negative discrimination important.

### Representative Failure Modes

BM25 can over-rank abstracts that share rare terminology but do not verify the claim. Dense retrieval can over-rank abstracts in the same scientific neighborhood without the exact evidential finding. Hybrid retrieval improves candidate coverage but can still include lexical distractors near the top. Failure analysis should check whether a retrieved abstract supports or refutes the specific claim, not just whether it mentions the same entities.

### Training and Leakage Considerations

Training should exclude SciFact, BEIR, NanoBEIR, and translated claims or abstracts likely to overlap with this evaluation slice. Useful non-overlapping data includes scientific claim-evidence pairs, biomedical abstract retrieval data, CORD-19-style claim retrieval, and German or multilingual scientific NLI and evidence selection data. Synthetic data should generate atomic German scientific claims from non-evaluation abstracts and include hard negatives from related abstracts that mention the same entities but do not provide the needed evidence.

### Model Improvement Signals

Strong models should preserve exact scientific terminology while learning claim-to-evidence semantics. Useful improvements include better biomedical entity representation, abbreviation handling, contradiction-aware evidence retrieval, and hard-negative training with related abstracts. Hybrid systems should use sparse retrieval to protect rare scientific terms and dense retrieval to bridge phrasing differences in findings and mechanisms.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q steuert die Organisation der Migration von Neutrophilen zu Entzündungsherden, indem es die Fun... [100 / 136 chars] | Neutrophile durchlaufen eine schnelle Polarisation und gerichtete Bewegung, um Infektions- und Entzündungsherde zu infiltrieren. Wir zeigen, dass ein inhibitorischer MHC-I-Rezeptor, Ly49Q, für die sch... [200 / 1,116 chars] |
| Antiretrovirale Therapie verringert die Häufigkeit von Tuberkulose bei verschiedenen CD4-Werten. [96 chars] | HINTERGRUND Die Infektion mit dem humanen Immundefizienz-Virus (HIV) ist der stärkste Risikofaktor für die Entwicklung von Tuberkulose und hat deren Wiederauftreten, insbesondere in Subsahara-Afrika,... [200 / 2,378 chars] |
| Eine schnelle Hochregulierung und eine höhere basale Expression von Interferon-induzierten Genen ver... [100 / 199 chars] | Obwohl die Anfälligkeit von Neuronen im Gehirn für mikrobiologische Infektionen ein entscheidender Faktor für den klinischen Verlauf ist, ist wenig über die molekularen Faktoren bekannt, die diese Anf... [200 / 1,264 chars] |
| Primäre Zervixkarzinom-Screening mit HPV-Nachweis weist eine höhere longitudinale Sensitivität auf a... [100 / 192 chars] | HINTERGRUND Das Screening auf Gebärmutterhalskrebs durch HPV-Tests erhöht die Sensitivität bei der Erkennung von hochgradigen (Grad 2 oder 3) zervikalen intraepithelialen Neoplasien, aber ob dieser Ge... [200 / 2,622 chars] |
| Die Hemmung der Interaktion zwischen TDP-43 und den Proteinen ND3 und ND6 des Atmungskomplexes I füh... [100 / 157 chars] | Genetische Mutationen im TAR-DNA-bindenden Protein 43 (TARDBP, auch bekannt als TDP-43) verursachen amyotrophe Lateralsklerose (ALS), und eine erhöhte Präsenz von TDP-43 (kodiert durch TARDBP) im Zyto... [200 / 1,463 chars] |

## Public Sources

- [SciFact paper](https://arxiv.org/abs/2004.14974)
- [SciFact repository](https://github.com/allenai/scifact)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| SciFact paper (https://arxiv.org/abs/2004.14974) |
| SciFact repository (https://github.com/allenai/scifact) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
