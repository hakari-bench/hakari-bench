import type { ReactNode } from 'react';
import { cn } from '../lib/cn';

const baseChip =
  'inline-flex items-center gap-1.5 rounded-md px-2 py-1 text-[12px] font-medium leading-tight ' +
  'transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent';

interface ControlChipProps {
  active?: boolean;
  onClick?: () => void;
  children: ReactNode;
  icon?: ReactNode;
  title?: string;
  className?: string;
}

/** A clickable selection chip (mode, scope, metric, language). */
export function ControlChip({ active, onClick, children, icon, title, className }: ControlChipProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      title={title}
      aria-pressed={active}
      className={cn(
        baseChip,
        active
          ? 'bg-control-active text-accent'
          : 'bg-control text-muted-foreground hover:bg-control-hover hover:text-accent',
        className,
      )}
    >
      {icon}
      {children}
    </button>
  );
}

interface ToggleChipProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  children: ReactNode;
  icon?: ReactNode;
  title?: string;
}

/**
 * Boolean display / variant toggle. Keeps a real (visually hidden) checkbox for
 * form semantics and focus, with the chip adopting the active surface when set.
 */
export function ToggleChip({ checked, onChange, children, icon, title }: ToggleChipProps) {
  return (
    <label
      title={title}
      className={cn(
        baseChip,
        'cursor-pointer select-none focus-within:ring-2 focus-within:ring-accent',
        checked
          ? 'bg-control-active text-accent'
          : 'bg-control text-muted-foreground hover:bg-control-hover hover:text-accent',
      )}
    >
      <input
        type="checkbox"
        className="sr-only"
        checked={checked}
        onChange={(event) => onChange(event.target.checked)}
      />
      {icon}
      {children}
    </label>
  );
}

interface ControlLabelProps {
  icon?: ReactNode;
  children: ReactNode;
  className?: string;
}

/** A non-clickable group label (e.g. "Benchmark scope", "Metric"). */
export function ControlLabel({ icon, children, className }: ControlLabelProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 px-1 py-1 text-[12px] font-semibold text-foreground',
        className,
      )}
    >
      {icon}
      {children}
    </span>
  );
}
