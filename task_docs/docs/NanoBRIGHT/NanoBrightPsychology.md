# NanoBRIGHT / NanoBrightPsychology

## Overview

NanoBrightPsychology is the Psychology StackExchange slice of NanoBRIGHT. Queries are user posts about psychology, perception, cognition, behavior, emotion, social interaction, or research methods, and relevant documents are passages that support answers to those posts. The task is useful for evaluating retrieval systems on lay-to-scientific concept matching: a user may describe a phenomenon in everyday language, while the supporting source may use formal psychological terminology.

## Details

### What the Original Data Measures

BRIGHT's StackExchange tasks treat retrieval as source-support search. A post title and body form the query, and positives are cited or validated sources from answers. In Psychology, relevant passages can define a construct, describe an experiment, summarize a cognitive mechanism, or provide evidence for a behavioral explanation.

The task is not simple fact lookup. Many queries ask for the name of a phenomenon, a mechanism behind a behavior, or literature that supports a subjective observation. Relevance depends on whether the passage supports the specific psychological explanation, not merely whether it mentions broad terms such as attention, memory, emotion, or behavior.

### Observed Data Profile

The task contains 101 queries, 10,000 documents, and 692 relevance judgments. It is moderately multi-positive: there are 6.85 positives per query on average, a minimum of 1, a median of 3.0, a maximum of 54, and 66 multi-positive queries, or 65.35% of the set.

Queries average 693.16 characters and often contain a concrete scenario plus a request for a term or explanation. Documents average 504.47 characters and include research-related passages, reference excerpts, encyclopedia-like pages, and explanatory psychology text.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2474, hit@10 of 0.4653, and recall@100 of 0.3829 using the top-500 BM25 candidate subset. Lexical matching works when the query already includes the formal term, a named construct, or distinctive words from the source.

The limitation is that many psychology questions begin from everyday descriptions. A query may describe "knowing what you mean but being unable to explain it" or "being unable to see beyond the current emotional state," while the relevant passage may use terms such as mental block, flow, attention seeking, or hot-cold empathy gap. BM25 struggles when the formal construct is absent from the query.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4591, hit@10 of 0.6634, and recall@100 of 0.6329. Dense retrieval is the strongest profile for nDCG@10 and recall@100, and it ties reranking_hybrid for hit@10.

This is a clear dense-favorable task. Embedding similarity helps bridge lay descriptions and formal psychology language. It can connect a scenario, feeling, or behavioral pattern to the source passage that names the construct or explains the mechanism, even when exact words do not overlap.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4124, hit@10 of 0.6634, and recall@100 of 0.5853. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 11 safeguard rows, candidate counts from 100 to 101, and a mean of 100.11 candidates.

Hybrid retrieval improves substantially over BM25 and matches dense hit@10, but dense remains better for nDCG@10 and recall@100. The hybrid pool is still useful for reranking because it keeps exact terms and formal labels when they appear, but the overall task trend is semantic rather than lexical.

### Metric Interpretation for Model Researchers

This task is a strong example of dense retrieval outperforming BM25 because relevance often requires conceptual paraphrase. BM25 finds passages when formal terms are shared; dense retrieval finds passages when the query describes the phenomenon indirectly. Reranking_hybrid adds sparse anchors but does not surpass dense on ranking quality.

Researchers should focus on whether a model retrieves explanatory support rather than merely same-topic psychology text. A top result should name or substantiate the mechanism needed for the user's question. Because many queries have multiple positives, recall@100 is also important for downstream answer generation or reranking.

### Query and Relevance Type Tendencies

Queries ask about extreme views becoming normalized, flow-like experience, mental blocks, attention-seeking behavior, empathy gaps, perception, cognition, and research terminology. Positive passages may come from psychology articles, reference pages, research explanations, or popular-science summaries grounded in psychological constructs.

The relevance relation is often term discovery or mechanism support. A relevant passage may provide the name of a phenomenon, describe the cognitive state, or offer evidence that helps answer a user's scenario.

### Representative Failure Modes

Likely failures include retrieving broad pages about emotion or attention that do not explain the specific phenomenon, missing formal terminology when the query uses lay phrasing, over-ranking popular articles with similar words but weak support, and confusing adjacent constructs such as attention, motivation, flow, and empathy.

BM25 is vulnerable to vocabulary mismatch. Dense retrieval can over-match broad conceptual similarity without enough evidence specificity. Hybrid retrieval can help when formal terms appear, but it still needs a reranker that distinguishes explanatory support from topical relatedness.

### Training Data That May Help

Useful training data includes non-overlapping Psychology StackExchange posts with cited sources, psychology QA with references, paper-to-question retrieval pairs, and hard negatives about the same construct but a different mechanism or measurement.

Synthetic data should generate realistic user descriptions of psychological experiences and pair them with passages that name the relevant construct, experiment, or measure. Hard negatives should share broad terms such as attention, perception, addiction, emotion, or memory while failing to support the specific explanation.

### Model Improvement Notes

Strong models should bridge everyday language and formal psychology terminology. Dense retrieval is the strongest observed first-stage method, so training should emphasize paraphrase, scenario-to-construct mapping, and source-backed explanation. Sparse features remain useful for named constructs, experiments, and measurement terms.

The observed scores suggest that reranking_hybrid is useful but not sufficient to beat dense retrieval. A good reranker should judge whether the source passage actually supports the described phenomenon, not merely whether it is about psychology.

## Example Data

| Query | Positive document |
| --- | --- |
| Asking for illogical things to make extreme views normal? A couple of months back I was reading an article about how politicians were asking to make decisions that are way beyond possible (name it unreasonable, unacceptable, illogical) just as a medium of getting extreme views to become (to be seen as) normal and/or acceptable. What is the name of this effect? [363 chars] | **Share** All sharing options for: How Trump makes extreme things look normal * [ Reddit ](https://reddit.com/submit?title=How+Trump+makes+extreme+things+look+normal&url=https%3A%2F%2Fwww.vox.com%2F2017%2F12%2F21%2F16806676%2Fstrikethrough-how-trump-overton-window-extreme-normal) * [ Pocket ](https://getpocket.com/save?url=https%3A%2F%2Fwww.vox.com%2F2017%2F12%2F21%2F16806676%2Fstrikethrough-how-trump-overton-window-extreme-normal) * [ Flipboard ](https://share.flipboard.com/bookmarklet/popout?title=How+Trump+makes+extreme+things+look+normal&url=https%3A%2F%2Fwww.vox.com%2F2017%2F12%2F21%2F16806676%2Fstrikethrough-how-trump-overton-window-extreme-normal&v=2) * [ Email ](mailto:?subject=How%20Trump%20makes%20extreme%20things%20look%20normal&body=Why%20we%20should%20worry%20about%20the%20%22Overton%20Window%22%0A%0Ahttps%3A%2F%2Fwww.vox.com%2F2017%2F12%2F21%2F16806676%2Fstrikethrough-how-trump-overton-window-extreme-normal) “Don’t normalize this” has become a kind of rallying cry during... [1,000 / 2,714 chars] |
| What term can describe the feeling that a job just does itself? Is there a term that can describe that a job, however exhausting it might be, just does itself? Meaning, for example, that all doubt concerning how you're doing a job, whether or not you should do the job instead of something else, or any doubt of the value you're creating is just not there? As an example, I saw an interview where an author was asked how much effort it took to write a particular book. The answer was "No effort at al... [500 / 943 chars] | Challenges to maintaining flow [ [ edit ](/w/index.php?title=Flow_\(psychology\)&action=edit&section=10 "Edit section: Challenges to maintaining flow") ] Some of the challenges to staying in flow include states of [ apathy ](/wiki/Apathy "Apathy") , [ boredom ](/wiki/Boredom "Boredom") , and [ anxiety ](/wiki/Anxiety "Anxiety") . The state of apathy is characterized by easy challenges and low skill level requirements, resulting in a general lack of interest in the activity. Boredom is a slightly different state that occurs when challenges are few, but one's skill level exceeds those challenges causing one to seek higher challenges. A state of anxiety occurs when challenges are high enough to exceed perceived skill level, causing distress and uneasiness. These states in general prevent achieving the balance necessary for flow. [34] Csíkszentmihályi has said, "If challenges are too low, one gets back to flow by increasing them. If challenges are too great, one can return to the flow stat... [1,000 / 1,037 chars] |
| What is the term for the "knowing what you think but can't explain it" phenomenon? I think we all experience this phenomenon once in a while, and I am experiencing it right now. It's the feeling that whatever word one tries to say it seems to be wrong (for them) or confusing (for the listeners), and would require a period of time to think out the right word that they have already known. If severed, it can lead to frustration, but it's not really about feeling insecurity. What is the word for tha... [500 / 504 chars] | sitelinks- wikipedia "Edit interlanguage links") * [ Article ](/wiki/Mental_block "View the content page \[c\]") * [ Talk ](/wiki/Talk:Mental_block "Discuss improvements to the content page \[t\]") English * [ Read ](/wiki/Mental_block) * [ Edit ](/w/index.php?title=Mental_block&action=edit "Edit this page \[e\]") * [ View history ](/w/index.php?title=Mental_block&action=history "Past revisions of this page \[h\]") Tools Tools move to sidebar hide Actions * [ Read ](/wiki/Mental_block) * [ Edit ](/w/index.php?title=Mental_block&action=edit "Edit this page \[e\]") * [ View history ](/w/index.php?title=Mental_block&action=history) General * [ What links here ](/wiki/Special:WhatLinksHere/Mental_block "List of all English Wikipedia pages containing links to this page \[j\]") * [ Related changes ](/wiki/Special:RecentChangesLinked/Mental_block "Recent changes in pages linked from this page \[k\]") * [ Upload file ](/wiki/Wikipedia:File_Upload_Wizard "Upload files \[u\]") * [ Special pages... [1,000 / 3,508 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BRIGHT](https://arxiv.org/abs/2407.12883) |
| Project page | [BRIGHT project page](https://brightbenchmark.github.io/) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| NanoBRIGHT dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| What is it called when extreme claims make extreme views seem normal? | A source discusses how repeated extreme statements can shift what looks normal. |
| What term describes work that seems to do itself despite effort? | A reference passage describes flow and challenges to maintaining that state. |
| What is the term for knowing what you mean but being unable to explain it? | A page about mental blocks discusses difficulty accessing or expressing thought. |
| Why would someone say shocking things to enjoy others' reactions? | A passage discusses attention-seeking behavior and how it can develop. |
| What is the term for being unable to see beyond one's current emotional state? | A reference page discusses the hot-cold empathy gap. |
