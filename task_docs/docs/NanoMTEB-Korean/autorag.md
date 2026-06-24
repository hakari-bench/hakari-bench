# NanoMTEB-Korean / autorag

## Overview

`autorag` is a Korean RAG-oriented retrieval task built from public-document QA
data associated with the AutoRAG ecosystem. Queries are Korean questions over
finance, public-sector, legal, medical, healthcare, and commerce documents, and
the positive document is the chunk that contains the evidence needed by a RAG
system. The Nano split contains 114 queries, 720 documents, and 114 positive
qrels, with exactly one positive chunk per query. Queries average 69.61
characters, and documents average 823.60 characters. The task is a practical
test of Korean evidence retrieval from report-like chunks with numbers,
headings, policy conditions, and domain terminology.

## Details

### What the Original Data Measures

[AutoRAG: Automated Framework for optimization of Retrieval Augmented Generation Pipeline](https://arxiv.org/abs/2410.20878)
introduces AutoRAG as an open-source framework for evaluating and optimizing RAG
pipeline components, including lexical retrieval, dense retrieval, hybrid
retrieval, reranking, query expansion, and passage augmentation. The exact
`markers_bm` construction is primarily documented by dataset metadata and the
observed data rather than by a standalone task paper.

In retrieval terms, this split measures whether a Korean retriever can locate
the answer-bearing chunk for a RAG question. The target is not broad topical
similarity; the chunk should contain the specific evidence needed to answer the
query without external context.

### Observed Data Profile

The Nano split has 114 Korean queries, 720 documents, and 114 positive
judgments. Every query has one positive. Documents are public-report-like
chunks with headings, tables, percentages, dates, legal references, policy
conditions, and domain-specific terminology. Queries are often longer than
simple keyword searches because they ask for an explanation, condition, or
specific fact.

Examples include customs royalty rules, Yahoo Sports co-watching features, B2B
commerce automation, court findings about store columns, and local public
institution restructuring plans. These are realistic RAG retrieval cases where
the correct chunk may be one paragraph inside a larger report or PDF.

### BM25 Evaluation Profile

BM25 is the strongest profile, with nDCG@10 of 0.9053, hit@10 of 0.9912, and
recall@100 of 1.0000. This indicates that the task is highly favorable to
lexical matching. Queries often reuse distinctive Korean legal terms, report
phrases, named services, numerals, or policy expressions that appear in the
positive chunk.

The result is important for RAG engineering: a simple lexical retriever is a
very strong baseline for this dataset. Dense models must preserve exact Korean
domain terms and numeric anchors if they are to improve top-rank quality.

### Dense Evaluation Profile

The dense harrier-oss-270m candidates are weaker than BM25, with nDCG@10 of
0.7745, hit@10 of 0.9211, and recall@100 of 0.9561. Dense retrieval still finds
most positives, but it loses some exact evidence chunks that BM25 recovers. The
likely issue is that embedding similarity can blur report chunks that share
topic or domain while missing the exact clause, number, or named measure needed
for the answer.

For model researchers, this is a lexical-precision stress test in Korean. A
dense model that improves here must retain fine-grained terms, table-like facts,
and policy wording, not only broad semantic topic.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.8530, hit@10 of 0.9737,
and recall@100 of 1.0000. It restores complete recall like BM25 and improves
over dense retrieval, but it remains below BM25 in top-10 ordering. There are
no safeguard-positive rows, and each query has 100 hybrid candidates.

This pattern shows that hybrid search is useful as a robust RAG candidate pool:
it combines dense semantic coverage with lexical evidence and preserves full
top-100 recoverability. However, when exact Korean report terms dominate, the
BM25 ordering can still be better at the top.

### Metric Interpretation for Model Researchers

`autorag` is BM25-favorable. The main diagnostic is whether dense or hybrid
methods can avoid losing exact evidence that lexical matching captures. Since
there is exactly one positive per query, hit@10 directly measures whether the
answer chunk reaches an early result page, while recall@100 measures whether a
reranker has access to the answer at all.

The near-ceiling BM25 recall and hit rate mean that improvements should be
judged carefully. A dense model may look semantically strong but still be less
useful for RAG if it misses exact legal, financial, or policy evidence.

### Query and Relevance Type Tendencies

Queries are Korean RAG questions asking for factual explanations, quantities,
policy conditions, comparisons, or named measures. Positive documents are report
chunks that contain the needed evidence. Many chunks include mixed formats such
as headings, bullet markers, tables, and OCR-like text.

Relevance is evidence-specific. A chunk from the same report or domain is not
positive unless it contains the answer evidence. This makes same-report hard
negatives useful for training and analysis.

### Representative Failure Modes

BM25 can fail when the query paraphrases the report wording or when OCR and
tokenization artifacts alter Korean terms. Dense retrieval can fail by ranking a
topically related chunk that lacks the exact condition, percentage, or legal
clause. Hybrid retrieval can recover the positive but still rank a more
lexically attractive nearby chunk above it.

Numerical evidence is a common risk. If a question asks for a quantity or year,
the retriever must preserve the exact numeric context, not only retrieve a
related paragraph.

### Training Data That May Help

Useful training data includes non-overlapping Korean public-report RAG QA pairs,
Korean finance, government, legal, medical, and commerce document retrieval
pairs, question-to-chunk supervision from public PDFs, and hard negatives from
the same report or domain. Training should exclude `markers_bm` evaluation
queries, qrels, answers, and positive chunks likely to overlap with this Nano
split.

Synthetic data should generate Korean report chunks with headings, tables,
dates, percentages, policy conditions, and domain terminology, then create
grounded RAG questions requiring evidence from one chunk.

### Model Improvement Notes

Models should preserve Korean domain terms, numerals, and table-like evidence.
Dense encoders may need contrastive training with same-report negatives to avoid
topic-only matching. Rerankers should explicitly compare the requested fact or
condition against the candidate chunk's evidence.

## Example Data

| Query | Positive document |
| --- | --- |
| 관세법 시행령 제19조 제3항 제1호 다목, 제2호는 어떠한 상황에서 권리사용료가 해당 물품과 관련된 것으로 간주하는가? [67 chars] | 특허, 디자인, 노하우, 영업비밀 등의 무형의 권리가 다른 종류라고 볼 수는 없다. 구 관세법 시행령 제19조 제3항 제1호 다목, 제2호 등이 수입물품이 국내에서 생산 될 물품의 부분품이나 원재료인 경우, 권리사용료의 지급대상인 권리가 '국내에서 생산 될 물품'에 관한 것인지, 수입한 부분품이나 원재료에 관한 것인지 구별하지 않고, '국 내에서 당해 특허에 의하여 생산될 물품의 부분품·원재료 또는 구성요소로서 그 자체 에 당해 특허의 전부 또는 일부가 구현되어 있는 경우', '수입물품이 당해 디자인을 표 현하는 물품이거나 국내에서 당해 디자인권에 의하여 생산되는 물품의 부분품 또는 구 성요소로서 당해 디자인의 전후 또는 일부가 표현되어 있는 경우' 등을 권리사용료가 당해 물품과 관련되는 것으로 본다고 규정한 것도 위와 같은 점이 당연히 전제되어 있 기 때문일 것으로 보인다. (나) '상표권'의 경우, 구 관세법 시행령 제19조 제3항 제3호는 같은 항 제1호 다목이나 제2호와 달리, '부분품', '구성요소'와 같은 문구를 명시하고 있지는 않 으나, 뒤에서 보는 바와 같이 1 구 관세법 시행령 제3항 제3호의 '수입물품'을 '완제 품' 또는 소비자에게 최종 판매되는 상품' 등으로 제한하여 해석할 근거는 없는 점, 2 상표권은 물품에 상표를 부착 내지 표시하는 방식으로 구현되는 점, 3 상표의 사용에 는 상품 또는 상품의 포장에 상표를 표시하는 행위, 상품 또는 상품의 포장에 상표를 표시한 것을 양도 · 인도하거나 이를 목적으로 수입하는 행위도 당연히 포함되는 점(상 표법 제2조 제1항 제11호) 등에 비추어 볼 때. 이 사건 각 라이선스 계약에 따라 원고 에게 허여된 '계약제품의 제조·판매를 위해 상표를 사용할 권리'에는 담배 완제품 제 조에 사용할 목적으로 상표가 부착된 재료를 수입할 수 있는 권리가 당연히 포함되어 있다고 봄이 타당하다. - 26 - [939 chars] |
| 미국의 야후가 NFL 팬들을 위하여 어떠한 새로운 기능을 도입하였으며, 이 기능을 통해 팬들에게 어떠한 체험을 제공하였나요? [69 chars] | 트렌드 리포트 2. 커뮤니티에 초점을 맞춘 소셜 시청 트렌드와 특징 콘텐츠와 커뮤니티의 상관관계를 강조하며 이를 하나의 서비스로 제공하는 데 주력한 곳 은 주로 스트리밍 서비스와 빅테크 진영이다. 미국의 야후(Yahoo!)는 버라이즌 미디어 (Verizon Media) 시절부터 야후 스포츠(Yahoo Sports)에 친구들과 함께 영상을 시 정할 수 있는 Watch Together 기능을 도입해 호응을 얻은 바 있다. 이 기능은 NFL 팬 들이 야후 스포츠 앱에서 생방송 중계나 황금 시간대 콘텐츠를 시청하면서 친구들과 휴대 폰으로 영상 채팅을할 수 있도록 지원한다. 무료로 제공되는 이 기능은 축구 팬들이 NFL 생중계를 시청하면서 자체 커뮤니티를 만들 수 있는 새로운 방법을 제공한 것으로 높이 평 가받았다. 애플(Apple)이 지난해 말iOS 15부터 선보인 'SharePlay'도 플랫폼 차원에서 공동 시청 경험을 제공하는 사례로 주목받았다. 'SharePlay'는 다른 이용자와 함께 애플의 제휴 스트 리밍 서비스 영상을 시청할 수 있는 일종의 미디어 공유 기능으로, 애플의 영상 통화 기능인 Face Time'을 기반으로 한다. 이용자는 Face Time에서 영상 통화를 하면서 화면을 공유 하여 다른 이용자외 콘텐츠를 공동 시청할 수 있다. 디즈니+(Disney+), ESPN+, HBO맥스 (HBO Max), 훌루(Hulu), 마스터클래스(MasterClass). 파라마운트+(Parannount+) 플루토TV(Pluto TV), 틱톡(TikTok) 트위치 (Twitch) 등이 SharePlay 서비스 출시 시 점부터 애플과 제휴하여 서비스를 제공하고 있다. 1) 사모펀드인 아폴로 글로벌 매니지먼트(ApolloGlobal Management)에게 ACL과 Yahoo! 등이 포함된 Verizon Media가 매각된 후 사명을 이후로 변경했다. Modia ISSJP & Trend 84 2022.5x6.Vpl.50 [970 chars] |
| bigin의 가장 큰 차별점이 무엇이며, 이를 통해 어떤 이점을 얻을 수 있나요? [45 chars] | e-Commerce Solution BESPIN GLOBAL # 자동화 솔루션 # CRM마케팅 # 이커머스마케팅 # 마테크는_빅인 마케팅 자동화 솔루션 빅인 bigin Q. bigin은 어떤 들인가요? 어떤 점이 다른가요? A. 기존의 웹데이터 분석 둘은 단순히 데이터분석값만 제공하는 수준에 제한되었다면, bigin은 별도의 데이터팀의 도움없이도 데이터 열람뿐 아니라 원하는 데이터만 분류해서 마케팅목적에 맞게 캠페인이나 보고서 생성에 바로 활용할 수 있습니다. 반복적인 액션은 AI자동화로 셋팅해 둘수 있는 점도 큰 차별점입니다. 구매패턴 데이터를 확인하면서 최적화를 통해 더 나은 전환율도 기대할 수 있겠죠? Q 일단 사용해보고 싶은데 결제부터 해야하나요? A. 정식 빌링 전 기본 14일의 PoC(Proof of Concept)기간을 제공하며 사용하며 생기는 문의사항은 빅인 내 컨설턴트에게 문의할 수 있습니다. Q. 설치가 어렵지는 않나요? A. 웹사이트 내에 스크립트 삽입으로 간편하게 설치할 수 있으며 사용 웹사이트의 환경에 따라 (e.g. 호스팅몰) 셋팅환경이 더 간단하게 지원되기도 합니다. 기술적오류는 빅인 내부 기술지원팀에서 지원하고 있습니다. + 19 [600 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| AutoRAG: Automated Framework for optimization of Retrieval Augmented Generation Pipeline | 2024 | Paper | [https://arxiv.org/abs/2410.20878](https://arxiv.org/abs/2410.20878) |
| AutoRAG GitHub repository | 2024 | Repository | [https://github.com/Marker-Inc-Korea/AutoRAG](https://github.com/Marker-Inc-Korea/AutoRAG) |
| yjoonjang/markers_bm | 2025 | Dataset card | [https://huggingface.co/datasets/yjoonjang/markers_bm](https://huggingface.co/datasets/yjoonjang/markers_bm) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| 관세법 시행령의 권리사용료 관련 조건을 묻는 질문. | A Korean legal chunk discussing intangible rights, imported materials, and royalty relevance. |
| 미국 야후가 NFL 팬들을 위해 도입한 기능을 묻는 질문. | A trend-report chunk describing Yahoo Sports Watch Together and social viewing. |
| bigin의 차별점과 이점을 묻는 질문. | An e-commerce solution chunk about marketing automation and data selection. |
| 점포 내부 기둥이 어떤 요소에 영향을 미치는지 묻는 질문. | A court-document chunk discussing store columns, visibility, size, and placement. |
| 지방공공기관 구조개혁 계획과 부채관리 기준을 묻는 질문. | A public-sector report chunk on local public institution restructuring and debt management. |
