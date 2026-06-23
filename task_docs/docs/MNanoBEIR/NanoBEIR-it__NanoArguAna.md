# MNanoBEIR / NanoBEIR-it / NanoArguAna

## Overview

This task is the Italian NanoBEIR version of ArguAna, an argument-counterargument retrieval benchmark. The original ArguAna task studies retrieval of the best counterargument for a given argument, using debate-style text where a relevant document usually shares the issue but takes an opposing stance. In this NanoBEIR slice, Italian translated argumentative passages must retrieve Italian translated counterarguments from 3,635 candidate documents. The task contains 50 queries and 50 positive relevance judgments, with exactly one positive per query. It is a compact benchmark for long-form argument retrieval, where models must distinguish the correct rebuttal from same-topic arguments that may share many words but respond to a different premise or support the same side.

## Details

### What the Original Data Measures

ArguAna measures argument-to-counterargument retrieval. A strong retriever should find the passage that challenges the query's central claim or premise. This is different from ordinary topical search because the correct document can be lexically similar while reversing stance, and many hard negatives can discuss the same issue without being the intended rebuttal. The task therefore tests argument structure, stance relation, and premise-level alignment.

### Observed Data Profile

The Italian Nano task has 50 queries, 3,635 documents, and 50 positives. Every query has one positive. Queries are long, averaging about 1,187 characters, and documents average about 1,102 characters. Example topics include reform apathy, Heathrow expansion, excessive consumer choice, cyberattacks by non-state actors, and religiously motivated speech. Both sides are long translated debate passages with claims, supporting reasons, examples, and citations.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.393, Hit@10 of 0.700, and Recall@100 of 0.880. Sparse retrieval gets useful candidate coverage because counterarguments share topic vocabulary, named policies, institutions, or controversy-specific terms. However, BM25 is limited at top ranking: term overlap does not tell whether a passage is a rebuttal, a supporting argument, or a different aspect of the same debate.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline performs best, with nDCG@10 of 0.471, Hit@10 of 0.740, and Recall@100 of 0.980. Dense retrieval better captures long-passage argumentative fit and paraphrased premise relation. It also substantially improves recall over BM25, suggesting that some counterarguments are semantically aligned without repeating enough exact terms. Dense is the strongest direct ranker in this Italian slice.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.414, Hit@10 of 0.720, and Recall@100 of 0.980, with one safeguard row at 101 candidates. It matches dense recall but trails dense ranking. This indicates that hybrid search is useful as a candidate generator, while dense semantic similarity is better calibrated for the top of the ranking. A stance-aware reranker would likely benefit from the hybrid pool.

### Metric Interpretation for Model Researchers

Because each query has one positive, Recall@100 directly measures whether the correct counterargument is available for later reranking. nDCG@10 and Hit@10 measure whether the retriever itself places the rebuttal early. The dense-versus-hybrid pattern is important: candidate coverage is high for both, but dense is better at ordering rebuttals above same-topic distractors.

### Query and Relevance Type Tendencies

Queries are long Italian arguments about controversial issues. Relevant documents are paired counterarguments, not generic answer passages. Hard negatives can share the issue and many terms while taking the same stance or answering a different premise. The task is sensitive to stance reversal, premise targeting, and discourse-level similarity.

### Representative Failure Modes

BM25 can retrieve a same-topic support passage because it shares many terms. Dense retrieval can retrieve an argument that is broadly semantically related but not the paired counterargument. Hybrid retrieval can include the positive but still rank a lexical distractor too high. Failure analysis should ask whether the retrieved passage actually challenges the query's central claim.

### Training and Leakage Considerations

Training should exclude ArguAna, BEIR, NanoBEIR, and translated argument records likely to overlap with this evaluation slice. Useful non-overlapping data includes argument-counterargument pairs, debate retrieval data, stance-aware retrieval datasets, and Italian or multilingual argument mining corpora. Synthetic data should create paired pro and con arguments with same-topic hard negatives.

### Model Improvement Signals

Strong models should improve stance-sensitive long-passage ranking while preserving topic coverage. Useful signals include premise-targeted rebuttals, same-topic same-stance hard negatives, multilingual argument mining data, and long-context contrastive examples. Hybrid systems should use BM25 for issue anchoring and dense or cross-encoder scoring for rebuttal relation.

## Example Data

| Query | Positive document |
| --- | --- |
| Il pubblico è indifferente alle riforme. Se la riforma della Camera dei Lord dovrebbe essere una priorità assoluta nel clima economico attuale è discutibile, figuriamoci se un governo di coalizione sarebbe in grado di avviare e implementare tali misure. I tentativi di riformare la Camera dei Lord sono stati rinviati più volte, dimostrando le riserve della Camera dei Comuni riguardo al cambiamento. Un sentimento che senza dubbio rispecchia l'opinione pubblica britannica – come dimostrato dall'esi... [500 / 612 chars] | La campagna AV non può essere paragonata a una riforma del sistema elettorale. Inoltre, non si deve confondere un pubblico disinformato a causa della propaganda politica con l'apatia. Spesso gli elettori esprimono apatia perché sentono di non poter cambiare nulla, che il loro voto non conta: una riforma che garantisce che chi governa il paese sia direttamente eletto dal popolo aiuterebbe a contrastare questi sentimenti. [423 chars] |
| L'espansione di Heathrow è cruciale per l'economia. L'espansione di Heathrow garantirebbe molti posti di lavoro attuali e ne creerebbe di nuovi. Attualmente, Heathrow sostiene circa 250.000 posti di lavoro. A questo si aggiungono centinaia di migliaia di persone che dipendono dal turismo a Londra, che a sua volta dipende da buone connessioni di trasporto come Heathrow. Perder competitività rispetto ad altri aeroporti europei non solo comporterebbe la perdita dell'opportunità di creare nuovi post... [500 / 1,317 chars] | La comunità imprenditoriale è lungi dall'essere unita nel suo presunto sostegno a una terza pista. I sondaggi suggeriscono che molte aziende influenti, in realtà, non sostengono l'espansione. Una lettera che esprime preoccupazione è stata firmata da Justin King, amministratore delegato di J Sainsbury, e da James Murdoch di BskyB. È quindi fuorviante considerare la comunità imprenditoriale come una sola voce che chiede l'espansione. Dobbiamo anche ricordare, quando si considerano le alternative alla nuova pista di Heathrow, come una nuova pista in un altro aeroporto di Londra o un aeroporto completamente nuovo, che queste avrebbero probabilmente un impatto economico simile all'espansione di Heathrow. Se ciò che conta sono le connessioni per attrarre affari e turisti, allora non importa da quale aeroporto provenga la connessione, purché sia con Londra. Potrebbe esserci addirittura meno bisogno che l'aeroporto sia un hub se ci concentriamo sui benefici per Londra, come ha dichiarato Bob A... [1,000 / 1,238 chars] |
| Le persone hanno troppe scelte, il che le rende meno felici. La pubblicità porta molte persone a sentirsi sopraffatte dalla necessità infinita di scegliere tra richieste concorrenti della loro attenzione – un fenomeno noto come la tirannia della scelta o sovraccarico di scelta. Ricerche recenti suggeriscono che, in media, le persone sono meno felici di quanto non lo fossero 30 anni fa, nonostante stiano meglio e abbiano molte più scelte su come spendere i loro soldi. Le affermazioni delle pubbli... [500 / 1,005 chars] | Le persone sono infelici perché non possono avere tutto, non perché hanno troppe scelte e si sentono stressate. In realtà, la pubblicità svolge un ruolo cruciale nel garantire che le persone spendano i loro soldi per il prodotto più adatto a loro. Se la pubblicità non fosse permessa, le persone sprecerebbero i loro soldi su un prodotto iniziale, mentre, avendo la scelta, opterebbero chiaramente per un altro. Una meta-analisi che ha incorporato ricerche di 50 studi indipendenti non ha trovato alcuna connessione significativa tra scelta e ansia, ma ha ipotizzato che la varianza negli studi lasciasse aperta la possibilità che il sovraccarico di scelta potesse essere legato a determinate condizioni preesistenti altamente specifiche e ancora poco comprese. Scheibehenne, Benjamin; Greifeneder, R. & Todd, P. M. (2010). 'Può mai esserci troppa scelta? Una revisione meta-analitica del sovraccarico di scelta'. Journal of Consumer Research 37: 409-425. [955 chars] |

## Public Sources

- [ArguAna paper](https://aclanthology.org/P18-1023/)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| ArguAna paper (https://aclanthology.org/P18-1023/) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
