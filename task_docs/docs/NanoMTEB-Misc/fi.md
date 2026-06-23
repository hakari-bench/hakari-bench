# NanoMTEB-Misc / fi

## Overview

`fi` is the Finnish EuroPIRQ retrieval split. Queries are synthetic Finnish
questions, and documents are Finnish passages derived from DGT-Acquis
paragraph-level European Union legal and administrative text. The Nano split
contains 100 queries, 9,422 documents, and 100 positive qrels, with exactly one
positive passage per query. Queries average 146.53 characters, and documents
average 594.55 characters. The task tests Finnish retrieval over formal EU
institutional language, where exact legal terms, inflected forms, directive
numbers, and institutional names all affect passage selection.

## Details

### What the Original Data Measures

The [EuroPIRQ dataset card](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval)
describes a retrieval dataset built from DGT-Acquis paragraph-level text. It
extracts, cleans, language-validates, aligns English, Finnish, and Portuguese
chunks, and generates 100 synthetic questions per language. No standalone
EuroPIRQ task paper was confirmed; this description is based on the dataset
card and MTEB/MMTEB benchmark context.

In the Finnish split, the model must retrieve the source Finnish passage for a
synthetic question about EU law, administration, committees, courts, or policy.
The source language and formal register make morphology and legal boilerplate
important.

### Observed Data Profile

The split has 100 Finnish queries, 9,422 documents, and 100 positive judgments.
Every query has one positive. Questions are long and specific, often naming EU
institutions, directives, offices, or legal mechanisms. Documents are formal
Finnish passages with dense administrative and legal wording.

Examples ask about data-protection reasoning, the role of ECoB, health and
safety of pregnant and breastfeeding mothers, maritime governance, and Directive
98/37/EC machinery safety obligations.

### BM25 Evaluation Profile

BM25 is strongest, with nDCG@10 of 0.9092, hit@10 of 0.9500, and recall@100 of
0.9900. Synthetic questions often retain distinctive terms from the positive
passage, and BM25 benefits from legal entities, directive numbers, and
institutional phrases.

Finnish morphology makes this slightly harder than the English split. Inflected
forms and legal phrase variation can reduce exact overlap, but the lexical
signal remains dominant.

### Dense Evaluation Profile

Dense retrieval reaches nDCG@10 of 0.8542, hit@10 of 0.9200, and recall@100 of
0.9300. It handles many semantic matches but loses some candidates that BM25
recovers through exact legal wording. This indicates that the dense model can
represent Finnish EU-domain meaning, but may not preserve enough specific
surface detail for near-ceiling performance.

Dense errors are likely to involve near-duplicate legal passages or passages
with similar institutional framing.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.8813, hit@10 of 0.9300,
and recall@100 of 1.0000. It has complete top-100 coverage, but its top-10
ordering remains below BM25. There are no safeguard-positive rows.

Hybrid search is therefore a strong candidate-generation option: it recovers
the positive for every query by rank 100, while still relying on a reranker to
match BM25's early precision.

### Metric Interpretation for Model Researchers

`fi` is BM25-favorable at top-10, with hybrid search best for recall. The task
is near ceiling for lexical retrieval, so the main diagnostic is whether dense
or hybrid systems preserve exact Finnish legal references and formal wording.
Since every query has one positive, nDCG@10 directly reflects rank of the source
passage.

This split is useful for Finnish legal-domain precision and regression testing
rather than broad semantic difficulty.

### Query and Relevance Type Tendencies

Queries are Finnish synthetic questions about EU legal and administrative
passages. Positive documents are formal passages from DGT-Acquis-derived
content. Many queries include exact institutional names, directive numbers, or
specialized legal concepts.

Relevance is source-passage identity. Similar EU boilerplate can create hard
negatives if it does not answer the generated question.

### Representative Failure Modes

BM25 can confuse passages with similar directive numbers or repeated EU legal
phrases. Dense retrieval can rank semantically similar legal text that lacks the
specific condition asked in the question. Hybrid retrieval improves coverage
but can still rank near-duplicate legal passages above the target.

Finnish inflection and compound terminology are additional sources of lexical
and embedding mismatch.

### Training Data That May Help

Useful training data includes Finnish legal retrieval pairs, multilingual EU
parallel corpora, DGT-Acquis-style passage pairs, and synthetic question-passage
training. Hard negatives should come from similar EU committee, court, and
directive passages. Training should exclude EuroPIRQ evaluation questions and
positive passages overlapping this Nano split.

Synthetic data should mix surface-overlap questions with paraphrased questions
that require semantic matching across Finnish inflected forms.

### Model Improvement Notes

Models should preserve Finnish legal entities, directive numbers, and
morphological variants. Dense encoders can improve through Finnish legal hard
negatives. Rerankers should compare the asked legal condition against the exact
passage details.

## Example Data

| Query | Positive document |
| --- | --- |
| Mikä on tietosuojavaltuutetun perustelu sille, että tietojen tallentamistoimenpiteiden tarkempi tutk... [100 / 122 chars] | Tietosuojavaltuutettu myöntää, että käytettävissä on vähemmän tietoja, jos käytössä on tietojen tallentamisen kaltainen järjestelmä laajemman tietojen säilyttämisjärjestelmän sijasta. Tietojen tallent... [200 / 705 chars] |
| Mikä rooli Eurooppalaisella viljelykasvien rinnakkaiselon toimistolla (ECo B) on kansallisten toimen... [100 / 252 chars] | COEX-NET-työryhmän kautta tapahtuvaa koordinointia ja Eurooppalaisen viljelykasvien rinnakkaiselon toimiston (ECo B) kautta annettavaa teknistä neuvontaa on tarkoitus jatkaa. ECo B pitää ajan tasalla... [200 / 607 chars] |
| Miten ehdotus direktiiviksi yhdistää raskaana olevien ja imettävien äitien terveyden ja turvallisuud... [100 / 140 chars] | Käsillä olevan ehdotuksen pääasiallinen oikeusperusta on raskaana olevien ja imettävien äitien terveys ja turvallisuus. Terveys- ja turvallisuuskysymyksillä on kuitenkin looginen yhteys i) lasten oike... [200 / 572 chars] |
| Mitä lähestymistapaa ETSK tukee voimakkaasti merialan toiminnan hallinnassa, ja miksi tätä lähestymi... [100 / 125 chars] | ETSK on antanut kaksi lausuntoa nyt esitetyn tiedonannon edeltäjistä eli 26. huhtikuuta 2007 lausunnon tiedonannosta Euroopan unionin tuleva meripolitiikka: meriä ja valtameriä koskeva eurooppalainen... [200 / 570 chars] |
| Mitä toimenpiteitä jäsenvaltioiden on toteutettava direktiivin 98/37/EY 2 artiklan 1 kohdan mukaises... [100 / 143 chars] | Koneita koskevan jäsenvaltioiden lainsäädännön lähentämisestä annetun direktiivin 98/37/EY (jota sovellettiin 29 päivään joulukuuta 2009 asti) 2 artiklan 1 kohdassa säädetään, että jäsenvaltioiden on... [200 / 606 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| EuroPIRQ-retrieval | 2025 | Dataset card | [https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | Benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| MTEB: Massive Text Embedding Benchmark | 2022 | Benchmark paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| A Finnish question about the data-protection supervisor's justification for examining storage measures. | A Finnish passage comparing data storage with broader data-retention systems. |
| A Finnish question about ECoB's role in national coexistence measures. | A passage on COEX-NET coordination and European Coexistence Bureau technical advice. |
| A Finnish question about pregnant and breastfeeding mothers' health and employment. | A passage linking health and safety to children's care and career opportunities. |
| A Finnish question about maritime governance approach supported by the EESC. | A passage discussing prior EESC opinions on EU maritime policy. |
| A Finnish question about Directive 98/37/EC and machinery safety. | A passage on Member State obligations under Article 2(1). |
