import { useEffect, useState } from 'react';
import { AppHeader } from './components/AppHeader';
import { DocsPage } from './components/DocsPage';
import { Footer } from './components/Footer';
import { ViewerModalsProvider } from './components/ViewerModals';
import { fetchConfig, type ViewerConfigResponse } from './lib/api';

/** Standalone docs shell: shares the leaderboard chrome (header, theme, footer). */
export function DocsApp() {
  const [config, setConfig] = useState<ViewerConfigResponse | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetchConfig(controller.signal)
      .then(setConfig)
      .catch(() => {
        /* docs render without config chrome metadata */
      });
    return () => controller.abort();
  }, []);

  return (
    <div className="mx-auto max-w-[1280px] px-3">
      <AppHeader
        githubUrl={config?.links.github ?? 'https://github.com/hakari-bench/hakari-bench'}
        docsUrl={config?.links.docs ?? '/docs/'}
      />
      <ViewerModalsProvider result={null}>
        <DocsPage path={window.location.pathname} />
      </ViewerModalsProvider>
      <Footer
        latestUpdate={config?.footer.latest_update ?? ''}
        databaseLabel={config?.footer.database_label ?? ''}
      />
    </div>
  );
}
