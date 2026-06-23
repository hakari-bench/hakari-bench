# NanoBEIR-en / NanoFEVER

## Overview

NanoFEVER is the compact English NanoBEIR version of FEVER, a fact verification evidence retrieval task. Each query is a short declarative claim, and the corpus contains Wikipedia-style passages that can support or refute the claim. The retrieval goal is to surface evidence-bearing documents for a downstream verifier, not to answer a question directly. This makes the task useful for evaluating claim-to-evidence retrieval, entity grounding, relation matching, and retrieval for false or partially false claims.

## Details

### What the Original Data Measures

FEVER was created for fact extraction and verification over Wikipedia. The original benchmark requires a system to retrieve evidence and then decide whether a claim is supported, refuted, or not supported by available evidence. In the retrieval setting, the important question is whether the evidence page or passage is ranked high enough to be used.

This differs from ordinary question answering because the query is a claim, and the claim itself may be false. A retriever must not assume the wording is correct. It must retrieve the page that contains the decisive evidence about the entity, date, occupation, nationality, title, location, or relation.

### Observed Data Profile

The task contains 50 queries, 4,996 documents, and 57 relevance judgments. Most queries have one positive evidence document, with an average of 1.14 positives per query. The minimum is 1, the median is 1.0, the maximum is 3, and 6 queries are multi-positive, or 12.0% of the set.

Queries average 45.42 characters, while documents average 1,228.71 characters. The short claim must be matched to a much longer evidence passage. Many claims include entity names or titles, but the relevant evidence may be determined by a specific relation or correction rather than broad topical overlap.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.8143, hit@10 of 0.9400, and recall@100 of 1.0000 using the top-500 BM25 candidate subset. This is a very strong lexical profile. FEVER claims often contain rare entity names, media titles, or factual anchors that appear in the relevant Wikipedia passage.

The remaining difficulty is top-rank evidence selection. BM25 may retrieve related pages about the same person, work, place, or year before the passage that actually verifies the claim. Lexical overlap is excellent for candidate generation, but it can confuse same-entity context with decisive evidence.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.8816, hit@10 of 0.9800, and recall@100 of 0.9825. Dense retrieval is the strongest direct top-rank profile. It improves nDCG@10 and hit@10 over BM25, showing that embedding similarity helps connect claims to evidence relations beyond exact term overlap.

This is particularly useful for refuted or mutated claims. The relevant passage may contradict the claim through a profession, date, nationality, genre, or title relation. Dense retrieval is better at ranking evidence-bearing passages above adjacent same-topic pages, although BM25 retains slightly better complete recall@100.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.8521, hit@10 of 0.9800, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no safeguard rows. The hybrid profile matches BM25's complete recall@100 and dense retrieval's hit@10, while sitting between them on nDCG@10.

This makes reranking_hybrid a strong evidence candidate pool. BM25 contributes exact entity and title coverage, while dense retrieval contributes relation-sensitive ranking. A downstream verifier or reranker should benefit from the complete candidate availability while still seeing dense-like top-10 visibility.

### Metric Interpretation for Model Researchers

Because most queries have one positive, hit@10 measures whether the evidence is visible, and nDCG@10 measures how early it appears. recall@100 is especially important for multi-stage fact verification because a verifier cannot recover if the evidence page is absent from the candidate pool.

The comparison shows that BM25 is excellent for recall, dense retrieval is best for direct evidence ranking, and reranking_hybrid offers the best reranking-ready tradeoff. This task is useful for evaluating whether a model retrieves evidence, not merely same-topic Wikipedia text.

### Query and Relevance Type Tendencies

Queries include claims such as Keith Godchaux knew the Grateful Dead, Taarak Mehta Ka Ooltah Chashmah is a sitcom, advanced airplanes were produced in Burbank, Nero is a person, and Scream 2 is exclusively a German film. Relevant passages usually contain the entity description or factual relation needed to support or refute the claim.

The task rewards precise entity grounding and claim relation matching. A passage can mention the right entity yet fail to settle the claim. Evidence for false claims is especially challenging because the correct passage often contradicts rather than repeats the query.

### Representative Failure Modes

Likely failures include retrieving pages that share the same entity but lack the decisive evidence, ranking generic pages above the specific evidence passage, confusing similar titles, and treating false claim wording as if it were correct. BM25 may over-reward surface overlap, while dense retrieval may occasionally miss rare exact entity anchors.

### Training Data That May Help

Useful training data includes non-overlapping FEVER training claims with evidence, claim-verification datasets with evidence annotations, Wikipedia claim-evidence pairs, and synthetic claim mutations based on entity, date, relation, and profession substitutions. Upstream FEVER or BEIR-derived evaluation examples should be excluded when overlap is possible.

### Model Improvement Notes

A model targeting this task should preserve high entity recall while improving evidence relation ranking. Sparse systems need strong title and alias handling. Dense systems should train on claim-to-evidence pairs rather than only question answering. Hybrid systems are promising because the observed profile keeps complete recall while improving top-10 visibility.

## Example Data

| Query | Positive document |
| --- | --- |
| Keith Godchaux knew the Grateful Dead. [38 chars] | The Grateful Dead was an American rock band formed in 1965 in Palo Alto , California . Ranging from quintet to septet , the band is known for its unique and eclectic style , which fused elements of rock , psychedelia , experimental music , modal jazz , country , folk , bluegrass , blues , reggae , and space rock , for live performances of lengthy instrumental jams , and for their devoted fan base , known as `` Deadheads '' . `` Their music , '' writes Lenny Kaye , `` touches on ground that most other groups do n't even know exists . '' These various influences were distilled into a diverse and psychedelic whole that made the Grateful Dead `` the pioneering Godfathers of the jam band world '' . The band was ranked 57th by Rolling Stone magazine in its The Greatest Artists of All Time issue . The band was inducted into the Rock and Roll Hall of Fame in 1994 and a recording of their May 8 , 1977 performance at Cornell University 's Barton Hall was added to the National Recording Registry... [1,000 / 3,024 chars] |
| Taarak Mehta Ka Ooltah Chashmah is a sitcom. [44 chars] | Taarak Mehta Ka Ooltah Chashmah ( English : Taarak Mehta 's Different Perspective ) is India 's longest running sitcom serial produced by Neela Tele Films Private Limited . The show went on-air on July 28 , 2008 . It airs from Monday to Friday at 8:30 pm , with its repeat telecast at 11:00 pm and the next day at 3:00 pm on SAB TV . The show started its re-run on Sony Pal from November 2 , 2015 at 4:30 pm and 8:00 pm everyday . The show is based on the column Duniya Ne Oondha Chashma written by columnist and journalist Taarak Mehta for Gujarati weekly magazine Chitralekha . [581 chars] |
| Secret and technologically advanced airplanes were produced in Burbank, California. [83 chars] | Burbank is a city in Los Angeles County in Southern California , United States , 12 mi northwest of downtown Los Angeles . The population at the 2010 census was 103,340 . Billed as the `` Media Capital of the World '' and only a few miles northeast of Hollywood , numerous media and entertainment companies are headquartered or have significant production facilities in Burbank , including The Walt Disney Company , Warner Bros. . Entertainment , Nickelodeon Animation Studios , NBC , Cartoon Network Studios with the West Coast branch of Cartoon Network , and Insomniac Games . The city is also home to Bob Hope Airport . It was the location of Lockheed 's Skunk Works , which produced some of the most secret and technologically advanced airplanes , including the U-2 spy planes that uncovered the Soviet Union missile components in Cuba in October 1962 . Burbank consists of two distinct areas : a downtown/foothill section , in the foothills of the Verdugo Mountains , and the flatland section .... [1,000 / 1,401 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset paper | [FEVER](https://arxiv.org/abs/1803.05355) |
| Project site | [FEVER project site](http://fever.ai) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-en dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| Keith Godchaux knew the Grateful Dead. | The Grateful Dead was an American rock band formed in 1965 in Palo Alto, California. |
| Taarak Mehta Ka Ooltah Chashmah is a sitcom. | Taarak Mehta Ka Ooltah Chashmah is India's longest running sitcom serial. |
| Secret and technologically advanced airplanes were produced in Burbank, California. | Burbank is a city in Los Angeles County in Southern California. |
| Nero is a person. | The Julio-Claudian dynasty refers to the first five Roman emperors, including Nero. |
| Scream 2 is exclusively a German film. | Scream 2 is a 1997 American slasher film directed by Wes Craven. |
