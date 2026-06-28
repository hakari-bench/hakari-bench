import { ChevronDown, ChevronRight, Filter } from 'lucide-react';
import { useEffect, useState, type ReactNode } from 'react';
import type { FilterFacetKey, LeaderboardResponse } from '../lib/api';
import { cn } from '../lib/cn';
import type { ViewerState } from '../lib/urlState';
import { ToggleChip } from '../ui/controls';

interface FilterPanelProps {
  result: LeaderboardResponse;
  state: ViewerState;
  update: (patch: Partial<ViewerState>) => void;
}

const FACET_TO_FIELD: Record<Exclude<FilterFacetKey, 'dim'>, keyof ViewerState> = {
  quant: 'quantFilter',
  commercial: 'commercialFilter',
  model_type: 'modelTypeFilter',
  dtype: 'dtypeFilter',
  attn: 'attnFilter',
  prompt: 'promptFilter',
};

function dimBound(values: string[], prefix: string): string {
  const hit = values.find((value) => value.startsWith(prefix));
  return hit ? hit.slice(prefix.length) : '';
}

/** Small numeric input that only reports its value on Enter / blur. */
function NumericInput({
  value,
  placeholder,
  onCommit,
  width = 'w-16',
}: {
  value: string;
  placeholder: string;
  onCommit: (value: string) => void;
  width?: string;
}) {
  const [pending, setPending] = useState(value);
  useEffect(() => setPending(value), [value]);
  return (
    <input
      type="number"
      inputMode="numeric"
      value={pending}
      placeholder={placeholder}
      onChange={(event) => setPending(event.target.value)}
      onBlur={() => onCommit(pending.trim())}
      onKeyDown={(event) => {
        if (event.key === 'Enter') {
          event.preventDefault();
          onCommit(pending.trim());
        }
      }}
      className={cn(
        width,
        'rounded-sm border border-border bg-surface px-1.5 py-0.5 text-[12px] tnum',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent',
      )}
    />
  );
}

function TextInput({
  value,
  placeholder,
  onCommit,
}: {
  value: string;
  placeholder: string;
  onCommit: (value: string) => void;
}) {
  const [pending, setPending] = useState(value);
  useEffect(() => setPending(value), [value]);
  return (
    <input
      type="text"
      value={pending}
      placeholder={placeholder}
      onChange={(event) => setPending(event.target.value)}
      onBlur={() => onCommit(pending.trim())}
      onKeyDown={(event) => {
        if (event.key === 'Enter') {
          event.preventDefault();
          onCommit(pending.trim());
        }
      }}
      className={cn(
        'w-36 rounded-sm border border-border bg-surface px-1.5 py-0.5 text-[12px]',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent',
      )}
    />
  );
}

function Label({ children }: { children: ReactNode }) {
  return <span className="text-[11px] font-semibold text-muted-foreground">{children}</span>;
}

export function FilterPanel({ result, state, update }: FilterPanelProps) {
  const hasParamsOrLength =
    !!(state.activeParamsMin || state.activeParamsMax || state.totalParamsMin || state.totalParamsMax) ||
    !!(state.queryLenMin || state.queryLenMax || state.docLenMin || state.docLenMax);
  const autoOpen = state.filters || hasParamsOrLength || !!state.modelFilter || !!state.taskFilter;
  const [open, setOpen] = useState(autoOpen);
  useEffect(() => {
    if (autoOpen) setOpen(true);
  }, [autoOpen]);

  const facets = result.filter_facets;
  const selected = result.filter_selected;

  const toggleFacet = (facet: Exclude<FilterFacetKey, 'dim'>, value: string) => {
    const options = facets[facet].map((option) => option.value);
    const current = new Set(selected[facet]);
    if (current.has(value)) current.delete(value);
    else current.add(value);
    const next = options.filter((option) => current.has(option));
    const field = FACET_TO_FIELD[facet];
    update({ [field]: next.length === options.length ? [] : next, filters: true } as Partial<ViewerState>);
  };

  const commitDims = (which: 'min' | 'max', raw: string) => {
    const min = which === 'min' ? raw : dimBound(state.dimFilter, 'gte:');
    const max = which === 'max' ? raw : dimBound(state.dimFilter, 'lte:');
    const next: string[] = [];
    if (min) next.push(`gte:${min}`);
    if (max) next.push(`lte:${max}`);
    update({ dimFilter: next, filters: true });
  };

  const facetGroup = (facet: Exclude<FilterFacetKey, 'dim'>, label: string) =>
    facets[facet].length ? (
      <div className="flex flex-wrap items-center gap-1.5">
        <Label>{label}</Label>
        {facets[facet].map((option) => (
          <ToggleChip
            key={option.value}
            checked={selected[facet].includes(option.value)}
            onChange={() => toggleFacet(facet, option.value)}
          >
            {option.label}
          </ToggleChip>
        ))}
      </div>
    ) : null;

  const shownCount = result.rows.length;
  const totalCount = result.total_row_count;

  return (
    <section className="rounded-lg border border-border bg-surface p-1.5 text-[12px]">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="flex w-full items-center gap-1.5 rounded-md px-1 py-1 text-left text-muted-foreground hover:text-accent"
      >
        {open ? (
          <ChevronDown className="h-3.5 w-3.5" strokeWidth={1.75} />
        ) : (
          <ChevronRight className="h-3.5 w-3.5" strokeWidth={1.75} />
        )}
        <Filter className="h-3.5 w-3.5 text-accent" strokeWidth={1.75} />
        <span className="font-semibold text-foreground">Filter results</span>
        {shownCount !== totalCount ? (
          <span className="tnum text-faint-foreground">
            {shownCount} / {totalCount}
          </span>
        ) : null}
      </button>

      {open ? (
        <div className="mt-1.5 grid gap-2 border-t border-border/60 pt-2">
          <div className="grid gap-3 md:grid-cols-2">
            {/* Left lane: Model, Dims, Active params, Query length */}
            <div className="grid gap-2">
              <div className="flex items-center gap-1.5">
                <Label>Model</Label>
                <TextInput
                  value={state.modelFilter}
                  placeholder="jina bge…"
                  onCommit={(value) => update({ modelFilter: value })}
                />
              </div>
              <div className="flex items-center gap-1.5">
                <Label>Dims</Label>
                <NumericInput
                  value={dimBound(state.dimFilter, 'gte:')}
                  placeholder="min"
                  onCommit={(value) => commitDims('min', value)}
                />
                <span className="text-faint-foreground">–</span>
                <NumericInput
                  value={dimBound(state.dimFilter, 'lte:')}
                  placeholder="max"
                  onCommit={(value) => commitDims('max', value)}
                />
              </div>
              <div className="flex items-center gap-1.5">
                <Label>Active params (M)</Label>
                <NumericInput
                  value={state.activeParamsMin}
                  placeholder="min"
                  onCommit={(value) => update({ activeParamsMin: value, filters: true })}
                />
                <span className="text-faint-foreground">–</span>
                <NumericInput
                  value={state.activeParamsMax}
                  placeholder="max"
                  onCommit={(value) => update({ activeParamsMax: value, filters: true })}
                />
              </div>
              <div className="flex items-center gap-1.5">
                <Label>Query length</Label>
                <NumericInput
                  value={state.queryLenMin}
                  placeholder="min"
                  onCommit={(value) => update({ queryLenMin: value, filters: true })}
                />
                <span className="text-faint-foreground">–</span>
                <NumericInput
                  value={state.queryLenMax}
                  placeholder="max"
                  onCommit={(value) => update({ queryLenMax: value, filters: true })}
                />
              </div>
            </div>

            {/* Right lane: Task, Quantization, Total params, Document length */}
            <div className="grid gap-2">
              <div className="flex items-center gap-1.5">
                <Label>Task</Label>
                <TextInput
                  value={state.taskFilter}
                  placeholder="nq miracl…"
                  onCommit={(value) => update({ taskFilter: value })}
                />
              </div>
              {facetGroup('quant', 'Quantization')}
              <div className="flex items-center gap-1.5">
                <Label>Total params (M)</Label>
                <NumericInput
                  value={state.totalParamsMin}
                  placeholder="min"
                  onCommit={(value) => update({ totalParamsMin: value, filters: true })}
                />
                <span className="text-faint-foreground">–</span>
                <NumericInput
                  value={state.totalParamsMax}
                  placeholder="max"
                  onCommit={(value) => update({ totalParamsMax: value, filters: true })}
                />
              </div>
              <div className="flex items-center gap-1.5">
                <Label>Document length</Label>
                <NumericInput
                  value={state.docLenMin}
                  placeholder="min"
                  onCommit={(value) => update({ docLenMin: value, filters: true })}
                />
                <span className="text-faint-foreground">–</span>
                <NumericInput
                  value={state.docLenMax}
                  placeholder="max"
                  onCommit={(value) => update({ docLenMax: value, filters: true })}
                />
              </div>
            </div>
          </div>

          {/* Buckets: license, model type, dtype, attn, prompt */}
          <div className="grid gap-1.5 border-t border-border/60 pt-2">
            {facetGroup('commercial', 'License')}
            {facetGroup('model_type', 'Model type')}
            {facetGroup('dtype', 'Dtype')}
            {facetGroup('attn', 'Attention')}
            {facetGroup('prompt', 'Prompt')}
          </div>

          <div className="flex items-center gap-1.5 border-t border-border/60 pt-2">
            <ToggleChip
              checked={state.rankFiltered}
              onChange={(value) => update({ rankFiltered: value })}
            >
              Recalculate ranks among filtered rows
            </ToggleChip>
          </div>
        </div>
      ) : null}
    </section>
  );
}
