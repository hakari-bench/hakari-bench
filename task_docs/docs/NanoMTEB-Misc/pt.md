# NanoMTEB-Misc / pt

## Overview

`pt` is the Portuguese EuroPIRQ retrieval split. Queries are synthetic
Portuguese questions, and documents are Portuguese EU legal and administrative
passages derived from DGT-Acquis. The Nano split contains 100 queries, 9,517
documents, and 100 positive qrels, with one positive passage per query. Queries
average 149.75 characters, and documents average 583.83 characters. The task
evaluates Portuguese retrieval over formal EU text where legal references,
institutions, article wording, and administrative phrasing provide strong
lexical anchors.

## Details

### What the Original Data Measures

The [EuroPIRQ dataset card](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval)
describes European Parallel Information Retrieval Queries built from
DGT-Acquis paragraph chunks in English, Finnish, and Portuguese. The data was
cleaned, language-checked, aligned, and paired with synthetic questions. No
standalone EuroPIRQ task paper was confirmed; interpretation is based on the
dataset card and MTEB/MMTEB context.

The Portuguese split measures whether a retriever can map a generated question
to the original Portuguese EU passage. The passages are formal and often
contain legal bases, committee language, court formulas, or policy-specific
phrases.

### Observed Data Profile

The split has 100 Portuguese queries, 9,517 documents, and 100 positive
judgments. Every query has exactly one positive. Questions are long and usually
ask about legal, institutional, or policy implications. Documents are medium
length and dense with EU administrative style.

Examples ask about business failure as an opportunity, REACH burden on SMEs,
the ongoing process of an integrated market, Greek habitat-protection measures,
and promotion of typical non-agricultural products.

### BM25 Evaluation Profile

BM25 is strongest, with nDCG@10 of 0.9186, hit@10 of 0.9800, and recall@100 of
1.0000. The split is lexically friendly because synthetic questions preserve
many distinctive names, institutions, legal references, and policy terms from
the target passage. BM25 nearly saturates both early hit rate and candidate
coverage.

Remaining errors are likely caused by repeated legal boilerplate or very
similar passages from the same EU administrative domain.

### Dense Evaluation Profile

Dense retrieval reaches nDCG@10 of 0.8623, hit@10 of 0.9300, and recall@100 of
0.9600. It is strong but clearly below BM25, showing that semantic matching
alone loses some exact legal references and surface anchors. The formal
Portuguese register and near-duplicate passages make precise wording important.

This task therefore checks whether dense models preserve legal and
administrative specificity, not only broad meaning.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.8901, hit@10 of 0.9400,
and recall@100 of 1.0000. It restores complete top-100 coverage but remains
below BM25 in top-10 ordering. There are no safeguard-positive rows.

Hybrid search is a useful robust candidate pool here, but the lexical baseline
already captures most of the needed signal. A reranker would need to resolve
near-duplicate legal passages to improve beyond BM25.

### Metric Interpretation for Model Researchers

`pt` is BM25-favorable. Hybrid search has full recall but not the best early
ranking, and dense retrieval is slightly weaker. Because every query has one
positive, nDCG@10 and hit@10 directly evaluate whether the exact source passage
is ranked early.

This split is valuable for Portuguese legal-domain precision and for testing
whether dense systems regress on exact legal wording.

### Query and Relevance Type Tendencies

Queries are Portuguese synthetic questions over EU legal and administrative
content. Positive documents are formal passages from the same domain. Questions
often ask for the reason, legal effect, required measure, or institutional
purpose stated in the passage.

Relevance is exact source-passage answerability. A similar passage from the same
institution or regulation can be a hard negative.

### Representative Failure Modes

BM25 can confuse repeated court or committee formulas. Dense retrieval can
retrieve a semantically related EU passage that lacks the specific legal basis
or measure. Hybrid retrieval improves recall but can still rank a nearby
boilerplate passage above the target.

Portuguese legal phrasing can also include long clauses where the decisive
condition is a small part of the passage.

### Training Data That May Help

Useful training data includes Portuguese legal retrieval, EU-domain passage
retrieval, multilingual DGT-Acquis parallel corpora, and synthetic
question-passage pairs. Hard negatives should be passages with the same legal
basis, institution, or administrative domain. Training should exclude EuroPIRQ
evaluation questions and positive passages overlapping this Nano split.

Synthetic data should generate Portuguese questions from non-evaluation EU
passages and include both entity-heavy and paraphrased questions.

### Model Improvement Notes

Models should preserve Portuguese legal references, institutional names, and
formal phrase structure. Dense encoders should be trained with near-duplicate
legal hard negatives. Rerankers should verify the precise legal or procedural
answer, not only the domain match.

## Example Data

| Query | Positive document |
| --- | --- |
| Por que a Comissão acredita que o insucesso empresarial deve ser visto como uma oportunidade para um novo arranque? [115 chars] | O CESE subscreve a importância atribuída pela Comissão à necessidade de superar o estigma do insucesso empresarial. A Comissão está certa em afirmar que a criação de empresas e o êxito e o insucesso empresariais são inerentes à realidade da economia de mercado. Salienta ainda que, no quadro da ausência generalizada nas sociedades de apreço e de compreensão pelo espírito empresarial, os problemas nos negócios ou mesmo o insucesso empresarial não são ainda suficientemente entendidos como uma evolução económica normal e uma oportunidade para um novo arranque. [562 chars] |
| Como o Conselho propõe aliviar a sobrecarga das PME em relação ao regulamento REACH? [84 chars] | Nesta base, a posição comum não integra algumas das alterações adoptadas pelo Parlamento Europeu em primeira leitura (alterações 169 e 726). No que se refere à alteração 169, que introduziria um procedimento menos pesado para as PME, o Conselho partilha da opinião que a sobrecarga deste grupo de empresas deve ser aliviada. Isto encontra-se claramente expresso nos considerandos 8 (deverá ser dada especial atenção ao potencial impacto do REACH nas PME) e 34 (Orientação) e nos artigos 73.o (taxas reduzidas para as PME) e 76.o (assistência da Agência). [554 chars] |
| O que é necessário para o processo contínuo de construção e operação de um mercado integrado? [93 chars] | Finalmente, a construção de um mercado totalmente integrado não é uma tarefa definida e com um fim finito, mas antes um processo permanente que requer um esforço, vigilância e actualização constantes. Há sempre novos desafios e, à medida que forem sendo eliminados obstáculos ao funcionamento do mercado único, outras barreiras aparecerão e terão de ser abordadas. Assim, é da máxima importância que qualquer novo tratado contenha os poderes e competências jurídicos necessários para continuar a obra de construir e manter em funcionamento um mercado integrado. [561 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| EuroPIRQ-retrieval | 2025 | Dataset card | [https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | Benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| MTEB: Massive Text Embedding Benchmark | 2022 | Benchmark paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| A Portuguese question about why business failure should be seen as a new-start opportunity. | A passage supporting the Commission's view that business creation includes success and failure. |
| A Portuguese question about reducing SME burden under REACH. | A passage discussing a less burdensome procedure and Parliament amendments. |
| A Portuguese question about building and operating an integrated market. | A passage describing integration as an ongoing process requiring effort and vigilance. |
| A Portuguese question about Greek authorities' failure to protect habitats. | A passage saying necessary measures were not taken to establish adequate protection. |
| A Portuguese question about promoting typical non-agricultural products. | A passage on preparatory work for an EU instrument to valorize and promote such products. |
