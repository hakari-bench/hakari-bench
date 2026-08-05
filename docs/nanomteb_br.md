# NanoMTEB-BR

NanoMTEB-BR is the Brazilian Portuguese language-focused retrieval suite in
HAKARI-Bench. It is derived from the six Retrieval tasks in
[MTEB-BR](https://github.com/tardellirs/mteb-br), using native Brazilian
Portuguese sources rather than machine-translated benchmark copies.

The dataset is published as
[`hakari-bench/NanoMTEB-BR`](https://huggingface.co/datasets/hakari-bench/NanoMTEB-BR).
The built-in definition is
[`config/datasets/nanomteb_br.yaml`](../config/datasets/nanomteb_br.yaml).

## Evaluation Scope

NanoMTEB-BR contributes six tasks to `evaluate --all`. When introduced, it
changed the complete built-in evaluation target from 551 to **557 tasks**. It
is available as a dedicated viewer benchmark and a Portuguese language page.

NanoMTEB-BR is included in the canonical 544-task Overall manifest. All six
result files must be evaluated, stored, and submitted.

| Task | Domain | Queries | Documents | Positive qrels |
| --- | --- | ---: | ---: | ---: |
| `BRTaxQAR` | Brazilian tax law | 200 | 461 | 546 |
| `FaQuADIR` | Higher-education FAQ | 200 | 243 | 201 |
| `FaqBacenRetrieval` | Central-bank FAQ | 200 | 1,654 | 201 |
| `JurisTCU` | Federal audit-court case law | 150 | 10,000 | 1,711 |
| `MedPTRetrieval` | Medical question answering | 200 | 500 | 204 |
| `Quati` | General passage retrieval | 49 | 10,000 | 892 |

## Dataset Layout

The dataset follows the standard HAKARI Nano layout:

- `corpus`, `queries`, and `qrels` contain the evaluation data;
- `bm25` contains the fixed BM25 top-500 candidate ranking;
- `harrier_oss_v1_270m` contains the fixed dense top-500 ranking;
- `reranking_hybrid` contains the reciprocal-rank-fused reranker candidate set.

The dataset revision used for the initial benchmark wave was
`00541a0fce4048057fb7ddec30d37155a5c23d95`. Result JSON records the resolved
dataset revision, so later dataset revisions remain auditable.

## Evaluation

Evaluate only NanoMTEB-BR with the same runtime policy used for other built-in
datasets:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_ID \
  --dataset NanoMTEB-BR \
  --attn-implementation sdpa
```

After this dataset is installed in the built-in registry, a normal complete run
includes it automatically:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_ID \
  --all \
  --attn-implementation sdpa
```

Reranker evaluation uses the standard `reranking_hybrid` candidate ranking and
does not require a NanoMTEB-BR-specific backend.

## Full-to-Nano Validation

The initial validation matched 29 models with complete results in both the
official MTEB-BR leaderboard and NanoMTEB-BR as of 2026-08-04. For each
benchmark, the same 29 models were ranked independently on the six Retrieval
tasks by nDCG@10, and their six task ranks were summed into a Borda rank.

- Spearman rank correlation: **0.9860**
- Kendall rank correlation: **0.9320**
- **28 of 29 models** remained within plus or minus two Borda-rank positions.
- The single exception was
  `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, with a
  five-position difference.

This validates NanoMTEB-BR as a close rank-preserving proxy for the full
MTEB-BR Retrieval suite within the compared model population. It does not imply
that absolute nDCG@10 values are interchangeable, because the Nano corpora and
query samples are smaller.

## Sources

- [MTEB-BR source repository](https://github.com/tardellirs/mteb-br)
- [MTEB-BR leaderboard](https://huggingface.co/spaces/MTEB-BR/leaderboard)
- [MTEB-BR results dataset](https://huggingface.co/datasets/MTEB-BR/mteb-pt-results)
- [NanoMTEB-BR dataset](https://huggingface.co/datasets/hakari-bench/NanoMTEB-BR)
