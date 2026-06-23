# MNanoBEIR / NanoBEIR-ja / NanoTouche2020

## Overview

`NanoBEIR-ja__NanoTouche2020` is the Japanese NanoBEIR version of the Touché
2020 argument retrieval benchmark for controversial questions. The task uses
Japanese translated debate questions as queries and asks a retriever to rank
Japanese translated argument documents that address each issue. The Nano split
contains 49 queries, 5,745 documents, and 932 positive qrels. Every query is
multi-positive, with 19.02 positives per query on average. This makes the task
a broad argument retrieval benchmark: finding at least one relevant argument is
usually easy, but ranking substantive and diverse arguments above topical
mentions is harder.

## Details

### What the Original Data Measures

[Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26) evaluated argument
retrieval for controversial questions. Relevance depends on both topic match
and argumentative content: a useful result should contain a reasoned argument
that supports, opposes, or otherwise addresses the issue. BEIR includes Touché
2020 as an argument retrieval task, and this Japanese NanoBEIR version preserves
that structure after translation. Queries are short controversial questions;
documents are much longer debate-style arguments.

### Observed Data Profile

The task has 49 queries and 5,745 documents. It contains 932 positive qrels,
with positives per query ranging from 6 to 32 and a median of 19.00. Every
query is multi-positive. Queries average 21.73 characters, while documents
average 928.55 characters. The examples ask about homework, prescription drug
advertising, mandatory vaccination, abortion legality, and standardized tests.
The many-positive structure makes hit@10 high for most systems, while nDCG@10
and Recall@100 are more informative about ranking quality and coverage.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.5361, hit@10 = 0.9592, and
Recall@100 = 0.7661. BM25 is strong because controversial questions and
argument documents share topic words such as homework, drugs, vaccines,
abortion, and tests. With many positives per query, lexical matching usually
finds at least one relevant argument. Its strength is early topic anchoring,
but it can still rank long documents that merely mention the issue above
better arguments.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.4354, hit@10 =
0.9592, and Recall@100 = 0.7350. Dense retrieval ties BM25 on hit@10 but is
weaker on nDCG@10 and Recall@100. This suggests that broad embedding similarity
can find documents about the same controversy, but it is less effective at
ordering the most relevant arguments near the top. In argument retrieval, the
difference between "related opinion text" and "argument that answers the
question" matters.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.5296, hit@10 = 1.0000, and Recall@100 = 0.7790, with no rank-101
safeguard rows. Hybrid retrieval has the best hit@10 and Recall@100, while BM25
is slightly higher on nDCG@10. This means that combining lexical and dense
signals improves coverage and ensures at least one relevant argument in the top
10 for every query, but BM25's pure lexical ordering remains marginally stronger
for the very top ranks.

### Metric Interpretation for Model Researchers

This task is a case where BM25 is difficult to beat at early ranking because
topic terms and many positives make lexical retrieval powerful. Dense retrieval
does not dominate; it broadens semantic matching but can over-rank general
topical text. Hybrid retrieval is the best candidate source because it achieves
perfect hit@10 and the highest Recall@100. Researchers should evaluate whether
a model retrieves substantive arguments, covers both sides of a debate, and
avoids long topical passages that do not directly answer the query.

### Query and Relevance Type Tendencies

Queries are short controversial questions. Relevant documents are long
argumentative passages, often including claims, evidence, examples, and
rhetorical framing. A relevant document may argue for or against the issue, so
stance alone is not the relevance criterion. The model must match the issue and
recognize argumentative content.

### Representative Failure Modes

BM25 can over-rank documents that repeat query terms but contain weak or
off-target argumentation. Dense retrieval can retrieve broad opinion passages
that discuss the same controversy without directly addressing the question.
Hybrid retrieval improves coverage but can still mix strong arguments with
topic-only distractors. Long documents also introduce partial-match errors when
only one section is relevant to the query.

### Training Data That May Help

Useful training data includes non-overlapping Touché argument retrieval, debate
portal argument collections, pro/con retrieval pairs, and Japanese or
multilingual argument quality data. Hard negatives should share the same
controversial topic but lack a direct argument for the query. Training should
exclude Touché 2020, BEIR, NanoBEIR, and overlapping translated argument
documents from this benchmark.

### Model Improvement Notes

Strong systems should combine topic matching with argument-quality and
argument-specificity signals. Candidate generation should retrieve many
relevant pro and con arguments, while reranking should prefer documents that
directly answer the controversial question with explicit reasons. Because all
queries are multi-positive, result diversity and broad relevant coverage are
important.

## Example Data

| Query | Positive document |
| --- | --- |
| 宿題は有益ですか？ [9 chars] | まず、宿題が優れており、現代の学校で継続されるべきであるという主張には三つの理由がある。1. 宿題は「行動して学ぶタイプ」の学習者に役立つ。一般的に、学習者には三つのタイプがあるとされている。すなわち、聞くことで学ぶ者、見ることで学ぶ者、そして行動することで学ぶ者である。多くの人は、ある科目について聞くことや見ることで満足できるが、中には実際にやってみなければ理解できない人もいる。したがって、宿題は後者のグループにとって有益である。なぜなら、彼らは行動を通じて学ぶからだ。2. 宿題は学習内容の定着を助ける。多くの人が宿題のない生活を望んでいるかもしれないが、もし宿題が廃止された場合、教育の質は確実に低下するだろう。宿題が読書の課題であろうと、学期末レポートであろうと、すべては生徒の頭の中に学習内容を定着させるために設計されている。結局のところ、宿題をする生徒の方が、しない生徒よりも学業成績が優れている。これは自明の理だと私は感じるが、それを否定するのは相手側に任せよう。3. 宿題は現実社会の要求を反映している。高校卒業後、卒業生が進む道は主に二つある。大学進学か就職かだ。どちらの道に進んでも、課題が割り当てられ、教授や上司がその完了を期待する。これまで期限付きの宿題を経験してきた卒業生は、こうした要求に慣れ親しんでいるため、成功する可能性が高くなる。しかし、もし宿題がなければ、生徒は長期的な課題や締め切りといったものに不慣れなままになってしまう。つまり、宿題は卒業生が現実社会の要求に備えるための準備になるのである。次に、相手側の主張を反論しよう。1. 「宿題の確認には貴重な授業時間を取られる」という主張。いいえ、これはまったくの誤りである。教師は通常、授業中に宿題を採点しない。なぜなら、授業時間は教育のための時間であり、評価のためではないからだ。教師は通常、自宅やオフィスで採点を行い、その仕事に対して給与が支払われている。宿題の採点が授業時間に影響を与えることは、めったにない、あるいはまったくない。相手の主張は馬鹿げている。2. 「子供たちは短い集中力ではこれほどの学業量をこなせない」という主張。これは半分は正しい。確かに子供は大人に比べて集中力が短い傾向にあるが、宿題は彼らの能力に合わせて調整されていると私は答える。つまり、ある教師がXという生徒がY分しか集中でき... [1,000 / 1,623 chars] |
| 処方薬は消費者に直接広告されるべきでしょうか？ [23 chars] | 多くの広告は、薬がどれほど効果的かについて十分な情報を提供していません。たとえば、ルネスタ（Lunesta）の広告では、静かに眠っている人の上を、蛾が寝室の窓を通って漂っている様子が描かれています。しかし実際には、ルネスタは6か月間の治療後でようやく入眠が15分早まり、夜間の睡眠時間が1晩あたり37分長くなるだけです。広告の多くは感情的な訴求に基づいていますが、病状の原因、リスク要因、重要な生活習慣の変更についてはほとんど触れていません。38件の製薬広告を対象とした研究では、82％が事実に基づく主張をしており、86％が製品使用の合理的な根拠を示していました。しかし、病状の原因、リスク要因、または有病率について説明していたのはわずか26％にとどまりました[1]。このため、患者はバランスの取れた情報を得られず、薬を服用すれば問題が魔法のように解決するわけではないという認識を持てないままになっています。実際、米国とニュージーランドで行われた研究によると、調査対象の診療の12％で患者が処方を要求していました。これらの要求のうち42％が消費者向けに広告された製品に関するものであり、患者は4種類以上の薬品名を正確に思い出せないことがわかりました[2]。これは、患者の意思決定がより情報に基づいているわけではなく、主に広告された薬品への圧力にすぎないことを示しています。 [1] 処方薬の需要創出：テレビによる消費者向け広告の内容分析。Ann Fam Med. 2007年1月; 5(1): 6–13. http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1783924/ [2] ミントゼスB.ら、消費者向け製薬広告および患者の処方要求が処方決定に与える影響：2か所での横断的調査、BMJ 2002、http://www.bmj.com/content/324/7332/278.full.pdf、2011年1月8日アクセス [836 chars] |
| 子供にワクチン接種は義務付けるべきでしょうか？ [23 chars] | まだ完全な主張ではない…ただいくつかの要点をまとめただけだ…政府は、親が子供のために下す健康上の決定に介入する権利を持ってはいない。ミシガン大学の2010年の調査によると、31％の親が、子供の学校入学に必要なワクチン接種を拒否する権利を持っていると考えている。多くの親は、ワクチン接種に反対する宗教的信念を持っている。このような親に子供へのワクチン接種を強制することは、市民が宗教を自由に実践する権利を保障する第一修正憲法に違反する。死亡のリスクが小さい多くの場合、ワクチンは不要である。19世紀初頭、免疫接種が普及する以前に、百日咳、はしか、猩紅熱といった小児期の病気による死亡率は大幅に低下した。この死亡率の低下は、個人衛生の改善、水の浄化、効果的な下水処理、そしてより良い食の衛生と栄養状態によるものとされている。ワクチンは自然法則や神の人類に対する計画に干渉する。病気は自然な現象であり、人間がその経過に介入すべきではない。一般的な小児用ワクチンは、アナフィラキシーショック、麻痺、突然死など、まれだが深刻な反応を引き起こす可能性がある。特に、ワクチンで予防される多くの病気が必ずしも命を脅かすものではないことを考えれば、このリスクを冒す価値はない。ワクチンは関節炎、多発性硬化症、ループス、ギラン・バレー症候群（GBS）などの自己免疫疾患を引き起こす可能性がある。ワクチンは脳炎（脳症）を引き起こし、それが死亡や永久的な脳損傷、自閉症、ADD/ADHD、その他の発達障害につながる可能性がある。さらに、ワクチン添加物であるチメロサール（1999年以前のほとんどのワクチンに含まれていた）は、特に自閉症の発症と関連しており、現在でも特定の髄膜炎菌ワクチン、破傷風ワクチン、H1N1インフルエンザワクチンなどに含まれている。ワクチンは、リンパ系に大きな異種タンパク質分子（ワクチンに含まれる有効成分）を蓄積させ、リンパ系のがん（白血病やリンパ腫など）を引き起こす可能性がある。すべてのワクチンは免疫系の抑制を引き起こし、自然免疫系に永久的な損傷を与える可能性がある。ワクチンを接種していない子供たちは、はしかや水ぼうそうなどの感染症と戦うことで免疫系を構築・強化し、自然な免疫を獲得する。一方、ワクチンによって得られる人工的な免疫は免疫系を弱め、他のあらゆる病気や感染症に対して子供をより脆弱に... [1,000 / 1,774 chars] |

### Public Sources

- [Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26).
- [Touche20-Argument-Retrieval-for-Controversial-Questions](https://doi.org/10.5281/zenodo.6862281).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | benchmark paper | [https://doi.org/10.1007/978-3-030-58219-7_26](https://doi.org/10.1007/978-3-030-58219-7_26) |
| Touche20-Argument-Retrieval-for-Controversial-Questions | 2022 | dataset page | [https://doi.org/10.5281/zenodo.6862281](https://doi.org/10.5281/zenodo.6862281) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
