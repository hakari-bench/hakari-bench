# NanoFaMTEB-v2 / argu_ana_fa

## Overview

`argu_ana_fa` is a Persian argument retrieval task in NanoFaMTEB-v2. The query is a paragraph-length argument or claim, and the positive document is a paired Persian argument from an ArguAna-style dataset. The retrieval relation is not simple paraphrase: the target is often an opposing, responding, or stance-related argument.

This task is useful for evaluating Persian semantic retrieval where topical overlap and stance relation must be separated. A model must recognize that two texts discuss the same issue while also capturing the argument relation between them. The task is harder than keyword search because opposing arguments may share vocabulary but differ in position and rhetorical framing.

## Details

### What the Original Data Measures

FaMTEB is a Persian text embedding benchmark modeled after MTEB. It includes retrieval datasets built from Persian data, translated resources, and synthetic or adapted datasets. `argu_ana_fa` uses a Persian ArguAna-style retrieval source from `MCINext/arguana-fa-v2`.

The original ArguAna task measures retrieval of a paired argumentative text. In this Persian version, the model must retrieve the correct related argument among many candidates. The relation often depends on topic, stance, and argumentative role rather than exact wording.

### Observed Data Profile

This Nano split contains 199 queries, 8,669 documents, and 199 positive qrels. Every query has exactly one positive. Queries average 1,100.98 characters, and documents average 973.15 characters, so both sides are long Persian argument passages.

Observed examples discuss abortion policy, climate technology, vegetarianism and food safety, sports collisions, and community radio. The positive document generally shares the policy or social topic but may take a different stance or qualify the query's argument.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2860, hit@10 of 0.6432, and recall@100 of 0.9347 with a top-500 candidate pool. Lexical overlap is useful because paired arguments often share domain words, named concepts, and issue-specific vocabulary.

BM25's limitation is ranking. Argument pairs can be topically similar without being the correct counterargument or response. A lexical system may retrieve texts about the same topic, such as climate policy or healthcare ethics, but miss the stance relation that defines the positive.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest by top-rank metrics, with nDCG@10 of 0.3287, hit@10 of 0.7236, and recall@100 of 0.9397. Dense retrieval improves over BM25 by capturing discourse-level and semantic relatedness between arguments.

Dense similarity helps when the positive text uses different wording to address the same issue. It can connect an argument about a policy outcome to a response about feasibility, ethics, or social consequences. The improvement is meaningful but moderate, reflecting that stance-aware retrieval remains difficult.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.3128, hit@10 of 0.6834, and recall@100 of 0.9598. It uses top-100 candidates with optional rank-101 safeguards; eight rows contain 101 candidates and eight safeguard-positive rows are recorded. Hybrid retrieval has the best recall@100, while dense retrieval has better top-10 ranking.

This pattern suggests that lexical and dense signals are complementary. BM25 contributes topic-specific vocabulary, and dense retrieval contributes argument-level similarity. A downstream reranker could benefit from the hybrid candidate pool, but final ranking needs stance-sensitive reasoning.

### Metric Interpretation for Model Researchers

`argu_ana_fa` is a dense-favored Persian argument retrieval task with strong lexical candidate coverage. The high recall@100 across all systems means the positive is often in the candidate pool, but nDCG@10 remains modest. The main difficulty is choosing the correct paired argument among many topical neighbors.

Researchers should inspect errors for topic-only retrieval. A model that retrieves a text about the same policy area but not the correct argumentative relation may look plausible yet fail the task.

### Query and Relevance Type Tendencies

Queries and documents are paragraph-length Persian argumentative texts. They may include policy claims, examples, causal reasoning, ethical positions, or social consequences. The positive is a single paired argument.

Relevance is stance-aware and relation-aware. The correct document usually shares topic vocabulary but also plays the intended counterargument or response role.

### Representative Failure Modes

BM25 may retrieve any passage with the same topic words. Dense retrieval may retrieve a semantically similar passage that shares a broad stance but is not the paired argument. Hybrid retrieval may recover the positive but rank a more lexically similar distractor higher.

Another failure mode is topic dominance: long passages contain many issue terms, so the model may underweight rhetorical role or argumentative direction.

### Training Data That May Help

Useful training data includes Persian argument-pair retrieval, translated ArguAna-style counterargument pairs, debate datasets, and stance-aware semantic search data. Hard negatives should share topic vocabulary but differ in stance relation or argumentative role.

Training should exclude NanoFaMTEB-v2 evaluation queries, positives, and source dataset rows used in this split.

### Model Improvement Notes

Improving this task requires Persian embeddings that represent stance, argument structure, and topical semantics together. Models should preserve issue vocabulary while distinguishing support, opposition, qualification, and rebuttal.

For reranking, useful features include stance relation, rhetorical role, entity/topic match, and whether the target directly responds to the query argument.

## Example Data

| Query | Positive document |
| --- | --- |
| مخالفت با سقط جنین ناقص زایمان بخشی از استراتژی‌ای است که هدف آن ممنوع کردن سقط جنین به طور کلی است. سقط جنین ناقص زایمان درصد بسیار کمی از کل سقط جنین‌ها را تشکیل می‌دهد، اما از نظر پزشکی و روان‌شناختی، باید کمترین بحث‌برانگیز باشد. دلیل این تمرکز این است که سقط جنین در مراحل پایانی بارداری از نظر ظاهری ناخوشایندتر است، زیرا جنین در مراحل پایانی بارداری بیشتر شبیه نوزاد است تا جنین در مراحل اولیه رشد. بنابراین، سقط جنین در مراحل پایانی بارداری بهترین ماده برای تبلیغات ضد سقط جنین است. با تلاش ب... [500 / 668 chars] | فلسفه بارداری، اخلاق، زندگی، خانواده، خانه، ممنوعیت سقط جنین ناقص اگرچه بسیاری از مخالفان سقط جنین نوع خاص، در اصل با سقط جنین مخالف هستند، اما ارتباط ضروری بین این دو وجود ندارد، زیرا سقط جنین نوع خاص، شکلی به‌ویژه وحشتناک از سقط جنین است. این موضوع به دلایلی است که پیش‌تر توضیح داده شد: این عمل شامل یک حمله فیزیکی عمدی و جنایتکارانه به جنینی است که نیمی از تولد خود را گذرانده و ما با اطمینان می‌دانیم که درد را احساس می‌کند و در نتیجه رنج می‌برد. ما می‌پذیریم که بحث‌های پزشکی معتبری در مورد احساس درد توسط جنین‌های اولیه و эмبریون‌ها وجود دارد؛ اما در این مورد چنین بحثی وجود ندارد و به همین دلیل است که سقط جنین نوع خاص به‌طور منحصربه‌فرد وحشتناک و به‌طور منحصربه‌فرد غیرقابل توجیه است. [694 chars] |
| فناوری نوین بشر بارها از طریق اختراعات عظیمی مانند کشاورزی، فولاد، آنتی‌بیوتیک‌ها و ریزتراشه‌ها، جهان را دگرگون کرده است. و همانطور که فناوری پیشرفت کرده، سرعت پیشرفت فناوری نیز افزایش یافته است. پیش‌بینی می‌شود که بین سال‌های ۲۰۰۰ تا ۲۰۵۰، ۳۲ برابر تغییرات بیشتری نسبت به دوره ۱۹۵۰ تا ۲۰۰۰ رخ دهد. در میان این تحولات، بسیاری از ذهن‌های بزرگ بر کاهش انتشار گازهای گلخانه‌ای و فناوری‌های کنترل آب و هوا متمرکز خواهند بود. بنابراین، حتی اگر بدترین پیش‌بینی‌های مربوط به تغییرات آب و هوایی به واقعیت بپی... [500 / 966 chars] | خانه اقلیم معتقد است برای تغییرات اقلیمی جهانی خیلی دیر شده است. پیشرفت‌های تکنولوژیکی تقریباً به‌طور قطع برای کسانی که توانایی پرداخت آن را دارند توسعه خواهند یافت (همانطور که معمولاً در مورد بیشتر فناوری‌ها اتفاق می‌افتد). با این حال، تغییرات آب و هوایی بیشترین تأثیر را بر کشورهای فقیر خواهد گذاشت که توانایی مقابله با آن را ندارند. این احتمال وجود دارد که بتوانیم افراد ثروتمند را محافظت کنیم، اما این بدان معنا نیست که برای تغییرات آب و هوایی جهانی خیلی دیر شده است. [472 chars] |
| گیاهخواری خطر مسمومیت غذایی را کاهش می‌دهد. تقریباً تمام انواع خطرناک مسمومیت غذایی از طریق گوشت یا تخم‌مرغ منتقل می‌شوند. به عنوان مثال، باکتری کمپیلوباکتر که شایع‌ترین علت مسمومیت غذایی در انگلستان است، معمولاً در گوشت و طیور خام، شیر غیر پاستوریزه و آب تصفیه نشده یافت می‌شود. سالمونلا از گوشت، طیور و محصولات لبنی خام می‌آید و بیشتر موارد مسمومیت غذایی با اشریشیا کلی (E-Coli) پس از خوردن گوشت گاو نپخته یا نوشیدن شیر غیر پاستوریزه رخ می‌دهد. [1] تماس نزدیک بین انسان و حیوانات همچنین منجر به زئو... [500 / 808 chars] | حیوانات، محیط زیست، سلامت عمومی، بهداشت عمومی، وزن، فلسفه، اخلاق. ایمنی و بهداشت مواد غذایی برای همه بسیار مهم است و دولت‌ها باید برای اطمینان از وجود استانداردهای بالا، به ویژه در رستوران‌ها و سایر مکان‌هایی که مردم غذا تهیه می‌کنند، اقدام کنند. اما مسمومیت غذایی می‌تواند در هر جایی رخ دهد؛ «افراد دوست ندارند اعتراف کنند که میکروب‌ها ممکن است از خانه خودشان آمده باشند» [۱] و در حالی که گوشت به ویژه در معرض آلودگی است، باکتری‌هایی وجود دارند که می‌توانند از طریق سبزیجات منتقل شوند، به عنوان مثال لیستریای مونوسیتوژنز می‌تواند از طریق سبزیجات خام منتقل شود. [۲] تقریباً سه چهارم از انتقال‌های زئونوزیک (انتقال بیماری از حیوانات به انسان) توسط عوامل بیماری‌زای منشأ حیات وحش ایجاد می‌شوند؛ حتی برخی از مواردی که ممکن است ناشی از دام‌ها مانند آنفولانزای پرندگان باشد، می‌توانند به طور مشابه از حیوانات وحشی منشا گرفته باشند. ما نمی‌توانیم کار زیادی برای جلوگیری از انتقال چنین بیماری‌هایی انجام دهیم، مگر اینکه تماس نزدیک را کاهش دهیم. بنابراین، تغییر به گیاهخواری ممکن است با کاهش تماس، چنین بیمار... [1,000 / 1,605 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General benchmark framework that FaMTEB follows. |
| [MCINext/arguana-fa-v2](https://huggingface.co/datasets/MCINext/arguana-fa-v2) | Public source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Persian argument about abortion policy and medical or ethical framing. | A paired argument discussing the same abortion-policy issue from a related or opposing standpoint. |
| A passage about technology development and climate change. | A response about whether technological progress can address climate risk. |
| A vegetarianism argument focused on food poisoning risk. | A related passage about food safety, public health, and ethical or regulatory considerations. |
| A sports argument defending collisions as part of baseball tradition. | A paired passage about whether collisions should continue in professional baseball. |
| A passage about community radio and public communication. | A related argument about the value and limits of local or community radio. |
