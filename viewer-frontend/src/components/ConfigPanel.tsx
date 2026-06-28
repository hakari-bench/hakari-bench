import { BarChart3, Database, Languages, Layers, ListOrdered, Search, Sigma, Table2 } from 'lucide-react';
import { useState } from 'react';
import type { LeaderboardResponse, ViewerConfigResponse } from '../lib/api';
import { scoreMetricLabel } from '../lib/format';
import type { ViewerState } from '../lib/urlState';
import { ControlChip, ControlLabel, ToggleChip } from '../ui/controls';
import { DocIcon, HelpIcon } from './ViewerModals';

interface ConfigPanelProps {
  config: ViewerConfigResponse;
  result: LeaderboardResponse;
  state: ViewerState;
  update: (patch: Partial<ViewerState>) => void;
}

const VISIBLE_LANGUAGES = 8;

function benchmarkOf(selectionKey: string): string {
  return selectionKey.split(':')[0];
}

export function ConfigPanel({ config, result, state, update }: ConfigPanelProps) {
  const [showAllLanguages, setShowAllLanguages] = useState(false);

  const selectedBenchmarks = result.selected_benchmarks;
  const benchmarkNames = new Set(config.benchmarks.map((b) => b.name));

  const presetActive = (name: string): boolean =>
    name !== config.clear_scope && name === result.view_name;

  const suiteActive = (selectionKey: string): boolean => {
    if (selectedBenchmarks.length) return selectedBenchmarks.includes(selectionKey);
    return benchmarkOf(selectionKey) === result.view_name;
  };

  const onPreset = (name: string) => {
    if (name === 'Overall (EN)') update({ view: name, bench: [], langFilter: ['en'] });
    else if (name === config.clear_scope) update({ view: 'Clear', bench: [], langFilter: [] });
    else update({ view: name, bench: [], langFilter: [] });
  };

  const onToggleSuite = (selectionKey: string) => {
    const benchmark = benchmarkOf(selectionKey);
    let selected = [...selectedBenchmarks];
    if (selected.length === 0 && benchmarkNames.has(result.view_name)) {
      selected = [result.view_name];
    }
    if (selected.includes(selectionKey)) {
      selected = selected.filter((key) => key !== selectionKey);
    } else {
      selected = selected.filter((key) => benchmarkOf(key) !== benchmark);
      selected.push(selectionKey);
    }
    // Order by the suite display order, mirroring _ordered_benchmark_selection.
    const byBenchmark = new Map(selected.map((key) => [benchmarkOf(key), key]));
    const ordered: string[] = [];
    for (const suite of config.scope.suites) {
      const key = byBenchmark.get(suite.benchmark);
      if (key && !ordered.includes(key)) ordered.push(key);
    }
    for (const key of selected) if (!ordered.includes(key)) ordered.push(key);

    if (ordered.length === 0) update({ view: 'Clear', bench: [], langFilter: [] });
    else update({ view: 'Overall', bench: ordered });
  };

  const toggleLanguage = (code: string) => {
    const set = new Set(state.langFilter);
    if (set.has(code)) set.delete(code);
    else set.add(code);
    update({ langFilter: [...set] });
  };

  const languages = result.available_languages;
  const visibleLanguages = showAllLanguages ? languages : languages.slice(0, VISIBLE_LANGUAGES);

  return (
    <nav
      aria-label="Leaderboard configuration"
      className="grid gap-1.5 rounded-lg border border-border bg-surface p-1.5 text-[12px]"
    >
      {/* Mode / Score / Metric */}
      <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 rounded-md border border-border/70 bg-surface p-1.5">
        <div className="flex items-center gap-1">
          <ControlChip
            active={state.target === 'all'}
            onClick={() => update({ target: 'all' })}
            icon={<Search className="h-3.5 w-3.5" strokeWidth={1.75} />}
          >
            Retrieval
          </ControlChip>
          <ControlChip
            active={state.target !== 'all'}
            onClick={() => update({ target: 'reranking' })}
            icon={<ListOrdered className="h-3.5 w-3.5" strokeWidth={1.75} />}
          >
            Reranking
          </ControlChip>
          <HelpIcon id="mode" />
        </div>
        <div className="flex items-center gap-1">
          <ControlLabel icon={<Sigma className="h-3.5 w-3.5 text-accent" strokeWidth={1.75} />}>
            Score
          </ControlLabel>
          <ControlChip active={state.score === 'micro'} onClick={() => update({ score: 'micro' })}>
            Micro
          </ControlChip>
          <ControlChip active={state.score === 'macro'} onClick={() => update({ score: 'macro' })}>
            Macro
          </ControlChip>
          <HelpIcon id="score" />
        </div>
        {result.available_score_metrics.length > 1 ? (
          <div className="flex flex-wrap items-center gap-1">
            <ControlLabel icon={<BarChart3 className="h-3.5 w-3.5 text-accent" strokeWidth={1.75} />}>
              Metric
            </ControlLabel>
            <HelpIcon id="metric" />
            {result.available_score_metrics.map((metric) => (
              <ControlChip
                key={metric}
                active={result.selected_score_metric === metric}
                onClick={() => update({ metric })}
              >
                {scoreMetricLabel(metric)}
              </ControlChip>
            ))}
          </div>
        ) : null}
      </div>

      {/* Benchmark scope */}
      <div className="rounded-md border border-border/70 bg-surface p-1.5">
        <div className="mb-1.5 flex flex-wrap items-center gap-2">
          <ControlLabel icon={<Database className="h-3.5 w-3.5 text-accent" strokeWidth={1.75} />}>
            Benchmark scope
          </ControlLabel>
          <div className="flex flex-wrap gap-1.5">
            {config.scope.presets.map((preset) => (
              <span key={preset.name} className="inline-flex items-center gap-1">
                <ControlChip active={presetActive(preset.name)} onClick={() => onPreset(preset.name)}>
                  {preset.label}
                </ControlChip>
                {preset.help ? <HelpIcon id={preset.help} /> : null}
              </span>
            ))}
          </div>
        </div>
        <div className="mb-1.5 border-t border-border/60" aria-hidden />
        <div className="flex min-w-0 flex-wrap gap-1.5">
          {config.scope.suites.map((suite) => (
            <span key={suite.selection_key} className="inline-flex items-center gap-1">
              <ControlChip
                active={suiteActive(suite.selection_key)}
                onClick={() => onToggleSuite(suite.selection_key)}
              >
                {suite.label}
              </ControlChip>
              {suite.help ? <HelpIcon id={suite.help} /> : null}
              {suite.doc ? <DocIcon doc={suite.doc} label={`${suite.label} documentation`} /> : null}
            </span>
          ))}
        </div>
      </div>

      {/* Task facets: languages */}
      {languages.length ? (
        <div className="flex flex-wrap items-center gap-1.5 rounded-md border border-border/70 bg-surface p-1.5">
          <ControlLabel icon={<Languages className="h-3.5 w-3.5 text-accent" strokeWidth={1.75} />}>
            Task facets
          </ControlLabel>
          <HelpIcon id="task_facets" />
          <ControlChip
            active={state.langFilter.length === 0}
            onClick={() => update({ langFilter: [] })}
          >
            All languages
          </ControlChip>
          {visibleLanguages.map((lang) => (
            <ControlChip
              key={lang.code}
              active={state.langFilter.includes(lang.code)}
              onClick={() => toggleLanguage(lang.code)}
            >
              {lang.label} <span className="tnum text-faint-foreground">{lang.task_count}</span>
            </ControlChip>
          ))}
          {languages.length > VISIBLE_LANGUAGES ? (
            <ControlChip onClick={() => setShowAllLanguages((value) => !value)}>
              {showAllLanguages ? 'Fewer languages' : 'More languages'}
            </ControlChip>
          ) : null}
        </div>
      ) : null}

      {/* Table display + Efficiency variants */}
      <div className="grid gap-1.5 md:grid-cols-2">
        <div className="flex flex-wrap items-center gap-1.5 rounded-md border border-border/70 bg-surface p-1.5">
          <ControlLabel icon={<Table2 className="h-3.5 w-3.5 text-accent" strokeWidth={1.75} />}>
            Table display
          </ControlLabel>
          <HelpIcon id="table_display" />
          <ToggleChip checked={state.taskScores} onChange={(v) => update({ taskScores: v })}>
            Task columns
          </ToggleChip>
          <ToggleChip checked={state.taskZScores} onChange={(v) => update({ taskZScores: v })}>
            STD
          </ToggleChip>
          <ToggleChip checked={state.taskRanks} onChange={(v) => update({ taskRanks: v })}>
            Task ranks
          </ToggleChip>
          <ToggleChip checked={state.otherColumns} onChange={(v) => update({ otherColumns: v })}>
            Others
          </ToggleChip>
        </div>
        <div className="flex flex-wrap items-center gap-1.5 rounded-md border border-border/70 bg-surface p-1.5">
          <ControlLabel icon={<Layers className="h-3.5 w-3.5 text-accent" strokeWidth={1.75} />}>
            Efficiency variants
          </ControlLabel>
          <HelpIcon id="efficiency_variants" />
          <ToggleChip checked={state.truncate} onChange={(v) => update({ truncate: v })}>
            Dims
          </ToggleChip>
          <ToggleChip checked={state.quantization} onChange={(v) => update({ quantization: v })}>
            Quantization
          </ToggleChip>
          <ToggleChip checked={state.rescore} onChange={(v) => update({ rescore: v })}>
            Rescore
          </ToggleChip>
          <ToggleChip checked={state.otherVariant} onChange={(v) => update({ otherVariant: v })}>
            Sparse pruning
          </ToggleChip>
        </div>
      </div>
    </nav>
  );
}
