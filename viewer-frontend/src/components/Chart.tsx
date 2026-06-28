import { useState } from 'react';
import type { LeaderboardResponse, LeaderboardRow } from '../lib/api';
import { displayModelName, formatDim, formatParams, formatScore } from '../lib/format';
import type { ViewerState } from '../lib/urlState';

interface ChartProps {
  result: LeaderboardResponse;
  state: ViewerState;
  update: (patch: Partial<ViewerState>) => void;
}

interface AxisField {
  value: string;
  label: string;
  log: boolean;
  get: (row: LeaderboardRow) => number | null;
}

const Y_FIELDS: AxisField[] = [
  { value: 'borda_score', label: 'Borda Score', log: false, get: (r) => r.borda_score },
  { value: 'macro_mean', label: 'Macro Mean', log: false, get: (r) => r.macro_mean },
  { value: 'micro_mean', label: 'Micro Mean', log: false, get: (r) => r.micro_mean },
];

const X_FIELDS: AxisField[] = [
  { value: 'active_parameters', label: 'Active Params (log)', log: true, get: (r) => r.active_parameters },
  { value: 'total_parameters', label: 'Total Params (log)', log: true, get: (r) => r.total_parameters },
  { value: 'max_seq_length', label: 'Max Tokens', log: false, get: (r) => r.max_seq_length },
  { value: 'embedding_dim', label: 'Dims (log)', log: true, get: (r) => r.embedding_dim },
];

const COLOR_FIELDS: AxisField[] = [
  { value: 'embedding_dim', label: 'Dims', log: true, get: (r) => r.embedding_dim },
  { value: 'active_parameters', label: 'Active Params', log: true, get: (r) => r.active_parameters },
  { value: 'none', label: 'None', log: false, get: () => null },
];

const WIDTH = 920;
const HEIGHT = 460;
const PAD = { top: 16, right: 96, bottom: 44, left: 52 };

function findField(fields: AxisField[], value: string): AxisField {
  return fields.find((f) => f.value === value) ?? fields[0];
}

function colorStops(t: number): string {
  const stops = [
    [124, 58, 237],
    [6, 182, 212],
    [245, 158, 11],
  ];
  const clamped = Math.min(1, Math.max(0, t));
  const seg = clamped < 0.5 ? 0 : 1;
  const local = clamped < 0.5 ? clamped * 2 : (clamped - 0.5) * 2;
  const a = stops[seg];
  const b = stops[seg + 1];
  const mix = a.map((channel, i) => Math.round(channel + (b[i] - channel) * local));
  return `rgb(${mix[0]}, ${mix[1]}, ${mix[2]})`;
}

function scaleValue(value: number, min: number, max: number, log: boolean): number {
  if (log) {
    const lv = Math.log10(Math.max(value, 1));
    const lmin = Math.log10(Math.max(min, 1));
    const lmax = Math.log10(Math.max(max, 1));
    return lmax <= lmin ? 0.5 : (lv - lmin) / (lmax - lmin);
  }
  return max <= min ? 0.5 : (value - min) / (max - min);
}

function Selector({
  label,
  value,
  options,
  onChange,
}: {
  label: string;
  value: string;
  options: AxisField[];
  onChange: (value: string) => void;
}) {
  return (
    <label className="inline-flex items-center gap-1 text-[11px] text-muted-foreground">
      {label}
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="rounded-sm border border-border bg-surface px-1 py-0.5 text-[11px] text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}

export function Chart({ result, state, update }: ChartProps) {
  const [hover, setHover] = useState<number | null>(null);
  const yField = findField(Y_FIELDS, state.chartY);
  const xField = findField(X_FIELDS, state.chartX);
  const colorField = findField(COLOR_FIELDS, state.chartColor);

  const points = result.rows
    .map((row, index) => ({ row, index, x: xField.get(row), y: yField.get(row) }))
    .filter((p): p is { row: LeaderboardRow; index: number; x: number; y: number } => p.x !== null && p.y !== null);

  const xs = points.map((p) => p.x);
  const ys = points.map((p) => p.y);
  const xMin = Math.min(...xs, 1);
  const xMax = Math.max(...xs, 1);
  const yMin = yField.value === 'borda_score' ? 0 : Math.min(...ys);
  const yMax = yField.value === 'borda_score' ? 100 : Math.max(...ys);

  const colorValues = colorField.value === 'none' ? [] : points.map((p) => colorField.get(p.row) ?? 0);
  const cMin = colorValues.length ? Math.min(...colorValues) : 0;
  const cMax = colorValues.length ? Math.max(...colorValues) : 1;

  const plotW = WIDTH - PAD.left - PAD.right;
  const plotH = HEIGHT - PAD.top - PAD.bottom;
  const px = (x: number) => PAD.left + scaleValue(x, xMin, xMax, xField.log) * plotW;
  const py = (y: number) => PAD.top + (1 - scaleValue(y, yMin, yMax, false)) * plotH;

  const pointColor = (row: LeaderboardRow): string => {
    if (colorField.value === 'none') return 'var(--color-accent)';
    const value = colorField.get(row);
    if (value === null) return 'var(--color-faint-foreground)';
    return colorStops(scaleValue(value, cMin, cMax, colorField.log));
  };

  const yTicks = 5;
  const tickValues = Array.from({ length: yTicks + 1 }, (_, i) => yMin + ((yMax - yMin) * i) / yTicks);

  return (
    <div className="rounded-lg border border-border bg-surface p-2">
      <div className="mb-1 flex flex-wrap justify-end gap-3">
        <Selector label="Y" value={yField.value} options={Y_FIELDS} onChange={(v) => update({ chartY: v })} />
        <Selector label="X" value={xField.value} options={X_FIELDS} onChange={(v) => update({ chartX: v })} />
        <Selector label="Color" value={colorField.value} options={COLOR_FIELDS} onChange={(v) => update({ chartColor: v })} />
      </div>
      <div className="hidden md:block">
        <svg viewBox={`0 0 ${WIDTH} ${HEIGHT}`} className="w-full" role="img" aria-label="Leaderboard scatter plot">
          {/* Y grid + ticks */}
          {tickValues.map((value) => {
            const y = py(value);
            return (
              <g key={value}>
                <line x1={PAD.left} x2={WIDTH - PAD.right} y1={y} y2={y} stroke="var(--color-border)" strokeOpacity={0.4} />
                <text x={PAD.left - 6} y={y + 3} textAnchor="end" fontSize={10} fill="var(--color-faint-foreground)">
                  {formatScore(value)}
                </text>
              </g>
            );
          })}
          {/* axis labels */}
          <text x={PAD.left + plotW / 2} y={HEIGHT - 8} textAnchor="middle" fontSize={11} fill="var(--color-muted-foreground)">
            {xField.label}
          </text>
          <text
            x={14}
            y={PAD.top + plotH / 2}
            textAnchor="middle"
            fontSize={11}
            fill="var(--color-muted-foreground)"
            transform={`rotate(-90 14 ${PAD.top + plotH / 2})`}
          >
            {yField.label}
          </text>
          {/* points */}
          {points.map((p) => (
            <circle
              key={`${p.row.model_name}-${p.index}`}
              cx={px(p.x)}
              cy={py(p.y)}
              r={hover === p.index ? 6 : 4}
              fill={pointColor(p.row)}
              fillOpacity={0.85}
              stroke="var(--color-surface)"
              strokeWidth={0.75}
              onMouseEnter={() => setHover(p.index)}
              onMouseLeave={() => setHover(null)}
            />
          ))}
          {/* tooltip */}
          {hover !== null
            ? (() => {
                const p = points.find((pt) => pt.index === hover);
                if (!p) return null;
                const lines = [
                  displayModelName(p.row.model_name),
                  `${yField.label}: ${formatScore(p.y)}`,
                  `${xField.label.replace(' (log)', '')}: ${
                    xField.value.includes('param') ? formatParams(p.x) : formatDim(p.x)
                  }`,
                ];
                const boxW = 220;
                const boxH = 14 + lines.length * 14;
                const bx = Math.min(px(p.x) + 8, WIDTH - PAD.right - boxW);
                const by = Math.max(py(p.y) - boxH - 6, PAD.top);
                return (
                  <g pointerEvents="none">
                    <rect x={bx} y={by} width={boxW} height={boxH} rx={4} fill="var(--color-surface)" stroke="var(--color-border-strong)" />
                    {lines.map((line, i) => (
                      <text
                        key={line}
                        x={bx + 8}
                        y={by + 16 + i * 14}
                        fontSize={11}
                        fill={i === 0 ? 'var(--color-foreground)' : 'var(--color-muted-foreground)'}
                        fontWeight={i === 0 ? 600 : 400}
                      >
                        {line}
                      </text>
                    ))}
                  </g>
                );
              })()
            : null}
          {/* color legend */}
          {colorField.value !== 'none' ? (
            <g>
              <defs>
                <linearGradient id="hakari-color-legend" x1="0" y1="1" x2="0" y2="0">
                  <stop offset="0%" stopColor={colorStops(0)} />
                  <stop offset="50%" stopColor={colorStops(0.5)} />
                  <stop offset="100%" stopColor={colorStops(1)} />
                </linearGradient>
              </defs>
              <rect x={WIDTH - PAD.right + 24} y={PAD.top} width={12} height={plotH} fill="url(#hakari-color-legend)" rx={2} />
              <text x={WIDTH - PAD.right + 30} y={PAD.top - 4} textAnchor="middle" fontSize={10} fill="var(--color-faint-foreground)">
                {colorField.value === 'embedding_dim' ? formatDim(cMax) : formatParams(cMax)}
              </text>
              <text x={WIDTH - PAD.right + 30} y={PAD.top + plotH + 12} textAnchor="middle" fontSize={10} fill="var(--color-faint-foreground)">
                {colorField.value === 'embedding_dim' ? formatDim(cMin) : formatParams(cMin)}
              </text>
              <text
                x={WIDTH - 14}
                y={PAD.top + plotH / 2}
                textAnchor="middle"
                fontSize={11}
                fill="var(--color-muted-foreground)"
                transform={`rotate(-90 ${WIDTH - 14} ${PAD.top + plotH / 2})`}
              >
                {colorField.label}
              </text>
            </g>
          ) : null}
        </svg>
      </div>
      <div className="py-8 text-center text-[12px] text-faint-foreground md:hidden">
        Chart view requires a wider device.
      </div>
    </div>
  );
}
