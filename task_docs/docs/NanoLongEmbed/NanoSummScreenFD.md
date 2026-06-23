# NanoLongEmbed / NanoSummScreenFD

## Overview

`NanoLongEmbed / NanoSummScreenFD` is the ForeverDreaming subset of SummScreen
as used in LongEmbed. Queries are human-written TV episode recaps, and
documents are long screenplay-style transcripts. The retrieval goal is to find
the episode transcript whose dialogue and scene actions correspond to the
recap. The Nano split has 200 queries, 336 documents, and one positive
transcript per query. Queries average 600.67 characters, and documents average
30,854.33 characters. Current diagnostics are high across all methods, with
BM25 nearly saturated, `reranking_hybrid` second, and dense retrieval close but
lower.

## Details

### What the Original Data Measures

SummScreen was introduced as an abstractive screenplay summarization dataset
pairing TV transcripts with episode recaps. The paper notes that important plot
details may be communicated indirectly through dialogue, that many transcript
lines are not central to the plot, and that parallel subplots can be separated
by scene breaks.

LongEmbed adapts SummScreenFD into retrieval by using the recap as the query
and full episode transcripts as candidate documents. The task therefore tests
whether a model can match a concise plot summary to a long, dialogue-heavy
transcript.

### Observed Data Profile

The Nano split contains 200 recap queries, 336 transcript documents, and 200
positive qrel rows. Every query has exactly one positive, with no multi-positive
queries. Queries average 600.67 characters. Documents average 30,854.33
characters.

Representative examples come from shows such as Buffy the Vampire Slayer, One
Tree Hill, Charmed, Frasier, and Roswell. The queries mention characters,
conflicts, supernatural events, relationships, episode outcomes, and major plot
points. Transcripts contain dialogue, speaker names, scene labels, and action
descriptions.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset covers the 336-document corpus and
achieves nDCG@10 = 0.9813, hit@10 = 1.0000, and recall@100 = 1.0000. BM25 is
near ceiling. Recaps contain many character names, show-specific terms, event
phrases, and episode-specific details that also appear in the transcript.

The task is long-document retrieval, but not lexically sparse. A recap often
names the main characters and conflict directly, making exact matching very
powerful. Remaining difficulty is mostly distinguishing adjacent or same-show
episodes where recurring character names and settings overlap.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset covers 336 documents per query
and achieves nDCG@10 = 0.9198, hit@10 = 0.9600, and recall@100 = 0.9700. Dense
retrieval is strong, but below BM25. It can match paraphrased plot summaries to
dialogue-heavy transcripts, but it may blur specific episode identity when
several episodes share characters and themes.

This pattern shows that semantic plot similarity is useful but insufficient.
In this split, exact character names, episode-specific events, and rare
phrases provide the clearest evidence for the correct transcript.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.9443, hit@10 = 0.9700,
and recall@100 = 1.0000. Hybrid retrieval improves over dense retrieval and
matches BM25's full recall@100, but it does not surpass BM25's top-10 ranking.

Hybrid search is still useful because it combines exact recap terms with
semantic plot matching. However, BM25's near-ceiling result indicates that the
lexical side already captures most episode identity cues. A reranker should
focus on verifying the episode-specific event sequence rather than broad show
or character similarity.

### Metric Interpretation for Model Researchers

This is a single-positive retrieval task. Hit@10 measures whether the correct
episode transcript appears in the top ten, nDCG@10 rewards placing it near the
top, and recall@100 measures whether candidate generation keeps it available.

The metric pattern shows a high lexical-overlap long-document task. BM25 is the
best observed profile, hybrid is second, and dense is strong but lower. This
task is useful for testing whether long-document representations preserve
names, scenes, and episode-specific events.

### Query and Relevance Type Tendencies

Queries are recap-like summaries that name characters, conflicts, decisions,
and outcomes. Documents are long TV transcripts with speaker labels, scene
breaks, dialogue, and action descriptions. The positive transcript may contain
the relevant evidence across multiple scenes rather than one contiguous span.

The task rewards models that can connect plot summaries to dialogue and scene
structure. It also tests whether a model can distinguish episodes from the same
show with shared recurring vocabulary.

### Representative Failure Modes

BM25 can fail when multiple episodes share characters, settings, and recurring
phrases. Dense retrieval can fail by ranking another episode with similar plot
themes or character relationships above the exact recap match. Hybrid retrieval
can include the correct transcript but still require event-level reranking.

Long-document issues remain relevant: important recap events may be distributed
across scenes, while large sections of dialogue do not matter for the summary.

### Training Data That May Help

Useful training data includes non-overlapping SummScreen train examples, TV
recap-to-transcript retrieval pairs, long dialogue summarization pairs, and
adjacent-episode hard negatives from the same show. Training should preserve
speaker labels, scene breaks, recurring character names, and parallel subplots.

Comparable evaluation should exclude SummScreenFD evaluation examples, Nano
queries, qrels, and positive transcripts likely to overlap with this task.

### Model Improvement Notes

Dense retrievers can improve by preserving exact character and episode-event
signals while still matching abstractive recap language. Sparse systems already
perform near ceiling, but should handle names, capitalization, and script
formatting robustly. Rerankers should compare recap events with transcript
scenes, especially for same-show hard negatives.

For hybrid systems, `NanoSummScreenFD` is a high-ceiling calibration task:
semantic retrieval helps, but exact plot and character terms are usually the
strongest signals.

## Example Data

| Query | Positive document |
| --- | --- |
| Angel decides to do the right thing and break up with Buffy. Meanwhile, Buffy has to save the prom from Hellhounds with a fetish for formal wear. Angel shows up for the last dance. [180 chars] | Buffy is napping in Angel's bed. Angel is watching her sleep. He smiles at her as she wakes. Buffy: (smiles) What? Do I have funny bed hair or something? Angel: Or something? Buffy: I guess we got a little carried away with the whole post-slayage nap thing. (feels her hair) Ohhh, not good. (sits up) Angel: Where you going? Buffy: To go kill a cat on my head. Angel: No mirrors. Buffy: You know, this place really isn't girl-friendly. No mirrors, no natural light. Angel: I think you look perfect. Buffy: Oh yeah, I really like... Okay! (lays down) Maybe we should think about getting a few mirrors. And maybe a drawer, you know, for some of my stuff. Because that's what couples do, they have drawers. Angel: Mmmm, that's right. Buffy: You know, I-I figure, that way sometimes I could spend the night. Like, after the prom, it would be nice to be able to just come back here and spend some time together. Angel: The prom? Buffy: End of high school rite of passage thingy. Think cotillion with spike... [1,000 / 31,147 chars] |
| Whilst Haley cares for their new daughter, Lydia, Nathan confronts Professor Kellerman (guest star Peter Riegert) about the accident. Meanwhile Quinn organizes a concert at Tric and Brooke gets an offer to return to Clothes Over Bro's as vice president. Skills and Mouth help Millie think of a story for her to cover and focus on the river court which is about to be destroyed. This episode is named after a song by The Belle Brigade . Opening theme song performed by Lucero . [476 chars] | [PREVIOUSLY_ON] IAN: What the hell? I knew you guys couldn't be complete dorks. CLAY: Complete dorks and officially your agents. NATHAN: You got a bathroom in this place? IAN: There's one in the back of the house passed the kitchen. BROOKE: Julian! CHLOE: I want two people who are gonna love this baby, and that's the reason why I want you guys to be the parents. BROOKE: Well, since we don't know the s*x, I like yellow. Julian likes green. JULIAN: She just changed her mind, Brooke. She held her in her arms, and she just couldn't go through with it. HALEY: Quinn? It's time. NATHAN: It's a girl. QUINN: Yay! HALEY: This is Lydia Bob Scott. NALEY'S HOUSE Haley puts Lydia in her crib. BRULIAN'S HOUSE Brooke arranges the businesses of the baby. KELLERMAN'S HOUSE Nathan, Julian and Clay looks at car which is the garage. NATHAN: Was that the car from the bridge that night? FLASHBACK, GABEL BRIDGE JULIAN: No, stop! Stop! Stop! BROOKE: Julian! JULIAN: No, Brooke! CLAY'S CAR Julian is with Clay. J... [1,000 / 26,247 chars] |
| Led by Prue, the Charmed Ones help a young man named Brendan ( Michael Weatherly ) who wants to become a priest in order to avoid fulfilling his predicted destiny as a warlock along with his brothers. They begin attacking people who are close to Brendan in order to coerce him to give into his darker side. Eventually, his brothers kill each other and he becomes ordained as a priest and cleared of the attacks on innocents and an esteemed priest. [447 chars] | [Scene: Church. Brendan and a priest are there.] Brendan: I wake up at night, my heart pounding, a voice whispering in my head your a fraud, you can't fool God. Priest: These are not new fears, Brendan. I've watched you grow, wept for you, rejoiced in you, you are not a fraud. I know your heart. Brendan: You don't know my family, father. Generations of evil. Evil that's in my blood. Priest: The blood of the sacrament washes it clean. Greg: Hello, Brendan. Paul: Long time no see. Brendan: How'd you find me? Greg: Yeah, good to see you too. Didn't mean to interrupt your conversation. We'll wait outside for you so we can have a family reunion. [Scene: Outside the church. Prue, Phoebe and Piper are getting stuff out of the van.] Prue: Hey, you know what? The next time the Quake does a food pantry why don't you call some guys. Piper: Yeah, I'll just go through my handy guy rolodex. Phoebe: Which I believe now stops a 'J' for Josh or is it 'B' for boyfriend. Piper: I don't wanna talk about i... [1,000 / 31,115 chars] |

### Public Sources

- [SummScreen: A Dataset for Abstractive Screenplay Summarization](https://arxiv.org/abs/2104.07091),
  2022.
- [LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096),
  2024.
- [dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed), source
  dataset card.
- [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SummScreen: A Dataset for Abstractive Screenplay Summarization | 2022 | arXiv paper | [https://arxiv.org/abs/2104.07091](https://arxiv.org/abs/2104.07091) |
| LongEmbed: Extending Embedding Models for Long Context Retrieval | 2024 | arXiv paper | [https://arxiv.org/abs/2404.12096](https://arxiv.org/abs/2404.12096) |
| dwzhu/LongEmbed | 2024 | dataset card | [https://huggingface.co/datasets/dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A recap about Angel deciding to break up with Buffy and Hellhounds threatening prom. | The Buffy episode transcript with Angel and Buffy dialogue and prom plot scenes. |
| A recap about Haley, Nathan, Professor Kellerman, Quinn, and Brooke. | A One Tree Hill transcript containing those concurrent storylines. |
| A recap about the Charmed Ones helping Brendan avoid his warlock destiny. | A Charmed transcript with church scenes, Brendan, and related supernatural conflict. |
| A recap about Frasier's recurring erotic dream involving Gil Chesterton. | A Frasier transcript structured by acts and scenes. |
| A recap about the Skins making humans disappear in Roswell. | A Roswell transcript with episode title, scene breaks, and related dialogue. |
