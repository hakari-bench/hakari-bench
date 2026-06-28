import { Database, Download, Search } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { AppHeader } from './components/AppHeader';
import { ConfigPanel } from './components/ConfigPanel';
import { Footer } from './components/Footer';
import { LeaderboardTable } from './components/LeaderboardTable';
import {
  fetchConfig,
  fetchLeaderboard,
  leaderboardCsvUrl,
  type LeaderboardResponse,
  type ViewerConfigResponse,
} from './lib/api';
import { useViewerState } from './lib/urlState';

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

  const onSort = (column: string) => {
    if (state.sort === column) {
      update({ direction: state.direction === 'desc' ? 'asc' : 'desc' });
    } else {
      update({ sort: column, direction: column === 'model_name' ? 'asc' : 'desc' });
    }
  };

  return (
    <div className="mx-auto max-w-[1280px] px-3">
      <AppHeader
        githubUrl={config?.links.github ?? 'https://github.com/hakari-bench/hakari-bench'}
        docsUrl={config?.links.docs ?? '/docs/'}
      />

      <main>
        {config && result ? (
          <ConfigPanel config={config} result={result} state={state} update={update} />
        ) : null}

        <div className="flex items-center justify-between gap-2 py-2 text-[12px] text-muted-foreground">
          <div className="flex items-center gap-2">
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
                <span className="tnum">{result.rows.length} shown</span>
                <span className="text-faint-foreground">/</span>
                <span className="tnum">{result.expected_tasks} tasks</span>
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
            <LeaderboardTable
              result={result}
              sort={state.sort}
              direction={state.direction}
              onSort={onSort}
            />
          </div>
        ) : (
          <div className="flex min-h-[400px] items-center justify-center text-[12px] text-faint-foreground">
            Loading leaderboard…
          </div>
        )}
      </main>

      <Footer
        latestUpdate={config?.footer.latest_update ?? ''}
        databaseLabel={config?.footer.database_label ?? ''}
      />
    </div>
  );
}

export default App;
