import { BarChart3, Database, Download, Search, Table2 } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { AppHeader } from './components/AppHeader';
import { Chart } from './components/Chart';
import { ConfigPanel } from './components/ConfigPanel';
import { FilterPanel } from './components/FilterPanel';
import { Footer } from './components/Footer';
import { LeaderboardTable } from './components/LeaderboardTable';
import { useModals, ViewerModalsProvider } from './components/ViewerModals';
import {
  fetchConfig,
  fetchLeaderboard,
  leaderboardCsvUrl,
  type LeaderboardResponse,
  type ViewerConfigResponse,
} from './lib/api';
import { useViewerState, type ViewerState } from './lib/urlState';

interface MainContentProps {
  config: ViewerConfigResponse | null;
  result: LeaderboardResponse | null;
  state: ViewerState;
  update: (patch: Partial<ViewerState>) => void;
  loading: boolean;
  error: string | null;
}

function MainContent({ config, result, state, update, loading, error }: MainContentProps) {
  const { openModelDetails, openDoc, openCountBreakdown } = useModals();

  const onSort = (column: string) => {
    if (state.sort === column) update({ direction: state.direction === 'desc' ? 'asc' : 'desc' });
    else update({ sort: column, direction: column === 'model_name' ? 'asc' : 'desc' });
  };

  const countButton = (label: string, section: 'shown' | 'complete' | 'tasks') => (
    <button
      type="button"
      onClick={() => openCountBreakdown(section)}
      className="tnum underline-offset-2 hover:text-accent hover:underline"
    >
      {label}
    </button>
  );

  return (
    <main>
      {config && result ? (
        <div className="grid gap-1.5">
          <ConfigPanel config={config} result={result} state={state} update={update} />
          <FilterPanel result={result} state={state} update={update} />
        </div>
      ) : null}

      <div className="flex items-center justify-between gap-2 py-2 text-[12px] text-muted-foreground">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-0.5">
            <button
              type="button"
              onClick={() => update({ resultView: 'table' })}
              className={`inline-flex items-center gap-1 rounded-md px-1.5 py-0.5 ${state.resultView !== 'chart' ? 'bg-control-active text-accent' : 'text-muted-foreground hover:text-accent'}`}
            >
              <Table2 className="h-3.5 w-3.5" strokeWidth={1.75} />
              Table
            </button>
            <button
              type="button"
              onClick={() => update({ resultView: 'chart' })}
              className={`inline-flex items-center gap-1 rounded-md px-1.5 py-0.5 ${state.resultView === 'chart' ? 'bg-control-active text-accent' : 'text-muted-foreground hover:text-accent'}`}
            >
              <BarChart3 className="h-3.5 w-3.5" strokeWidth={1.75} />
              Chart
            </button>
          </div>
          <span className="inline-flex items-center gap-1 text-foreground">
            <Database className="h-3.5 w-3.5 text-accent" strokeWidth={1.75} />
            {result?.view_label ?? state.view}
          </span>
          <span className="text-faint-foreground">/</span>
          <span className="inline-flex items-center gap-1">
            <Search className="h-3.5 w-3.5" strokeWidth={1.75} />
            {state.target === 'all' ? 'Retrieval' : 'Reranking'}
          </span>
          {result ? (
            <>
              <span className="text-faint-foreground">/</span>
              {countButton(`${result.rows.length} shown`, 'shown')}
              <span className="text-faint-foreground">/</span>
              {countButton(`${result.total_row_count} complete models`, 'complete')}
              <span className="text-faint-foreground">/</span>
              {countButton(`${result.expected_tasks} tasks`, 'tasks')}
            </>
          ) : null}
        </div>
        <a
          href={leaderboardCsvUrl(state)}
          className="inline-flex items-center gap-1 rounded-md px-2 py-1 text-muted-foreground hover:bg-control-hover hover:text-accent"
        >
          <Download className="h-3.5 w-3.5" strokeWidth={1.75} />
          Download CSV
        </a>
      </div>

      {error ? (
        <div className="rounded-md bg-warn px-3 py-2 text-[12px] text-warn-foreground">{error}</div>
      ) : null}

      {result ? (
        <div className={loading ? 'opacity-60 transition-opacity' : 'transition-opacity'}>
          {state.resultView === 'chart' ? (
            <Chart result={result} state={state} update={update} />
          ) : (
            <LeaderboardTable
              result={result}
              sort={state.sort}
              direction={state.direction}
              onSort={onSort}
              onSelectModel={openModelDetails}
              onOpenDoc={openDoc}
            />
          )}
        </div>
      ) : (
        <div className="flex min-h-[400px] items-center justify-center text-[12px] text-faint-foreground">
          Loading leaderboard…
        </div>
      )}
    </main>
  );
}

function App() {
  const { state, update } = useViewerState();
  const [config, setConfig] = useState<ViewerConfigResponse | null>(null);
  const [result, setResult] = useState<LeaderboardResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const requestId = useRef(0);

  useEffect(() => {
    const controller = new AbortController();
    fetchConfig(controller.signal)
      .then(setConfig)
      .catch((err) => {
        if (!controller.signal.aborted) setError(String(err));
      });
    return () => controller.abort();
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    const id = ++requestId.current;
    setLoading(true);
    fetchLeaderboard(state, controller.signal)
      .then((data) => {
        if (id === requestId.current) {
          setResult(data);
          setError(null);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (!controller.signal.aborted) {
          setError(String(err));
          setLoading(false);
        }
      });
    return () => controller.abort();
  }, [state]);

  return (
    <div className="mx-auto max-w-[1280px] px-3">
      <AppHeader
        githubUrl={config?.links.github ?? 'https://github.com/hakari-bench/hakari-bench'}
        docsUrl={config?.links.docs ?? '/docs/'}
      />
      <ViewerModalsProvider result={result}>
        <MainContent
          config={config}
          result={result}
          state={state}
          update={update}
          loading={loading}
          error={error}
        />
      </ViewerModalsProvider>
      <Footer
        latestUpdate={config?.footer.latest_update ?? ''}
        databaseLabel={config?.footer.database_label ?? ''}
      />
    </div>
  );
}

export default App;
