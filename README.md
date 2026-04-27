# nano-ir-bench

Nano-style information retrieval benchmark runner for SentenceTransformers-compatible models.

## Example

```bash
uv run nano-ir-bench evaluate \
  --model hotchpotch/bekko-embedding-pico-beta-unir-v7 \
  --dataset sentence-transformers/NanoBEIR-en \
  --dtype bf16
```

Results are written under:

```text
output/results/{model_name}/{dataset_name}/{split_or_task}.json
```
