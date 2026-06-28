import { BookOpen, CircleHelp } from 'lucide-react';
import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react';
import type { LeaderboardResponse, LeaderboardRow } from '../lib/api';
import { HELP } from '../lib/help';
import { Modal } from '../ui/modal';
import { TooltipLayer } from '../ui/tooltip';
import { ModelDetailsModal } from './ModelDetailsModal';

export interface DocSummary {
  title: string;
  description: string;
  url: string;
}

type CountSection = 'shown' | 'complete' | 'tasks';

interface ModalsContextValue {
  openHelp: (id: string) => void;
  openDoc: (doc: DocSummary) => void;
  openModelDetails: (row: LeaderboardRow) => void;
  openCountBreakdown: (section: CountSection) => void;
}

const NOOP_MODALS: ModalsContextValue = {
  openHelp: () => {},
  openDoc: () => {},
  openModelDetails: () => {},
  openCountBreakdown: () => {},
};

const ModalsContext = createContext<ModalsContextValue>(NOOP_MODALS);

/** Access modal openers. Falls back to no-ops outside a provider (e.g. stories). */
export function useModals(): ModalsContextValue {
  return useContext(ModalsContext);
}

/** A circle-help button that opens the shared help modal for a control. */
export function HelpIcon({ id, label }: { id: string; label?: string }) {
  const { openHelp } = useModals();
  if (!HELP[id]) return null;
  return (
    <button
      type="button"
      onClick={() => openHelp(id)}
      aria-label={label ?? HELP[id].title}
      className="inline-flex h-3.5 w-3.5 shrink-0 items-center justify-center rounded-full text-muted-foreground hover:text-accent"
    >
      <CircleHelp className="h-3.5 w-3.5" strokeWidth={1.75} />
    </button>
  );
}

/** A book button that opens the benchmark/task documentation summary modal. */
export function DocIcon({ doc, label }: { doc: DocSummary; label?: string }) {
  const { openDoc } = useModals();
  return (
    <button
      type="button"
      onClick={() => openDoc(doc)}
      aria-label={label ?? `${doc.title} documentation`}
      className="inline-flex h-3.5 w-3.5 shrink-0 items-center justify-center rounded-full text-faint-foreground hover:text-accent"
    >
      <BookOpen className="h-3.5 w-3.5" strokeWidth={1.75} />
    </button>
  );
}

function ModelList({ rows, onSelect }: { rows: LeaderboardRow[]; onSelect: (row: LeaderboardRow) => void }) {
  if (!rows.length) return <p className="mt-2 text-[12px] text-faint-foreground">No models.</p>;
  return (
    <ul className="mt-2 max-h-72 overflow-auto">
      {rows.map((row, index) => (
        <li key={`${row.model_name}-${index}`} className="border-t border-border/50 py-1">
          <button
            type="button"
            onClick={() => onSelect(row)}
            className="break-all text-left text-[12px] text-foreground underline-offset-2 hover:text-accent hover:underline"
          >
            {row.model_name}
          </button>
        </li>
      ))}
    </ul>
  );
}

export function ViewerModalsProvider({
  result,
  children,
}: {
  result: LeaderboardResponse | null;
  children: ReactNode;
}) {
  const [helpId, setHelpId] = useState<string | null>(null);
  const [doc, setDoc] = useState<DocSummary | null>(null);
  const [modelRow, setModelRow] = useState<LeaderboardRow | null>(null);
  const [countSection, setCountSection] = useState<CountSection | null>(null);

  const value = useMemo<ModalsContextValue>(
    () => ({
      openHelp: setHelpId,
      openDoc: setDoc,
      openModelDetails: setModelRow,
      openCountBreakdown: setCountSection,
    }),
    [],
  );

  const help = helpId ? HELP[helpId] : null;
  const facetTable =
    helpId === 'task_facets' && result ? result.available_languages : null;

  const countTitle =
    countSection === 'shown'
      ? 'Visible rows'
      : countSection === 'complete'
        ? 'Complete models'
        : 'Tasks';

  const selectFromCount = useCallback((row: LeaderboardRow) => {
    setCountSection(null);
    setModelRow(row);
  }, []);

  return (
    <ModalsContext.Provider value={value}>
      {children}
      <TooltipLayer />

      <Modal
        open={!!help}
        onClose={() => setHelpId(null)}
        icon={<CircleHelp className="h-4 w-4 text-accent" strokeWidth={1.75} />}
        title={help?.title ?? ''}
      >
        {help ? (
          <div className="text-[12px]">
            <p className="font-medium text-foreground">{help.summary}</p>
            <p className="mt-2 whitespace-pre-line text-muted-foreground">{help.details}</p>
            {facetTable && facetTable.length ? (
              <table className="mt-3 w-full border-collapse text-[12px]">
                <thead>
                  <tr className="text-left text-muted-foreground">
                    <th className="border-b border-border px-2 py-1 font-semibold">Facet</th>
                    <th className="border-b border-border px-2 py-1 font-semibold">Tasks</th>
                  </tr>
                </thead>
                <tbody>
                  {facetTable.map((lang) => (
                    <tr key={lang.code}>
                      <td className="border-b border-border/50 px-2 py-1">{lang.label}</td>
                      <td className="border-b border-border/50 px-2 py-1 tnum">{lang.task_count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : null}
          </div>
        ) : null}
      </Modal>

      <Modal
        open={!!doc}
        onClose={() => setDoc(null)}
        icon={<BookOpen className="h-4 w-4 text-accent" strokeWidth={1.75} />}
        title={doc?.title ?? ''}
      >
        {doc ? (
          <div className="text-[12px]">
            <p className="whitespace-pre-line text-muted-foreground">{doc.description}</p>
            <a className="mt-3 inline-block text-accent hover:underline" href={doc.url}>
              Read the {doc.title} overview
            </a>
          </div>
        ) : null}
      </Modal>

      <Modal
        open={!!countSection}
        onClose={() => setCountSection(null)}
        title={countTitle}
      >
        {countSection && result ? (
          countSection === 'tasks' ? (
            <div className="text-[12px]">
              <h4 className="font-semibold text-foreground">Tasks: {result.expected_tasks}</h4>
              <ul className="mt-2 max-h-72 overflow-auto">
                {result.task_breakdowns.map((task) => {
                  const taskDoc = result.task_breakdown_docs?.[task.key];
                  return (
                    <li key={task.key} className="border-t border-border/50 py-1">
                      {taskDoc ? (
                        <a className="text-accent hover:underline" href={taskDoc.url} target="_blank" rel="noreferrer">
                          {taskDoc.title}
                        </a>
                      ) : (
                        <span className="text-muted-foreground">{task.label}</span>
                      )}
                    </li>
                  );
                })}
              </ul>
            </div>
          ) : (
            <div className="text-[12px]">
              <h4 className="font-semibold text-foreground">
                {countTitle}: {countSection === 'shown' ? result.rows.length : result.total_row_count}
              </h4>
              <ModelList
                rows={countSection === 'shown' ? result.rows : (result.all_rows ?? result.rows)}
                onSelect={selectFromCount}
              />
            </div>
          )
        ) : null}
      </Modal>

      <ModelDetailsModal row={modelRow} onClose={() => setModelRow(null)} />
    </ModalsContext.Provider>
  );
}
