# NanoMTEB-Thai / belebele_eng_latn_tha_thai

## Overview

`belebele_eng_latn_tha_thai` is a cross-lingual Belebele retrieval split in the Thai NanoMTEB set. The task uses Thai reading-comprehension questions as queries and English passages as documents. It tests whether a retriever can map a Thai question to the corresponding English source passage from a parallel reading-comprehension dataset. The task is therefore both passage retrieval and cross-lingual semantic alignment.

The Nano split contains 200 queries, 488 documents, and exactly 200 positive relevance judgments. Each query has one positive passage. Queries average about 58 characters, while documents average about 476 characters. The sampled questions ask what follows from a passage, who may have created an agricultural society, how subsistence agriculture is described, which Chinese era was especially violent, and when King Tutankhamun became notorious. Correct documents are English explanatory passages.

## Details

### What the Original Data Measures

Belebele is a fully parallel multiple-choice reading-comprehension benchmark covering 122 language variants. Each item is grounded in a short passage and associated with questions and answer options. In retrieval form, the question becomes the query and the passage becomes the relevant document.

This split uses different languages for query and document. A Thai question must retrieve the matching English passage. The model is not answering the question directly; it is finding the passage that supports the reading-comprehension item.

### Observed Data Profile

The corpus is small and contains parallel passage topics from general informational text. Documents are medium-length English paragraphs. Queries are Thai questions that usually refer to the passage through phrasing like "according to the passage" or ask about a detail in the passage.

Because each query has one positive, ranking precision is direct: the right passage is either high in the ranking or not. Cross-lingual matching dominates the task; exact Thai-English lexical overlap is rare except for names, digits, or quoted entities.

### BM25 Evaluation Profile

BM25 is weak, with nDCG@10 of 0.0891, hit@10 of 0.1050, and recall@100 of 0.3550. This is expected because Thai queries and English documents do not share normal vocabulary. BM25 can only use language-independent cues such as names, numbers, punctuation, and occasional borrowed terms.

The low BM25 score is useful as a diagnostic. It confirms that sparse lexical matching is not a meaningful solution for this cross-lingual direction. Term frequency does not capture the translation relation between the Thai question and English passage.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is very strong, with nDCG@10 of 0.8483, hit@10 of 0.9150, and recall@100 of 0.9800. Dense retrieval successfully maps Thai questions and English passages into a shared semantic space. It can connect passage-level ideas such as the French Revolution, New Zealand settlement, subsistence agriculture, Chinese dynasties, and King Tutankhamun across languages.

This is a strongly dense-favorable profile. The task rewards multilingual semantic alignment much more than lexical matching.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.2919, hit@10 of 0.3500, and recall@100 of 0.9750. Candidate lists contain 100 to 101 items, and 5 rows use the positive safeguard. Hybrid retrieval preserves nearly as many positives at top 100 as dense retrieval, but its top-10 ranking is far worse.

This pattern shows that hybrid search can be useful for candidate preservation but is not a strong final ranker here. Lexical candidates are mostly noise in a Thai-to-English setting, so dense retrieval should carry the main ranking signal.

### Metric Interpretation for Model Researchers

This split is strongly dense-favorable. BM25 provides a low lexical floor, dense retrieval provides the meaningful cross-lingual ranking, and hybrid retrieval is useful mostly for recall. A model that improves over dense retrieval here is likely improving Thai-English semantic alignment for reading-comprehension style text.

Because every query has one positive, hit@10 and nDCG@10 are straightforward. Recall@100 indicates whether the passage remains available for downstream reranking, but direct search quality is best reflected by dense nDCG@10.

### Query and Relevance Type Tendencies

Representative questions ask about historical changes after the French Revolution, the first inhabitants or agricultural society in New Zealand, the definition of subsistence agriculture, violent eras in ancient China, and King Tutankhamun's modern notoriety. The relevant English passages contain the evidence needed to answer those questions.

The task requires matching the meaning of the Thai question to the English passage, not matching an answer option. Some queries ask about inference from the passage, so retrieval must connect to the supporting paragraph as a whole.

### Representative Failure Modes

BM25 fails whenever there are no shared cross-script terms. Dense retrieval may confuse passages from similar educational topics, such as multiple historical or agricultural passages. Hybrid retrieval may preserve the correct passage but rank lexical distractors above it.

Another failure mode is passage-level ambiguity. Since the questions are derived from reading comprehension, several passages may discuss broad similar themes. The model must retrieve the exact source passage for the question.

### Training Data That May Help

Useful training data includes Thai-English parallel retrieval pairs, question-to-passage translation pairs, multilingual reading-comprehension retrieval data, and hard negatives from similar topics. Training should avoid using the same Belebele evaluation items.

Hard negatives should be English passages from the same broad topic that do not answer the Thai question. These force the model to learn exact cross-lingual passage alignment rather than broad topical similarity.

### Model Improvement Notes

Dense models can improve through Thai-English dual-encoder training, Thai segmentation robustness, and passage-level multilingual alignment. Sparse systems have little upside beyond named-entity and numeric matching. Hybrid systems may help candidate recall but need semantic reranking for top quality.

For evaluation, this task is a clean cross-lingual retrieval probe. The expected strong system is a multilingual dense model that handles Thai questions and English passages without relying on translation at query time.

## Example Data

| Query | Positive document |
| --- | --- |
| การเปลี่ยนแปลงใดที่เกิดจากการปฏิวัติฝรั่งเศสมีผลกระทบอย่างมากต่อพลเมืองชนชั้นแรงงาน [83 chars] | There are a lot of social and political effects such as the use of metric system, a shift from absolutism to republicanism, nationalism and the belief the country belongs to the people not to one sole ruler. Also after the Revolution occupations were open to all male applicants allowing the most ambitious and successful to succeed. Same goes for the military because instead of army rankings being based on class they were now based on cailaber. The French Revolution also inspired many other repressed working class people of other country's to began their own revolutions. [576 chars] |
| จากบทความ ใครน่าจะเป็นผู้สร้างสังคมเกษตรกรรมขึ้น [48 chars] | For a long time during the nineteenth and twentieth centuries, it was believed the first inhabitants of New Zealand were the Maori people, who hunted giant birds called moas. The theory then established the idea that the Maori people migrated from Polynesia in a Great Fleet and took New Zealand from the Moriori, establishing an agricultural society. However, new evidence suggests that the Moriori were a group of mainland Maori who migrated from New Zealand to the Chatham Islands, developing their own distinctive, peaceful culture. There was also another tribe on the Chatham islands these were Maori who migrated away from New Zealand. They called themselves the Moriori there were a few skirmishes and in the end, the Moriori were wiped out [747 chars] |
| ข้อใดต่อไปนี้กล่าวถึงเกษตรกรรมเพื่อยังชีพได้ถูกต้อง [51 chars] | Subsistence agriculture is agriculture carried out for the production of enough food to meet just the needs of the agriculturalist and his/her family. Subsistence agriculture is a simple, often organic, system using saved seed native to the ecoregion combined with crop rotation or other relatively simple techniques to maximize yield. Historically most farmers were engaged in subsistence agriculture and this is still the case in many developing nations. [456 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| Belebele paper | Original parallel reading-comprehension benchmark. |
| Belebele repository | Source data and benchmark resources. |
| MTEB task card | Retrieval packaging of Belebele. |

### Representative Snippets

- A Thai query asks which French Revolution change affected working-class citizens; the English passage discusses social and political effects.
- A query asks who may have started an agricultural society; the English passage discusses New Zealand settlement theories.
- A query asks how subsistence agriculture is accurately described; the English passage defines subsistence agriculture.
- A query asks which era was one of China's most violent; the English passage describes unstable periods between dynasties.
- A query asks when King Tutankhamun gained notoriety; the English passage discusses his modern fame.
