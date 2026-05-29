# NanoMIRACL / zh

## Overview

MIRACL frames Chinese as native same-language retrieval over Chinese Wikipedia
passages, with human relevance judgments rather than translated English labels.
The Nano split is a compact one-positive passage search task. Its queries are
among the shortest inspected MIRACL examples, often complete questions such as
`耶稣哪一年逝世？`, `马来西亚位于哪一大洲？`, or `联合国五常国家有哪些？`, so the
retriever must use very little context to select passages about countries,
institutions, history, religion, transportation, people, geography, companies,
entertainment, and definitions.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as a monolingual
ad hoc retrieval benchmark over Wikipedia passages. Chinese queries retrieve
Chinese Wikipedia passages, so the task measures same-language retrieval rather
than cross-lingual search. The paper states that MIRACL uses well-formed
questions and native-speaker relevance judgments over passage-level corpora.

Chinese is one of the new known MIRACL languages, not one of the languages
inherited from Mr. TyDi. The paper explains that for new languages such as
Chinese, data was generated from scratch and split into training, development,
and test-B sets, with no test-A split. This matters because Chinese MIRACL
queries do not simply reuse TyDi or Mr. TyDi query distributions.

MIRACL annotators generated questions from Wikipedia prompts and judged
candidate passages returned by an ensemble of BM25, mDPR, and mColBERT. For
Chinese, the MIRACL overview reports development-set BM25 nDCG@10 of 0.180 and
hybrid BM25+mDPR nDCG@10 of 0.526. The large gap is important context:
character-based lexical matching can be brittle for short Chinese questions,
while dense or hybrid retrieval can recover semantic matches that do not share
the exact same wording.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,700 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 10.86
characters, making this one of the shortest inspected NanoMIRACL splits. The
sampled queries are compact complete questions such as `耶稣哪一年逝世？`,
`马来西亚位于哪一大洲？`, `卡梅伦哪一年上任？`, and `联合国五常国家有哪些？`.

Documents average 179.69 characters and usually begin with a Chinese Wikipedia
article title. The observed positives cover Malaysia, China railway design,
Good Friday, Brazilian athletes, Academia Sinica, permanent members of the UN
Security Council, Sui dynasty canals, British rail transport, David Cameron,
Australia, the Four Horsemen of the Apocalypse, and Christian symbols. Some
positives are broad or indirect, so the task rewards finding the labeled
evidence passage rather than extracting a single canonical answer string.

The task is dominated by short entity-attribute questions. Because the queries
are so short, many candidates share the same key phrase: country area, railway
length, UN members, Christian symbols, canals, or football players. A strong
retriever must use the whole query relation, not only the most salient entity.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.4466
and hit@10 = 0.7400 on this Nano split. BM25 places 39 of 200 positives at rank
1 and 148 of 200 positives in the top 10. It is much stronger on this sampled
Nano split than the full MIRACL development-set BM25 score reported in the
paper, but it still misses 52 positives from the top 10.

The failures show short-query ambiguity. For "联合国五常国家有哪些?", BM25 ranks
general UN member-list and UNCTAD pages before a passage that explicitly lists
the Security Council permanent members. For "隋朝修建了哪些运河?", the Grand Canal
article and other canal pages outrank the Sui Yangdi passage that lists the
segments. For "卡梅伦哪一年上任?", government-formation and Brexit pages outrank
the David Cameron biography passage. For "澳大利亚国土面积多大?", environmental and
federal-state pages outrank the country article with the area statement.

Because this Nano split is single-positive, hit@10 measures whether the labeled
evidence passage appears at all. nDCG@10 is still important because many
positives are present just below near-topic distractors, and the short query
length makes rank ordering especially sensitive to small lexical differences.

### Training Data That May Help

Non-overlapping Chinese MIRACL training data is the first source to inspect.
Because this task is MIRACL-derived, upstream development or test queries,
qrels, and positive passages likely to overlap with NanoMIRACL should
preferably be excluded from training. Other useful data includes Chinese
Wikipedia question-to-passage retrieval pairs, Chinese open-domain QA evidence
retrieval, and hard negatives from related Chinese Wikipedia pages with similar
entity or attribute words.

Training should focus on short-query relation binding. The model needs to
distinguish country-area questions from general geography pages, institution
membership questions from organization overviews, and person-date questions
from related event pages.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Chinese
Wikipedia-style passages and generate concise Chinese questions grounded in one
selected passage. Useful forms include `哪一年`, `在哪里`, `有多大`, `有哪些`,
`是谁`, `代表什么`, `什么时候`, and `多少`, with realistic short phrasing.

For joint document-and-question generation, create Chinese encyclopedia-style
passages with article titles, aliases, dates, lists, areas, memberships,
historical events, institutions, geography, and biographies, then generate
answerable short Chinese questions. Do not seed generation with Nano evaluation
queries or positive passages. Include hard negatives that reuse the same entity
or attribute phrase but answer a different relation.

## Example Data

| Query | Positive document |
| --- | --- |
| 新疆面积有多大？ (8 chars) | 新疆维吾尔自治区 新疆维吾尔自治区（），通称新疆，简称新，是中華人民共和國的一个自治区，也是中國面积第一大的省级行政区。自治區由新疆省改置，成立于1955年，首府位於乌鲁木齐。新疆总面积为1,664,897平方公里，约占中国陆地面积六分之一；陆地边境线达5690.142公里，占中国边界总长度四分之一。 (151 chars) |
| 英国王室有哪些成员？ (10 chars) | 英國王室 英国王室允许与皇室有血缘关系的女性继承王位，这造成了英国王室血缘相同而王朝名称不同的现象，诺曼底王朝建立者威廉一世与英国的盎格鲁-撒克逊王朝无直接的血缘关系，忏悔者爱德华死后无嗣，威廉通过自己的姨祖母艾玛（埃塞烈德的妻子和爱德华的母亲），主张英国王位应该由他继承，威廉的妻子弗兰德的玛蒂尔达是英国的盎格鲁-撒克逊王朝阿尔弗烈德大帝的第七代直系后裔，她和威廉的婚姻提高了威廉要求王位的权利，威廉一世死后，王位由威廉一世与弗兰德的玛蒂尔达所生的 ... [truncated 225 chars](314 chars) |
| 美国有哪些流行音乐派别？ (12 chars) | 美国流行音乐 19世纪早期，美国流行音乐开始分化出不同的风格。美国音樂產業在20世纪从布鲁斯和民间音乐中发展出了一系列新音乐类型，包括乡村、节奏布鲁斯、爵士和摇滚。20世纪60年代和70年代见证了美国流行音乐的几个重要变化，如重金属、朋克、灵魂乐和嘻哈乐这些新类型的诞生。这些音乐类型属于“流行音乐”是因为它们是商业性的（与民谣和古典音乐相对），并不是说它们是“主流的”。 (186 chars) |
| 委内瑞拉位于哪一大洲？ (11 chars) | 2018年委內瑞拉地震 发生此次地震的委内瑞拉位于南美洲北部，濒临加勒比海，地震频发。除本次地震外，近年该地区附近还曾多次较大地震。 (66 chars) |
| 黄帝的妻子叫什么？ (9 chars) | 黄帝 黃帝有四妃十嬪。正妃為西陵氏，名嫘祖，她教人民養蠶繅絲，織出絲綢做衣裳，故有「先蠶」的稱號。次妃名嫫母，傳說發明了鏡子，雖長相醜陋，但德行高尚，深受黃帝敬重。黃帝共有二十五個兒子，其中十四人被分封得姓。這十四人共得到十二個姓，它們是：姬、酉、祁、己、滕、葴、任、荀、僖、姞、儇、衣。而少昊、顓頊、帝嚳、唐堯、虞舜，以及夏朝、商朝、周朝的君主都是黃帝的子孫。据《山海经》大荒北经、大荒西经、大荒东经，北方的北狄、西方的犬戎、东方的东夷都是黄帝后裔 ... [truncated 225 chars](241 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | zh |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | zh |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,700 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.4022 |
| BM25 hit@10 | 0.7300 |
| BM25 Recall@100 | 0.8514 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7191 |
| Dense hit@10 | 0.9850 |
| Dense Recall@100 | 0.9873 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5619 |
| Reranking hybrid hit@10 | 0.8800 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 10.86 |
| Document length avg chars | 179.69 |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984); 2022; Xinyu Zhang, Nandan Thakur, Odunayo Ogundepo, Ehsan Kamalloo, David Alfonso-Hermelo, Xiaoguang Li, Qun Liu, Mehdi Rezagholizadeh, Jimmy Lin; DOI: `10.48550/arXiv.2210.09984`.
- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/); 2023 TACL version; DOI: `10.1162/tacl_a_00595`.
- [MIRACL GitHub repository](https://github.com/project-miracl/miracl).
- [MIRACL corpus dataset card](https://huggingface.co/datasets/miracl/miracl-corpus).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL)
- Source corpus: [miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus)
- Source queries and qrels: [miracl/miracl](https://huggingface.co/datasets/miracl/miracl)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | https://arxiv.org/abs/2210.09984 |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | https://aclanthology.org/2023.tacl-1.63/ |
| MIRACL GitHub repository |  | project repository | https://github.com/project-miracl/miracl |
| miracl/miracl-corpus |  | dataset card | https://huggingface.co/datasets/miracl/miracl-corpus |
| miracl/miracl |  | dataset card | https://huggingface.co/datasets/miracl/miracl |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMIRACL
  backing_dataset: NanoMIRACL
  dataset_id: hakari-bench/NanoMIRACL
  task_name: zh
  split_name: zh
  language: zh
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/zh.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1700
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 10.86
    document_mean: 179.691765
  bm25:
    ndcg_at_10: 0.40217498810953084
    hit_at_10: 0.73
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived
      data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
    - non-overlapping MIRACL Chinese train split data
    - Chinese Wikipedia question-to-passage retrieval pairs
    - Chinese open-domain QA evidence retrieval datasets
    - related Chinese Wikipedia hard negatives with similar entity or attribute words
    synthetic_data:
      document_generation: Chinese Wikipedia-style passages with titles, aliases,
        dates, lists, areas, memberships, historical events, institutions, geography,
        and biographies
      question_generation: concise Chinese fact questions using which-year, where,
        how-large, which-items, who, what-represents, when, and how-many forms
      answerability: questions should be grounded in explicit facts or relations in
        the generated or selected passage
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMIRACL
    source_urls:
    - label: MIRACL corpus dataset
      url: https://huggingface.co/datasets/miracl/miracl-corpus
    - label: MIRACL source queries and qrels
      url: https://huggingface.co/datasets/miracl/miracl
    - label: MIRACL GitHub repository
      url: https://github.com/project-miracl/miracl
    source_notes: []
  references:
  - title: 'Making a MIRACL: Multilingual Information Retrieval Across a Continuum
      of Languages'
    url: https://arxiv.org/abs/2210.09984
    year: 2022
    doi: 10.48550/arXiv.2210.09984
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages'
    url: https://aclanthology.org/2023.tacl-1.63/
    year: 2023
    doi: 10.1162/tacl_a_00595
    is_paper: true
    source_confidence: definitive_paper_link
  - title: MIRACL GitHub repository
    url: https://github.com/project-miracl/miracl
    year: null
    doi: null
    is_paper: false
    source_confidence: official_project_repository
  - title: MIRACL corpus dataset
    url: https://huggingface.co/datasets/miracl/miracl-corpus
    year: null
    doi: null
    is_paper: false
    source_confidence: official_dataset_card
  - title: MIRACL source queries and qrels
    url: https://huggingface.co/datasets/miracl/miracl
    year: null
    doi: null
    is_paper: false
    source_confidence: official_dataset_card
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4021749881
      hit_at_10: 0.73
      recall_at_100: 0.8513800425
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8513800425
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7190546116
      hit_at_10: 0.985
      recall_at_100: 0.9872611465
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9872611465
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5619414451
      hit_at_10: 0.88
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
