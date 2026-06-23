# MNanoBEIR / NanoBEIR-it / NanoNFCorpus

## Overview

`NanoBEIR-it__NanoNFCorpus` is the Italian NanoBEIR version of NFCorpus, a
medical and nutrition information retrieval benchmark. The task uses Italian
translated health-related queries and Italian translated biomedical documents.
This split contains 50 queries, 2,953 documents, and 1,651 positive qrels. It is
highly multi-positive: the average query has 33.02 positives, the median is
23.50, and 47 of 50 queries have more than one relevant document. The task is
therefore not mainly about finding one exact answer passage. It tests whether a
retriever can cover many relevant biomedical abstracts for short health phrases,
while still ranking the most useful documents near the top.

## Details

### What the Original Data Measures

[NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
was built for medical information retrieval over nutrition and health claims.
It includes queries that may look like consumer health searches, medical topic
phrases, or short questions, and it maps them to scientific and biomedical
documents. BEIR includes NFCorpus as a domain-specific retrieval benchmark, and
the Italian NanoBEIR task exposes the same biomedical retrieval problem through
translated queries and documents. The resulting benchmark is useful for studying
domain vocabulary, layperson-to-technical matching, synonymy, and high-recall
retrieval under many-positive relevance judgments.

### Observed Data Profile

The dataset profile is very different from single-answer web retrieval. Queries
are short, averaging 28.52 characters, while documents are long biomedical
abstracts averaging 1,725.46 characters. There are 1,651 positive qrels for only
50 queries, with positives per query ranging from 1 to 100. This means that
top-10 metrics measure whether the model can rank especially central relevant
documents, while Recall@100 measures only a fraction of the total relevant set
for broad queries. Short phrases such as foods, nutrients, symptoms, or medical
concepts can have many relevant abstracts and many close distractors.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.3016, hit@10 = 0.7200, and
Recall@100 = 0.1478. BM25 is the strongest profile on hit@10 and is narrowly the
best on nDCG@10. This reflects the importance of exact biomedical terminology:
when a query contains a food name, compound, condition, or phrase that appears
in abstracts, lexical matching can identify strong candidates quickly. However,
the Recall@100 score is low because many relevant documents do not fit into the
first 100 positions, and broad medical topics often have large pools of
potentially relevant literature. BM25 is useful for precise anchors but cannot
cover the full judged set.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.2450, hit@10 =
0.6200, and Recall@100 = 0.1823. Dense retrieval improves relevant coverage at
100 compared with BM25, but it ranks fewer positives in the top 10. This pattern
is important: embedding similarity helps find semantically related abstracts
that may not repeat the exact query words, yet it may also spread probability
mass across broad biomedical neighborhoods. For NFCorpus, a dense model can be
better at exploration and worse at early precision unless it has strong medical
domain alignment and hard-negative training.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.3005, hit@10 = 0.6600, and Recall@100 = 0.1908. Six queries use the
rank-101 safeguard. The hybrid result nearly matches BM25 on nDCG@10 and
provides the best Recall@100 among the three profiles. This is a useful hybrid
signature for biomedical retrieval: lexical matching keeps exact domain terms
near the top, while dense matching adds semantically related abstracts that
increase coverage. The tradeoff is that hybrid top-10 hit rate remains below
BM25, so candidate fusion alone does not fully solve early precision.

### Metric Interpretation for Model Researchers

This task should be interpreted as a precision-and-coverage tradeoff. BM25 is
strongest for top-rank lexical anchoring, dense retrieval is better for broad
semantic coverage, and hybrid retrieval gives the best top-100 coverage while
retaining BM25-like nDCG@10. Because most queries have many positives,
Recall@100 is naturally low even for the best profile. A model that improves
NFCorpus should not only lift nDCG@10, but also increase the diversity of
relevant biomedical documents retrieved for broad health topics. Error analysis
should separate failures caused by missing medical synonyms from failures caused
by ranking general topical abstracts above documents that directly address the
query.

### Query and Relevance Type Tendencies

The sample queries include short phrases such as "fave" and "Grassi saturi",
layperson questions such as "Cosa contengono esattamente i nugget di pollo?",
and general health concepts such as medical ethics. Positive documents are
often long abstracts with sections, objectives, methods, and conclusions.
Relevance can depend on technical terms, biomedical entities, population
descriptions, interventions, or claims. This makes the task sensitive to both
Italian surface forms and domain-specific semantic equivalence.

### Representative Failure Modes

BM25 can under-retrieve relevant abstracts that use technical synonyms,
alternative spellings, or related biomedical concepts instead of the exact query
phrase. Dense retrieval can overgeneralize and return broad health or nutrition
documents that are semantically close but not judged relevant. Hybrid retrieval
can improve coverage but may still rank dense topical matches above exact
domain-term hits. For multi-positive queries, another common failure is low
result diversity: the model may retrieve many similar abstracts while missing
other relevant subtopics.

### Training Data That May Help

Useful training data includes non-overlapping biomedical retrieval, nutrition
question answering, clinical abstract retrieval, and multilingual health search
pairs. Italian or multilingual biomedical terminology resources can help with
translation variation and synonym matching. Training should exclude NFCorpus,
BEIR, NanoBEIR, and overlapping medical abstracts or translated variants from
this benchmark.

### Model Improvement Notes

A strong model for this task should combine exact domain-term sensitivity with
semantic expansion over biomedical concepts. Candidate generation should keep
BM25-like anchors for precise terms, while ranking should learn which abstracts
directly satisfy the health information need. Hard negatives are especially
important: they should share foods, symptoms, organisms, or interventions with
the query while differing in the claim or biomedical finding.

## Example Data

| Query | Positive document |
| --- | --- |
| Frullati di cioccolato salutari [31 chars] | Obiettivo: Studiare la relazione tra il consumo di ciliegie e il rischio di attacchi di gotta ricorrenti tra individui affetti da gotta. Metodi: Abbiamo condotto uno studio caso-crossover per esaminare le associazioni di un insieme di fattori di rischio putativi con attacchi di gotta ricorrenti. Gli individui con gotta sono stati reclutati prospetticamente e seguiti online per un anno. Ai partecipanti è stato chiesto di fornire le seguenti informazioni in caso di attacco di gotta: la data di insorgenza dell'attacco, i sintomi e i segni, i farmaci (inclusi i farmaci anti-gotta) e i potenziali fattori di rischio (incluso il consumo quotidiano di ciliegie e estratto di ciliegia) nel periodo di 2 giorni precedente all'attacco di gotta. Abbiamo valutato le stesse informazioni di esposizione in periodi di controllo di 2 giorni. Abbiamo stimato il rischio di attacchi di gotta ricorrenti correlati al consumo di ciliegie utilizzando la regressione logistica condizionale. Risultati: Il nostro st... [1,000 / 1,901 chars] |
| etica medica [12 chars] | SFONDO: Uno dei principali problemi nel controllare il colesterolo sierico attraverso l'intervento dietetico sembra essere la necessità di migliorare l'aderenza del paziente. OBIETTIVI: Esplorare le molte domande riguardanti le barriere e i motivatori per l'aderenza a una dieta ipocolesterolemizzante. METODI: Abbiamo indagato le pratiche dietetiche dei medici di base francesi per i pazienti con ipercolesterolemia e abbiamo esaminato l'atteggiamento dei loro pazienti verso tale approccio. RISULTATI: Abbiamo analizzato 234 questionari personali dei medici e 356 questionari di autovalutazione dei pazienti. Le ragioni dei pazienti per non seguire la dieta prescritta includono: 'avere già abitudini alimentari soddisfacenti' (34,7%), 'non voler soffrire di privazioni nutrizionali' (33,3%), 'difficoltà a conciliare la dieta con la vita familiare' (27,8%) e 'assumere farmaci per abbassare il colesterolo' (22,2%). Nonostante una comprensione generalmente buona delle raccomandazioni dei medici d... [1,000 / 2,032 chars] |
| fave [4 chars] | Negli ultimi 20 anni, l'interesse crescente per la biochimica, la nutrizione e la farmacologia della L-arginina ha portato a studi estesi per esplorare i suoi ruoli nutrizionali e terapeutici nel trattamento e nella prevenzione dei disturbi metabolici umani. Le evidenze emergenti mostrano che l'integrazione dietetica di L-arginina riduce l'adiposità nei ratti geneticamente obesi, nei ratti obesi per dieta, nei maiali da ingrasso e nei soggetti umani obesi con diabete di tipo 2. I meccanismi responsabili degli effetti benefici della L-arginina sono probabilmente complessi, ma coinvolgono infine la modifica dell'equilibrio tra l'assunzione e il dispendio energetico a favore della perdita di grasso o della riduzione della crescita del tessuto adiposo bianco. Studi recenti indicano che l'integrazione di L-arginina stimola la biogenesi mitocondriale e lo sviluppo del tessuto adiposo bruno, possibilmente attraverso la sintesi aumentata di molecole di segnalazione cellulare (ad esempio, ossid... [1,000 / 1,443 chars] |

### Public Sources

- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | [https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
