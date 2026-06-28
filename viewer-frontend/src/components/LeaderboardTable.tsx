import { ArrowDown, ArrowUp } from 'lucide-react';
import { useMemo } from 'react';
import type { LeaderboardResponse, LeaderboardRow } from '../lib/api';
import { cn } from '../lib/cn';
import { heatBackground, normalize, zScoreColor } from '../lib/heat';
import {
  dimBadge,
  displayModelName,
  formatDim,
  formatMaxLen,
  formatParams,
  formatScore,
  shortModelTypeLabel,
} from '../lib/format';

interface LeaderboardTableProps {
  result: LeaderboardResponse;
  sort: string;
  direction: 'asc' | 'desc';
  onSort: (column: string) => void;
  onSelectModel: (row: LeaderboardRow) => void;
}

type Align = 'left' | 'right';

interface ColumnDef {
  key: string; // sort key
  label: string;
  sortable: boolean;
  align: Align;
  kind: 'score' | 'metric' | 'plain';
  metricKey?: string;
  scoreField?: 'borda_score' | 'macro_mean' | 'micro_mean' | 'mean_score';
  render?: (row: LeaderboardRow) => string;
}

function SortIcon({ active, direction }: { active: boolean; direction: 'asc' | 'desc' }) {
  if (!active) return null;
  return direction === 'desc' ? (
    <ArrowDown className="ml-0.5 inline h-3 w-3" strokeWidth={2} />
  ) : (
    <ArrowUp className="ml-0.5 inline h-3 w-3" strokeWidth={2} />
  );
}

function ScoreText({
  score,
  z,
  rank,
  showRank,
  showZ,
}: {
  score: number | null | undefined;
  z?: number | null;
  rank?: number | null;
  showRank: boolean;
  showZ: boolean;
}) {
  if (score === null || score === undefined) return <span className="text-faint-foreground">—</span>;
  // Ranks-only: render the rank value plainly, like a Borda rank.
  if (showRank && !showZ) {
    return <span>{rank !== null && rank !== undefined ? Math.round(rank) : '—'}</span>;
  }
  return (
    <span>
      {showRank && rank !== null && rank !== undefined ? (
        <span className="text-faint-foreground">[{Math.round(rank)}] </span>
      ) : null}
      {formatScore(score)}
      {showZ && z !== null && z !== undefined ? (
        <span className="ml-0.5 text-[10px]" style={{ color: zScoreColor(z) }}>
          {z >= 0 ? '+' : ''}
          {z.toFixed(2)}σ
        </span>
      ) : null}
    </span>
  );
}

export function LeaderboardTable({ result, sort, direction, onSort, onSelectModel }: LeaderboardTableProps) {
  const rows = result.rows;
  const showZ = result.show_task_z_scores;
  const showRank = result.show_task_ranks;
  const maxBorda = rows.reduce((max, r) => Math.max(max, r.borda_score), 0);

  const columns = useMemo<ColumnDef[]>(() => {
    const cols: ColumnDef[] = [
      { key: 'borda_score', label: 'Borda Score', sortable: true, align: 'right', kind: 'score', scoreField: 'borda_score' },
    ];
    const meansAsOverall = result.is_overall && !(result.rank_filtered && result.task_filter);
    if (meansAsOverall) {
      cols.push({ key: 'macro_mean', label: 'Macro Mean', sortable: true, align: 'right', kind: 'score', scoreField: 'macro_mean' });
      cols.push({ key: 'micro_mean', label: 'Micro Mean', sortable: true, align: 'right', kind: 'score', scoreField: 'micro_mean' });
    } else {
      cols.push({ key: 'mean_score', label: 'Mean Score', sortable: true, align: 'right', kind: 'score', scoreField: 'mean_score' });
    }
    for (const column of result.metric_columns) {
      cols.push({
        key: `metric:${column}`,
        label: result.metric_column_labels[column] ?? column,
        sortable: true,
        align: 'right',
        kind: 'metric',
        metricKey: column,
      });
    }
    cols.push({ key: 'active_parameters', label: 'Active Params', sortable: true, align: 'right', kind: 'plain', render: (r) => formatParams(r.active_parameters) });
    cols.push({ key: 'total_parameters', label: 'Total Params', sortable: true, align: 'right', kind: 'plain', render: (r) => formatParams(r.total_parameters) });
    cols.push({ key: 'max_seq_length', label: 'Max Tokens', sortable: true, align: 'right', kind: 'plain', render: (r) => formatMaxLen(r.max_seq_length) });
    cols.push({ key: 'embedding_dim', label: 'Dims', sortable: true, align: 'right', kind: 'plain', render: (r) => formatDim(r.embedding_dim) });
    if (result.include_quantization_variants) {
      cols.push({ key: 'quantization', label: 'Quant', sortable: true, align: 'left', kind: 'plain', render: (r) => r.quantization ?? '—' });
    }
    if (result.show_other_columns) {
      cols.push({ key: 'license', label: 'License', sortable: false, align: 'left', kind: 'plain', render: (r) => r.license?.label ?? '—' });
      cols.push({ key: 'model_type', label: 'Model Type', sortable: false, align: 'left', kind: 'plain', render: (r) => shortModelTypeLabel(r.model_type) });
    }
    return cols;
  }, [result]);

  // Per-column value ranges for heat shading.
  const ranges = useMemo(() => {
    const map = new Map<string, { min: number; max: number }>();
    const track = (key: string, value: number | null | undefined) => {
      if (value === null || value === undefined || Number.isNaN(value)) return;
      const current = map.get(key);
      if (!current) map.set(key, { min: value, max: value });
      else {
        current.min = Math.min(current.min, value);
        current.max = Math.max(current.max, value);
      }
    };
    for (const row of rows) {
      for (const col of columns) {
        if (col.kind === 'score' && col.scoreField) track(col.key, row[col.scoreField] as number | null);
        else if (col.kind === 'metric' && col.metricKey) track(col.key, row.metric_values[col.metricKey]);
      }
    }
    return map;
  }, [rows, columns]);

  const heatFor = (col: ColumnDef, value: number | null | undefined): string | undefined => {
    if (value === null || value === undefined) return undefined;
    if (showRank && !showZ && col.kind === 'metric') return undefined; // ranks-only: no heat
    const range = ranges.get(col.key);
    if (!range) return undefined;
    return heatBackground(normalize(value, range.min, range.max));
  };

  const zField: Record<string, 'borda_score_z' | 'macro_mean_z' | 'micro_mean_z' | undefined> = {
    borda_score: 'borda_score_z',
    macro_mean: 'macro_mean_z',
    micro_mean: 'micro_mean_z',
  };

  return (
    <div className="overflow-x-auto rounded-lg border border-border">
      <table className="w-full border-collapse text-[12px]">
        <thead>
          <tr className="border-b border-border text-[11px] text-muted-foreground">
            <th className="sticky left-0 z-20 w-8 bg-surface px-2 py-1.5 text-right font-normal" />
            <th
              className="sticky left-8 z-20 cursor-pointer bg-surface px-2 py-1.5 text-left font-normal hover:text-accent"
              onClick={() => onSort('model_name')}
            >
              Model Name
              <SortIcon active={sort === 'model_name'} direction={direction} />
            </th>
            {columns.map((col) => (
              <th
                key={col.key}
                className={cn(
                  'whitespace-nowrap px-3 py-1.5 font-normal',
                  col.align === 'right' ? 'text-right' : 'text-left',
                  col.sortable ? 'cursor-pointer hover:text-accent' : '',
                )}
                onClick={col.sortable ? () => onSort(col.key) : undefined}
                title={col.label}
              >
                {col.label}
                {col.sortable ? <SortIcon active={sort === col.key} direction={direction} /> : null}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => {
            const badge = dimBadge(row);
            const barWidth = maxBorda > 0 ? Math.max(0, (row.borda_score / maxBorda) * 100) : 0;
            return (
              <tr key={`${row.model_name}-${index}`} className="group border-b border-border/60 last:border-0">
                <td className="sticky left-0 z-10 w-8 bg-surface px-2 py-1 text-right tnum text-faint-foreground group-hover:bg-surface-faint">
                  {index + 1}
                </td>
                <td className="sticky left-8 z-10 bg-surface px-2 py-1 group-hover:bg-surface-faint">
                  <span
                    className="pointer-events-none absolute inset-y-0 left-0 bg-accent-soft"
                    style={{ width: `${barWidth}%` }}
                    aria-hidden
                  />
                  <span className="relative inline-flex items-center gap-1.5">
                    <button
                      type="button"
                      onClick={() => onSelectModel(row)}
                      className="font-medium text-foreground hover:text-accent hover:underline"
                      title={row.model_name}
                    >
                      {displayModelName(row.model_name)}
                    </button>
                    {badge ? (
                      <span className="rounded-sm bg-control px-1 py-px text-[10px] text-accent tnum">{badge}</span>
                    ) : null}
                  </span>
                </td>
                {columns.map((col) => {
                  if (col.kind === 'plain') {
                    return (
                      <td
                        key={col.key}
                        className={cn(
                          'whitespace-nowrap px-3 py-1 tnum text-muted-foreground group-hover:bg-surface-faint',
                          col.align === 'right' ? 'text-right' : 'text-left',
                        )}
                        title={col.key === 'license' ? (row.license?.label ?? undefined) : undefined}
                      >
                        {col.render ? col.render(row) : ''}
                      </td>
                    );
                  }
                  const value =
                    col.kind === 'metric' && col.metricKey
                      ? row.metric_values[col.metricKey]
                      : (row[col.scoreField as string] as number | null);
                  const z =
                    col.kind === 'metric' && col.metricKey
                      ? row.metric_z_values[col.metricKey]
                      : (row[zField[col.key] ?? ''] as number | null | undefined);
                  const rank =
                    col.kind === 'metric' && col.metricKey ? row.metric_rank_values[col.metricKey] : undefined;
                  const bg = heatFor(col, value);
                  return (
                    <td
                      key={col.key}
                      className={cn(
                        'whitespace-nowrap px-3 py-1 text-right tnum',
                        col.key === 'borda_score' ? 'font-medium text-foreground' : 'text-foreground',
                      )}
                      style={bg ? { backgroundColor: bg } : undefined}
                    >
                      <ScoreText score={value} z={z} rank={rank} showRank={showRank} showZ={showZ} />
                    </td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
