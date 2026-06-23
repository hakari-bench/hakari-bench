# MNanoBEIR / NanoBEIR-sr / NanoSCIDOCS

## Overview

NanoSCIDOCS in the Serbian NanoBEIR slice is a scientific-document retrieval task derived from SCIDOCS and related SPECTER evaluation work. The queries are Serbian translated scientific paper titles or short descriptions, and the corpus contains Serbian translated scientific abstracts. The task asks a retriever to find papers that are scientifically related to the query paper, often through topical, methodological, or citation-style similarity rather than direct answer support. This makes it a compact diagnostic for academic search behavior in a multilingual setting.

## Details

### What the Original Data Measures

SCIDOCS measures scientific document similarity and retrieval, with relevance grounded in scholarly relationships such as citation, co-citation, and paper relatedness. In retrieval form, the model must connect a paper-like query to other papers that belong in the same research neighborhood. Compared with web QA tasks, the relevant documents are not answer passages; they are related scientific abstracts.

The Serbian translated version adds multilingual retrieval pressure on technical terminology, transliterated names, and domain phrases. Some scientific terms remain lexically similar across languages, while surrounding syntax and morphology change. A useful model must therefore combine lexical anchors such as method names with broader semantic understanding of research contribution and domain context.

### Observed Data Profile

The task contains 50 queries, 2,210 documents, and 244 relevance judgments. Every query is multi-positive, with an average of 4.88 positives per query. The minimum number of positives is 3, the median is 5.0, and the maximum is 5, so the task consistently evaluates ranked retrieval of a relevant set rather than single-target lookup.

Queries average 77.12 characters, while documents average 944.48 characters. The documents are long scientific abstracts, and the queries are usually compact scientific titles. This asymmetry creates a strong title-to-abstract matching problem: the query names a method, system, or research topic, while the positive abstracts may describe related work with more explanatory vocabulary.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2561, hit@10 of 0.7600, and recall@100 of 0.4836 using the top-500 BM25 candidate subset. The relatively high hit@10 shows that exact scientific terminology can often locate at least one related abstract. However, recall@100 is low for a multi-positive task, and nDCG@10 remains modest because BM25 struggles to rank the full related-paper set.

This is a typical pattern for scientific retrieval. Technical words, acronyms, and domain nouns are valuable lexical signals, but relatedness is not the same as word overlap. BM25 can over-rank abstracts that share terminology with the query while missing papers that express the same method or problem using different vocabulary. For model researchers, this task exposes whether lexical candidate generation is broad enough for multi-positive scientific search.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3382, hit@10 of 0.8400, and recall@100 of 0.6189. Dense retrieval improves all three metrics over BM25, especially recall@100. This indicates that embedding similarity captures scientific relatedness beyond exact term overlap, helping retrieve abstracts that are conceptually close to the query even when the wording differs.

The dense advantage is meaningful but not overwhelming. Scientific abstracts often contain dense technical vocabulary, and many relevant relations depend on fine-grained methodology, task setting, or contribution type. A general dense model may find the right topical area while still confusing adjacent subfields or ranking only the most obvious positives. The multi-positive structure makes those ranking errors visible.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3229, hit@10 of 0.8600, and recall@100 of 0.6311. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 1 safeguard row and a mean of 100.02 candidates. The hybrid profile has the best hit@10 and recall@100, while dense retrieval has the best nDCG@10.

This suggests that hybrid search is useful for coverage on NanoSCIDOCS-sr. Combining lexical scientific terms with dense similarity brings more positives into the candidate pool. However, the dense ordering is slightly stronger at the very top. A later reranker could benefit from the hybrid candidate set, but the first-stage hybrid ordering alone does not fully solve fine-grained scientific relatedness ranking.

### Metric Interpretation for Model Researchers

Because every query has multiple positives, recall@100 is especially important. A model that retrieves only one obvious related paper can still achieve a decent hit@10, but it will not represent the full relevant set. nDCG@10 measures whether several of those positives rise near the top, which is important for academic search and recommendation scenarios.

The metric spread shows three different behaviors. BM25 is useful for high-precision lexical anchors but has weak relevant-set coverage. Dense retrieval better captures semantic relatedness and provides the strongest top-10 graded ranking. reranking_hybrid gives the broadest candidate coverage, making it a strong input for a second-stage model that can inspect abstracts more deeply.

### Query and Relevance Type Tendencies

Queries are scientific titles such as a new DC-DC converter, sparse Gaussian Markov random field learning, texture synthesis using convolutional neural networks, RFID antenna design, and digital heart-rate monitoring. Positives are abstracts from related papers, often in the same technical area or methodological family.

The task therefore rewards models that understand scientific phrase structure: method names, devices, experimental settings, and field-specific terminology. It also punishes overly broad topic matching. A paper about neural networks is not automatically relevant to every neural network title; the relation may depend on the specific application, architecture, or evaluation context.

### Representative Failure Modes

Likely failures include retrieving abstracts from the same broad field but with a different contribution, overvaluing repeated acronyms, missing related papers that use alternative technical terms, and ranking one obvious positive while failing to recover the remaining relevant set. Dense models may blur neighboring subfields, while BM25 may be brittle when Serbian translations alter technical phrasing or morphology.

### Training Data That May Help

Helpful data includes scientific-paper retrieval, citation and co-citation ranking, paper recommendation data, multilingual academic abstracts, and hard negatives from the same research field. Serbian scientific abstracts are useful for language coverage, but domain-transfer data from English scientific retrieval may also help if the model has strong multilingual alignment. For reranking, negatives should be close: same field, similar terminology, but a different contribution or method.

### Model Improvement Notes

A model targeting this task should improve multi-positive coverage without sacrificing top-rank precision. Dense retrievers need better discrimination among adjacent scientific topics, while lexical systems need normalization and term expansion that preserve technical specificity. Hybrid systems look promising because they combine terminology and semantics, but the final ranking should explicitly model scientific relatedness rather than treating lexical and embedding scores as sufficient on their own.

## Example Data

| Query | Positive document |
| --- | --- |
| Novi DC-DC višestepeni pojačavački pretvarač [44 chars] | Apstrakt Višenaponski pretvarači sa više nivoa postaju nova vrsta opcija za pretvarače snage u primenama velike snage. Višenaponski pretvarači tipično sintetizuju stepenasti naponski talas iz nekoliko nivoa napona istosmernih kondenzatora. Jedno od glavnih ograničenja višenivo pretvarača je neravnoteža napona između različitih nivoa. Tehnike za balansiranje napona između različitih nivoa obično uključuju stezanje napona ili kontrolu punjenja kondenzatora. Postoji nekoliko načina za postizanje naponske ravnoteže u višenivo pretvaračima. Bez razmatranja tradicionalnih magnetski spregnutih pretvarača, ovaj rad predstavlja tri nedavno razvijena višenaponska pretvarača: 1) diodno-vezani, 2) leteći kondenzatori i 3) kaskadni pretvarači sa odvojenim istosmernim izvorima. Biće razmotreni princip rada, karakteristike, ograničenja i potencijalne primene ovih pretvarača. [872 chars] |
| Brzo Učenje Retkih Gaussovih Markovljevih Slučajnih Polja Bazirano na Čoleskijevoj Faktorizaciji [96 chars] | Poštovani korisniče, Zahvaljujem vam se što ste me kontaktirali. Kao veštačka inteligencija, moja osnovna svrha je pružanje informacija i pomoći u različitim oblastima. Nažalost, trenutno nemam pristup spoljnim bazama podataka ili internetu, tako da ne mogu da vam pružim najnovije informacije ili pristup aktuelnim sadržajima. Međutim, imam opsežnu internu bazu znanja koja obuhvata širok spektar tema do mog poslednjeg ažuriranja. Radovaću na tome da vam pružim najtačnije i najkorisnije informacije na osnovu dostupnih podataka. Molim vas da postavite svoje pitanje ili opišete svoj zahtev, i biće mi zadovoljstvo da vam pomognem na najbolji mogući način. Srdačno, Vaš AI asistent [687 chars] |
| Sinteza teksture korišćenjem konvolucionih neuronskih mreža [59 chars] | U ovom radu istražujemo uticaj dubine konvolucione mreže na njenu tačnost u okruženju za prepoznavanje slika velikih razmera. Naš glavni doprinos je temeljna evaluacija mreža sve veće dubine, koja pokazuje da se značajno poboljšanje u odnosu na prethodne konfiguracije može postići povedanjem dubine na 16–19 slojeva težina. Ovi nalazi bili su osnova našeg prijavnog rada za ImageNet Challenge 2014, gde je naš tim osigurao prvo i drugo mesto u kategorijama za lokalizaciju i klasifikaciju respektivno. Takođe pokazujemo da se naše reprezentacije dobro generalizuju na druge skupove podataka, gde postižu vrhunske rezultate. Što je posebno važno, naša dva najbolja modela konvolucione mreže učinili smo javno dostupnim kako bismo olakšali dalja istraživanja upotrebe dubokih vizuelnih reprezentacija u računarskom vidu. [819 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original task context | [SPECTER](https://arxiv.org/abs/2004.07180) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sr dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |

Representative query and positive abstract snippets:

| Query | Positive document snippet |
| --- | --- |
| Novi DC-DC višestepeni pojačavački pretvarač | Apstrakt Višenaponski pretvarači sa više nivoa postaju nova vrsta opcija za pretvarače snage... |
| Brzo Učenje Retkih Gaussovih Markovljevih Slučajnih Polja Bazirano na Čoleskijevoj Faktorizaciji | Poštovani korisniče, Zahvaljujem vam se što ste me kontaktirali... |
| Sinteza teksture korišćenjem konvolucionih neuronskih mreža | U ovom radu istražujemo uticaj dubine konvolucione mreže na njenu tačnost... |
| Planarna širokopojasna prstenasta antena sa kružnom polarizacijom za RFID sistem | U ovom radu predlaže se tehnika horizontalno meandrirajuće trake (HMS)... |
| Dizajn naprednog digitalnog monitora srčanog ritma korišćenjem osnovnih elektronskih komponenti | U ovom radu, predstavili smo dizajn i razvoj novog integrisanog uređaja za merenje srčanog ritma... |
