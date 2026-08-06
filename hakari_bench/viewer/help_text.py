"""User-facing help copy for the leaderboard viewer.

The leaderboard packs a lot of retrieval-evaluation vocabulary into a very dense
control area, so the help modals are the main onboarding surface for a first-time
reader. Keeping every string here makes the whole explanation set readable and
editable as one piece of documentation instead of fragments buried inside render
functions.

Each entry follows the same shape:

* ``title`` is the short concept name in the dialog header, never a generic
  "Help" and never a descriptive sentence.
* ``eyebrow`` names the group the concept belongs to, when the short title alone
  would be ambiguous. It renders as a small chip above the lead line, which
  keeps "Benchmark scope" or "Score column" out of the header itself.
* ``summary`` is one plain sentence a reader can act on immediately.
* ``details`` explains what the control is, what it changes, a concrete example,
  and when to reach for it. Paragraphs are separated by blank lines and split
  into real paragraphs by ``viewer.js``.
"""

from __future__ import annotations

from dataclasses import dataclass

from hakari_bench.viewer.config import CLEAR_SCOPE_NAME


@dataclass(frozen=True)
class HelpCopy:
    """One help modal: heading, optional group chip, lead sentence, and details."""

    title: str
    summary: str
    details: str
    eyebrow: str | None = None


PAGE_OVERVIEW = HelpCopy(
    title="HAKARI-Bench",
    eyebrow="Getting started",
    summary=(
        "Every row is one retrieval model, and every score is how well it ranked relevant "
        "documents across hundreds of small retrieval tasks."
    ),
    details=(
        "HAKARI-Bench measures information retrieval: given a query, does the model put the "
        "relevant documents at the top? Each task is a Nano-set, a compact rebuild of a public "
        "retrieval benchmark with roughly 50 to 200 queries and a corpus capped at about 10K documents, "
        "which keeps every positive document plus hard negatives from the original data. Nano-sets are small "
        "enough that every model can be re-run on all of them, which is what makes the same-condition "
        "comparison on this page possible.\n\n"
        "Scores are nDCG@10 multiplied by 100 unless you change Metric. Roughly: 100 means the "
        "relevant documents were placed perfectly at the top of the first 10 results, and 0 means "
        "nothing relevant was found. Borda Score, the default sort, is a ranking-based score instead "
        "of an average score; Macro Mean and Micro Mean are two ways of averaging the same per-task "
        "numbers. Each of those column headers has its own help icon.\n\n"
        "The controls above the table apply from top to bottom. Evaluation mode picks full-corpus "
        "retrieval or reranking of a fixed candidate list. Score and Metric decide how task scores are "
        "averaged and which metric is averaged. Benchmark scope picks which benchmark families count. "
        "Task facets narrows those tasks by language or category. Table display adds per-task columns, "
        "Efficiency variants adds compressed or truncated embedding rows, and Filter results only hides "
        "rows from the table you already have.\n\n"
        "Only models that completed every task in the current scope are ranked, so the table always "
        "compares like with like; the counts under the controls show how many models and tasks that is. "
        "Click a model name for its run metadata, click the book icon beside a benchmark for its "
        "documentation, switch to Chart to plot quality against size, and use Download CSV to take the "
        "visible table with you."
    ),
)


EVALUATION_MODE = HelpCopy(
    title="Evaluation mode",
    summary="Chooses whether models are ranked on searching a whole corpus, or on reordering a fixed candidate list.",
    details=(
        "Retrieval, the default, ranks systems that search the entire document corpus of each task on "
        "their own: dense embedding models, BM25, learned sparse models, and late-interaction "
        "(ColBERT-style) models. It answers the question 'which model finds the relevant documents in "
        "the first place?'\n\n"
        "Reranking ranks models that never search the corpus. Every query starts from the same fixed "
        "list of 100 candidate documents and the model only reorders it. It answers a different "
        "question: 'given a candidate list, which model pulls the best documents to the top?'\n\n"
        "That candidate list is built once per query and shared by every model in this mode. BM25 "
        "contributes its top 500 lexical candidates, a fixed dense retriever contributes its top 500 "
        "semantic candidates, and reciprocal rank fusion merges the two rankings into a single top 100. "
        "Because the input is identical for everyone, reranking scores stay comparable across model "
        "families; in the result database this is the reranking_hybrid candidate set.\n\n"
        "The BM25 row here is not a reranked score. It is BM25's ordinary full-corpus retrieval result, "
        "carried into this table as a lexical reference point, and it is hidden for @100 metrics because "
        "the way the candidate subsets were built would flatter it there.\n\n"
        "Do not compare Retrieval scores with Reranking scores. A reranker only has to sort 100 "
        "documents that someone else retrieved, while a retriever has to find them among thousands."
    ),
)


SAFEGUARD_POSITIVES = HelpCopy(
    title="Safeguard positives",
    summary="Guarantees that every query has at least one correct answer inside the candidate list rerankers see.",
    details=(
        "This switch exists only in Reranking mode, where models reorder a fixed top-100 candidate list "
        "instead of searching the corpus.\n\n"
        "For some queries that list contains no relevant document at all, because the first-stage "
        "retrievers missed everything. Such a query is unsolvable for a reranker: no ordering can score "
        "above zero, so it adds noise that no model can do anything about.\n\n"
        "With Safeguard positives on, which is the default, one known-relevant document is appended at "
        "rank 101 for exactly those queries. Every query then has something to promote, so the score "
        "measures reranking skill rather than first-stage luck.\n\n"
        "Turn it off when you want the unmodified picture: how rerankers behave on the raw hybrid "
        "top-100, including the queries where success was impossible. Scores drop, and results from the "
        "two settings should not be mixed inside one comparison."
    ),
)


SCORE_AGGREGATION = HelpCopy(
    title="Score aggregation",
    summary="Chooses whether every task counts equally (Micro) or every benchmark counts equally (Macro).",
    details=(
        "A model's average is built from its per-task scores. Micro and Macro differ only in what gets "
        "one vote.\n\n"
        "Micro, the default, averages all raw tasks equally, so a benchmark with many tasks pulls the "
        "average harder. M-BEIR alone contributes all 182 cells of its 13-task x 14-language matrix. "
        "Macro first averages the tasks inside each benchmark into a single benchmark score and then "
        "averages those benchmarks, so a 182-task suite and a 5-task suite have exactly the same "
        "influence.\n\n"
        "Pick Micro when you want a straight average over everything that was measured, and Macro when "
        "you do not want one large suite to decide the ranking. In the Overall scope both averages stay "
        "visible side by side as the Macro Mean and Micro Mean columns, so this switch decides which of "
        "them counts as the model's single headline score: the Mean Score used in every other scope, the "
        "mean-based rank, and the STD delta on the mean. The default Borda Score ranking is computed from "
        "per-task ranks and does not change with this switch.\n\n"
        "Table display and Score are linked, because per-task columns only make sense with per-task "
        "weighting: Task columns forces Micro and Grouped columns forces Macro, and while either is "
        "active the incompatible Score choice is disabled.\n\n"
        "M-BEIR is displayed as 13 task means or 14 language means so the table does not grow to 182 "
        "columns. Those compact columns are a display summary only: Micro still averages all 182 raw "
        "cells underneath."
    ),
)


SCORE_METRIC = HelpCopy(
    title="Score metric",
    summary="Chooses which retrieval-quality measure every number in the table is computed from.",
    details=(
        "Each evaluation stores the model's top-100 ranking per query, so several standard IR metrics "
        "can be recomputed from the same run. This control picks the one used everywhere on the page: "
        "model means, Borda ranking, per-task columns, the chart, and the CSV export. All of them are "
        "shown multiplied by 100, so 65.51 means a score of 0.6551.\n\n"
        "nDCG@10, the default, grades the ordering of the first 10 results and gives more credit the "
        "higher a relevant document sits. It is the primary metric of BEIR and of this benchmark, so use "
        "it unless you have a reason not to.\n\n"
        "Recall@100 and Acc@100 answer a different question: did the relevant documents survive into the "
        "top 100 at all? These are the metrics to read when the retriever feeds a reranker, a RAG "
        "pipeline, or an agent that can afford to look at 100 candidates. Recall@100 measures how many "
        "of them survived; Acc@100 only asks whether at least one did.\n\n"
        "Acc@1 and Acc@10 ask whether any relevant document appears in the top 1 or top 10, which is the "
        "easiest number to interpret. MRR@10 rewards how early the first relevant document appears, and "
        "MAP@100 rewards finding many relevant documents early, which matters for tasks with several "
        "correct answers."
    ),
)


BENCHMARK_SCOPE = HelpCopy(
    title="Benchmark scope",
    summary="Chooses which benchmark families the leaderboard scores are computed from.",
    details=(
        "Every button here is a Nano-set: a compact rebuild of a public retrieval benchmark, with up to "
        "roughly 50 to 200 queries and a corpus capped at about 10K documents per task, so that all "
        "models can realistically be run on all of them. They cover multilingual suites, single-language suites, and domain-specific sets "
        "such as code, law, medicine, and long documents.\n\n"
        "Overall, the default, uses every benchmark in the database and gives the broadest ranking. "
        "Overall (EN) is the same set restricted to English tasks. Selecting individual benchmark "
        "buttons instead builds a custom scope from just those benchmarks, and you can select several at "
        "once. Clear removes every selection and empties the table so you can start a fresh custom set.\n\n"
        "Scope is the first control that decides which tasks exist at all. Task facets then narrows "
        "inside them, and Filter results only hides rows afterwards. Because a model is ranked only when "
        "it has a result for every task in the scope, narrowing the scope can bring more models into the "
        "table and widening it can remove them.\n\n"
        "The book icon next to a benchmark opens its documentation page, which describes what the tasks "
        "measure and where the data came from."
    ),
)


_SCOPE_PRESET_HELP = {
    "Overall": HelpCopy(
        title="Overall",
        eyebrow="Benchmark scope",
        summary="Ranks models over every benchmark in the database, which is the default view of this page.",
        details=(
            "Overall is the broadest scope. It includes the multilingual, single-language, and "
            "domain-specific Nano-sets together, before any task facet, model, task, or variant filter is "
            "applied, so it is the closest thing to a single headline ranking.\n\n"
            "Only models that completed every task in this scope appear, which is why the model count "
            "here is smaller than the number of models in the database.\n\n"
            "Pair it with Micro when you want every task to weigh the same, or with Macro when you want "
            "every benchmark to weigh the same regardless of how many tasks it contains."
        ),
    ),
    "Overall (EN)": HelpCopy(
        title="Overall (EN)",
        eyebrow="Benchmark scope",
        summary="Uses the same benchmarks as Overall, restricted to English tasks.",
        details=(
            "Overall (EN) keeps the full benchmark set of Overall and then applies the EN task facet, so "
            "multilingual suites contribute only their English slices. It is an English view of the whole "
            "benchmark, not a separate curated subset.\n\n"
            "Use it when your application is English-only and multilingual tasks would otherwise move the "
            "ranking. Score, Metric, and every other control keep working the same way.\n\n"
            "Selecting it switches Task facets to EN. Switching Task facets back to All languages returns "
            "you to the full Overall scope."
        ),
    ),
    CLEAR_SCOPE_NAME: HelpCopy(
        title="Clear",
        eyebrow="Benchmark scope",
        summary="Deselects every benchmark so you can build a custom scope from nothing.",
        details=(
            "Clear is an action, not a scope you can be in. It resets the page to an empty custom "
            "selection: no benchmark is selected, Task facets return to all languages and categories, and "
            "the table has no rows to show because no tasks are in scope.\n\n"
            "Use it when you want a small, deliberate comparison, for example only the code retrieval "
            "sets or only the Japanese suites. Press Clear, then select the benchmarks you care about.\n\n"
            "After pressing it the URL stays on the custom view with no benchmark selected, so the next "
            "benchmark you click starts a clean set."
        ),
    ),
}


def scope_preset(view_name: str) -> HelpCopy:
    """Help copy for a Benchmark scope preset button."""

    preset = _SCOPE_PRESET_HELP.get(view_name)
    if preset is not None:
        return preset
    return HelpCopy(
        title=view_name,
        eyebrow="Benchmark scope",
        summary=f"Ranks models on the {view_name} scope defined in the viewer configuration.",
        details=(
            "Benchmark scope decides which tasks are eligible before any row filter runs, so it is the "
            "control to use first when you want to compare models on one benchmark family.\n\n"
            "Only models with a result for every task in this scope are ranked, which keeps the "
            "comparison fair but can change how many models are listed.\n\n"
            "After choosing a scope, refine the view with Task facets for languages and categories, and "
            "with the model, task, and variant controls below."
        ),
    )


_MNANOBEIR_MATRIX_NOTE = (
    "M-BEIR runs 13 retrieval tasks in 14 languages, which produces 182 raw result cells per model. "
    "Showing them all would mean 182 table columns, so the viewer summarizes them along one axis and "
    "this control picks which axis that is."
)

_MNANOBEIR_RANKING_NOTE = (
    "This choice changes the breakdown you see, not the weight M-BEIR carries. With Micro scoring all "
    "182 raw cells still contribute individually, exactly like raw tasks from any other benchmark. With "
    "Macro scoring M-BEIR is still averaged down to one benchmark score."
)


def mnanobeir_scope(score_group: str) -> HelpCopy:
    """Help copy for the M-BEIR task/language scope selector."""

    if score_group == "lang_mean":
        return HelpCopy(
            title="M-BEIR(lang)",
            eyebrow="Benchmark scope",
            summary="Breaks M-BEIR down into 14 language columns, each averaging that language's 13 tasks.",
            details=(
                f"{_MNANOBEIR_MATRIX_NOTE}\n\n"
                "M-BEIR(lang) shows one column per language, such as M-BEIR-ja, M-BEIR-de, or M-BEIR-fr. "
                "Each column is the mean of all 13 retrieval tasks in that language. Choose it to see how "
                "evenly a model covers languages, for example whether a strong overall score hides a weak "
                "Japanese or Arabic result.\n\n"
                f"{_MNANOBEIR_RANKING_NOTE}\n\n"
                "M-BEIR(task) is the other axis: 13 task columns, each averaging the 14 languages inside "
                "that task."
            ),
        )
    return HelpCopy(
        title="M-BEIR(task)",
        eyebrow="Benchmark scope",
        summary="Breaks M-BEIR down into 13 task columns, each averaging that task's 14 languages.",
        details=(
            f"{_MNANOBEIR_MATRIX_NOTE}\n\n"
            "M-BEIR(task) shows one column per retrieval task, such as M-BEIR-arguana, M-BEIR-fever, or "
            "M-BEIR-scifact. Each column is the mean of that task across all 14 languages. Choose it to "
            "compare behaviour per task type, for example argument retrieval versus fact checking, with "
            "language differences averaged out.\n\n"
            f"{_MNANOBEIR_RANKING_NOTE}\n\n"
            "M-BEIR(lang) is the other axis: 14 language columns, each averaging the 13 tasks inside that "
            "language."
        ),
    )


TASK_FACETS = HelpCopy(
    title="Task facets",
    summary="Keeps only the tasks of one language or category inside the benchmark scope you already chose.",
    details=(
        "Benchmark scope decides which benchmarks are counted; Task facets narrows the tasks inside "
        "them. Selecting JA, for example, keeps only Japanese tasks from every selected benchmark and "
        "recomputes all scores from that subset. Code keeps only tasks whose metadata marks them as code "
        "retrieval. All languages removes the facet again.\n\n"
        "The number on each button is how many tasks that facet has in the current scope, and the table "
        "below lists every available facet with its full name. Facets with few tasks give noisier "
        "rankings, so read a 5-task language differently from a 200-task one.\n\n"
        "Use this when you care about one language or domain rather than a global average. Because "
        "models are ranked only when they completed every task in view, a narrower facet often brings "
        "additional models into the table."
    ),
)


TABLE_DISPLAY = HelpCopy(
    title="Table display",
    summary="Chooses how much per-task detail the result table shows next to each model's average.",
    details=(
        "By default the table shows one summary row per model. These toggles add columns so you can see "
        "where a score comes from instead of just how large it is.\n\n"
        "Task columns adds one score column per raw task, which is the most detailed view and is where "
        "you look to find the tasks a model wins or loses. Grouped columns instead adds one column per "
        "benchmark group, such as JMTEB-v2 or IFIR, which is easier to scan across many benchmarks. The "
        "two are alternatives: Task columns always uses Micro scoring and Grouped columns always uses "
        "Macro scoring, so selecting one locks the Score control accordingly.\n\n"
        "STD shows each score as its distance from the column mean in standard deviations, which makes "
        "'clearly above average' easy to spot even when raw scores sit close together. Task ranks shows "
        "the model's rank in each visible task column instead of the score. Others adds the license and "
        "model-family columns.\n\n"
        "M-BEIR stays compact in both modes: 13 task columns in task scope or 14 language columns in "
        "language scope, rather than all 182 raw cells."
    ),
)


EFFICIENCY_VARIANTS = HelpCopy(
    title="Efficiency variants",
    summary="Adds extra rows for the same model run in cheaper settings, so you can price quality against cost.",
    details=(
        "A production retrieval system rarely stores full-precision, full-dimension vectors for millions "
        "of documents. These toggles bring in extra result rows where the same model was evaluated under "
        "such compressions, so a compact setting can be compared directly with its own baseline. They are "
        "off by default to keep the base leaderboard readable.\n\n"
        "Dims adds rows where only the leading dimensions of a dense vector are kept, labelled like 512d "
        "or 512d <- 1024 when the label also records the dimension it was cut from. Quantization adds "
        "compressed numeric formats: int8 stores each dimension in "
        "one byte, and binary keeps only the sign of each dimension, which is 32x smaller than float32 "
        "but loses the most quality. Rescore adds two-stage rows that repair much of that loss, and has "
        "its own help icon.\n\n"
        "Sparse pruning applies to learned sparse encoders instead of dense vectors: it caps how many "
        "term weights stay active per query or per document, with labels such as q32d or d256d. Fewer "
        "active dimensions means a smaller and faster inverted index.\n\n"
        "When variant rows are visible the table also shows how far each one sits from its own base row, "
        "which is the number to look at: the question is usually not which variant is best overall but "
        "how much quality a given compression costs."
    ),
)


RESCORE = HelpCopy(
    title="Rescore",
    summary="Retrieves with small compressed vectors, then re-scores the shortlist with the original vectors.",
    details=(
        "Compressed embeddings make search cheap but blur fine distinctions. Rescore is the standard "
        "two-stage fix: retrieve the top 100 with int8 or binary vectors, then recompute the scores of "
        "just those 100 candidates with the original full-precision embeddings and reorder them.\n\n"
        "The cost is small, because full-precision vectors are needed only for a shortlist, while most of "
        "the quality lost to quantization comes back. Comparing an int8 or binary row with its rescore "
        "row shows exactly how much.\n\n"
        "Enable Quantization together with Rescore to include the full-dimension int8_rescore and "
        "binary_rescore rows, and enable Dims as well to also include truncated-dimension rescore rows. "
        "As a convenience, turning Rescore on while both Dims and Quantization are off enables both so "
        "that rows appear immediately; turning Rescore off again leaves them as they are. A URL that "
        "restores Rescore alone, or Dims plus Rescore without Quantization, matches no rows."
    ),
)


FILTER_RESULTS = HelpCopy(
    title="Filter results",
    summary="Narrows the table to the models, tasks, and variant rows you actually want to look at.",
    details=(
        "Everything in this panel runs last, after Evaluation mode, Benchmark scope, Task facets, and "
        "Efficiency variants have decided which results exist. Filters therefore change what you see, not "
        "what was measured.\n\n"
        "The Model and Task text boxes and the Params and Length ranges apply when you press Enter; "
        "checkboxes and facet filters apply immediately. Hidden rows and columns are also excluded from "
        "Download CSV, so this panel is the way to export a subset.\n\n"
        "By default the ranks and means you see keep the context of the current scope, so a filtered "
        "table still tells you where a model stands in the full comparison. Enable Recalculate ranks from "
        "filters when you want the opposite: ranks and averages recomputed from the filtered set alone. "
        "The Params and Length ranges are the exception and always narrow the ranked population, because "
        "they change which models and tasks take part at all.\n\n"
        "Typical uses: keep only models under 500M active parameters, keep only commercially usable "
        "models, or compare a single model family against the rest of the board."
    ),
)


MODEL_FILTER = HelpCopy(
    title="Model filter",
    summary="Keeps only rows whose model name matches your keywords.",
    details=(
        "Type part of a model name and press Enter. Matching is case-insensitive and partial, so bge "
        "matches bge-m3 and every other name containing it.\n\n"
        "Separate several keywords with spaces to match any of them. For example, jina bge keeps rows "
        "whose model name contains jina or bge, which is the quick way to put two families side by side. "
        "Keywords shorter than 3 characters are ignored so a stray letter does not match half the board.\n\n"
        "By default this only changes which rows are visible; ranks and means keep the context of the "
        "current benchmark scope. Enable Recalculate ranks from filters if you want the ranking recomputed "
        "among the matching models only. It never changes the benchmark scope or the available task "
        "columns."
    ),
)


TASK_FILTER = HelpCopy(
    title="Task filter",
    summary="Keeps only the task columns or task rows whose names match your keywords.",
    details=(
        "This searches task identifiers: benchmark name, dataset name, split name, task name, and task "
        "key. It is most useful with Task columns or Grouped columns enabled, where matching columns stay "
        "and the rest are hidden.\n\n"
        "Separate several keywords with spaces to match any of them. For example, arguana fever keeps "
        "task columns or task rows whose identifiers contain arguana or fever. Short task names such as "
        "nq also work, because task keywords are accepted from 2 characters; single characters are "
        "ignored.\n\n"
        "The model ranking keeps its original context unless Recalculate ranks from filters is enabled, "
        "so by default you are looking at a subset of columns from the full ranking rather than a new "
        "ranking over those tasks."
    ),
)


LICENSE_FILTERS = HelpCopy(
    title="License filters",
    summary="Keeps only models whose reviewed license allows the kind of use you have in mind.",
    details=(
        "License buckets come from the reviewed model-card metadata in this repository, not from an "
        "automatic scan, and they are a starting point rather than legal advice. Always check the model's "
        "own license before shipping it.\n\n"
        "Commercial covers permissive licenses and proprietary terms that allow commercial use under "
        "conditions, including the MIT-licensed BM25 baseline. Non-commercial covers licenses such as "
        "CC BY-NC. N/A marks rows where the classification does not apply, and Unknown keeps rows that "
        "have no reviewed license metadata yet.\n\n"
        "Use it when you are shortlisting a model for a product and want the board to show only "
        "candidates you could actually deploy."
    ),
)


RUN_METADATA_FILTERS = HelpCopy(
    title="Run metadata filters",
    summary="Keeps only results produced with a particular runtime setup, such as a dtype or a prompt.",
    details=(
        "Every result records how it was produced. Dtype is the numeric precision of the model weights, "
        "such as bf16 or fp32. Attention is the attention implementation used, such as sdpa or "
        "flash_attention_2, when the run recorded one. Prompt records whether query or document prompt "
        "prefixes were applied, which matters because many embedding models expect them.\n\n"
        "These filters do not change the benchmark scope or the task definitions. They exist for auditing "
        "comparability: if you suspect two rows are not directly comparable, this is where you check, and "
        "you can isolate a single runtime configuration to be sure.\n\n"
        "If you are simply reading the leaderboard, you can leave all of them alone."
    ),
)


RANK_FILTERED = HelpCopy(
    title="Recalculate ranks from filters",
    summary="Recomputes ranks and averages from the filtered rows instead of keeping the full-board context.",
    details=(
        "Off, which is the default, means filters only hide rows: a model that is 7th on the full board "
        "still shows as 7th after you filter the others away. That is what you want when the question is "
        "'where does this model stand overall?'\n\n"
        "On means the numbers are rebuilt from what is left. Borda ranks, mean ranks, task counts, and "
        "visible means are recalculated after the active text, model-family, license, runtime, "
        "efficiency, and task filters have been applied. That is what you want for a local question, such "
        "as which dense model under 500M parameters is best, or who wins on one task family.\n\n"
        "Params and Length range filters already narrow the ranked model or task population whenever "
        "they are set, so those two behave the same way with this switch on or off."
    ),
)


MODEL_FAMILY = HelpCopy(
    title="Model family",
    summary="Keeps only rows from the retrieval architectures you want to compare.",
    details=(
        "Every result records the architecture that produced it, and the families work in noticeably "
        "different ways.\n\n"
        "Dense models encode a query and a document into one vector each and compare them, which makes "
        "search fast and captures meaning beyond exact wording. BM25 is the classic lexical baseline that "
        "scores word overlap, with no neural model involved. Sparse models learn weights over vocabulary "
        "terms, so they keep an inverted index but learn which terms matter. Late interaction models such "
        "as ColBERT keep one vector per token and match tokens against tokens, which is more accurate and "
        "more expensive to store. Rerankers read the query and document together and appear only in "
        "Reranking mode.\n\n"
        "Reranking mode can also list dense or late-interaction rows scored over the same candidates, "
        "plus a BM25 row carried over from full-corpus retrieval as a lexical reference, so this filter "
        "is useful there to compare one family at a time.\n\n"
        "A good first use is to check BM25: any dense model that cannot beat a lexical baseline on your "
        "task family is not worth the serving cost."
    ),
)


ACTIVE_PARAMS = HelpCopy(
    title="Active params",
    summary="Keeps only models whose active parameter count, in millions, falls inside the range you set.",
    details=(
        "Active params here is the non-embedding parameter count, in millions: total parameters minus the "
        "input embedding table. It is not the per-token active count that mixture-of-experts model cards "
        "advertise; see the Active Params column help for what the number does and does not mean.\n\n"
        "For example, a max of 500 keeps models with at most 500M non-embedding parameters, which is a "
        "reasonable ceiling for indexing a large corpus on modest hardware.\n\n"
        "Rows without active-parameter metadata are excluded as soon as either bound is set. This range "
        "narrows the ranked model population immediately, even when Recalculate ranks from filters is "
        "off, so the ranks you see are ranks among models of that size."
    ),
)


TOTAL_PARAMS = HelpCopy(
    title="Total params",
    summary="Keeps only models whose total parameter count, in millions, falls inside the range you set.",
    details=(
        "Total params is the full parameter count of the model, in millions, including the input embedding "
        "table. It predicts the memory and download footprint, while Active params drops the embedding "
        "table so models with very different vocabulary sizes can be compared.\n\n"
        "For example, a max of 1000 keeps models of roughly 1B parameters or less.\n\n"
        "Rows without total-parameter metadata are excluded as soon as either bound is set. This range "
        "narrows the ranked model population immediately, even when Recalculate ranks from filters is off."
    ),
)


QUERY_LENGTH = HelpCopy(
    title="Query length",
    summary="Keeps only tasks whose queries are, on average, as long as you specify.",
    details=(
        "Query length is task metadata: the average number of characters per query in that task. Short "
        "queries behave like keyword search, while long ones look more like questions or whole "
        "paragraphs, and models are not equally good at both.\n\n"
        "For example, a max of 120 keeps the tasks with short, search-box style queries, which is the "
        "right subset if that is what your product sends.\n\n"
        "Tasks without query-length metadata are excluded as soon as either bound is set. This range "
        "narrows the ranked task population immediately, even when Recalculate ranks from filters is off."
    ),
)


DOCUMENT_LENGTH = HelpCopy(
    title="Document length",
    summary="Keeps only tasks whose documents are, on average, as long as you specify.",
    details=(
        "Document length is task metadata: the average number of characters per document in that task. It "
        "matters because long documents can exceed a model's maximum token length and get truncated, "
        "which is where models with short context windows lose ground.\n\n"
        "For example, a min of 4000 keeps the long-document tasks, which is the subset to read together "
        "with the Max Tokens column.\n\n"
        "Tasks without document-length metadata are excluded as soon as either bound is set. This range "
        "narrows the ranked task population immediately, even when Recalculate ranks from filters is off."
    ),
)


DIMS_FILTER = HelpCopy(
    title="Dims",
    summary="Keeps only dense rows whose embedding vectors have the number of dimensions you specify.",
    details=(
        "Dims is the length of the vector a dense model stores per document. It drives index size and "
        "memory directly: 1024 dimensions in float32 is 4KB per document, so 10M documents need about "
        "40GB before any compression.\n\n"
        "Both bounds are inclusive and an empty max means no upper limit, so a max of 768 keeps every row "
        "at 768 dimensions or fewer. Rows without dimension metadata, such as BM25, are excluded as soon "
        "as either bound is set.\n\n"
        "Turn on Dims under Efficiency variants to also see truncated versions of larger models here, "
        "which is the honest way to ask whether a 1024-dimension model cut to 256 beats a native "
        "256-dimension model."
    ),
)


QUANTIZATION_FILTER = HelpCopy(
    title="Quantization",
    summary="Keeps only rows stored in the numeric formats you select.",
    details=(
        "Quantization is how each number in an embedding is stored. Original keeps the uncompressed "
        "float rows, int8 keeps rows where each dimension was reduced to one byte, and binary keeps rows "
        "where only the sign of each dimension survives, which is 32x smaller than float32.\n\n"
        "The int8 and binary options only match anything when the matching variant rows have been brought "
        "into the table by the Quantization toggle under Efficiency variants.\n\n"
        "Use it to answer a storage-budget question, for example by showing only binary rows and reading "
        "the delta against each model's own base row."
    ),
)


BORDA_SCORE_COLUMN = HelpCopy(
    title="Borda Score",
    summary="Ranks models by how they place against each other on every task, not by their raw average.",
    details=(
        "For each task the models are ranked by score, and each model earns points from its position: "
        "100 for first place, 0 for last, and a proportional value in between, following "
        "100 x (N - rank) / (N - 1) for N models. A model's Borda Score is the mean of those per-task "
        "points, so it always sits between 0 and 100 and is a ranking score, not a quality score.\n\n"
        "Why it is the default sort: raw scores are not comparable across tasks. Some tasks are easy and "
        "everyone scores 0.9, others are hard and everyone scores 0.2, and averaging them lets a handful "
        "of high-variance tasks dominate. Borda asks the more robust question, 'how often does this model "
        "beat the others?', so a model that is consistently second everywhere can outrank one that wins "
        "loudly on a few tasks and stumbles elsewhere.\n\n"
        "Its trade-off is that it depends on the field: the score says how a model placed against exactly "
        "the models present in the current view, and it changes when the set of ranked models changes. It "
        "also hides margins, since beating the next model by 0.001 and by 0.2 earn the same points.\n\n"
        "Read it together with Macro Mean and Micro Mean, which give the absolute quality that Borda "
        "deliberately ignores. Ties share a rank and the following rank is skipped, as usual for "
        "competition ranking."
    ),
)


MACRO_MEAN_COLUMN = HelpCopy(
    title="Macro Mean",
    summary="The model's average score with every benchmark counting once, whatever its task count.",
    details=(
        "Macro Mean first averages the tasks inside each benchmark into one score per benchmark, then "
        "averages those benchmark scores. A suite with 182 tasks and a suite with 5 tasks therefore have "
        "the same influence on the result.\n\n"
        "It is the number to read when you want breadth across benchmark families rather than a raw "
        "average dominated by whichever suite happens to be largest.\n\n"
        "The value is the selected metric multiplied by 100, nDCG@10 by default. Compare it with Micro "
        "Mean in the next column: a model whose Macro Mean is clearly lower than its Micro Mean is strong "
        "on the big suites and weaker on the smaller, often more specialized ones."
    ),
)


MICRO_MEAN_COLUMN = HelpCopy(
    title="Micro Mean",
    summary="The model's plain average over every task in scope, with each task counting once.",
    details=(
        "Micro Mean averages all raw task scores equally, so benchmarks contribute in proportion to how "
        "many tasks they contain. M-BEIR alone contributes all 182 cells of its 13-task x 14-language "
        "matrix.\n\n"
        "It is the straightforward 'average over everything that was measured' number, and it is the one "
        "to use when the task mix of the benchmark already reflects what you care about.\n\n"
        "The value is the selected metric multiplied by 100, nDCG@10 by default. Compare it with Macro "
        "Mean in the previous column to see whether a model's standing depends on the large multilingual "
        "suites."
    ),
)


ACTIVE_PARAMS_COLUMN = HelpCopy(
    title="Active Params",
    summary="The parameters that actually compute: the model without its token embedding lookup table.",
    details=(
        "HAKARI-Bench computes this as Total Params minus the input embedding parameters, and stores the "
        "same value as transformer_parameters. Looking a token up in the embedding table is a table read, "
        "not arithmetic, so those weights inflate a checkpoint without doing the work of encoding a "
        "document. Dropping them is what makes a model with a 250K-token multilingual vocabulary "
        "comparable to one with a 30K English vocabulary.\n\n"
        "One caveat, because the term is overloaded: this is not the mixture-of-experts sense of active "
        "parameters. Expert routing is not modelled here, so every expert is counted whether or not a "
        "token would use it. nomic-embed-text-v2-moe shows 283M in this column, which is its 475M total "
        "minus a 192M embedding table - not the smaller per-token expert subset its model card "
        "advertises. The two numbers share a name and measure different things, so do not compare this "
        "column against a published MoE active-parameter figure.\n\n"
        "Read it as encoder size, which is a reasonable proxy for cost among dense transformers of "
        "similar shape, and a poor one across architectures. Hosted API models that do not publish their "
        "size show Unknown. Switch to Chart with Active Params on the x axis to see which models sit "
        "above the quality-per-size trend, and use the Active params range under Filter results to keep "
        "only the sizes you could deploy."
    ),
)


TOTAL_PARAMS_COLUMN = HelpCopy(
    title="Total Params",
    summary="Every parameter in the checkpoint, which is what has to fit in memory.",
    details=(
        "Total Params counts the whole model: the transformer, the token embedding matrix, and, for a "
        "mixture-of-experts model, all experts whether or not a given token uses them.\n\n"
        "The gap between this column and Active Params is exactly the input embedding table, so a wide "
        "gap means a large vocabulary rather than sparse computation. embeddinggemma-300m is the clear "
        "case: 308M total against 106M in Active Params, because a vocabulary of roughly 260K tokens carries "
        "most of the checkpoint.\n\n"
        "Read it as the memory and download footprint. As a rough guide, bf16 weights need about 2 bytes "
        "per parameter, so a 600M-parameter model is around 1.2GB before any runtime overhead. Hosted API "
        "models that do not publish their size show Unknown."
    ),
)


MAX_TOKENS_COLUMN = HelpCopy(
    title="Max Tokens",
    summary="The longest input the model accepts; anything past this point is cut off before encoding.",
    details=(
        "This is the model's configured maximum sequence length. A document longer than the limit is "
        "truncated, so its tail never reaches the encoder and can never help it match a query. That is "
        "why a 512-token model can look fine on short-passage tasks and fall behind on long-document ones.\n\n"
        "Read it together with the Document length filter: restrict the tasks to long documents and the "
        "gap between short-context and long-context models becomes visible in the ranking.\n\n"
        "Every model here was evaluated at its own configured maximum. The benchmark never shortens a "
        "model's sequence length to save time, because that would make its scores incomparable; if a run "
        "ever had to deviate, it is recorded in that result's metadata."
    ),
)


DIMS_COLUMN = HelpCopy(
    title="Dims",
    summary="How many numbers each embedding stores, which sets the index size for your whole corpus.",
    details=(
        "Dims is the length of the dense vector the model produces per query and per document. The "
        "storage cost is immediate: 1024 dimensions in float32 is 4KB per document, so a 10M-document "
        "corpus needs roughly 40GB of vectors before any compression.\n\n"
        "More dimensions is not automatically better. Small, well-trained models frequently beat larger "
        "vectors on this board, and the badge next to a model name repeats its dimension so a compact "
        "model is easy to spot.\n\n"
        "Many models are trained so the leading dimensions carry most of the signal, which lets you cut a "
        "vector down without re-encoding. Turn on Dims under Efficiency variants to see those truncated "
        "rows with the quality they actually cost. Rows without a dense vector, such as BM25 and learned "
        "sparse retrieval, have no value here."
    ),
)


DELTA_VS_BASE_COLUMN = HelpCopy(
    title="Δ vs Base",
    summary="How much quality an efficiency variant gains or loses against the same model's uncompressed row.",
    details=(
        "This column appears once Efficiency variants brings in compressed, truncated, or rescored rows. "
        "For each such row it shows the relative change of the mean score against that model's own base "
        "row, as a percentage: -3.0 means the variant scores 3% lower than the full-precision, "
        "full-dimension version of the same model.\n\n"
        "It is relative, not absolute, so it answers 'what does this compression cost?' rather than "
        "'how good is this model?'. Base rows themselves have no value here, because they are the "
        "reference.\n\n"
        "This is the number to sort by when you are choosing a serving configuration: look for the "
        "variant with the largest size or speed win and the smallest loss, and remember that a rescore "
        "row usually recovers most of what quantization gave away."
    ),
)


MEAN_SCORE_COLUMN = HelpCopy(
    title="Mean Score",
    summary="The model's average score over the tasks currently in scope.",
    details=(
        "Mean Score is the average of the model's per-task scores in the selected benchmark scope, shown "
        "as the selected metric multiplied by 100. Unlike Borda Score it is an absolute quality number, so "
        "it can be compared with published results for the same metric.\n\n"
        "In the Overall scope this column is replaced by Macro Mean and Micro Mean, which show the two "
        "aggregation choices side by side; here a single benchmark is in view, so one average is enough.\n\n"
        "Read it alongside Borda Score. A model can have a slightly lower mean but a better Borda Score "
        "when it wins more of the individual tasks by small margins."
    ),
)
