# NanoIndicQA / ml

## Overview

`NanoIndicQA / ml` is the Malayalam split of IndicQA retrieval. The queries are Malayalam reading-comprehension questions, and the documents are Malayalam context paragraphs.

This task evaluates Malayalam paragraph retrieval for QA. It has relatively long queries and very long context paragraphs, so a retriever must match the question to the specific supporting passage rather than rely only on short answer terms.

## Details

### What the Original Data Measures

IndicQA is part of IndicXTREME, introduced in "Towards Leaving No Indic Language Behind". It is a manually curated cloze-style reading-comprehension benchmark across Indic languages.

The MTEB retrieval version asks models to retrieve the context paragraph that supports each question. In this Malayalam split, the task tests paragraph-level evidence retrieval over a small corpus.

### Observed Data Profile

This Nano split contains 200 queries, 247 documents, and 200 positive qrels. Each query has exactly one positive. Queries average 81.55 characters, the longest query average among the observed NanoIndicQA splits here, and documents average 2,522.64 characters.

Observed examples ask about a Mughal ruler after the East India Company revolt, the year India received independence after years of struggle, R. K. Narayan's first work, a large gate built by Alauddin Khalji, and the year a Nike Apache satellite was launched. Documents are long Malayalam historical, biographical, scientific, and cultural paragraphs.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6528, hit@10 of 0.7950, and recall@100 of 0.9400. The candidate pool contains the full 247-document corpus. BM25 is strong when the question includes names, dates, or distinctive concepts that also appear in the paragraph.

However, long paragraphs and long questions can dilute lexical scoring. BM25 may select a passage with overlapping historical or biographical terms while missing the exact evidence context.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.8214, hit@10 of 0.9550, and recall@100 of 0.9900. Dense retrieval is the strongest direct profile.

The high dense score suggests strong semantic matching between Malayalam questions and contexts. Dense retrieval is particularly helpful when the question paraphrases the paragraph or when the paragraph contains a broad narrative with the answer embedded inside it.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.7807, hit@10 of 0.9150, and recall@100 of 0.9900. It uses 100 candidates per query, with two rank-101 safeguard positives.

Hybrid retrieval matches dense retrieval on recall@100 but trails dense on top-10 ranking. It remains a good reranking pool, while dense retrieval is the best direct ranker for this split.

### Metric Interpretation for Model Researchers

`NanoIndicQA / ml` is a high-performing Malayalam context retrieval task. BM25 is already strong, but dense retrieval provides a large top-10 improvement. The split is useful for checking whether models support Malayalam semantic QA retrieval rather than only lexical matching.

Since each query has one positive, nDCG@10 and hit@10 directly measure whether the correct context is ranked early. Recall@100 is near ceiling for dense and hybrid candidate pools.

### Query and Relevance Type Tendencies

Queries are Malayalam factual or cloze-style questions, often about historical events, rulers, literature, architecture, science, and biography. Documents are long context paragraphs from encyclopedic or educational sources.

The relevance relation is evidence support: a positive paragraph contains the fact needed to answer the question.

### Representative Failure Modes

BM25 may retrieve paragraphs with the same person, empire, or institution but not the exact answer. Dense retrieval may confuse related historical passages when several contexts describe the same period or ruler. Hybrid retrieval improves candidate coverage but still requires evidence-sensitive reranking.

Long paragraphs also make answer-localization difficult after retrieval; a top result may need downstream reading comprehension.

### Training Data That May Help

Useful training data includes Malayalam QA, Malayalam Wikipedia passage retrieval, Indic multilingual context retrieval, and long-paragraph positives with same-topic hard negatives.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Malayalam semantic representation and long-context evidence matching. Models should preserve names, dates, titles, and historical relations while handling question paraphrases.

For reranking, the model should verify answer evidence inside the paragraph, not only match the general topic.

## Example Data

| Query | Positive document |
| --- | --- |
| ഈസ്റ്റ് ഇന്ത്യാ കമ്പനി കലാപം അടിച്ചമർത്തപ്പെട്ടതിനെ തുടർന്ന്,രാജ്യം വിട്ട് തന്റെ പുത്രന്മാരെ വെടിവെച്ചു കൊല്ലേണ്ടിവന്ന മുഗൾ ഭരണാധികാരി ആരായിരുന്നു ? [148 chars] | 1803-ലെ ദില്ലി യുദ്ധത്തിൽ മറാഠരെ പരാജയപ്പെടുത്തി ബ്രിട്ടീഷുകാർ ഉത്തരേന്ത്യയുടെ നിയന്ത്രണം കൈയടക്കി. മുഗളരുടെ സംരക്ഷകരായി ദില്ലിയിലെത്തിയ ബ്രിട്ടീഷുകാർ തുടക്കത്തിൽ ചക്രവർത്തിയോട് ബഹുമാനപൂർവ്വമായിരുന്നു പെരുമാറിയിരുന്നത്. അവർ നാണയങ്ങൾ ചക്രവർത്തിയുടെ പേരിലായിരുന്നു അടിച്ചിറക്കിയിരുന്നത്. കമ്പനിയുടെ സീലിൽപ്പോലും മുഗൾ ചക്രവർത്തി ഷാ ആലത്തെ അംഗീകരിച്ചുകൊണ്ട് ഫിദ്വി ഷാ ആലം (ഷാ ആലത്തിന്റെ വിനീതവിധേയൻ) എന്ന വാചകം ഉൾപ്പെടുത്തിയിരുന്നു. പത്തൊമ്പതാം നൂറ്റാണ്ട് പുരോഗമിക്കുമ്പോൾ അധികാരം മുഴുവൻ ബ്രിട്ടീഷ് റെസിഡന്റിൽ കേന്ദ്രീകരിക്കപ്പെട്ടു. ചാൾസ് മെറ്റ്കാഫ്, രണ്ടാം വട്ടം റെസിഡന്റ് സ്ഥാനത്തിരിക്കുന്ന കാലം മുതൽക്കാണ് മുഗൾചക്രവർത്തിയോടുള്ള ബ്രിട്ടീഷുകാരുടെ പെരുമാറ്റത്തിൽ പ്രകടമായ മാറ്റം വന്നുതുടങ്ങിയത്. ചക്രവർത്തിയുടെ മേൽക്കോയ്മ അംഗീകരിച്ച് ബ്രിട്ടീഷുകാർ അദ്ദേഹത്തിന് കാഴ്ച സമർപ്പിച്ചുകൊണ്ടിരുന്ന പതിവ്, ചാൾസിന്റെ പ്രേരണപ്രകാരം, 1832-ൽ ഗവർണർ ജനറൽ നിർത്തലാക്കി. തൊട്ടടുത്ത വർഷം ഈസ്റ്റ് ഇന്ത്യ കമ്പനി പുറത്തിറക്കുന്ന നാണയങ്ങളിൽനിന്ന് മുഗൾ ചക്രവർത്തിയുടെ പേര് ഒഴിവാക്കി. ബ്രിട്ടീഷ് ഗവർണർ ജനറലായിരുന്ന ഓക്ലൻഡ് പ്രഭ... [1,000 / 1,588 chars] |
| വർഷങ്ങളുടെ പോരാട്ടത്തിന് ശേഷം, ബ്രിട്ടീഷുകാരിൽ നിന്ന് ഇന്ത്യയ്ക്ക് സ്വാതന്ത്ര്യം ലഭിച്ചതെന്ന്? [94 chars] | 1857-ൽ ഇംഗ്ലീഷ്‌ ഈസ്റ്റിന്ത്യാ കമ്പനിക്കു നേരെയുണ്ടായ കലാപമാണ്‌ യൂറോപ്യൻ അധിനിവേശത്തിനു നേരെ ഇന്ത്യക്കാർ നടത്തിയ പ്രധാന ചെറുത്തുനിൽപ്പ്‌ ശ്രമം. ഒന്നാം ഇന്ത്യൻ സ്വാതന്ത്ര്യ സമരം എന്നറിയപ്പെടുന്ന ഈ കലാപം പക്ഷേ ബ്രിട്ടീഷ്‌ സൈന്യം അടിച്ചൊതുക്കി. ഇന്ത്യയുടെ ഭൂരിഭാഗം പ്രദേശങ്ങളും ബ്രിട്ടീഷ്‌ സാമ്രാജ്യത്തിനു കീഴിലുമായി. ഇരുപതാം നൂറ്റാണ്ടിന്റെ തുടക്കത്തിൽ മഹാത്മാ ഗാന്ധിയുടെ നേതൃത്വത്തിൽ അഹിംസയിൽ അധിഷ്ഠിതമായ ഇന്ത്യൻ സ്വാതന്ത്ര്യ സമര പ്രസ്ഥാനം ശക്തിപ്രാപിച്ചു. വർഷങ്ങൾ നീണ്ട സഹന സമരങ്ങൾക്കൊടുവിൽ 1947 ഓഗസ്റ്റ്‌ 15ന്‌ ഇന്ത്യ ബ്രിട്ടീഷ്‌ ആധിപത്യത്തിൽനിന്ന് സ്വതന്ത്രമായി. എന്നാൽ ഇന്ത്യയുടെ ഒരു ഭാഗം പാകിസ്താൻ എന്ന പേരിൽ വിഭജിച്ച്‌ മറ്റൊരു രാജ്യമാകുന്നത്‌ കണ്ടാണ്‌ സ്വതന്ത്ര ഇന്ത്യയുടെ ചരിത്രം തുടങ്ങുന്നത്‌. ക്രി. മു. 3000–1500 സിന്ധു നദിതട സംസ്കാരം, ഇന്നത്തെ പാകിസ്താൻ. ഹരപ്പ, മോഹൻജൊ ദാരോഎന്നിവിടങ്ങളിൽ ചെറിയ പട്ടണങ്ങൾ. ക്രി. മു. 3000 യോഗാഭ്യാസം ഇന്ത്യയിൽ വികസിക്കുന്നു. ക്രി. മു. 1450–1000 ഋഗ് വേദം എഴുതപ്പെടുന്നു. ക്രി. മു. 800s വൈദിക കാലം ഉപനിഷത്തുക്കൾ, ബ്രാഹമണങ്ങൾ എന്നിവ എഴുതപ്പെടുന്നു. ഹിന്ദു ധർമ്മത്ത... [1,000 / 2,424 chars] |
| ആർ കെ നാരായണന്റെ ആദ്യ കൃതി ഏത് ? [32 chars] | ആർ. കെ. നാരായണൻ ബ്രിട്ടീഷ് ഇന്ത്യയിലെ മദ്രാസിൽ (ഇപ്പോൾ ചെന്നൈ, തമിഴ്‌നാട്) ഒരു അയ്യർ വടാമ തമിഴ് ബ്രാഹ്മണ കുടുംബത്തിൽ 1906 ഒക്ടോബർ 10-ന് ജനിച്ചു. ആറ് ആൺമക്കളും രണ്ട് പെൺമക്കളുമുള്ള ഒരു കുടുംബത്തിലെ എട്ട് മക്കളിൽ ഒരാളായിരുന്നു അദ്ദേഹം. ആൺകുട്ടികളിൽ രണ്ടാമനായിരുന്ന നാരായണന്റെ ഇളയ സഹോദരൻ രാമചന്ദ്രൻ പിന്നീട് ജെമിനി സ്റ്റുഡിയോയിൽ പത്രാധിപരായി. പ്രശസ്തനായ ഇന്ത്യൻ കാർട്ടൂണിസ്റ്റായ ആർ. കെ. ലക്ഷ്മൺ ഇളയ സഹോദരനാണ്‌. ഒരു സ്കൂൾ ഹെഡ്മാസ്റ്ററായിരുന്ന പിതാവിന്റെ സ്കൂളിലാണ് നാരായൺ ഏതാനും കാലം വിദ്യാഭ്യാസം നിർവ്വഹിച്ചത്. പിതാവിന്റെ ജോലിസ്ഥലം പതിവായി മാറിയിരുന്നതിനാൽ നാരായണൻ തന്റെ ബാല്യകാലത്തിന്റെ ഒരു ഭാഗം മാതൃ മുത്തശിയായ പാർവതിയുടെ സംരക്ഷണയിൽ ചെലവഴിച്ചു. ഇക്കാലത്ത് അദ്ദേഹത്തിന്റെ ഉറ്റസുഹൃത്തുക്കളും കളിക്കൂട്ടുകാരുമായി ഉണ്ടായിരുന്നത് ഒരു മയിലും വികൃതിയായ ഒരു കുരങ്ങുമായിരുന്നു. മുത്തശ്ശി അദ്ദേഹത്തിന് നൽകിയ കുഞ്ഞപ്പ എന്ന വിളിപ്പേരിലാണ് കുടുംബ വൃത്തങ്ങളിൽ അദ്ദേഹം അറിയപ്പെട്ടത്. അവർ കുട്ടിയെ ഗണിതശാസ്ത്രം, പുരാണം, ഇന്ത്യൻ ശാസ്ത്രീയ സംഗീതം, സംസ്‌കൃതം എന്നിവ പഠിപ്പിച്ചു. ലക്ഷ്മണന്റെ അഭിപ്രായത്തിൽ, കുടുംബം കൂടുതല... [1,000 / 4,050 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409) | IndicXTREME and IndicQA benchmark paper. |
| [mteb/IndicQARetrieval](https://huggingface.co/datasets/mteb/IndicQARetrieval) | MTEB retrieval task dataset card. |
| [ai4bharat/IndicQA](https://huggingface.co/datasets/ai4bharat/IndicQA) | Upstream IndicQA dataset card. |
| [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Malayalam question asking which Mughal ruler left the country after the East India Company revolt was suppressed. | A paragraph about British control of Delhi, Mughal rulers, and the aftermath of rebellion. |
| A question asking when India gained independence after years of struggle. | A paragraph about the 1857 revolt and later anti-colonial resistance. |
| A question asking R. K. Narayan's first work. | A long biographical paragraph about R. K. Narayan, his family, education, and writing. |
| A question asking which large gate Alauddin Khalji built. | A paragraph about Qutb Minar, Delhi Sultanate construction, and related architecture. |
| A question asking the year the Nike Apache satellite was launched. | A paragraph about A. P. J. Abdul Kalam, defense work, and early Indian space activity. |
