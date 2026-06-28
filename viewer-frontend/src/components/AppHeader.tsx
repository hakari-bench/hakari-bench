import { BookOpen, Moon, Scale, Sun } from 'lucide-react';
import { useTheme } from '../lib/theme';

// lucide-react dropped brand marks; keep a compact stroke-style GitHub glyph.
function GithubMark({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.75}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22" />
    </svg>
  );
}

interface AppHeaderProps {
  githubUrl: string;
  docsUrl: string;
}

const iconButton =
  'inline-flex h-7 w-7 items-center justify-center rounded-md text-muted-foreground ' +
  'hover:bg-control-hover hover:text-accent focus-visible:outline-none focus-visible:ring-2 ' +
  'focus-visible:ring-accent transition-colors';

export function AppHeader({ githubUrl, docsUrl }: AppHeaderProps) {
  const { theme, toggle } = useTheme();
  return (
    <header className="flex items-center justify-between gap-3 py-2">
      <a
        href="/"
        className="flex items-center gap-2 text-foreground hover:text-accent transition-colors"
        aria-label="Refresh HAKARI-Bench leaderboard"
      >
        <Scale className="h-4 w-4 text-accent" strokeWidth={1.75} />
        <span className="text-[13px] font-semibold">HAKARI-Bench leaderboard</span>
      </a>
      <div className="flex items-center gap-1">
        <a
          href={githubUrl}
          target="_blank"
          rel="noreferrer noopener"
          className={iconButton}
          aria-label="Open hakari-bench/hakari-bench on GitHub"
        >
          <GithubMark className="h-4 w-4" />
        </a>
        <a href={docsUrl} className={iconButton} aria-label="Open documentation">
          <BookOpen className="h-4 w-4" strokeWidth={1.75} />
        </a>
        <button
          type="button"
          onClick={toggle}
          className={iconButton}
          aria-label={theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'}
        >
          {theme === 'dark' ? (
            <Sun className="h-4 w-4" strokeWidth={1.75} />
          ) : (
            <Moon className="h-4 w-4" strokeWidth={1.75} />
          )}
        </button>
      </div>
    </header>
  );
}
