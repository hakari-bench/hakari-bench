# MNanoBEIR / NanoBEIR-sr / NanoNFCorpus

## Overview

NanoBEIR-sr NanoNFCorpus is a Serbian biomedical and nutrition information
retrieval task derived from NFCorpus. Queries are very short translated health
or biomedical information needs, and documents are translated scientific or
medical passages. The task is demanding because almost every query has many
positive documents, while the query itself may be only a short phrase. It is
useful for evaluating whether retrieval models can connect Serbian consumer
health terms to long technical abstracts and recover a broad evidence set.

## Details

### What the Original Data Measures

NFCorpus was built from nutrition and health information needs with expert
relevance judgments over medical text. BEIR includes it as a domain-specific
biomedical retrieval task. The MNanoBEIR Serbian version keeps this health-
query to scientific-document structure after translation. It measures whether
models can retrieve medically relevant documents when the query may use
layperson wording, short keywords, or translated biomedical terminology.

### Observed Data Profile

This Nano subset contains 50 queries, 2,953 documents, and 1,651 positive
qrels. Nearly all queries are multi-positive, with an average of 33.02
positives per query, a minimum of 1, median of 23.50, and maximum of 100.
There are 47 multi-positive queries, covering 94.0% of the task. Queries are
extremely short at 23.08 characters on average, while documents average
1,522.71 characters. This creates a broad biomedical recall problem rather
than a simple one-answer retrieval task.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.1602,
hit@10 0.4200, and recall@100 0.0927. This is a very difficult lexical setting.
Short Serbian health queries provide few terms, and relevant abstracts may use
different scientific vocabulary, synonyms, or transliterated expressions. BM25
can retrieve some exact term matches, but it covers only a small fraction of
the positive evidence set. The low recall is especially important because many
queries have dozens of positives.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.2165, hit@10 0.5200, and recall@100 0.1545, improving over
BM25 across all reported metrics. Dense retrieval is better at connecting short
health phrases to related abstracts when exact wording differs. However, the
absolute recall remains low, which suggests that generic embeddings still
struggle with Serbian biomedical terminology and with the breadth of the
positive set. Domain adaptation would likely matter more here than in general
web retrieval tasks.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.22 and 11 safeguard rows. It reaches nDCG@10 0.1954, hit@10
0.5400, and recall@100 0.1484. Hybrid retrieval has the best hit@10 but trails
dense nDCG@10 and recall@100 slightly. This means lexical anchors can help
place at least one relevant abstract in the first page, while dense retrieval
is still better for broader semantic coverage. A final reranker would need to
use both biomedical term precision and semantic relevance.

### Metric Interpretation for Model Researchers

Because most queries have many positives, hit@10 is only a minimal success
signal. A model can find one relevant abstract and still miss most of the
evidence. Recall@100 is crucial, but the top-100 budget is tight when some
queries have up to 100 positives. The observed pattern shows that Serbian
NFCorpus is hard for all candidate profiles: dense retrieval improves coverage,
hybrid improves first-page presence, and BM25 alone is insufficient. This task
is best read as a biomedical domain stress test.

### Query and Relevance Type Tendencies

Queries are short health phrases or consumer biomedical questions, such as
healthy chocolate milkshake, medical ethics, beans, chicken nuggets, and
saturated fat. Relevant documents are long abstracts or scientific passages
with background, methods, and findings. The task favors models that can bridge
consumer wording and scientific language, handle synonyms and translations,
and retrieve multiple relevant documents for a health topic.

### Representative Failure Modes

BM25 may miss relevant abstracts that use different biomedical terminology or
do not repeat the short query terms. Dense models may retrieve broadly related
medical documents that are not directly relevant to the query's condition,
food, or finding. Hybrid retrieval can improve first-page hits but still fails
to cover enough positives. Translation and transliteration of medical terms
can further fragment both lexical and semantic matching.

### Training Data That May Help

Helpful training data includes non-overlapping biomedical retrieval, Serbian
medical QA, consumer health search, scientific abstract retrieval, nutrition
QA, and multi-positive relevance training. Hard negatives should share
symptoms, foods, interventions, or organisms while addressing a different
finding or population. Training should exclude NFCorpus, BEIR, NanoBEIR, and
overlapping translated abstracts.

### Model Improvement Notes

NanoNFCorpus-sr is a demanding biomedical retrieval benchmark with short
queries and many positives. Improvements should focus on biomedical domain
embeddings, Serbian medical terminology, synonym and transliteration handling,
and reranking that distinguishes direct health evidence from loose topical
similarity. Researchers should inspect both early precision and evidence-set
coverage, because no candidate profile provides high recall in this subset.

## Example Data

| Query | Positive document |
| --- | --- |
| Zdrav čokoladni milkshake [25 chars] | Cilj Ispitati odnos između unosa trešanja i rizika od ponovljenih napada gihta kod osoba sa gihtom. Metode Sproveli smo studiju preseka slučajeva kako bismo ispitali povezanost niza pretpostavljenih faktora rizika s ponovljenim napadima gihta. Osobe sa gihtom su prospektivno regrutovane i praćene onlajn tokom jedne godine. Učesnici su bili upitani o sledećim informacijama prilikom doživljavanja napada gihta: datum početka napada gihta, simptomi i znaci, lekovi (uključujući lekove protiv gihta) i potencijalni faktori rizika (uključujući dnevni unos trešanja i ekstrakta trešanja) tokom dvodnevnog perioda pre napada gihta. Procenili smo iste informacije o izloženosti tokom dvodnevnih kontrolnih perioda. Procenili smo rizik od ponovljenih napada gihta povezanih s unosom trešanja koristeći uslovnu logističku regresiju. Rezultati Naša studija je uključila 633 osobe sa gihtom. Unos trešanja tokom dvodnevnog perioda bio je povezan s 35% nižim rizikom od napada gihta u poređenju s neunosom (mul... [1,000 / 1,596 chars] |
| medicinska etika [16 chars] | POZADINA: Jedan od glavnih problema u kontroli holesterola u krvi putem dijetetskih mera čini se potreba za poboljšanjem pridržavanja pacijenata preporukama. CILJEVI: Ispitati brojna pitanja u vezi s preprekama i motivatorima za pridržavanje holesterol-snižavajuće dijete. METODE: Anketirali smo francuske lekare opšte prakse o njihovim dijetetskim postupcima za pacijente sa hiperholesterolemijom i ispitali stavove njihovih pacijenata prema takvom pristupu. REZULTATI: Analizirali smo 234 lična upitnika lekara i 356 upitnika za samoopservaciju pacijenata. Razlozi pacijenata za nepoštovanje propisane dijete uključivali su: 'već imaju zadovoljavajuće prehrambene navike' (34,7%), 'nespremnost da trpe nutricionističku deprivaciju' (33,3%), 'poteškoće u usklađivanju dijete sa porodičnim životom' (27,8%) i 'uzimanje lekova za snižavanje holesterola' (22,2%). Uprkos opštenito dobrom razumevanju preporuka lekara od strane pacijenata, primećene su određene razlike između njihovih izjava. Dok su le... [1,000 / 1,853 chars] |
| grah [4 chars] | Tokom proteklih 20 godina, rastući interes za biohemiju, ishranu i farmakologiju L-arginina doveo je do opsežnih studija koje istražuju njegovu nutritivnu i terapeutsku ulogu u lečenju i prevenciji metaboličkih poremećaja kod ljudi. Sve brojniji dokazi pokazuju da dodatak L-arginina ishrani smanjuje gojaznost kod genetski gojaznih pacova, pacova sa gojaznošću izazvanom ishranom, tovnih svinja i gojaznih ljudi sa dijabetesom tipa 2. Mehanizmi odgovorni za blagotvorne efekte L-arginina verovatno su složeni, ali u konačnici uključuju promenu ravnoteže unosa i potrošnje energije u korist gubitka masti ili smanjenog rasta belog masnog tkiva. Nedavne studije ukazuju da dodatak L-arginina podstiče biogenezu mitohondrija i razvoj smedeg masnog tkiva, verovatno kroz pojačanu sintezu ćelijskih signalnih molekula (npr. azot monoksida, ugljen monoksida, poliamina, cGMP i cAMP) kao i povećanu ekspresiju gena koji podstiču oksidaciju energetskih supstrata u celom telu (npr. glukoze i masnih kiselina... [1,000 / 1,179 chars] |

### Public Sources

- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-sr dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | [https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
