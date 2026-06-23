# NanoChemTEB / NanoChemHotpotQA

## Overview

NanoChemHotpotQA is the chemistry-filtered HotpotQA retrieval task from NanoChemTEB. Queries are English multi-hop questions whose answers are supported by Wikipedia passages connected to chemistry or chemistry-adjacent scientific topics. The task measures whether a retriever can follow bridge entities and scientific clues rather than simply matching one prominent term.

## Details

### What the Original Data Measures

ChemTEB includes ChemHotpotQARetrieval as a chemistry-domain retrieval task derived from HotpotQA. HotpotQA was designed for multi-hop question answering over Wikipedia, where questions often require connecting entities or properties across supporting facts.

The chemistry filtering makes the corpus scientific, but it does not remove the multi-hop character. Queries may ask about a scientist, organism, preservation method, physical measurement, or chemistry-adjacent entity through an indirect clue. The relevant passage contains the final answer fact, while hard negatives can share only the bridge term.

### Observed Data Profile

The task contains 18 queries, 10,000 documents, and 18 relevance judgments. Every query has exactly one positive. Queries average 104.22 characters, and documents average 402.40 characters.

This is a very small Nano split, so metric differences are sensitive to a few examples. The documents are Wikipedia-style passages about scientists, fungi, food preservation, physics, plumbing, journals, and other scientific or chemistry-adjacent topics.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7178, hit@10 of 0.7778, and recall@100 of 0.8889 using the top-500 BM25 candidate subset. This is a strong lexical baseline because many queries contain rare scientific entities or phrases that appear in the positive passage.

The remaining failures are typical multi-hop failures. A passage may share a scientific term or bridge entity while not containing the final answer. BM25 can retrieve the wrong scientist, fungus, or related scientific page when the query requires resolving the property being asked.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.7748, hit@10 of 0.8333, and recall@100 of 1.0000. Dense retrieval improves over BM25 and recovers every positive within the top 100.

This suggests that semantic matching helps connect the full multi-hop question to the answer-bearing passage. Dense retrieval is useful when the exact bridge term alone is not enough to select the correct supporting paragraph.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7923, hit@10 of 0.8333, and recall@100 of 1.0000. It uses exactly 100 candidates per query in this slice, with no rank-101 safeguard rows.

The hybrid profile is the strongest nDCG@10 result and ties dense retrieval for hit@10 and recall@100. It benefits from both rare entity overlap and semantic question-passage matching. Because the split is only 18 queries, the dense and hybrid difference should be read cautiously.

### Metric Interpretation for Model Researchers

This task is a small chemistry-filtered multi-hop retrieval probe. BM25 is strong but not enough; dense and hybrid retrieval better handle the full question intent. The important distinction is whether the retriever finds the final answer passage, not merely a bridge-related page.

Researchers should treat the absolute scores with caution because of the small query count. The task is still useful as a diagnostic for entity-bridge reasoning in scientific Wikipedia retrieval.

### Query and Relevance Type Tendencies

Queries ask about Swiss physicists, food preservation, edible fungi, basidiomycete names, plumbing traps, journals, measurements, and other chemistry-adjacent facts. Positive documents are Wikipedia passages containing the final answer.

The relevance relation is answer support under multi-hop wording. A relevant passage often contains the final fact after the query has pointed through another entity or property.

### Representative Failure Modes

Likely failures include retrieving a page that shares the bridge entity but not the answer, confusing related scientific organisms or people, and selecting a topically adjacent chemistry page instead of the final supporting passage.

BM25 is vulnerable to bridge-term distraction. Dense retrieval can still over-match broad scientific relatedness. Hybrid retrieval helps by combining rare term anchors with semantic intent.

### Training Data That May Help

Useful training data includes non-overlapping ChemHotpotQA train retrieval pairs, HotpotQA multi-hop retrieval with supporting facts, chemistry-filtered Wikipedia QA pairs, and bridge-entity hard negatives.

Synthetic data should generate HotpotQA-style multi-hop questions from non-evaluation chemistry-related Wikipedia passages. The positive should contain the final answer fact, while negatives may share only the bridge term.

### Model Improvement Notes

Strong systems should represent both bridge entities and the requested final property. Hybrid retrieval is the best observed profile here, but dense retrieval is nearly tied and has perfect recall@100. Rerankers should be trained to distinguish bridge pages from final answer pages.

## Example Data

| Query | Positive document |
| --- | --- |
| In what field did a Swiss physicist who had a geometrical representation named after him work in? [97 chars] | Felix Bloch Felix Bloch (23 October 1905 – 10 September 1983) was a Swiss physicist, working mainly in the U.S. He and Edward Mills Purcell were awarded the 1952 Nobel Prize for Physics for "their development of new ways and methods for nuclear magnetic precision measurements." In 1954–1955, he served for one year as the first Director-General of CERN. [354 chars] |
| What company claims to manufacture one out of every three objects that provide a shelf life typically ranging from one to five years? [133 chars] | Canning Canning is a method of preserving food in which the food contents are processed and sealed in an airtight container. Canning provides a shelf life typically ranging from one to five years, although under specific circumstances it can be much longer. A freeze-dried canned product, such as canned dried lentils, could last as long as 30 years in an edible state. In 1974, samples of canned food from the wreck of the "Bertrand", a steamboat that sank in the Missouri River in 1865, were tested by the National Food Processors Association. Although appearance, smell and vitamin content had deteriorated, there was no trace of microbial growth and the 109-year-old food was determined to be still safe to eat. [715 chars] |
| WHat dish is Dacryopinax spathularia included in that is also sometimes called Luóhàn cài? [91 chars] | Dacryopinax spathularia Dacryopinax spathularia (syn. Guepinia spathularia) is an edible jelly fungus. It is orange in color. In Chinese culture, it is called "guìhuā'ěr" (桂花耳; literally "sweet osmanthus ear," referring to its similarity in appearance to that flower). It is sometimes included in a vegetarian dish called Buddha's delight. [339 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| ChemTEB paper | [ChemTEB](https://arxiv.org/abs/2412.00532) |
| HotpotQA paper | [HotpotQA](https://aclanthology.org/D18-1259/) |
| Source dataset | [BASF-AI/ChemHotpotQARetrieval](https://huggingface.co/datasets/BASF-AI/ChemHotpotQARetrieval) |
| NanoChemTEB dataset | [hakari-bench/NanoChemTEB](https://huggingface.co/datasets/hakari-bench/NanoChemTEB) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| In what field did a Swiss physicist with a geometrical representation named after him work? | A Felix Bloch passage states that he was a Swiss physicist known for work in the United States. |
| What preservation method provides a shelf life ranging from one to five years? | A canning passage explains food preservation in airtight containers. |
| What dish includes Dacryopinax spathularia? | A fungus passage describes the edible jelly fungus and its Chinese naming. |
| What is another name for a basidiomycete fungus? | A Boletus edulis passage lists common names such as porcini. |
| What substance remains in a plumbing trap to block sewer gases? | A plumbing trap passage explains the water bend used to prevent gases from entering buildings. |
