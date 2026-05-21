# MNanoBEIR / NanoBEIR-sr / NanoArguAna

## Overview

ArguAna is an argument-counterargument retrieval benchmark. `NanoBEIR-sr__NanoArguAna`
uses Serbian translated argumentative passages as queries and retrieves Serbian
translated counterarguments or closely paired arguments.

## Details

### What the Original Data Measures

[ArguAna](https://aclanthology.org/P18-1023/) is used in BEIR as argument
retrieval where relevance depends on argumentative relation, stance, and
response suitability. MMTEB provides the multilingual context.

### Observed Data Profile

The sampled task has 50 queries, 3,635 documents, and 50 positive qrels. Every
query has one positive. Queries are long argumentative passages averaging
1,182.86 characters, while documents average 989.77 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2817 and hit@10 = 0.5000. The median first-positive
rank is 10.5, so stance and counterargument matching are difficult for lexical
ranking.

### Training Data That May Help

Useful data includes non-overlapping argument retrieval, debate counterargument
pairs, stance-aware retrieval, and Serbian or multilingual argument mining data.
Exclude ArguAna, BEIR, NanoBEIR, and likely translated overlaps.

### Synthetic Data Guidance

Generate Serbian claims and counterarguments from non-evaluation debate text.
Hard negatives should address the same topic while answering a different
premise or stance.

## Example Data

| Query | Positive document |
| --- | --- |
| Javnost je apatična prema reformi. Da li bi reforma Doma lordova trebalo da bude glavni prioritet u trenutnoj ekonomskoj klimi je upitno, a kamoli da li bi koaliciona vlada bila sposobna da pokrene i sprovede takve mere. Poku ... [truncated 225 chars](737 chars) | Kampanja za alternativni glas ne može se porediti sa reformom Doma lordova, štaviše, ne treba mešati neinformisanu javnost usled političkog spinovanja sa apatijom. Često glasači izražavaju da su apatični jer osećaju da ne mog ... [truncated 225 chars](404 chars) |
| Proširenje Hitroua je od vitalnog značaja za ekonomiju. Širenje Hitroua bi osiguralo mnoga postojeća radna mesta, kao i stvaranje novih. Trenutno, Hitrou podržava oko 250.000 radnih mesta. [1] Povrh toga, još stotine hiljada ... [truncated 225 chars](1430 chars) | Poslovna zajednica je daleko od jedinstva u svom navodnom podržavanju treće piste. Ankete pokazuju da mnoge uticajne kompanije zapravo ne podržavaju proširenje. Pismo izražavajući zabrinutost potpisali su Džastin King, izvršn ... [truncated 225 chars](1272 chars) |
| Ljudi imaju previše izbora, što ih čini manje srećnim. Oglašavanje dovodi do toga da su mnogi preplavljeni beskrajnom potrebom da odlučuju između konkurentskih zahteva koji se bore za njihovu pažnju – ovo je poznato kao tiran ... [truncated 225 chars](1016 chars) | Ljudi su nesrećni jer ne mogu da imaju sve, a ne zato što im se daje previše izbora i to im stvara stres. Zapravo, reklame igraju ključnu ulogu u obezbeđivanju da novac koji ljudi imaju potroše na najprikladniji proizvod za s ... [truncated 225 chars](876 chars) |
| Kibernetički napadi se često izvode od strane ne-državnih aktera, kao što su kiberteroristi ili haktivisti (društveni aktivisti koji hakuju), bez ikakvog učešća same države. Na primer, 2007. godine masovan kibernetički napad ... [truncated 225 chars](941 chars) | U slučaju napada od strane nedržavnih aktera, mnogi praktičari međunarodnog prava slažu se da država i dalje može uzvratiti u samoodbrani ako druga država 'nije voljna ili nije u stanju da preduzme efikasne mere' u vezi sa na ... [truncated 225 chars](578 chars) |
| Pošto religija podstiče izvesnost u verovanju, mržnja nadahuta božanskim lako se koristi da opravda i promoviše nasilne radnje i diskriminatorne prakse. Sloboda govora mora biti na drugom mestu kada postoji mogućnost da taj g ... [truncated 225 chars](1259 chars) | Niko nije primoran da izvrši nasilne radnje zbog tuđih reči; to je njihov izbor. Isto tako, postoji mnogo ljudi koji zastupaju stavove koji bi se mogli smatrati homofobičnim, ali bi bili zgroženi nasilnim delima. U samim teme ... [truncated 225 chars](569 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sr |
| Task / split | NanoArguAna |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |
| Language | sr |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,635 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.2817 |
| BM25 hit@10 | 0.5000 |
| Query length avg chars | 1,182.86 |
| Document length avg chars | 989.77 |

### Public Sources

- [ArguAna source](https://aclanthology.org/P18-1023/), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Argument Mining for Understanding Peer Reviews | 2018 | task paper | https://aclanthology.org/P18-1023/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-sr
  dataset_id: hakari-bench/NanoBEIR-sr
  task_name: NanoArguAna
  split_name: NanoArguAna
  language: sr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoArguAna.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 3635, positive_qrels: 50}
  positives_per_query: {average: 1.0, min: 1, median: 1.0, max: 1, multi_positive_queries: 0, multi_positive_query_percent: 0.0}
  text_stats_chars: {query_mean: 1182.86, document_mean: 989.767263}
  bm25: {ndcg_at_10: 0.2817458475, hit_at_10: 0.5, source: dataset_bm25_column}
```
