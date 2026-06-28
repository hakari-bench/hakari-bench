import { useEffect, useState } from 'react';
import {
  fetchDocsIndex,
  fetchDocsPage,
  type DocsIndexResponse,
  type DocsPageResponse,
} from '../lib/api';

interface DocsPageProps {
  path: string;
}

function normalize(path: string): string {
  return path.replace(/\/+$/, '') || '/docs';
}

function Breadcrumb({ title }: { title?: string }) {
  return (
    <nav className="mb-3 text-[12px] text-muted-foreground" aria-label="Breadcrumb">
      <ol className="flex flex-wrap items-center gap-1">
        <li>
          <a className="underline underline-offset-2 hover:text-accent" href="/">
            Top
          </a>
        </li>
        <li aria-hidden className="px-1 text-faint-foreground">
          ›
        </li>
        <li>
          <a className="underline underline-offset-2 hover:text-accent" href="/docs/">
            Benchmark documentation
          </a>
        </li>
        {title ? (
          <>
            <li aria-hidden className="px-1 text-faint-foreground">
              ›
            </li>
            <li aria-current="page" className="text-foreground">
              {title}
            </li>
          </>
        ) : null}
      </ol>
    </nav>
  );
}

export function DocsPage({ path }: DocsPageProps) {
  const normalized = normalize(path);
  const isIndex = normalized === '/docs';
  const [index, setIndex] = useState<DocsIndexResponse | null>(null);
  const [page, setPage] = useState<DocsPageResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    setError(null);
    setPage(null);
    setIndex(null);
    const request = isIndex
      ? fetchDocsIndex(controller.signal).then(setIndex)
      : fetchDocsPage(normalized, controller.signal).then(setPage);
    request.catch((err) => {
      if (!controller.signal.aborted) setError(String(err));
    });
    return () => controller.abort();
  }, [normalized, isIndex]);

  if (error) {
    return (
      <main className="py-4">
        <Breadcrumb />
        <div className="rounded-md bg-warn px-3 py-2 text-[12px] text-warn-foreground">
          Documentation not found.
        </div>
      </main>
    );
  }

  if (isIndex) {
    return (
      <main className="py-2">
        <Breadcrumb />
        <h1 className="mb-3 text-[15px] font-semibold text-foreground">Benchmark documentation</h1>
        <ul className="divide-y divide-border/60 rounded-lg border border-border bg-surface">
          {(index?.groups ?? []).map((group) => (
            <li key={group.url}>
              <a
                href={group.url}
                className="block px-3 py-2 text-[13px] font-medium text-foreground hover:bg-surface-faint hover:text-accent"
              >
                {group.title}
              </a>
            </li>
          ))}
        </ul>
      </main>
    );
  }

  return (
    <main className="py-2">
      <Breadcrumb title={page?.title} />
      <article
        className="hakari-doc rounded-lg border border-border bg-surface px-5 py-4"
        // Server-rendered, trusted Markdown HTML from the viewer docs pipeline.
        dangerouslySetInnerHTML={{ __html: page?.html ?? '' }}
      />
    </main>
  );
}
