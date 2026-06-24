# MNanoBEIR / NanoBEIR-pt / NanoArguAna

## Overview

NanoBEIR-pt NanoArguAna is a Portuguese argument retrieval task derived from
ArguAna. Each query is a long argumentative passage, and the target document is
the paired counterargument or closely responding argument in the translated
Portuguese corpus. The task is useful for evaluating retrieval beyond topical
similarity: many candidates discuss the same issue, but the correct passage is
selected by argumentative relation, stance, and response fit. It is therefore a
compact multilingual benchmark for long-form discourse matching and
counterargument retrieval.

## Details

### What the Original Data Measures

ArguAna is used in BEIR as an argument retrieval benchmark where the retrieval
target is not a fact or answer passage but an argument that responds to another
argument. Relevance depends on topic, stance, premise, and argumentative
structure. The MNanoBEIR Portuguese version keeps that structure after
translation. It measures whether lexical, dense, and hybrid retrieval systems
can identify the paired argumentative response among many long passages that
may share the same debate topic.

### Observed Data Profile

This Nano subset contains 50 queries, 3,635 documents, and 50 positive qrels.
Every query has exactly one positive document, so the ranking target is narrow.
The text is long: queries average 1,158.52 characters, and documents average
1,064.28 characters. Long query and document fields provide many lexical
anchors, but also introduce many same-topic distractors. The task therefore
tests whether a model can distinguish a true counterargument or paired response
from passages that merely discuss the same policy, social issue, or moral
question.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.4131,
hit@10 0.7000, and recall@100 0.8800. These scores show that lexical matching
is useful in Portuguese ArguAna: long passages repeat issue terms, entities,
and debate vocabulary, so BM25 often retrieves the positive somewhere in the
candidate pool. The remaining difficulty is top-rank discrimination. A passage
can share many words with the query while arguing from the wrong stance or
responding to a different premise. BM25 is therefore a strong lexical
candidate generator but cannot fully model argumentative relation.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.4918, hit@10 0.8800, and recall@100 0.9600, outperforming BM25
on all reported metrics. This indicates that embedding similarity captures
more of the semantic relation between arguments than term matching alone.
Dense retrieval is especially helpful when the counterargument uses different
phrasing, summarizes the same premise, or attacks the claim through a related
example. The remaining errors likely involve same-topic arguments that are
semantically close but do not form the intended response pair.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with exactly 100 candidates
per query and no safeguard rows. It reaches nDCG@10 0.4474, hit@10 0.7800, and
recall@100 1.0000. This profile has the best top-100 coverage but weaker early
ranking than dense retrieval. The result is important for reranking research:
the hybrid pool successfully combines lexical and semantic evidence so that
all positives are available within 100 candidates, but the initial candidate
order still needs a stronger argument-aware reranker. Dense retrieval remains
the best single ordering signal, while hybrid retrieval is the best coverage
source.

### Metric Interpretation for Model Researchers

Because each query has one positive, hit@10 is a direct first-page success
measure, and recall@100 tells whether the positive can be passed to a reranker.
nDCG@10 reflects how high the paired argument is ranked. The dense profile is
strongest for early ranking, while reranking hybrid is strongest for candidate
coverage. This separation makes the task useful for evaluating two retrieval
stages: an encoder should capture argument semantics, and a reranker should
exploit a high-recall hybrid pool to identify the exact response relation.

### Query and Relevance Type Tendencies

Queries are long Portuguese argumentative passages about political reform,
airport expansion, choice overload, cyberattacks, religion and free speech, and
other controversial topics. Relevant documents typically respond to the same
issue but may take the opposite stance, challenge a premise, or provide a
counterexample. The task favors models that understand discourse roles and
argument intent. Shared topic vocabulary is helpful, but not enough: the model
must recognize which passage actually answers the argument.

### Representative Failure Modes

BM25 may over-rank passages with heavy topic-word overlap that are not the
paired response. Dense models may retrieve arguments that are broadly related
but differ in stance, target premise, or argumentative function. Hybrid
retrieval can recover the positive reliably, but it may still include many
same-topic distractors near the top. Translation adds another risk when
argumentative cues, rhetorical emphasis, or stance markers are rendered less
explicitly in Portuguese.

### Training Data That May Help

Helpful training data includes non-overlapping argument retrieval,
counterargument selection, debate response matching, stance-aware retrieval,
and Portuguese or multilingual argument mining. Hard negatives should discuss
the same topic while responding to a different premise or taking a related but
incorrect stance. Training should exclude ArguAna, BEIR, NanoBEIR, and
translated argument records likely to overlap with this benchmark.

### Model Improvement Notes

NanoArguAna-pt is a strong diagnostic for long-form argument matching. Dense
retrieval is the best single profile for ranking, while reranking hybrid gives
complete top-100 coverage and should be attractive for downstream reranking.
Improvements should focus on long-context pooling, stance and premise
representation, and hard negatives drawn from the same debate topic. A robust
system would use hybrid candidate generation for coverage and an
argument-aware reranker for final ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| O público é indiferente às reformas. É discutível se a reforma da Câmara dos Lordes deve ser uma prioridade máxima no atual clima econômico, sem falar se um governo de coalizão conseguiria iniciar e implementar tais medidas. As tentativas de reformar a Câmara dos Lordes têm sido adiadas repetidamente, mostrando as reservas da Câmara dos Comuns em relação às mudanças. Um sentimento que, sem dúvida, é refletido na opinião pública britânica, como demonstrado pelo resultado recente do voto alternati... [500 / 566 chars] | A campanha de voto alternativo não pode ser comparada a uma reforma do sistema político. Além disso, não se deve confundir um público mal informado devido à manipulação política com indiferença. Muitas vezes, os eleitores dizem que são indiferentes porque sentem que não podem mudar nada, que seu voto não vai contar. Uma reforma que assegure que os governantes sejam eleitos diretamente pelo povo ajudaria a combater esses sentimentos. [436 chars] |
| A expansão do Heathrow é vital para a economia. A expansão do Heathrow garantiria muitos empregos atuais e criaria novos. Atualmente, o Heathrow sustenta cerca de 250.000 empregos. Além disso, centenas de milhares de pessoas dependem do comércio turístico em Londres, que depende de boas conexões de transporte como o Heathrow. Perder competitividade em relação a outros aeroportos europeus não só poderia significar desperdiçar a oportunidade de criar novos empregos, mas também perder alguns dos qu... [500 / 1,228 chars] | A comunidade empresarial está longe de estar unida no suposto apoio a uma terceira pista. Pesquisas indicam que muitas empresas influentes, na verdade, não apoiam a expansão. Uma carta expressando preocupação foi assinada por Justin King, o Diretor Executivo da J Sainsbury, e James Murdoch, da BskyB. [1] Portanto, confundir a comunidade empresarial como uma única voz que defende a expansão é um equívoco. Devemos também lembrar, ao considerar alternativas à nova pista do Heathrow, como uma nova pista em outro aeroporto de Londres ou um aeroporto completamente novo, que essas alternativas provavelmente teriam um impacto econômico semelhante à expansão do Heathrow. Se o que importa são as conexões para atrair negócios e turistas, desde que a conexão seja com Londres, não importa qual aeroporto forneça a conexão. Pode até haver menos necessidade de o aeroporto ser um hub se o foco estiver nos benefícios para Londres. Como afirmou Bob Ayling, ex-Diretor Executivo da British Airways, o Heath... [1,000 / 1,369 chars] |
| As pessoas têm muitas opções, o que as deixa menos felizes. A publicidade faz com que muitas pessoas se sintam sobrecarregadas pela necessidade constante de decidir entre várias demandas de atenção – isso é conhecido como a tirania da escolha ou sobrecarga de escolha. Pesquisas recentes indicam que, em média, as pessoas são menos felizes do que há 30 anos – apesar de estarem melhor e terem muitas mais opções de coisas para gastar seu dinheiro. As afirmações dos anúncios se acumulam sobre as pess... [500 / 975 chars] | As pessoas ficam infelizes porque não podem ter tudo, e não porque têm muitas opções e acham isso estressante. Na verdade, os anúncios desempenham um papel crucial ao garantir que o dinheiro que as pessoas têm seja gasto no produto mais adequado para elas. Se os anúncios não fossem permitidos, as pessoas gastariam dinheiro em um produto inicial, quando, dada a escolha, claramente optariam por outro. Uma meta-análise que incorporou pesquisas de 50 estudos independentes não encontrou nenhuma conexão significativa entre escolha e ansiedade, mas especulou que a variância nos estudos deixou aberta a possibilidade de que a sobrecarga de opções possa estar relacionada a certas pré-condições altamente específicas e ainda pouco compreendidas. 1 ^ Scheibehenne, Benjamin; Greifeneder, R. & Todd, P. M. (2010). 'Pode haver muitas opções? Uma revisão meta-analítica da sobrecarga de escolha.' Journal of Consumer Research 37: 409-425. [933 chars] |

### Public Sources

- [Argument Mining for Understanding Peer Reviews](https://aclanthology.org/P18-1023/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-pt dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Argument Mining for Understanding Peer Reviews | 2018 | task paper | [https://aclanthology.org/P18-1023/](https://aclanthology.org/P18-1023/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
