import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

/**
 * Global hover/focus tooltip driven by `data-tooltip` attributes, mirroring the
 * legacy viewer.js behavior: 1s hover delay, click-to-pin, and viewport-aware
 * positioning. Works for any element (including server-rendered docs HTML).
 */
export function TooltipLayer() {
  const [state, setState] = useState<{ text: string; left: number; top: number } | null>(null);
  const tipRef = useRef<HTMLDivElement>(null);
  const timer = useRef<number | null>(null);
  const trigger = useRef<HTMLElement | null>(null);
  const pinned = useRef(false);

  useEffect(() => {
    const position = (el: HTMLElement, text: string) => {
      // Render off-screen first to measure, then clamp into the viewport.
      const margin = 8;
      const gap = 8;
      const rect = el.getBoundingClientRect();
      const tip = tipRef.current;
      const w = tip?.offsetWidth ?? 240;
      const h = tip?.offsetHeight ?? 40;
      const maxLeft = Math.max(margin, window.innerWidth - w - margin);
      const left = Math.min(Math.max(rect.left, margin), maxLeft);
      let top = rect.bottom + gap;
      if (top + h > window.innerHeight - margin) top = Math.max(margin, rect.top - h - gap);
      setState({ text, left, top });
    };

    const clear = () => {
      if (timer.current) window.clearTimeout(timer.current);
      timer.current = null;
      pinned.current = false;
      trigger.current = null;
      setState(null);
    };

    const findTrigger = (target: EventTarget | null): HTMLElement | null => {
      if (!(target instanceof Element)) return null;
      return target.closest<HTMLElement>('[data-tooltip]');
    };

    const onOver = (event: MouseEvent) => {
      const el = findTrigger(event.target);
      if (!el || pinned.current) return;
      const text = el.dataset.tooltip;
      if (!text) return;
      if (timer.current) window.clearTimeout(timer.current);
      trigger.current = el;
      const delay = el.dataset.tooltipDelay === '0' ? 0 : 700;
      timer.current = window.setTimeout(() => position(el, text), delay);
    };
    const onOut = (event: MouseEvent) => {
      if (pinned.current) return;
      const related = event.relatedTarget as Node | null;
      if (trigger.current && related && trigger.current.contains(related)) return;
      clear();
    };
    const onFocusIn = (event: FocusEvent) => {
      const el = findTrigger(event.target);
      if (!el) return;
      const text = el.dataset.tooltip;
      if (text) {
        trigger.current = el;
        position(el, text);
      }
    };
    const onClickCapture = (event: MouseEvent) => {
      if (event.target instanceof Element && event.target.closest('a, button, summary, input, select, textarea')) {
        return;
      }
      const el = findTrigger(event.target);
      if (!el || el.dataset.tooltipHoverOnly === 'true') return;
      const text = el.dataset.tooltip;
      if (!text) return;
      event.preventDefault();
      event.stopPropagation();
      pinned.current = true;
      trigger.current = el;
      position(el, text);
    };
    const onClick = (event: MouseEvent) => {
      if (pinned.current && !(event.target instanceof Element && event.target.closest('[data-tooltip]'))) clear();
    };
    const onScroll = () => {
      if (!pinned.current) clear();
    };

    document.addEventListener('mouseover', onOver);
    document.addEventListener('mouseout', onOut);
    document.addEventListener('focusin', onFocusIn);
    document.addEventListener('focusout', () => {
      if (!pinned.current) clear();
    });
    document.addEventListener('click', onClickCapture, true);
    document.addEventListener('click', onClick);
    document.addEventListener('scroll', onScroll, true);
    window.addEventListener('resize', clear);
    return () => {
      document.removeEventListener('mouseover', onOver);
      document.removeEventListener('mouseout', onOut);
      document.removeEventListener('focusin', onFocusIn);
      document.removeEventListener('click', onClickCapture, true);
      document.removeEventListener('click', onClick);
      document.removeEventListener('scroll', onScroll, true);
      window.removeEventListener('resize', clear);
    };
  }, []);

  if (!state) return null;
  return createPortal(
    <div
      ref={tipRef}
      role="tooltip"
      className="pointer-events-none fixed z-[60] max-w-xs whitespace-pre-line rounded-md border border-border-strong bg-surface px-2 py-1 text-[11px] text-foreground shadow-lg"
      style={{ left: state.left, top: state.top }}
    >
      {state.text}
    </div>,
    document.body,
  );
}
