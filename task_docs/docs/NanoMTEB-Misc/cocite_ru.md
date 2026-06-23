# NanoMTEB-Misc / cocite_ru

## Overview

`cocite_ru` is the Russian co-citation retrieval task from RuSciBench. Queries
are Russian scientific paper titles and abstracts, and documents are candidate
paper abstracts. Each query has exactly five positives: papers that are
co-cited with the query paper in the citation graph. The Nano split contains
200 queries, 10,000 documents, and 1,000 positive qrels. Queries average 961.80
characters, and documents average 908.88 characters. This task evaluates whether
a model can retrieve bibliographically related scientific papers, where
relevance is looser than direct citation but stricter than general topical
similarity.

## Details

### What the Original Data Measures

[RuSciBench: Open Benchmark for Russian and English Scientific Document Representations](https://doi.org/10.1134/S1064562424602191)
defines Russian and English scientific-document representation tasks using
eLibrary.ru and Russian Science Citation Index data. The co-citation retrieval
task labels papers as relevant when they are co-cited with the query paper,
specifically through repeated shared citation contexts in the source graph.

Co-citation is a community-usage relation. Two papers can be relevant because
later papers cite them together, even if they do not cite each other directly or
reuse many exact terms. This makes the task a hybrid of semantic similarity,
scientific field structure, and citation-network proximity.

### Observed Data Profile

The split has 200 Russian queries, 10,000 documents, and 1,000 positive
judgments. Every query has five positives. Queries and documents are title-plus-
abstract scientific texts. The examples cover industrial digitalization, bottom
pressure oscillations, agricultural budget financing, scientific and technical
progress, and modular heavy road trains.

Compared with direct citation retrieval, co-citation positives can be broader
and more indirect. A positive may share research area, method family, or
bibliographic community rather than direct problem wording.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3920, hit@10 of 0.7300, and recall@100 of 0.5960.
Lexical matching helps when co-cited papers share narrow terminology, methods,
or disciplinary vocabulary. However, the co-citation relation often extends
beyond exact surface overlap, so BM25 is weaker than in direct-citation
retrieval.

The result shows that scientific term frequency is useful but incomplete.
Same-field abstracts can be strong lexical matches while not being co-cited,
and co-cited papers can use different terminology for adjacent concepts.

### Dense Evaluation Profile

Dense retrieval improves over BM25, with nDCG@10 of 0.4249, hit@10 of 0.7550,
and recall@100 of 0.6620. Dense embeddings better capture broader scientific
relatedness and method-level similarity, which are important for co-citation.
The improvement is moderate rather than dramatic, reflecting that co-citation
relations are not always visible from abstracts alone.

For model researchers, this task tests whether Russian scientific embeddings
encode field structure and bibliographic relatedness, not just shared keywords.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile is strongest, with nDCG@10 of 0.4346, hit@10 of
0.7550, and recall@100 of 0.6810. It combines dense semantic relatedness with
lexical scientific terminology and achieves the best candidate coverage.
Candidate lists contain 100 to 101 entries, with 18 safeguard-positive rows.

This is a hybrid-favorable task. Lexical evidence remains useful, but semantic
similarity expands the candidate pool toward co-cited papers that do not share
exact phrasing. A downstream reranker can benefit from this broader pool.

### Metric Interpretation for Model Researchers

`cocite_ru` is hybrid-favorable, with dense retrieval also stronger than BM25.
Since every query has five positives, hit@10 is easier than full evidence
coverage. Recall@100 is important because the goal is to recover multiple
co-cited papers, not only one.

nDCG@10 measures whether co-citation targets are ranked early among many
same-field but non-positive abstracts. Models that improve here likely capture
scientific neighborhood structure rather than only local lexical similarity.

### Query and Relevance Type Tendencies

Queries and documents are Russian scientific titles and abstracts. Positive
documents are co-cited papers. Relevance can reflect shared methodology,
discipline, research tradition, or citation-community usage rather than direct
answerability or citation by the query paper.

This makes same-topic non-co-cited papers natural hard negatives. They may look
scientifically similar but lack the graph relation that defines relevance.

### Representative Failure Modes

BM25 can over-rank abstracts with overlapping terminology but no co-citation
relation. Dense retrieval can over-rank conceptually similar papers that belong
to the same field but are not co-cited. Hybrid retrieval improves balance but
still cannot fully infer graph relations from text alone.

Another failure mode is multidisciplinary abstracts: a query may mention several
themes, and only some of them correspond to the co-citation neighborhood.

### Training Data That May Help

Useful training data includes citation-network representation learning, Russian
scientific abstract retrieval, co-citation pair mining, SPECTER-style
objectives, and hard negatives from same-domain papers that are not co-cited.
Training should avoid evaluation query papers, qrels, and positive abstracts
from the Nano split.

Synthetic data should use real or carefully simulated citation graphs. Arbitrary
same-topic abstracts should not be treated as positives unless a co-citation
relation is known or explicitly simulated.

### Model Improvement Notes

Models should represent Russian scientific terminology and broader citation
neighborhoods. Dense encoders need graph-informed training, while rerankers
should learn to distinguish co-citation-like relatedness from ordinary topical
similarity. Hybrid systems are promising because lexical and semantic evidence
are both relevant.

## Example Data

| Query | Positive document |
| --- | --- |
| Трансформация промышленности в цифровой экономике: проблемы и перспективы В статье проведен анализ актуального состояния цифровизации российской промышленности, рассмотрены проблемы и выявлены перспективы трансформации промышленности в цифровой экономике. Актуальность статьи обусловлена быстрым развитием новых информационных и коммуникационных технологий, благодаря которым возникает новый способ производства, что строится на принципиально иных правилах, чем традиционный, и затрагивает все отрасл... [500 / 1,319 chars] | Soft power: опыт Российской Федерации через призму международных отношений В статье рассматриваются аспекты использования «мягкой силы» в процессе формирования межнациональных связей. Особое внимание уделяется позиции России на мировой арене. Дается определение «мягкой силы». Анализируется исторический опыт разных государств. Обосновывается необходимость применения инновационных инструментов дипломатии. Сравниваются варианты использования «мягкой» и «жесткой силы». Предлагаются пути совершенствования механизма soft power в конкретных условиях места и времени. Делается акцент на связи «мягкой силы» и публичной дипломатии в Российской Федерации. [652 chars] |
| КОЛЕБАНИЯ ДОННОГО ДАВЛЕНИЯ Дан обзор экспериментальных исследований низкочастотных колебаний, которые могут возникать при сверхзвуковом обтекании донной области. Приведены работы, в которых низкочастотные колебания впервые были обнаружены. Рассмотрены концепция квазистационарных колебаний, разработанная советскими авторами. Приведены сведения о различных явлениях (акустических, вихревых, турбулентных, расходных, вызывающих пульсации донного давления. Рассмотрены основные гипотезы возбуждения низ... [500 / 619 chars] | Об исследовании колебательного движения газового подвеса ротора турбохолодильных и детандерных машин. Часть II. Колебания давления в соплах питающей системы на сверхкритическом режиме работы Рассмотрен колебательный режим, возникающий в зазоре между статором и ротором газостатического подшипника при истечении из сопел питающей системы недорасширенных сверхзвуковых струй, взаимодействующих с поверхностью ротора. Представлены результаты исследования колебательных режимов, причины возникновения, механизмы и амплитудно-частотные характеристики пульсаций давления в системе подачи рабочего тела и смазочном слое газового подшипника. [634 chars] |
| ЭФФЕКТИВНОСТЬ БЮДЖЕТНОГО ФИНАНСИРОВАНИЯ СЕЛЬСКОГО ХОЗЯЙСТВА НА РЕГИОНАЛЬНОМ УРОВНЕ Дана оценка эффективности финансирования сельскохозяйственного производства в Новосибирской области, определены его объемы, обеспечивающие расширенное воспроизводство. [250 chars] | ПЛЕМЕННАЯ РАБОТА В МОЛОЧНОМ СКОТОВОДСТВЕ Рассматривается проблема улучшения генетического потенциала в молочном скотоводстве на современном этапе развития АПК. Приводятся основные причины, сдерживающие наращивание производства молока: ухудшение генофонда по причине отказа в ряде случаев от искусственного осеменения коров и телок семенем высокоценных быков, проверенных по качеству; отсутствие в некоторых хозяйствах, зоотехнического учета, контрольных доек и бонитировки. В порядке методической помощи владельцам животных авторами приведены материалы по оценке коров по молочной продуктивности; по экстерьеру и типу телосложения; определению класса животных по комплексу признаков, бонитировочным мероприятиям. [713 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RuSciBench: Open Benchmark for Russian and English Scientific Document Representations | 2024 | Benchmark paper | [https://doi.org/10.1134/S1064562424602191](https://doi.org/10.1134/S1064562424602191) |
| mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval | 2025 | Dataset card | [https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval) |
| ru_sci_bench_mteb | 2025 | Code repository | [https://github.com/mlsa-iai-msu-lab/ru_sci_bench_mteb](https://github.com/mlsa-iai-msu-lab/ru_sci_bench_mteb) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| A Russian abstract about industrial transformation in the digital economy. | A co-cited abstract discussing soft power and Russian international relations. |
| A Russian abstract on bottom-pressure oscillations. | A co-cited abstract on oscillatory gas-suspension motion in turbomachinery. |
| A Russian abstract on agricultural budget financing efficiency. | A co-cited abstract on breeding work in dairy cattle farming. |
| A Russian abstract on economic problems of scientific and technical progress. | A co-cited abstract on criminal law enforcement in bankruptcy procedure. |
| A Russian abstract on multi-link Scania road trains. | A co-cited abstract on introducing modular heavy road trains. |
