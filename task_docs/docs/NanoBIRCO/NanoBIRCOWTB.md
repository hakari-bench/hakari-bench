# NanoBIRCO / NanoBIRCOWTB

## Overview

NanoBIRCOWTB is a compact Nano task derived from BIRCO's WhatsThatBook retrieval setting. Each query is an informal memory post where a user describes a half-remembered book, and the corpus contains book descriptions. The retrieval goal is to find the one book description that holistically matches the remembered clues. This makes the task useful for evaluating tip-of-the-tongue retrieval, noisy long-query matching, multi-clue reasoning, and book recommendation under uncertainty.

## Details

### What the Original Data Measures

BIRCO describes WhatsThatBook as a literature retrieval task with complex user descriptions. The user may remember plot fragments, cover details, approximate dates, genre, character relationships, and uncertain or incorrect details. The relevant passage is the book description that best matches the whole memory.

This is not simple title or keyword lookup. A query can include many weak clues, and any one clue may be wrong or ambiguous. The model must weigh the combination of details rather than overfitting to a single remembered phrase.

### Observed Data Profile

The task contains 100 queries, 1,766 documents, and 100 relevance judgments. Every query has exactly one positive book description, so the positives-per-query average is 1.0, with minimum 1, median 1.0, maximum 1, and no multi-positive queries.

Queries average 811.34 characters, while documents average 1,091.24 characters. Queries are informal memory posts with uncertainty, partial plot recall, read-date estimates, cover memories, and genre guesses. Documents are longer book descriptions or synopsis-style passages.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2669, hit@10 of 0.4100, and recall@100 of 0.5900 using the top-500 BM25 candidate subset. Lexical matching helps when a user remembers distinctive names, settings, or rare plot terms, but it is unreliable for the full task.

The difficulty is clue integration. BM25 can over-rank books that share one salient detail, such as a cover color, romance trope, fantasy portal, or character name, while missing the only description that fits the entire remembered combination. It is a partial candidate generator rather than a robust solution.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.2714, hit@10 of 0.3500, and recall@100 of 0.7000. Dense retrieval improves recall@100 and slightly improves nDCG@10 over BM25, but it has lower hit@10. This indicates that embedding similarity broadens coverage but does not always place the exact book in the first page.

The result is plausible for tip-of-the-tongue retrieval. Dense retrieval can connect semantically similar plot descriptions, but long noisy memory posts contain many distractor details. A general embedding can retrieve genre-near books without identifying the exact remembered combination.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3376, hit@10 of 0.4500, and recall@100 of 0.7200. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 28 safeguard rows, candidate counts from 100 to 101, and a mean of 100.28 candidates. It is the strongest profile across the reported metrics.

The hybrid result shows that remembered-book search benefits from combining exact clue matching with semantic plot similarity. BM25 contributes rare remembered words, while dense retrieval captures broader story and genre relations. The combined pool is the best observed starting point for a reranker that can reason over all clues.

### Metric Interpretation for Model Researchers

Because every query has one positive, hit@10 is direct: the book is either visible or not. nDCG@10 captures how early it is ranked, while recall@100 measures whether a downstream reranker can access the correct description. The low scores show that this is a hard single-positive retrieval problem.

The comparison shows that BM25 alone misses many semantic matches, dense retrieval improves coverage, and reranking_hybrid is best overall. This task is useful for testing long noisy query retrieval where relevance depends on the intersection of many weak clues.

### Query and Relevance Type Tendencies

Queries describe books involving mermaid-like girls, kidnapped or stranded heroines, Native American family history, sawmill and mining-accident plots, teen horror memories, magical islands, fantasy portals, dystopian investigations, and romance or thriller elements. Users often express uncertainty with phrases like "I think", "maybe", or approximate reading years.

The task rewards holistic matching. A candidate can share genre, setting, or one memorable scene and still be wrong. The correct description must fit the combined pattern of plot, characters, setting, era, and remembered details.

### Representative Failure Modes

Likely failures include over-ranking books that share one striking clue, missing the correct book because the query contains wrong or uncertain details, confusing genre-near descriptions, and failing to combine cover, plot, and character clues. BM25 may be too literal, while dense retrieval may be too broad.

### Training Data That May Help

Useful training data includes non-overlapping book-finding posts matched to book descriptions, tip-of-the-tongue retrieval datasets, synthetic noisy memory queries paired with descriptions, and hard negatives that share genre or one memorable clue but differ in the core plot. Training should preserve uncertainty and partial recall.

### Model Improvement Notes

A model targeting this task should combine clue extraction with holistic description matching. Sparse systems need robust handling of names, titles, and rare remembered terms. Dense systems need training on noisy memory posts rather than clean summaries. Hybrid systems are especially promising because the observed profile is best across nDCG@10, hit@10, and recall@100.

## Example Data

| Query | Positive document |
| --- | --- |
| Heres what I can recall YA The cover was blue with a girls face on the frontThe girl began to suspec... [100 / 833 chars] | is a merrymaid or so she believes . . . Ellen and Jack are evacuated from London to Cornwall during the Second World War. Ellen relishes the opportunity to better herself. Jack is different. He finds... [200 / 791 chars] |
| Hi all!I'm looking for a book I started a couple of months ago (probably in January before the curre... [100 / 812 chars] | Kidnapped, drugged, and about to be sold to the highest bidder, Desdemona Carlisle is having a hell of a time maintaining her English pride. Then she sees the man in black, galloping through the Egypt... [200 / 1,272 chars] |
| Read around 2011. Cover was an illustration with several characters depicted. Likely from the 90’s.I... [100 / 745 chars] | When her mother died, she told 14-year-old Walking Breeze to seek out her family-the Chelmsfords of Salem. She will find solace there.But Ebie Chelmsford has other ideas. Ebie knows that her half-Shaw... [200 / 709 chars] |
| This book opens with a eastern woman who has been recently widowed when her husband died in a mining... [100 / 675 chars] | Welcome to Hope Falls where three enterprising young females are accepting applications for husbands-for-hire. With one woman already snagged, Lacey Lyman is one of only two remaining. No one really c... [200 / 983 chars] |
| I'm looking for a book I read as a teen. I thought it might be part of the Point Horror, Point Roman... [100 / 1,126 chars] | "And then you die!" - The grim message is scrawled across the script of the horror film Christina stars in - is it a joke, or for real? While shooting a horror film, of which she is the star, young ac... [200 / 571 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BIRCO](https://arxiv.org/abs/2402.14151) |
| Project repository | [BIRCO GitHub repository](https://github.com/BIRCO-benchmark/BIRCO) |
| NanoBIRCO dataset | [hakari-bench/NanoBIRCO](https://huggingface.co/datasets/hakari-bench/NanoBIRCO) |

Representative query and positive book snippets:

| Query | Positive document snippet |
| --- | --- |
| A YA memory about a blue cover, a girl who suspects she is part mermaid, and twins moving in nearby. | Ellen and Jack are evacuated from London to Cornwall during the Second World War. |
| A partially read ebook involving kidnapping, drugging, and an English heroine in danger. | Kidnapped, drugged, and about to be sold to the highest bidder, Desdemona Carlisle struggles to maintain her pride. |
| A 2011 memory about an illustrated cover and an Indian girl with mixed family history. | Walking Breeze seeks out the Chelmsfords of Salem after her mother's death. |
| A book opening with a recently widowed eastern woman after a mining accident. | Hope Falls features women accepting applications for husbands-for-hire. |
| A teen memory possibly from Point Horror, Point Romance, or Sweet Dreams. | A horror film script contains the message "And then you die!" |
