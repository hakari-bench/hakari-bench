# MNanoBEIR / NanoBEIR-fr / NanoFEVER

## Overview

This task is the French NanoBEIR version of FEVER, a Wikipedia fact verification retrieval benchmark. The original FEVER dataset contains claims generated from Wikipedia and annotated with evidence that supports or refutes each claim. In this NanoBEIR slice, French translated claims must retrieve French translated Wikipedia-style evidence documents from 4,996 candidates. The task contains 50 queries and 57 positive relevance judgments. Most claims have one positive document, while six have multiple positives. It is a compact diagnostic for entity-centric evidence retrieval, where models must find the page or passage that contains the facts needed for verification, including cases where the evidence contradicts the claim rather than repeating it.

## Details

### What the Original Data Measures

FEVER measures fact extraction and verification over Wikipedia. In retrieval form, the first-stage task is evidence discovery. A positive document is one that contains the evidence needed to verify a claim, whether the final label is support or refute. Claims often involve entities, works, places, people, dates, roles, or membership relations, so retrieval must combine entity matching with relation awareness.

### Observed Data Profile

The French Nano task has 50 queries, 4,996 documents, and 57 positives. Positives per query average 1.14, with a maximum of three. Queries average about 51 characters, while documents average about 1,325 characters. Example claims mention Keith Godchaux and the Grateful Dead, Taarak Mehta Ka Ooltah Chashmah, aircraft in Burbank, Nero, and Scream 2. Positive documents are translated Wikipedia-style pages containing verification evidence.

### BM25 Evaluation Profile

BM25 is strong, with nDCG@10 of 0.747, Hit@10 of 0.920, and Recall@100 of 0.965. This reflects the entity-heavy nature of FEVER claims: names, titles, and locations often appear directly in the evidence document. Sparse retrieval provides excellent candidate coverage. The remaining difficulty is relation precision, especially when a claim is false or when several pages share the same entity name but only one contains the verifying fact.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is the best direct ranker, with nDCG@10 of 0.819, Hit@10 of 0.940, and Recall@100 of 0.930. Dense retrieval improves early ordering by recognizing semantic relation between the claim and the evidence page, even when wording differs. Its lower Recall@100 compared with BM25 shows that exact entity anchoring is still important for broad coverage, but dense retrieval is better at placing the positive evidence high.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.780, Hit@10 of 0.920, and Recall@100 of 1.000. It gives perfect evidence coverage in the top 100, while dense retrieval gives the best top-10 ranking. This split is important for pipeline design: hybrid search is the safest candidate generator, while dense ranking may be better for direct first-page use. A downstream verifier or reranker benefits from the hybrid pool because it does not miss any annotated positive in this sample.

### Metric Interpretation for Model Researchers

With mostly one positive per claim, Hit@10 and Recall@100 are meaningful evidence discovery measures. nDCG@10 reflects whether the evidence appears early enough for practical use. The dense and hybrid profiles should be read together: dense optimizes the first page, while hybrid optimizes candidate coverage. Retrieval success should not be confused with verification success; a refuting evidence page is still a correct retrieval target.

### Query and Relevance Type Tendencies

Queries are short French factual claims. Relevant documents are Wikipedia-style evidence pages. Hard negatives often share an entity name, title family, or topic but do not contain the required relation. The task rewards entity normalization, alias handling, relation sensitivity, and the ability to retrieve contradictory evidence.

### Representative Failure Modes

BM25 can retrieve pages with high name overlap but no verifying relation. Dense retrieval can rank a semantically related page that does not contain the exact evidence. Hybrid retrieval improves coverage but may still put related lexical pages above the annotated evidence. Failure analysis should ask whether the retrieved document actually verifies the claim.

### Training and Leakage Considerations

Training should exclude FEVER, BEIR, NanoBEIR, and translated Wikipedia claim records likely to overlap with these claims or evidence pages. Useful non-overlapping data includes FEVER-style evidence retrieval pairs, French or multilingual Wikipedia claim verification data, entity-centric QA evidence pairs, and hard negatives from similar entity pages. Synthetic data should generate both supported and contradicted French claims from non-evaluation Wikipedia passages.

### Model Improvement Signals

Strong models should preserve exact entity recall while improving relation-aware evidence ranking. Useful signals include title and alias normalization, relation paraphrase examples, same-entity hard negatives, and multilingual fact verification supervision. Hybrid systems should use BM25 for names and dense retrieval for semantic evidence matching.

## Example Data

| Query | Positive document |
| --- | --- |
| Keith Godchaux connaissait les Grateful Dead. [45 chars] | Les Grateful Dead étaient un groupe de rock américain formé en 1965 à Palo Alto, en Californie. Composé de cinq à sept membres, le groupe est connu pour son style unique et éclectique, qui fusionnait des éléments de rock, de psychédélisme, de musique expérimentale, de jazz modal, de country, de folk, de bluegrass, de reggae et de space rock. Ils étaient également réputés pour leurs performances live de longs jams instrumentaux et pour leur base de fans dévoués, surnommés les "Deadheads". Leur musique, écrit Lenny Kaye, "touche à des terrains que la plupart des autres groupes ne connaissent même pas". Ces diverses influences ont été distillées en un tout diversifié et psychédélique qui a fait des Grateful Dead les "pionniers et parrains du monde des jam bands". Le groupe a été classé 57e par le magazine Rolling Stone dans son numéro des "Meilleurs Artistes de Tous les Temps". Ils ont été intronisés au Rock and Roll Hall of Fame en 1994, et un enregistrement de leur performance du 8 mai... [1,000 / 3,140 chars] |
| Taarak Mehta Ka Ooltah Chashmah est une sitcom. [47 chars] | Taarak Mehta Ka Ooltah Chashmah (en anglais : La Perspective Différente de Taarak Mehta) est la sitcom la plus longue en cours de diffusion en Inde, produite par Neela Tele Films Private Limited. La série a été diffusée pour la première fois le 28 juillet 2008. Elle est diffusée du lundi au vendredi à 20h30, avec une rediffusion à 23h00 et le lendemain à 15h00 sur SAB TV. La rediffusion de la série a commencé sur Sony Pal le 2 novembre 2015 à 16h30 et 20h00 tous les jours. La série s'inspire de la chronique Duniya Ne Oondha Chashma écrite par le chroniqueur et journaliste Taarak Mehta pour le magazine hebdomadaire gujarati Chitralekha. [643 chars] |
| Des avions de pointe et secrets ont été fabriqués à Burbank, en Californie. [75 chars] | Burbank est une ville située dans le comté de Los Angeles, en Californie du Sud, aux États-Unis, à environ 19 km au nord-ouest du centre-ville de Los Angeles. Lors du recensement de 2010, la population était de 103 340 habitants. Surnommée la « Capitale mondiale des médias » et située à quelques kilomètres au nord-est de Hollywood, de nombreuses entreprises de médias et de divertissement y ont leur siège ou des installations de production importantes, notamment The Walt Disney Company, Warner Bros. Entertainment, Nickelodeon Animation Studios, NBC, Cartoon Network Studios avec la branche ouest de Cartoon Network, et Insomniac Games. La ville abrite également l'aéroport de Bob Hope. Elle a été le siège des Skunk Works de Lockheed, qui ont produit certains des avions les plus secrets et technologiquement avancés, y compris les avions espions U-2 qui ont révélé les composants de missiles soviétiques à Cuba en octobre 1962. Burbank se compose de deux zones distinctes : une section centre-v... [1,000 / 1,525 chars] |

## Public Sources

- [FEVER paper](https://arxiv.org/abs/1803.05355)
- [FEVER shared task](https://fever.ai/)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| FEVER paper (https://arxiv.org/abs/1803.05355) |
| FEVER shared task (https://fever.ai/) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
