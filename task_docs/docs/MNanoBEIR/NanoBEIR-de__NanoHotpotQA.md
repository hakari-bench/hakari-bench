# MNanoBEIR / NanoBEIR-de / NanoHotpotQA

## Overview

This task is the German NanoBEIR version of HotpotQA, a multi-hop question answering retrieval benchmark derived from Wikipedia-based questions that require connecting evidence across more than one passage. The original HotpotQA benchmark was introduced to test explainable multi-hop reasoning, especially cases where the answer cannot be supported by a single isolated paragraph. In the retrieval setting, the query is a natural-language German question and the system must retrieve German passages that contain the supporting facts needed to answer it. The NanoBEIR slice keeps 50 queries, 5,090 candidate passages, and exactly 100 positive relevance judgments, giving every query two relevant passages. This makes the task especially useful for diagnosing whether a retrieval model can surface complementary evidence rather than only the most lexically obvious paragraph. Because the passages are translations or multilingual adaptations of encyclopedic content, the task combines ordinary German question matching with named-entity grounding, entity linking, and bridge reasoning.

## Details

### What the Original Data Measures

HotpotQA-style retrieval measures whether a system can recover the pieces of evidence behind a compositional question. Many queries name one entity and ask for a fact that is only available after following a relationship to another entity, event, film, team, person, or organization. A strong retriever must therefore rank both the directly mentioned passage and the bridge or answer-bearing passage highly enough for a downstream reader to use them together. This differs from single-fact factoid retrieval, where one paragraph often contains all required answer information.

### Observed Data Profile

The NanoBEIR-de version contains 50 queries and 5,090 documents, with two positives for every query. The average query length is about 100 characters, but there is noticeable variation: short entity questions coexist with long descriptions containing dates, event locations, rankings, or multiple named entities. Documents average about 386 characters, so passages are generally compact but still long enough to include entity descriptions and contextual facts. The fixed two-positive structure is important: recall matters as much as first-hit ranking because retrieving only one supporting paragraph can leave the reasoning chain incomplete.

### BM25 Evaluation Profile

BM25 is strong on this task, with nDCG@10 of 0.790, Hit@10 of 0.980, and Recall@100 of 0.950. This profile reflects the lexical nature of many HotpotQA questions: entity names, dates, titles, locations, and descriptive nouns often appear directly in one or both relevant passages. German morphology and translated proper names can still create mismatch, but the task includes enough surface overlap that term frequency and exact phrase matching are highly competitive. BM25 is particularly effective when the query contains rare entities such as personal names, film titles, sports teams, or historical figures, because those terms sharply narrow the candidate space.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline reaches nDCG@10 of 0.739, Hit@10 of 0.940, and Recall@100 of 0.910. Dense retrieval captures paraphrase and semantic relatedness, which helps when the German query describes a relation instead of repeating a passage phrase exactly. However, it trails BM25 here, suggesting that the task rewards precise entity anchoring more than broad semantic similarity. Dense retrieval can also over-rank passages that are topically close to the question but do not provide one of the two required supporting facts. For multi-hop data, that distinction is important: a semantically related Wikipedia paragraph is not necessarily part of the gold reasoning path.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile gives the best top-10 ranking, with nDCG@10 of 0.794, Hit@10 of 1.000, and Recall@100 of 0.950. Its Recall@100 matches BM25, which indicates that the candidate pool is already largely defined by lexical coverage, but the hybrid ordering still improves early precision. This is the expected behavior for a task where exact entity matches and semantic bridge recognition both matter. BM25 contributes strong candidate discovery for names and rare terms, while dense similarity can promote passages that are phrased differently but still semantically central to the question. The result is not a wholesale replacement of BM25; it is a modest but useful reranking gain over a lexical candidate base.

### Metric Interpretation for Model Researchers

For this task, nDCG@10 should be read as a measure of whether both supporting passages appear early enough to be useful. Hit@10 is nearly saturated for BM25 and hybrid, so it is less discriminative than nDCG and Recall@100. Recall@100 remains important because downstream multi-hop readers need both evidence pieces, and missing one positive document can break answerability. A model that improves only the first relevant hit but fails to retrieve the second evidence paragraph is less useful than its Hit@10 score may suggest.

### Query and Relevance Type Tendencies

Queries often combine a named entity with a relation, for example asking which actor appeared with another actor, who received a sword made by a specific school founder, or which film connects a writer-director with a composer. The relevant documents may include one passage about the query entity and another about the answer or bridge entity. This makes the task sensitive to cross-passage entity linking, translated name variants, and the ability to keep multiple constraints active at once.

### Representative Failure Modes

Lexical systems can miss relevant passages when the answer-bearing page does not repeat the query wording or when translation changes a relation phrase. Dense systems can retrieve thematically adjacent pages that share the same domain but are not the required supporting evidence. Hybrid systems reduce both risks, but can still fail when neither the lexical nor dense candidate pool includes the second support passage within the top 100. Because there are exactly two positives per query, these failures are easy to inspect manually.

### Training and Leakage Considerations

Training examples should exclude HotpotQA, BEIR, NanoBEIR, and derivative multilingual HotpotQA conversions when evaluating this task. Useful non-overlapping training data can include German Wikipedia entity pairs, manually written bridge questions, and multi-document QA data that explicitly labels supporting passages. The most important supervision pattern is not just question-to-answer similarity, but question-to-evidence-chain retrieval.

### Model Improvement Signals

Improvements on this task are likely to come from better German entity normalization, multilingual Wikipedia pretraining, hard negatives that are topically related but not supporting evidence, and training objectives that reward recovering multiple complementary positives. Dense models should avoid collapsing the two-hop structure into broad topical similarity. Sparse and hybrid systems should preserve rare entity terms while still recognizing paraphrased relation descriptions.

## Example Data

| Query | Positive document |
| --- | --- |
| Mit welchem anderen Schauspieler spielte Penny Rae Bridges in einer Fernseh-Sitcom? [83 chars] | Penny Rae Bridges (geboren am 29. Juli 1990) ist eine amerikanische Schauspielerin. Sie hat in folgenden Serien mitgespielt: "For Your Love", "Family Law", "Boy Meets World" und "The Parent 'Hood". Bekannt wurde sie durch ihre Rolle in "Half & Half" als die junge Mona. [269 chars] |
| Wer hat Kaganoi Shigemochi ein Schwert überreicht, das vom Gründer der Muramasa-Schule hergestellt wurde? [105 chars] | Kaganoi Shigemochi (加賀井 重望, 1561 – 27. August 1600) war ein japanischer Samurai der Azuchi-Momoyama-Zeit, der dem Oda-Clan diente. Er herrschte über die Burg Kaganoi. Während der Schlacht von Komaki und Nagakute kämpfte Shigemochi unter seinem Vater Shigemune, der den Truppen von Oda Nobukatsu angehörte. Bald darauf wurde die Burg Kaganoi von den Truppen von Toyotomi Hideyoshi umzingelt; Shigemune ergab sich, und Shigemochi wurde von Hideyoshi als Bote angestellt und erhielt eine Pension von 10.000 'Koku'. Er besaß auch ein Schwert, das von Muramasa gefertigt wurde und das Hideyoshi ihm 1598 überreichte. [611 chars] |
| Welcher Film wurde von Joby Harold geschrieben und inszeniert und hat Musik von Samuel Sim? [91 chars] | Samuel Sim ist ein Film- und Fernsehkomponist. Er erlangte erstmals Anerkennung durch seine preisgekrönte Filmmusik zur BBC-Dramaserie "Dunkirk". Seitdem hat er die Musik für eine Vielzahl von Film- und Fernsehproduktionen komponiert, zuletzt den Film "Awake" für The Weinstein Company und die BBC/HBO-Dramaserie "House of Saddam". Seine jüngste gefeierte Musik ist der Soundtrack zu "Home Fires". "Home Fires (Music from the Television Series)" wurde am 6. Mai 2016 von Sony Classical Records veröffentlicht. [509 chars] |

## Public Sources

- [HotpotQA paper](https://arxiv.org/abs/1809.09600)
- [HotpotQA official site](https://hotpotqa.github.io/)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://github.com/embeddings-benchmark/mteb)
- [NanoBEIR dataset](https://huggingface.co/datasets/zeta-alpha-ai/NanoBEIR)

## Source Reference Table

| Label | URL |
|---|---|
| HotpotQA paper (https://arxiv.org/abs/1809.09600) |
| HotpotQA official site (https://hotpotqa.github.io/) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://github.com/embeddings-benchmark/mteb) |
| NanoBEIR dataset (https://huggingface.co/datasets/zeta-alpha-ai/NanoBEIR) |
