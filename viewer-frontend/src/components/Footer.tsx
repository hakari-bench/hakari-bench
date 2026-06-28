import { CalendarDays } from 'lucide-react';

interface FooterProps {
  latestUpdate: string;
  databaseLabel: string;
}

export function Footer({ latestUpdate, databaseLabel }: FooterProps) {
  return (
    <footer className="mt-3 flex flex-wrap items-center justify-end gap-x-4 gap-y-1 py-2 text-[11px] text-faint-foreground">
      {latestUpdate ? (
        <span className="inline-flex items-center gap-1 tnum">
          <CalendarDays className="h-3 w-3" strokeWidth={1.75} />
          {latestUpdate}
        </span>
      ) : null}
      {databaseLabel ? <span className="break-all">{databaseLabel}</span> : null}
    </footer>
  );
}
