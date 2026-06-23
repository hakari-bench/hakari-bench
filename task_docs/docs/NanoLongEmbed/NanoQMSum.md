# NanoLongEmbed / NanoQMSum

## Overview

`NanoLongEmbed / NanoQMSum` is the QMSum meeting-transcript retrieval task in
LongEmbed. Queries are query-focused summaries or information needs about one
topic in a meeting, and documents are complete meeting transcripts. The model
must retrieve the transcript that supports the requested summary. The Nano
split has 200 queries, 197 documents, and one positive transcript per query.
Queries are relatively long, averaging 446.33 characters, while transcripts
average 53,335.82 characters and contain speaker labels, disfluencies, topic
shifts, and long turn-by-turn discussion. Current diagnostics show BM25 as the
strongest top-10 ranker, `reranking_hybrid` as intermediate, and dense retrieval
as much weaker for final top-10 ordering.

## Details

### What the Original Data Measures

QMSum was introduced as a query-based multi-domain meeting summarization
benchmark. It covers AMI product meetings, ICSI academic meetings, and
parliamentary committee meetings. The paper includes a locate-then-summarize
setup in which relevant utterances are found before generating a query-focused
summary.

LongEmbed adapts QMSum into long-context retrieval by using summaries or
information requests as queries and complete meeting transcripts as candidate
documents. The task therefore tests whether a retrieval model can identify the
meeting that contains the discussion supporting a topic-focused summary.

### Observed Data Profile

The Nano split contains 200 queries, 197 meeting transcripts, and 200 positive
qrel rows. Every query has exactly one positive, with no multi-positive
queries. Queries average 446.33 characters. Documents average 53,335.82
characters.

Representative queries summarize remote-control design decisions, COVID-19
parliamentary discussion, product evaluation outcomes, academic meeting updates,
and decisions about remote-control buttons. Documents contain speaker labels,
partial utterances, filler words, interruptions, and long conversations. The
query may summarize an outcome rather than repeat the exact transcript wording.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset covers the 197-document corpus and
achieves nDCG@10 = 0.7440, hit@10 = 0.8500, and recall@100 = 1.0000. BM25 is
the strongest observed profile for top-10 ranking and has complete top-100
coverage. Product names, agenda items, policy terms, named institutions, and
topic-specific words provide strong lexical anchors.

BM25 is not perfect because meeting summaries are abstractive. A query can
describe a decision or outcome using cleaner language than the transcript,
which may contain disfluencies and fragmented discussion. Still, in this Nano
split, lexical topic signals are strong enough that sparse retrieval is the
best final ranker among the observed profiles.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset covers the same 197 documents
and achieves nDCG@10 = 0.3660, hit@10 = 0.5450, and recall@100 = 0.9600. Dense
retrieval is much weaker in top-10 ordering, although it still keeps most
positives within the first 100. A single embedding for a full meeting transcript
can dilute the relevant agenda item among many unrelated turns.

Dense similarity may capture broad meeting domain or topic, but it appears less
effective at identifying the exact transcript from a query-focused summary.
Long multi-speaker conversations are difficult to compress into one vector
without losing specific decisions, speakers, or action items.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 1 safeguard positive row and a mean of 100.005 candidates. It
achieves nDCG@10 = 0.6097, hit@10 = 0.8000, and recall@100 = 0.9950. Hybrid
retrieval substantially improves over dense retrieval but remains below BM25 in
top-10 ranking and recall.

The hybrid result suggests that dense retrieval contributes some paraphrase and
summary-to-discussion matching, while BM25 contributes the strongest topic and
named-entity anchors. For reranking, the hybrid pool is useful, but a final
model must localize the relevant meeting segment rather than score the whole
meeting globally.

### Metric Interpretation for Model Researchers

This is a single-positive retrieval task. Hit@10 measures whether the correct
meeting appears in the first ten results, nDCG@10 rewards ranking it near the
top, and recall@100 measures whether candidate generation keeps it available
for reranking.

The metric pattern is important for long-context embedding research. Dense
retrieval is not enough when the relevant topic is a small part of a long
meeting. BM25 is strongest because topic-specific words survive in the
transcript, while hybrid retrieval gives a compromise between lexical anchoring
and semantic summary matching.

### Query and Relevance Type Tendencies

Queries are query-focused meeting summaries. They often describe decisions,
participant opinions, parliamentary explanations, project updates, or design
choices. Relevant documents are full meeting transcripts, not extracted
utterance spans.

The task rewards systems that can map summary language to disfluent spoken
conversation and preserve topic-level lexical cues across long transcripts. It
also tests whether a model can handle multi-domain meetings with very different
formats.

### Representative Failure Modes

BM25 can fail when the summary uses words that do not appear in the transcript
or when several meetings share the same product-design vocabulary. Dense
retrieval can fail by ranking a meeting with similar broad topic but different
agenda item. Hybrid retrieval can include the positive but still rank another
same-domain meeting above it.

Long transcript structure creates another failure mode: the relevant discussion
may occupy only a small portion of the document, while unrelated agenda items
dominate the global representation.

### Training Data That May Help

Useful training data includes non-overlapping QMSum train examples, meeting
summarization corpora with query or topic annotations, meeting transcript to
user-information-need retrieval pairs, and hard negatives from the same meeting
domain. Training should preserve speaker labels, disfluencies, topic shifts,
decisions, disagreements, and action items.

Comparable evaluation should exclude QMSum test data, Nano queries, qrels, and
positive meeting transcripts likely to overlap with this split.

### Model Improvement Notes

Dense retrievers can improve with segment-aware meeting representations,
hierarchical pooling, multi-vector indexes, or locate-then-rank training. Sparse
systems should preserve topic terms, participant names, institutions, product
features, and agenda language. Rerankers should inspect relevant utterance
clusters rather than relying on a full-transcript embedding.

For hybrid systems, `NanoQMSum` supports using BM25 for strong transcript
candidate generation and dense retrieval for abstractive summary phrasing.

## Example Data

| Query | Positive document |
| --- | --- |
| They felt that the battery design should be long-lived, original, and conventional to ensure the bat... [100 / 241 chars] | User Interface: .. . Project Manager: Okay . So , this is uh first meeting of this design project . Um and I um like to show you the agenda for the meeting , I don't know if it was sent round to all o... [200 / 22,629 chars] |
| The Prime Minister explained that the government recognized that several organizations and companies... [100 / 537 chars] | The Chair (Hon. Anthony Rota (NipissingTimiskaming, Lib.)): I call this meeting to order. Welcome to the 12th meeting of the House of Commons Special Committee on the COVID-19 Pandemic. This will be t... [200 / 120,229 chars] |
| In the product evaluation, the team was satisfied with its success in reducing the number of unused... [100 / 362 chars] | Project Manager: That should hopefully do the trick , um . 'Kay . Sorry about the small delay . Falling a little bit behind schedule . And that's uh fifteen twenty five . Okay . So just to try and rou... [200 / 43,300 chars] |
| Grad F explained that he was focusing on writing his proposal for his qualification exams, which was... [100 / 182 chars] | Professor B: I think for two years we were two months , uh , away from being done . PhD A: And what was that , Morgan ? What project ? Professor B: Uh , the , uh , TORRENT chip . PhD A: Oh . Professor... [200 / 56,387 chars] |
| The team agreed that there should be 17 buttons on the remote, including number 0 to 9, volume up an... [100 / 250 chars] | Project Manager: Right uh . So um . So where's the PowerPoint presentation ? Sorry ? Microsoft PowerPoint , right . Right , okay . So . Right . Okay , so we've got uh so we've got new project requirem... [200 / 43,476 chars] |

### Public Sources

- [QMSum: A New Benchmark for Query-based Multi-domain Meeting Summarization](https://arxiv.org/abs/2104.05938),
  2021.
- [LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096),
  2024.
- [dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed), source
  dataset card.
- [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| QMSum: A New Benchmark for Query-based Multi-domain Meeting Summarization | 2021 | arXiv paper | [https://arxiv.org/abs/2104.05938](https://arxiv.org/abs/2104.05938) |
| LongEmbed: Extending Embedding Models for Long Context Retrieval | 2024 | arXiv paper | [https://arxiv.org/abs/2404.12096](https://arxiv.org/abs/2404.12096) |
| dwzhu/LongEmbed | 2024 | dataset card | [https://huggingface.co/datasets/dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A query-focused summary about desired battery design properties for a remote control. | A product-design meeting transcript containing discussion of battery innovation and durability. |
| A summary of a parliamentary COVID-19 support-program exchange. | A House of Commons special committee transcript. |
| A summary of product-evaluation satisfaction and remaining design issues. | A design-team meeting transcript about remote-control interface evaluation. |
| A summary about a graduate student's proposal and qualification exam timeline. | An academic meeting transcript with participant updates. |
| A summary of agreed remote-control button layout. | A product meeting transcript discussing requirements and button choices. |
