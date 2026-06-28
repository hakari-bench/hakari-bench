import { ArrowDown, ArrowUp } from 'lucide-react';
import type { LeaderboardResponse, LeaderboardRow } from '../lib/api';
import { cn } from '../lib/cn';
import { formatDim, formatMaxLen, formatParams, formatScore, shortModelName } from '../lib/format';

interface Column {
  key: string;
  label: string;
  align: 'left' | 'right';
  render: (row: LeaderboardRow) => string;
}

const COLUMNS: Column[] = [
  { key: 'borda_score', label: 'Borda Score', align: 'right', render: (r) => formatScore(r.borda_score) },
  { key: 'macro_mean', label: 'Macro Mean', align: 'right', render: (r) => formatScore(r.macro_mean) },
  { key: 'micro_mean', label: 'Micro Mean', align: 'right', render: (r) => formatScore(r.micro_mean) },
  { key: 'active_parameters', label: 'Active Params', align: 'right', render: (r) => formatParams(r.active_parameters) },
  { key: 'total_parameters', label: 'Total Params', align: 'right', render: (r) => formatParams(r.total_parameters) },
  { key: 'max_seq_length', label: 'Max Tokens', align: 'right', render: (r) => formatMaxLen(r.max_seq_length) },
  { key: 'embedding_dim', label: 'Dims', align: 'right', render: (r) => formatDim(r.embedding_dim) },
];

interface LeaderboardTableProps {
  result: LeaderboardResponse;
  sort: string;
  direction: 'asc' | 'desc';
  onSort: (column: string) => void;
}

function dimBadge(row: LeaderboardRow): string | null {
  if (row.embedding_dim !== null && row.embedding_dim !== undefined) return `${row.embedding_dim}d`;
  const type = (row.model_type ?? '').toLowerCase();
  if (type.includes('sparse') || row.model_name.toLowerCase().includes('bm25')) return 'sparse';
  return null;
}

function SortIcon({ active, direction }: { active: boolean; direction: 'asc' | 'desc' }) {
  if (!active) return null;
  return direction === 'desc' ? (
    <ArrowDown className="ml-1 inline h-3 w-3" strokeWidth={2} />
  ) : (
    <ArrowUp className="ml-1 inline h-3 w-3" strokeWidth={2} />
  );
}

export function LeaderboardTable({ result, sort, direction, onSort }: LeaderboardTableProps) {
  const rows = result.rows;
  const maxBorda = rows.reduce((max, r) => Math.max(max, r.borda_score), 0);

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
            {COLUMNS.map((col) => (
              <th
                key={col.key}
                className="cursor-pointer whitespace-nowrap px-3 py-1.5 text-right font-normal hover:text-accent"
                onClick={() => onSort(col.key)}
              >
                {col.label}
                <SortIcon active={sort === col.key} direction={direction} />
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => {
            const badge = dimBadge(row);
            const barWidth = maxBorda > 0 ? Math.max(0, (row.borda_score / maxBorda) * 100) : 0;
            return (
              <tr key={row.model_name} className="group border-b border-border/60 last:border-0">
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
                    <span className="font-medium text-foreground">{shortModelName(row.model_name)}</span>
                    {badge ? (
                      <span className="rounded-sm bg-control px-1 py-px text-[10px] text-accent tnum">
                        {badge}
                      </span>
                    ) : null}
                  </span>
                </td>
                {COLUMNS.map((col) => (
                  <td
                    key={col.key}
                    className={cn(
                      'whitespace-nowrap px-3 py-1 tnum group-hover:bg-surface-faint',
                      col.align === 'right' ? 'text-right' : 'text-left',
                      col.key === 'borda_score' ? 'font-medium text-foreground' : 'text-muted-foreground',
                    )}
                  >
                    {col.render(row)}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
