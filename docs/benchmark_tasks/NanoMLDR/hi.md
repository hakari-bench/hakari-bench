# NanoMLDR / hi

## Overview

`hi` is the Hindi split of NanoMLDR. Hindi questions retrieve long Hindi
articles, mostly encyclopedia-style documents, that contain the answer-bearing
paragraph.

## Details

### What the Original Data Measures

[M3-Embedding](https://arxiv.org/abs/2402.03216) evaluates MLDR as a
multilingual long-document retrieval benchmark. The [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR)
lists Hindi as Wikipedia-sourced and explains that questions are generated from
randomly selected article paragraphs.

### Observed Data Profile

The Nano split has 159 queries, 2,858 documents, and 159 positive qrels. Each
query has one positive. Queries average 79.18 characters and documents average
11,900.81 characters. Examples include banking, biography, university,
anatomy, and celebrity articles.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6515 and hit@10 = 0.7421, with 92 positives ranked first. It is a solid but
not complete lexical baseline: some questions use general wording that does not
strongly identify the article, and long documents may contain many competing
terms.

### Training Data That May Help

Useful training data includes Hindi Wikipedia QA retrieval, multilingual MLDR
training data, Hindi long-document QA, and hard negatives from articles sharing
entities, professions, or institutional names.

### Synthetic Data Guidance

Synthetic data should generate Hindi questions from a specific paragraph in a
long article. Hard negatives should be long Hindi documents from the same topic
cluster but without the answer-bearing paragraph.

## Example Data

| Query | Positive document |
| --- | --- |
| मेड़ता रोड रेलवे स्टेशन किस जिले में स्थित है? (46 chars) | नागौर नागौर (Nagaur) भारत के राजस्थान राज्य के नागौर ज़िले में स्थित एक ऐतिहासिक नगर है। अपने धार्मिक स्थलों के लिए प्रसिद्ध यह शहर ज़िले का मुख्यालय भी है। परिचय नागौर जिला 26°25' और 27°40' उत्तरी अक्षांश और 73°10' और 75°15' ... [truncated 225 chars](20341 chars) |
| यदि विधान परिषद् है तो, उसके सभापति और उपसभापति के वेतन और भत्ते क्या हैं? (74 chars) | सातवीं अनुसूची भारत के संविधान में राज्य सरकारों और केन्द्र सरकार के मध्य मुद्दों अथवा अधिकारों के बंटवारे के लिए विभिन्न अनुसूचियाँ परिभाषित की गयी हैं। इनमें से महत्त्वपूर्ण अनुच्छेद २४५ और २४६ के अन्तर्गत आते हैं। भारतीय स ... [truncated 225 chars](23699 chars) |
| आपके फोन में हिन्दी फॉण्ट उपलब्ध है क्या? (41 chars) | मोबाइल उपकरणों में हिन्दी समर्थन मोबाइल फोन आजकल हर व्यक्ति की आवश्यकता बन चुका है। इण्टरनेट पर हिन्दी के प्रयोक्ता ऐसा फोन चाहते हैं जिससे कि वे अपने फोन पर भी हिन्दी का प्रयोग कर सकें जिसमें कि हिन्दी साइटों की सर्फिंग, ईमे ... [truncated 225 chars](18819 chars) |
| क्या आप वृक्कीय ऊतकों के बारे में अधिक जानकारी दे सकते हैं जो उन्हें जीवित रखने के लिए आवश्यक होते हैं? (103 chars) | गुर्दा वृक्क या गुर्दे का जोड़ा एक मानव अंग हैं, जिनका प्रधान कार्य मूत्र उत्पादन (रक्त शोधन कर) करना है। गुर्दे बहुत से वर्टिब्रेट पशुओं में मिलते हैं। ये मूत्र-प्रणाली के अंग हैं। इनके द्वारा इलेक्त्रोलाइट, क्षार-अम्ल संतुल ... [truncated 225 chars](22815 chars) |
| क्या सन १९४७ के बाद सांस्कृतिक तीर्थों की उन्नति में कोई बदलाव हुआ है? (70 chars) | मथुरा मथुरा (Mathura) भारत के उत्तर प्रदेश राज्य के मथुरा ज़िले में स्थित एक नगर है। मथुरा ऐतिहासिक रूप से कुषाण राजवंश द्वारा राजधानी के रूप में विकसित नगर है। उससे पूर्व भगवान कृष्ण के समय काल से भी पूर्व अर्थात लगभग 7500 व ... [truncated 225 chars](18204 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMLDR |
| Backing dataset | NanoMLDR |
| Task / split | hi |
| Hugging Face dataset | [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR) |
| Language | hi |
| Category | natural_language |
| Queries | 159 |
| Documents | 2858 |
| Positive qrels | 159 |
| BM25 nDCG@10 | 0.6515 |
| BM25 hit@10 | 0.7421 |
| Query length avg chars | 79.18 |
| Document length avg chars | 11900.81 |

### Public Sources

- [M3-Embedding](https://arxiv.org/abs/2402.03216); 2024; Jianlv Chen et al.
- [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR)
- Source dataset: [Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | https://arxiv.org/abs/2402.03216 |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | https://huggingface.co/datasets/Shitao/MLDR |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMLDR
  backing_dataset: NanoMLDR
  dataset_id: hakari-bench/NanoMLDR
  task_name: hi
  split_name: hi
  language: hi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMLDR/hi.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 159
    documents: 2858
    positive_qrels: 159
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 79.18238993710692
    document_mean: 11900.811406578026
  bm25:
    ndcg_at_10: 0.6515063205133107
    hit_at_10: 0.7421383647798742
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MLDR Hindi split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMLDR hi queries, qrels, and positive documents
    useful_training_data:
      - Hindi long-document QA retrieval pairs
      - Hindi Wikipedia article retrieval
      - multilingual MLDR training data outside this Nano split
      - entity-sharing Hindi hard negatives
    synthetic_data:
      document_generation: long Hindi encyclopedic articles
      question_generation: paragraph-grounded Hindi questions
      answerability: positives should be full articles containing the answer-bearing paragraph
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMLDR
    source_urls:
      - label: M3-Embedding arXiv
        url: https://arxiv.org/abs/2402.03216
      - label: Shitao/MLDR
        url: https://huggingface.co/datasets/Shitao/MLDR
    source_notes: []
  references:
    - title: "M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation"
      url: https://arxiv.org/abs/2402.03216
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
```
