# NanoMIRACL / hi

## Overview

MIRACL's Hindi split is native-language passage retrieval over Hindi Wikipedia,
not translated retrieval from English. The Nano version keeps a compact
single-positive sample of that benchmark. The observed Devanagari queries are
somewhat longer than many MIRACL languages and often begin with topical
entities such as `भारत`, `भारतीय`, or `विश्व`, while question intent appears in
forms like `किस`, `कौन`, and `कितनी`; the model must connect those entity-heavy
questions to evidence about history, administration, geography, science,
religion, politics, law, sports, and definitions.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as a monolingual
ad hoc retrieval benchmark over Wikipedia passages. Hindi queries retrieve Hindi
Wikipedia passages, so the task measures native-language evidence retrieval
rather than cross-lingual search. The paper states that MIRACL uses
well-formed natural-language questions and native-speaker relevance judgments.

Hindi belongs to MIRACL's "new known languages" group. The paper explains that
Hindi, Spanish, French, Farsi, and Chinese were added beyond Mr. TyDi/TyDi QA,
and that all data for these languages was generated from scratch. This means the
Hindi split is a MIRACL-created Hindi Wikipedia retrieval task rather than a
denser relabeling of an older Mr. TyDi split.

The annotation process is retrieval-specific. MIRACL annotators generated
questions from Wikipedia prompts and then judged candidate passages returned by
an ensemble of BM25, mDPR, and mColBERT. The relevant item is therefore an
evidence-bearing passage. For Hindi, the MIRACL overview reports
development-set BM25 nDCG@10 of 0.458 and hybrid BM25+mDPR nDCG@10 of 0.616,
which suggests that lexical matching is useful but can be improved by semantic
or hybrid ranking.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,748 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 54.75
characters, making this one of the longer NanoMIRACL query samples inspected so
far. Many queries begin with topical entities such as `भारत`, `भारतीय`, or
`विश्व`, while others begin with question forms such as `किस`, `कौन`, `किसने`,
and `कितनी`.

Documents average 580.36 characters and are Hindi Wikipedia passages that
usually begin with an article title. The observed positives cover Pakistani
constitutional history, Indian administrative divisions, the Tehri Dam, the
Great Barrier Reef, earthquakes, Mysore wars, lapse-rate terminology,
cattle-castration instruments, national media institutions, countries of the
world, Punjabi-language distribution, U.S. presidents, rural development, Jain
history, and resignation or impeachment procedures.

The task often requires retrieving a passage that contains a specific
administrative, historical, or technical relation. Topic overlap alone is not
enough. A question about union territories asks who administers them, a question
about Tehri Dam asks which river it is on, and a question about an instrument
asks what operation it is used for. Hindi morphology, Devanagari numerals,
English loanwords, and transliterated names all appear in the data.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5497
and hit@10 = 0.8550 on this Nano split. BM25 places 62 of 200 positives at rank
1 and 171 of 200 positives in the top 10. The baseline is strong when the query
contains distinctive terms such as `ग्रेट बेरियर रीफ`, `टिहरी बाँध`, or
`भूकंप`.

The failure cases show relation-level weaknesses. For the question about the
treaty ending the Third Anglo-Mysore War, BM25 retrieves Tipu Sultan and war
pages but the labeled passage about the Fourth Anglo-Mysore War is just outside
the top 10. For "कितनी ऊँचाई पर जाने से तापमान १ डिग्री की कमी होती है?", top
candidates contain temperature words but the positive inversion/lapse-rate
passage is rank 11. For the Burdizzo castrator question, survey and instrument
pages outrank the animal-castration passage that explains the device. For
questions about India administration and rural-development oversight, BM25
finds broad government or ministry pages but misses the specific passage that
contains the requested relation.

Because each query has one positive passage, hit@10 measures whether BM25 finds
the labeled evidence at all, while nDCG@10 captures how early that evidence is
ranked. A stronger model should preserve rare-term matching and improve
relation-sensitive retrieval for Hindi administrative, historical, and technical
questions.

### Training Data That May Help

Non-overlapping Hindi MIRACL training data is the first source to inspect.
Because this task is MIRACL-derived, upstream development or test queries,
qrels, and positive passages likely to overlap with NanoMIRACL should preferably
be excluded from training. Other useful data includes Hindi Wikipedia
question-to-passage retrieval pairs, Hindi open-domain QA evidence retrieval,
and entity-attribute supervision for Indian administration, history, geography,
religion, law, and science.

Training should focus on evidence passage retrieval. The model needs to retrieve
the passage that supports the answer, even when a broader article or a related
entity page has more lexical overlap with the query.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Hindi Wikipedia-style
passages and generate Hindi questions grounded in one selected passage. Useful
forms include `किस`, `कौन`, `किसने`, `कितनी`, `कहाँ`, `कब`, `क्या`, and
`किसके द्वारा`, with named entities, dates, numbers, administrative roles,
places, rivers, treaties, and definitions.

For joint document-and-question generation, create Hindi encyclopedia-style
passages with titles, aliases, dates, offices, locations, measurements, and
technical terms, then generate answerable Hindi questions. Do not seed
generation with Nano evaluation queries or positive passages. Include related
but non-answering passages around the same entity so the model learns to rank
evidence over topical overlap.

## Example Data

| Query | Positive document |
| --- | --- |
| रडार में किस प्रकार की तरंगें होती हैं ? (40 chars) | रडार रडार (Radar) वस्तुओं का पता लगाने वाली एक प्रणाली है जो सूक्ष्मतरंगों का उपयोग करती है। इसकी सहायता से गतिमान वस्तुओं जैसे वायुयान, जलयान, मोटरगाड़ियों आदि की दूरी (परास), ऊंचाई, दिशा, चाल आदि का दूर से ही पता चल जाता है ... [truncated 225 chars](684 chars) |
| भारत का गणतंत्र दिवस किस तारीख पर आता है? (41 chars) | गणतन्त्र दिवस (भारत) गणतन्त्र दिवस भारत का एक राष्ट्रीय पर्व है जो प्रति वर्ष 26 जनवरी को मनाया जाता है। इसी दिन सन् 1950 को भारत सरकार अधिनियम (1935) को हटाकर भारत का संविधान लागू किया गया था। यह भारत के तीन राष्ट्रीय अवकाशो ... [truncated 225 chars](286 chars) |
| कांग्रेस दल का नेता कौन है ? (28 chars) | भारतीय राष्ट्रीय कांग्रेस 1947 में भारत की स्वतन्त्रता के बाद से भारतीय राष्ट्रीय काँग्रेस भारत के मुख्य राजनैतिक दलों में से एक रही है। इस दल के कई प्रमुख नेता भारत के प्रधानमन्त्री रह चुके हैं। जवाहरलाल नेहरू, लाल बहादुर शा ... [truncated 225 chars](745 chars) |
| वाहनों में पेट्रोल के जलने से धातु वायु को प्रदूषित करती है ? (61 chars) | मोटरवाहन अधिकांश ऑटोमोबाइल जिनका आज हम प्रयोग करते हैं चलती है गैसोलीन () द्वारा (जिसे हम पेट्रोल भी कहते हैं) या डीजल आंतरिक दहन इंजन, जो वायु प्रदूषण () फैलाने के लिए भी जाने जाते हैं और इन्हे जलवायु परिवर्तन () और ग्लोबल व ... [truncated 225 chars](568 chars) |
| भारत की कौन सी फैक्ट्रियां पुर्तगालियों द्वारा स्थापित की? (58 chars) | भारत में यूरोपीय आगमन सन् 1500 में पुर्तगालियों ने कोचीन(केरल) के पास अपनी कोठी बनाई। शासक सामुरी (जमोरिन) से उसने कोठी की सुरक्षा का भी इंतजाम करवा लिया क्योंकि अरब व्यापारी उसके ख़िलाफ़ थे। इसके बाद कालीकट और कन्ननोर में भी ... [truncated 225 chars](715 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | hi |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | hi |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,748 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.3037 |
| BM25 hit@10 | 0.5200 |
| BM25 Recall@100 | 0.7049 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6847 |
| Dense hit@10 | 0.9100 |
| Dense Recall@100 | 0.9220 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5174 |
| Reranking hybrid hit@10 | 0.8200 |
| Reranking hybrid Recall@100 | 0.9634 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 7 |
| Query length avg chars | 54.75 |
| Document length avg chars | 580.36 |

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
  task_name: hi
  split_name: hi
  language: hi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/hi.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1748
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 54.75
    document_mean: 580.364989
  bm25:
    ndcg_at_10: 0.30365714381890047
    hit_at_10: 0.52
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived
      data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
    - non-overlapping MIRACL Hindi train split data
    - Hindi Wikipedia question-to-passage retrieval pairs
    - Hindi open-domain QA evidence retrieval datasets
    synthetic_data:
      document_generation: Hindi Wikipedia-style passages with titles, aliases, dates,
        places, administrative roles, measurements, technical terms, and factual evidence
      question_generation: Hindi fact questions using varied किस, कौन, किसने, कितनी,
        कहाँ, कब, क्या, and किसके द्वारा forms
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
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3036571438
      hit_at_10: 0.52
      recall_at_100: 0.7048780488
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7048780488
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6846927026
      hit_at_10: 0.91
      recall_at_100: 0.9219512195
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9219512195
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5173709134
      hit_at_10: 0.82
      recall_at_100: 0.9634146341
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.035
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9634146341
      safeguard_positive_rows: 7
      rows_with_101_candidates: 7
```
