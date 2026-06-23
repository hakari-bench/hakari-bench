# MNanoBEIR / NanoBEIR-sr / NanoSciFact

## Overview

NanoSciFact in the Serbian NanoBEIR slice is a scientific evidence retrieval task derived from SciFact. The queries are Serbian translated scientific claims, and the corpus contains Serbian translated scientific abstracts. The retrieval goal is to find abstracts that provide evidence for the claim, which may support, contradict, or otherwise ground the factual statement depending on the original SciFact framing. This makes the task a compact benchmark for evidence-sensitive scientific retrieval rather than broad topical search.

## Details

### What the Original Data Measures

SciFact was created for scientific claim verification using research abstracts as evidence. In the retrieval setting, a model receives a claim and must retrieve the abstract that contains the information needed to assess it. The relevant document is therefore not just a paper in the same field; it must contain the evidence relationship implied by the claim.

The Serbian translated setting requires the retriever to handle biomedical and scientific terminology in translated form. Many queries contain long technical phrases, named genes, diseases, therapies, or measurement concepts. Strong retrieval depends on preserving those lexical anchors while also recognizing the evidence relation expressed in an abstract.

### Observed Data Profile

The task contains 50 queries, 2,919 documents, and 56 relevance judgments. Most queries have one positive document, with an average of 1.12 positives per query. The minimum is 1, the median is 1.0, the maximum is 4, and 4 queries are multi-positive, or 8.0% of the query set. This makes the benchmark mostly a single-evidence retrieval problem.

Queries average 96.42 characters, and documents average 1,433.95 characters. Both sides are scientifically dense, but the abstracts are much longer and contain background, methods, results, and conclusions. The model must find the abstract where the claim is evidenced, not merely one that mentions the same biomedical terms.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6468, hit@10 of 0.8200, and recall@100 of 0.8750 using the top-500 BM25 candidate subset. This is a strong lexical profile. Scientific claims often include distinctive terminology such as gene names, disease names, therapy types, and experimental outcomes, and BM25 can use those rare terms effectively.

The result also shows that lexical overlap is not enough to dominate the task completely. Scientific evidence retrieval requires distinguishing an abstract that actually provides the evidence from nearby abstracts about the same entity or method. BM25 performs well when the claim and evidence share terminology, but it can over-rank related abstracts that do not resolve the claim.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.6223, hit@10 of 0.7800, and recall@100 of 0.8750. Dense retrieval matches BM25 recall@100 but trails slightly on top-10 ranking and hit@10. This indicates that embedding similarity captures the broad scientific topic, but exact lexical signals are very important for the highest ranks in this Serbian SciFact slice.

The dense profile is still strong. Its recall parity with BM25 means that relevant abstracts are generally present in the candidate set. The weakness is more about ordering: broad semantic similarity may place a topically related abstract above the true evidence abstract when both discuss the same biological process, treatment, or disease. Fine-grained factual matching remains difficult for general dense embeddings.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.6834, hit@10 of 0.8400, and recall@100 of 0.9286. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 3 safeguard rows and a mean of 100.06 candidates. This is the strongest overall profile among the three search modes.

The hybrid result is consistent with the nature of scientific claim retrieval. BM25 contributes precise terminology matching, while dense retrieval contributes semantic coverage for paraphrased evidence. Combining the two gives both better candidate recall and better top-rank ordering. For this task, hybrid search is not just a broader pool; it also produces the best nDCG@10.

### Metric Interpretation for Model Researchers

nDCG@10 is the most important signal for evidence retrieval because the system should place the evidence abstract high enough for verification or downstream reading. hit@10 is also practical: a researcher or verifier usually needs at least one relevant abstract in the first page. recall@100 measures whether a later reranker can recover evidence even if first-stage ordering is imperfect.

The three profiles clarify the task's retrieval bias. BM25 is very strong because scientific claims contain exact terminology. Dense retrieval is competitive but loses some top-rank precision because evidence matching is more specific than broad semantic similarity. reranking_hybrid performs best, showing that this benchmark benefits from a combination of lexical anchoring and semantic generalization.

### Query and Relevance Type Tendencies

Queries are long scientific claims, often biomedical. Examples mention neutrophil migration, antiretroviral therapy and tuberculosis, interferon-induced genes, HPV screening for cervical cancer, and TDP-43 interactions in neurodegeneration. Relevant documents are abstracts that contain experimental or clinical evidence related to the claim.

This means the task strongly rewards models that preserve technical detail. Small changes in gene names, diseases, measurement endpoints, or causal relations can change relevance. The model must distinguish a true evidence abstract from a merely related biomedical abstract, which is a harder requirement than topical matching.

### Representative Failure Modes

Likely failures include retrieving papers that mention the same entity but not the claim outcome, confusing support evidence with related background, overvaluing shared biomedical terminology, and missing evidence when the abstract paraphrases the claim. Dense models may retrieve semantically nearby abstracts without the exact factual relation, while BM25 may miss evidence when important terms are expressed differently in the translation.

### Training Data That May Help

Useful training data includes scientific claim verification, biomedical evidence retrieval, PubMed-style abstract search, multilingual scientific QA, and hard negatives that share entities but do not support or contradict the claim. Serbian biomedical data can help with translated terminology, while English scientific evidence datasets may help if multilingual transfer is strong. For rerankers, claim-evidence pairs with close non-evidence negatives are particularly valuable.

### Model Improvement Notes

A model targeting this task should combine exact terminology handling with evidence-aware semantic matching. Sparse systems benefit from strong tokenization and normalization of biomedical terms. Dense systems need better factual relation sensitivity and hard-negative training against near-topic abstracts. Hybrid systems are well aligned with this benchmark, but further gains likely require a reranker that reads enough of the abstract to identify whether the claim is actually evidenced.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q usmerava organizaciju migracije neutrofila do mesta zapaljenja regulišući funkcije membranskih splavova. [110 chars] | Neutrofili brzo podležu polarizaciji i usmerenom kretanju kako bi se infiltrirali na mesta infekcije i upale. Ovde pokazujemo da je inhibitorni MHC I receptor, Ly49Q, bio ključan za brzu polarizaciju i infiltraciju tkiva od strane neutrofila. Tokom stabilnog stanja, Ly49Q je inhibirao adheziju neutrofila sprečavajući formiranje fokalnih kompleksa, verovatno inhibirajući Src i PI3 kinaze. Međutim, u prisustvu inflamatornih podražaja, Ly49Q je posredovao brzu polarizaciju neutrofila i infiltraciju tkiva na način zavisni od ITIM domena. Čini se da su ove suprotne funkcije posredovane različitim korišćenjem efektorskih fosfataza SHP-1 i SHP-2. Polarizacija i migracija zavisna od Ly49Q bili su pod uticajem Ly49Q regulacije funkcija membranskih splavova. Predlažemo da je Ly49Q ključan u prebacivanju neutrofila u njihovu polarizovanu morfologiju i brzu migraciju tokom upale, kroz svoju prostorno-vremensku regulaciju membranskih splavova i signalnih molekula povezanih sa splavovima. [989 chars] |
| Antiretrovirusna terapija smanjuje stope oboljevanja od tuberkuloze u širokom rasponu CD4 slojeva. [98 chars] | POZADINA Infekcija virusom humane imunodeficijencije (HIV) predstavlja najznačajniji faktor rizika za razvoj tuberkuloze i podstaknula je njen ponovni porast, posebno u podsaharskoj Africi. Godine 2010. bilo je procenjeno 1,1 milion novih slučajeva tuberkuloze među 34 miliona ljudi širom sveta koji žive sa HIV-om. Antiretrovirusna terapija ima značajan potencijal u sprečavanju tuberkuloze povezane sa HIV-om. Sproveli smo sistematski pregled studija koje su analizirale uticaj antiretrovirusne terapije na incidenciju tuberkuloze kod odraslih sa HIV infekcijom. METODE I REZULTATI Sistemski su pretraživani PubMed, Embase, African Index Medicus, LILACS i registri kliničkih ispitivanja. Uključena su randomizovana kontrolisana ispitivanja, prospektivne kohortne studije i retrospektivne kohortne studije koje su upoređivale incidenciju tuberkuloze prema statusu antiretrovirusne terapije kod HIV-pozitivnih odraslih osoba u periodu od preko 6 meseci u zemljama u razvoju. Za meta-analize postojale... [1,000 / 2,174 chars] |
| Brza regulacija naviše i viši bazalni izražaj interferonom indukovanih gena smanjuju preživljavanje granuliranih neuronskih ćelija zaraženih virusom Zapadnog Nila. [163 chars] | Iako je podložnost neurona u mozgu mikrobnoj infekciji glavni faktor koji određuje klinički ishod, malo se zna o molekularnim faktorima koji upravljaju ovom osetljivošću. Ovde pokazujemo da su dve vrste neurona iz različitih regiona mozga pokazale različitu podložnost replikaciji nekoliko virusa sa pozitivnim RNK lancem. Granularni neuroni malog mozga i kortikalni neuroni iz moždane kore imaju jedinstvene programe prirodnog imuniteta koji obezbeđuju različitu podložnost virusnoj infekciji egz vivo i in vivo. Transdukcijom kortikalnih neurona genima koji su bili izraženiji u granularnim neuronima, identifikovali smo tri gena stimulisana interferonom (ISG; Ifi27, Irg1 i Rsad2 (takođe poznat kao Viperin)) koji su posredovali u antivirusnim efektima protiv različitih neurotrofnih virusa. Štaviše, otkrili smo da epigenetsko stanje i regulacija ISG posredovana mikroRNK (miRNK) korelira sa pojačanim antivirusnim odgovorom u granularnim neuronima. Dakle, neuroni iz evolutivno različitih region... [1,000 / 1,119 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [SciFact](https://arxiv.org/abs/2004.14974) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sr dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |

Representative query and positive abstract snippets:

| Query | Positive document snippet |
| --- | --- |
| Ly49Q usmerava organizaciju migracije neutrofila do mesta zapaljenja regulišući funkcije membranskih splavova. | Neutrofili brzo podležu polarizaciji i usmerenom kretanju kako bi se infiltrirali na mesta infekcije i upale... |
| Antiretrovirusna terapija smanjuje stope oboljevanja od tuberkuloze u širokom rasponu CD4 slojeva. | POZADINA Infekcija virusom humane imunodeficijencije (HIV) predstavlja najznačajniji faktor rizika... |
| Brza regulacija naviše i viši bazalni izražaj interferonom indukovanih gena smanjuju preživljavanje granuliranih neuronskih ćelija zaraženih virusom Zapadnog Nila. | Iako je podložnost neurona u mozgu mikrobnoj infekciji glavni faktor koji određuje klinički ishod... |
| Primarno skrining za rak grlića materice uz detekciju HPV-a ima veću longitudinalnu senzitivnost od konvencionalne citologije u otkrivanju cervikalne neoplazme intraepitelijuma stepena 2. | POZADINA Skrining za rak grlića materice zasnovan na testiranju na humani papiloma virus (HPV)... |
| Blokiranje interakcije između TDP-43 i proteina respiratornog kompleksa I, ND3 i ND6, dovodí do pojačanog gubitka neurona izazvanog TDP-43. | Genetičke mutacije u TAR DNK-vezujućem proteinu 43 uzrokuju amiotrofičnu lateralnu sklerozu... |
