# MNanoBEIR / NanoBEIR-es / NanoFEVER

## Overview

This task is the Spanish NanoBEIR version of FEVER, a Wikipedia fact verification retrieval benchmark. The original FEVER dataset contains claims generated from Wikipedia and annotated with evidence that supports or refutes them. In this NanoBEIR slice, Spanish translated claims must retrieve Spanish translated Wikipedia-style evidence documents from 4,996 candidates. The task contains 50 queries and 57 positive relevance judgments, with most claims having one positive document and six claims having multiple positives. It is a compact diagnostic for entity-centric claim evidence retrieval: models must find the page or passage that contains the facts needed for verification, including false claims where the evidence page may contradict rather than support the statement.

## Details

### What the Original Data Measures

FEVER measures fact extraction and verification over Wikipedia. In retrieval form, the first-stage task is to retrieve evidence documents, not to decide the final label. Claims may concern people, films, organizations, events, works, dates, locations, or roles. A relevant document is one that contains information needed to verify the claim. This means both supporting and refuting evidence are positive retrieval targets when they are annotated as evidence.

### Observed Data Profile

The Spanish Nano task has 50 queries, 4,996 documents, and 57 positives. Positives per query average 1.14, with a maximum of three. Queries are short, averaging about 50 characters, while documents average about 1,301 characters. Example claims mention Keith Godchaux and the Grateful Dead, Taarak Mehta Ka Ooltah Chashmah, aircraft made in Burbank, Nero, and Scream 2. Positive documents are translated Wikipedia pages or passages containing the relevant entity facts.

### BM25 Evaluation Profile

BM25 is very strong, with nDCG@10 of 0.780, Hit@10 of 0.920, and Recall@100 of 0.965. This reflects the entity-heavy nature of FEVER claims. Many claims contain explicit names, titles, or locations that occur in the evidence document, so sparse matching provides excellent candidate discovery. The remaining difficulty appears in relation details: the right evidence may not be the most obvious lexical page, and false claims can require retrieving a page that contradicts a relation rather than one that repeats the claim wording.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is strongest by top-10 ranking, with nDCG@10 of 0.843, Hit@10 of 0.940, and Recall@100 of 0.947. Dense retrieval improves the early ordering of evidence documents, likely because it can connect the claim to the relevant entity context and relation even when wording differs. Its Recall@100 is slightly lower than BM25, showing that exact entity matching remains important for broad coverage. Dense is the best direct ranker in this Spanish sample.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.803, Hit@10 of 0.960, and Recall@100 of 1.000. It gives perfect evidence coverage in the top 100 and the highest Hit@10, while dense retrieval gives the best nDCG@10. This is a useful retrieval-pipeline split: hybrid search is excellent for candidate generation because it combines exact entity matching with semantic relation matching, but dense ranking may still place the best evidence slightly higher in the first page.

### Metric Interpretation for Model Researchers

With mostly one positive per query, Hit@10 and Recall@100 are meaningful evidence-finding measures. nDCG@10 captures whether the evidence appears near the top, which matters for direct retrieval and lightweight verification pipelines. The dense and hybrid profiles should be read together: dense has better top rank quality, while hybrid has complete candidate coverage. Downstream verifiers may benefit most from the hybrid candidate pool.

### Query and Relevance Type Tendencies

Queries are short factual claims, often entity-centric. Relevant documents are Wikipedia-style evidence pages that may confirm or contradict the claim. Hard negatives often share the same entity name but lack the needed relation, or share the same title family but concern a different work, person, date, or location. This makes relation-aware entity retrieval important.

### Representative Failure Modes

BM25 can retrieve pages with strong name overlap but not the verifying relation. Dense retrieval can retrieve semantically related entity pages that do not contain the exact evidence. Hybrid retrieval improves coverage but can still rank a related page ahead of the annotated evidence. Failure analysis should ask whether the document actually contains evidence for the claim, not just whether it is about the named entity.

### Training and Leakage Considerations

Training should exclude FEVER, BEIR, NanoBEIR, and translated Wikipedia claim records likely to overlap with these evaluation claims or evidence pages. Useful non-overlapping data includes FEVER-style evidence retrieval pairs, Spanish or multilingual Wikipedia claim verification data, entity-centric QA evidence pairs, and hard negatives from similar entity pages. Synthetic data should generate both supported and contradicted Spanish claims from non-evaluation Wikipedia passages.

### Model Improvement Signals

Strong models should combine exact entity anchoring with relation-sensitive semantic ranking. Useful improvements include title normalization, alias handling, relation paraphrase training, and hard negatives from adjacent entity pages. Hybrid systems should use BM25 to protect rare names and dense retrieval to improve ranking when the evidence relation is phrased differently from the claim.

## Example Data

| Query | Positive document |
| --- | --- |
| Keith Godchaux conocía a los Grateful Dead [42 chars] | La Grateful Dead fue una banda de rock estadounidense formada en 1965 en Palo Alto, California. Conformada por entre cinco y siete miembros, la banda es conocida por su estilo único y ecléctico, que fusionaba elementos de rock, psicodelia, música experimental, jazz modal, country, folk, bluegrass, blues, reggae y space rock. También eran famosos por sus largos solos instrumentales en vivo y por su leal base de seguidores, conocidos como "Deadheads". Según Lenny Kaye, "su música toca terrenos que la mayoría de los otros grupos ni siquiera saben que existen". Estas diversas influencias se fusionaron en un todo diverso y psicodélico que convirtió a la Grateful Dead en "los pioneros padres del mundo de las bandas de jam". La banda fue ubicada en el puesto 57 por la revista Rolling Stone en su lista de "Los Mejores Artistas de Todos los Tiempos". Fueron incluidos en el Salón de la Fama del Rock and Roll en 1994, y una grabación de su presentación del 8 de mayo de 1977 en el Barton Hall de l... [1,000 / 3,117 chars] |
| Taarak Mehta Ka Ooltah Chashmah es una comedia de situación [59 chars] | Taarak Mehta Ka Ooltah Chashmah (en inglés: La Perspectiva Diferente de Taarak Mehta) es la sitcom más longeva de la India, producida por Neela Tele Films Private Limited. La serie se estrenó el 28 de julio de 2008. Se emite de lunes a viernes a las 8:30 pm, con su repetición a las 11:00 pm y al día siguiente a las 3:00 pm en SAB TV. La serie comenzó su retransmisión en Sony Pal el 2 de noviembre de 2015 a las 4:30 pm y 8:00 pm todos los días. La serie está basada en la columna Duniya Ne Oondha Chashma, escrita por el columnista y periodista Taarak Mehta para la revista semanal gujarati Chitralekha. [606 chars] |
| Aviones de alta tecnología y secretos se fabricaron en Burbank, California. [75 chars] | Burbank es una ciudad en el condado de Los Ángeles, en el sur de California, Estados Unidos, a 12 millas al noroeste del centro de Los Ángeles. Según el censo de 2010, su población era de 103,340 habitantes. Conocida como la "Capital Mundial de los Medios" y situada a solo unas pocas millas al noreste de Hollywood, numerosas empresas de medios y entretenimiento tienen su sede o instalaciones de producción significativas en Burbank, incluyendo The Walt Disney Company, Warner Bros. Entertainment, Nickelodeon Animation Studios, NBC, Cartoon Network Studios con la sucursal de la Costa Oeste de Cartoon Network, e Insomniac Games. La ciudad también alberga el Aeropuerto Bob Hope. Fue el lugar donde se encontraba el Skunk Works de Lockheed, que produjo algunos de los aviones más secretos y tecnológicamente avanzados, incluyendo los aviones espía U-2 que descubrieron componentes de misiles soviéticos en Cuba en octubre de 1962. Burbank se compone de dos áreas distintas: una sección céntrica/co... [1,000 / 1,475 chars] |

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
