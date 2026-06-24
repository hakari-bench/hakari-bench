# NanoJMTEB-v2 / ja_gov_faqs

## Overview

`NanoJMTEB-v2 / ja_gov_faqs` is the Nano split of JaGovFaqs-22k, a Japanese
government FAQ retrieval task. The query side contains formal FAQ questions
from Japanese government and bureau websites, and the corpus side contains the
corresponding answer passages mixed with other FAQ answers. The task tests
question-to-answer retrieval in public-administration language: policies,
applications, fees, regulations, institutional procedures, and official support
responses. In the Nano split, there are 200 queries, 10,000 documents, and one
positive answer per query. The current diagnostics show a balanced retrieval
profile: BM25 is reasonably strong, dense retrieval is slightly stronger at
top-10 ranking, and the reranking hybrid profile gives the best observed
nDCG@10, hit@10, and recall@100.

## Details

### What the Original Data Measures

The JMTEB dataset card describes JaGovFaqs-22k as a collection of Japanese FAQs
manually extracted from bureau and government websites. Questions are treated
as retrieval queries, and their matching FAQ answers are treated as relevant
documents. This differs from web-page search tasks: the relevant item is not a
source page or title snippet, but an answer passage that may be short, formal,
and dependent on the wording of the original question.

The task therefore measures how well a model connects official Japanese
question language to administrative answer language. Many pairs involve
procedures, eligibility, forms, fees, application timing, legal categories, or
public-service operations. Answers may not repeat the full question. Some are
terse, some reference documents or schedules, and some give procedural
conditions that only become clear when paired with the question.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel
rows. Every query has exactly one positive answer, with no multi-positive
queries. Queries average 59.97 characters, making them longer than many
web-search queries in other Nano tasks. Documents average 193.38 characters and
range from brief direct answers to multi-sentence administrative explanations.

Representative topics include student financial support after household-income
changes, how public research institutions should fill in application fields,
fees for disclosure requests, installation behavior of government software, and
recent radioactive inspection results. These examples show the corpus's formal
register: even when the answer is short, the retrieval decision often depends
on official terminology and procedural context.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.7196, hit@10 = 0.8250, and recall@100 = 0.9250. BM25 is
not weak on this task: many government FAQ questions share important legal,
procedural, or form names with their answers, and exact terms are useful.
However, BM25 does not reach full top-100 coverage, and its top-10 ranking is
below both dense retrieval and the reranking hybrid profile.

The BM25 pattern suggests that lexical overlap is important but incomplete.
Administrative answers often omit the full question wording, replace the user's
question form with an institutional answer form, or answer with a compact
condition such as whether something is possible. When the answer contains rare
tokens from the question, BM25 works well. When the answer expresses the same
procedure with different official phrasing, lexical matching alone is less
reliable.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset also contains 500 candidates
per query. It achieves nDCG@10 = 0.7487, hit@10 = 0.8350, and recall@100 =
0.9050. Dense retrieval has slightly better top-10 quality than BM25, which
fits the task's question-answer structure. Embedding similarity can connect a
formal question to a concise answer even when the answer does not repeat all of
the query's surface words.

The tradeoff is lower recall@100 than BM25. Dense retrieval appears better at
placing many positives near the top, but it misses a few more positives from
the first 100 candidates. For researchers, this indicates a task where semantic
matching improves ranking quality, while exact administrative terminology still
matters for candidate coverage. A dense model that ignores statute names,
system names, form labels, or fee terms may lose candidates that BM25 can keep.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 9 safeguard positive rows and a mean of 100.045 candidates. It
achieves nDCG@10 = 0.7614, hit@10 = 0.8700, and recall@100 = 0.9550. This is
the best of the observed profiles across top-10 ranking and candidate coverage.

The result is a clear example of hybrid search providing complementary value.
BM25 contributes official lexical anchors such as application names, fee terms,
and legal expressions. Dense retrieval contributes question-answer semantic
matching when the answer is phrased differently from the query. The hybrid
candidate set combines these strengths, improving recall beyond both individual
profiles and giving the best top-10 placement. For reranking experiments, this
task is well suited to testing whether a model can jointly use exact procedural
terms and answer-intent similarity.

### Metric Interpretation for Model Researchers

With one positive answer per query, hit@10 measures whether the correct FAQ
answer appears in the first ten results, while nDCG@10 rewards placing that
answer closer to rank 1. Recall@100 is especially important for reranking
pipelines because it tells whether the positive answer survives candidate
generation.

The metrics show that `ja_gov_faqs` is neither a pure lexical task nor a pure
semantic paraphrase task. Dense retrieval is slightly better than BM25 for
top-10 ranking, but the hybrid profile is stronger than both. This makes the
task useful for evaluating Japanese retrieval systems that combine sparse,
dense, and reranker stages rather than only measuring one retrieval family in
isolation.

### Query and Relevance Type Tendencies

Queries are formal Japanese FAQ questions. They frequently ask whether an
action is possible, what fee or procedure is required, how to fill out a field,
or where to find recent official results. The positive document is the matching
answer, not a broader page. That answer may be long and explanatory, but it can
also be a compact response that relies on the question for context.

This setup rewards models that understand Japanese administrative register,
question-answer entailment, and precise procedural terminology. It is also a
good diagnostic for whether a model can handle relatively long Japanese queries
without losing the decisive terms inside them.

### Representative Failure Modes

BM25 can fail when the answer does not reuse the query's wording, or when many
FAQ answers share the same government program names and procedural vocabulary.
Dense retrieval can fail when a semantically plausible answer belongs to a
different procedure, deadline, or institution. Hybrid retrieval reduces these
risks but still needs a reranker that can distinguish subtle official contexts.

Common error patterns include confusing related application processes, matching
on generic administrative words such as "application" or "procedure", and
ranking a broad explanatory answer above the exact answer tied to the FAQ
question.

### Training Data That May Help

Useful training data would include Japanese FAQ question-answer pairs,
government help-center retrieval data, administrative procedure QA, legal and
policy retrieval pairs, and hard negatives from similar agencies or related
procedures. It is important to preserve real answer brevity and official
wording. Training data where every answer restates the whole question would not
match this benchmark well.

Training and hard-negative mining should exclude the evaluation pairs from
JaGovFaqs, JMTEB, and the Nano split when reporting comparable benchmark
results.

### Model Improvement Notes

Dense retrievers can improve by learning stronger alignment between formal
questions and compact official answers, while preserving exact Japanese entity
and procedure names. Sparse systems can benefit from better Japanese
tokenization and careful handling of compound administrative terms. Rerankers
should compare the full question to the answer's procedural conditions rather
than relying only on overlapping nouns.

For production-style retrieval systems, this task suggests that hybrid search
is a sensible default for Japanese government FAQ retrieval. Exact terminology
and semantic answer matching both matter, and the current `reranking_hybrid`
profile reflects that combination.

## Example Data

| Query | Positive document |
| --- | --- |
| 入学後に家計が苦しくなった場合、後から申し込むことは可能ですか。 [32 chars] | 入学後に申し込むことも可能です。災害や生計維持者（父母等）の死亡などの予期できない事情があって家計が急変した場合には、特例的に、随時申込みを受け付け、急変後の所得に基づいて要件を満たすかどうかを判定し、支援対象とします。（資料７参照）（大学等の事務担当者におかれては、「授業料等減免事務処理要領」及びJASSOからの案内を御確認 の上、学生等の相談に応じていただけるよう、お願いします。） [194 chars] |
| 公的研究機関の場合、「事情」欄はどのように記載すればよいですか。 [32 chars] | 出願人が研究所の場合は、「出願人○○は公的研究機関である」と記載してください。なお、出願人が都道府県名等であって、当該研究所名と異なる場合は、ガイドラインのII. 5.（1）②の記載を参考にしてください。 [102 chars] |
| どのような手数料が必要ですか。 [15 chars] | 法人文書の開示にあたっては、情報公開法の規定による「開示請求手数料」および「開示実施手数料」の納付が必要です。開示請求手数料は、法人文書1件について300円の納付が必要です。開示実施手数料は、文書の種類、開示の実施方法、開示文書の量等により計算した額から開示請求の際に納付された300円を減額した額が納付する額となります。納付する開示実施手数料の額は、開示決定通知書に記載しお知らせします。 [195 chars] |

### Public Sources

- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB),
  source card describing JaGovFaqs-22k.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316),
  2022.
- [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2),
  Nano benchmark dataset.
- [mteb/JaGovFaqsRetrieval](https://huggingface.co/datasets/mteb/JaGovFaqsRetrieval),
  source task dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| sbintuitions/JMTEB | 2024 | dataset card | [https://huggingface.co/datasets/sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB) |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A question asking whether a student can apply after household finances become difficult after enrollment. | An answer explaining that later application is possible and describing special handling for sudden household-income changes. |
| A question about what to write in an application field for a public research institution. | An answer instructing the applicant to state that the institution is a public research organization. |
| A question asking what fees are required. | An answer describing disclosure request fees and disclosure implementation fees under information-disclosure procedures. |
| A question asking whether the installation drive for an application tool can be changed. | A short answer saying the tool installs to the default system drive and the destination cannot be changed. |
| A question asking for recent radioactive inspection results. | A compact answer stating that items exceeding strict standard values have been rare in recent years. |
