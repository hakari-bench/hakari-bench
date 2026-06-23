# NanoMTEB-Korean / lawir_ko

## Overview

`lawir_ko` is a Korean legal-information retrieval task based on statute and
regulation articles. Queries ask for the legal provision associated with a
Korean law title and article concept, and documents are individual article texts
from Korean legal sources. The Nano split contains 200 queries, 3,562 documents,
and 200 positive qrels, with exactly one positive article per query. Queries
average 50.62 characters, and documents average 387.79 characters. The task is
useful for evaluating whether Korean retrieval models can map a legal query to
the correct article among many formulaic and cross-referenced provisions.

## Details

### What the Original Data Measures

No standalone task paper was confirmed for this dataset. The interpretation is
based on the
[on-and-on/lawgov_ir-ko](https://huggingface.co/datasets/on-and-on/lawgov_ir-ko)
dataset card, Korea Law Information Center context, MTEB metadata, and observed
Nano data. The dataset was created for Korean legal information retrieval, with
documents representing statute or regulation articles.

In this retrieval formulation, the query often names a law and asks which
provision covers a particular article concept. The model must identify the
corresponding article text, not merely retrieve a legal document from the same
topic area.

### Observed Data Profile

The split has 200 Korean queries, 3,562 legal article documents, and 200
positive judgments. Every query has one positive. Queries usually mention a law
title and a provision concept, while documents contain numbered clauses,
definitions, duties, exceptions, and cross-references. The corpus includes many
articles with similar formulaic language.

Examples involve financial consumer protection, food sanitation standards,
agricultural product payment-settlement organizations, elderly-driver signs,
and personal-information dispute procedures. The correct article is often
distinguished by provision title and legal role rather than by broad domain.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5232, hit@10 of 0.7100, and recall@100 of 0.9200.
Lexical matching is helpful because law titles, article names, and specialized
terms often appear in the query and article. However, BM25 is not sufficient:
legal articles share common phrasing, enumerated structures, and
cross-reference patterns, so high term overlap can point to adjacent but
incorrect provisions.

BM25 failures are particularly important in legal retrieval because an adjacent
article may look plausible but answer a different legal question. Exact article
selection matters.

### Dense Evaluation Profile

Dense retrieval is stronger, with nDCG@10 of 0.6534, hit@10 of 0.8200, and
recall@100 of 0.9700. Dense embeddings appear to help connect the provision
concept in the query to the relevant article even when the wording is not a
perfect surface match. They also reduce some of the noise from boilerplate
legal language.

This split is a good diagnostic for Korean legal-domain semantic matching. A
model must preserve article names, legal concepts, and formal clause structure
while avoiding generic topical similarity across the same law.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.6491, hit@10 of 0.8200,
and recall@100 of 0.9750. It is nearly tied with dense retrieval at top-10 and
slightly better for candidate coverage. Candidate lists contain 100 to 101
entries, with five safeguard-positive rows.

This is a balanced hybrid case. Dense retrieval gives strong semantic ranking,
while lexical matching helps retain exact legal titles and provision terms.
The hybrid pool is likely a strong input for a legal reranker because it offers
the best top-100 relevant coverage.

### Metric Interpretation for Model Researchers

`lawir_ko` is dense-favorable, with hybrid search best for recall. BM25 remains
useful but is limited by legal boilerplate and adjacent provisions. Since each
query has one positive, nDCG@10 and hit@10 directly evaluate whether the correct
article is ranked early, while recall@100 indicates whether a downstream
reranker can still recover it.

The dense-vs-BM25 gap suggests that Korean legal retrieval benefits from
semantic article-title and provision-concept matching, not only exact term
frequency.

### Query and Relevance Type Tendencies

Queries are Korean legal retrieval requests naming a law and asking for the
article that defines, applies, or explains a provision. Positive documents are
single statute or regulation articles. They often contain numbered clauses,
subclauses, and formal legal wording.

Relevance is provision-specific. Documents from the same law can be strong hard
negatives if they share terms but govern a different article concept.

### Representative Failure Modes

BM25 can over-rank adjacent articles with shared legal phrases. Dense retrieval
can over-generalize within the same law or legal domain if it misses the exact
article concept. Hybrid retrieval can improve coverage but still needs a
reranker to resolve fine-grained provision distinctions.

Cross-references are another risk: a document may mention the right law or
article number only as a reference, not as the governing provision requested by
the query.

### Training Data That May Help

Useful training data includes non-overlapping lawgov_ir-ko examples, Korean
statute article retrieval pairs, law-title and article-title matching pairs,
and hard negatives from the same law and adjacent provisions. Training should
exclude lawgov_ir-ko evaluation rows, Nano queries, qrels, and positive statute
articles.

Synthetic data should generate Korean statute articles with numbered clauses,
article titles, definitions, duties, and cross-references, then create legal
retrieval queries naming a law and asking for the article that explains a
provision.

### Model Improvement Notes

Models should preserve Korean legal terminology, article titles, and clause
structure. Dense encoders need same-law hard negatives to avoid broad legal
topic matching. Rerankers should check whether the candidate is the requested
provision itself rather than an article that only references it.

## Example Data

| Query | Positive document |
| --- | --- |
| 금융소비자 보호에 관한 법률 상 '위원의 제척ㆍ기피 및 회피'에 대한 법규는 무엇입니까? [49 chars] | - 조정위원회 위원은 다음 각 호의 어느 하나에 해당하는 경우에는 그 분쟁조정신 청사건(이하 “사건”이라 한다)의 심의ㆍ의결에서 제척(--)된다. 1. 위원이나 그 배우자 또는 배우자였던 사람이 해당 사건의 당사자(당사자가 법인ㆍ단체 등인 경우에는 그 임원을 포함한다. 이하 이 호 및 제2호에서 같다)가 되거나 그 사건의 당사자와 공동권리자 또는 공동의무자... [200 / 645 chars] |
| '식품위생법'의 전체 내용 중 '기구 및 용기ㆍ포장에 관한 기준 및 규격'에 관한 법적 정의나 적용 사항과 범위 등을 명시한 조항이 있나요? [78 chars] | - 식품의약품안전처장은 국민보건을 위하여 필요한 경우에는 판매하 거나 영업에 사용하는 기구 및 용기ㆍ포장에 관하여 다음 각 호의 사항을 정하여 고시한다. 1. 제조 방법에 관한 기준 2. 기구 및 용기ㆍ포장과 그 원재료에 관한 규격 - 식품의약품안전처장은 제1항에 따라 기준과 규격이 고시되지 아니한 기구 및 용기ㆍ포장의 기준과 규격을 인정 받으려는 자에게... [200 / 696 chars] |
| 농수산물 유통 및 가격안정에 관한 법률에서 '대금정산조직 설립의 지원'와 관련되어 시행되고 있는 조항을 설명하시오. [64 chars] | 농림축산식품부장관, 해양수산부장관 및 도매시장 개설자는 도매시장법인ㆍ시 장도매인ㆍ중도매인 등이 다음 각 호의 대금의 정산을 위한 조합, 회사 등(이하 “대금정산조직”이라 한다)을 설립하 는 경우 그에 대한 지원을 할 수 있다. 1. 출하대금 2. 도매시장법인과 중도매인 또는 매매참가인 간의 농수산물 거래에 따른 판매대금 [180 chars] |
| 도로교통법 중 '고령운전자 표지'에 해당하는 부분이 뭐야? [32 chars] | - 국가 또는 지방자치단체는 고령운전자의 안전운전 및 교통사고 예방을 위하여 행정안전 부령으로 정하는 바에 따라 고령운전자가 운전하는 차임을 나타내는 표지(이하 “고령운전자 표지”라 한다)를 제작하 여 배부할 수 있다. - 고령운전자는 다른 차의 운전자가 쉽게 식별할 수 있도록 차에 고령운전자 표지를 부착하고 운전할 수 있다. [183 chars] |
| 개인정보 보호법에서 '자료의 요청 및 사실조사'에 관해 다루고 있는 하위 법령이 있나요? [49 chars] | - 분쟁조정위원회는 제43조제1항에 따라 분쟁조정 신청을 받았을 때에는 해당 분쟁의 조정을 위하여 필요한 자료를 분쟁당사자에게 요청할 수 있다. 이 경우 분쟁당사자는 정당한 사유가 없으면 요청에 따라야 한다. - 분쟁조정위원회는 분쟁의 조정을 위하여 사실 확인이 필요한 경우에는 분쟁조정위원회의 위원 또는 대통령령으 로 정하는 사무기구의 소속 공무원으로 하여... [200 / 526 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| on-and-on/lawgov_ir-ko | 2026 | Dataset card | [https://huggingface.co/datasets/on-and-on/lawgov_ir-ko](https://huggingface.co/datasets/on-and-on/lawgov_ir-ko) |
| Korea Law Information Center | 2026 | Public legal source | [https://www.law.go.kr/LSW/main.html](https://www.law.go.kr/LSW/main.html) |
| MTEB: Massive Text Embedding Benchmark | 2023 | Paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| 금융소비자 보호에 관한 법률의 위원 제척ㆍ기피 및 회피 조항을 묻는 질문. | A statute article describing when dispute-mediation committee members are excluded or recused. |
| 식품위생법의 기구 및 용기ㆍ포장 기준을 묻는 질문. | A food-sanitation article on standards and specifications for utensils, containers, and packaging. |
| 농수산물 유통 및 가격안정 법률의 대금정산조직 지원을 묻는 질문. | An article authorizing support for payment-settlement organizations in wholesale markets. |
| 도로교통법의 고령운전자 표지를 묻는 질문. | A traffic-law article on producing and attaching elderly-driver signs. |
| 개인정보 보호법의 자료 요청 및 사실조사를 묻는 질문. | A dispute-mediation article allowing document requests and fact investigations. |
