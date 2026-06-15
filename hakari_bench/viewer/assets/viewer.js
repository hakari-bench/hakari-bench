(() => {
  if (window.__hakariViewerInitialized) return;
  window.__hakariViewerInitialized = true;

  function closestElement(target, selector) {
    if (!target || !target.closest) return null;
    return target.closest(selector);
  }

  const themeStorageKey = "hakari-theme";
  const themeQuery = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

  function storedTheme() {
    try {
      const value = window.localStorage.getItem(themeStorageKey);
      return value === "dark" || value === "light" ? value : null;
    } catch (_error) {
      return null;
    }
  }

  function storeTheme(theme) {
    try {
      window.localStorage.setItem(themeStorageKey, theme);
    } catch (_error) {
      // Theme switching should still work when storage is unavailable.
    }
  }

  function effectiveTheme() {
    const root = document.documentElement;
    if (root.classList.contains("dark")) return "dark";
    if (root.classList.contains("light")) return "light";
    return themeQuery && themeQuery.matches ? "dark" : "light";
  }

  window.__hakariApplyTheme = (theme, persist) => {
    const root = document.documentElement;
    root.classList.toggle("dark", theme === "dark");
    root.classList.toggle("light", theme === "light");
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    if (persist) storeTheme(theme);
    window.__hakariSyncThemeToggle();
  };

  window.__hakariSyncThemeToggle = () => {
    const button = document.getElementById("hakari-theme-toggle");
    if (!button) return;
    const theme = effectiveTheme();
    const isDark = theme === "dark";
    const label = isDark ? "Switch to light theme" : "Switch to dark theme";
    button.setAttribute("aria-label", label);
    button.setAttribute("aria-pressed", String(isDark));
    button.setAttribute("title", label);
  };

  window.__hakariBindThemeToggle = () => {
    const button = document.getElementById("hakari-theme-toggle");
    if (!button || button.dataset.themeToggleBound === "true") return;
    button.dataset.themeToggleBound = "true";
    button.addEventListener("click", () => {
      const nextTheme = effectiveTheme() === "dark" ? "light" : "dark";
      window.__hakariApplyTheme(nextTheme, true);
    });
    window.__hakariSyncThemeToggle();
  };

  const initialStoredTheme = storedTheme();
  if (initialStoredTheme) window.__hakariApplyTheme(initialStoredTheme, false);
  if (themeQuery) {
    themeQuery.addEventListener("change", () => {
      if (!storedTheme()) window.__hakariSyncThemeToggle();
    });
  }

  function paramsFrom(value) {
    const raw = (value || "").replace(/^[#?]/, "");
    return raw ? new URLSearchParams(raw) : new URLSearchParams();
  }

  function mergedStateQueryString() {
    const params = new URLSearchParams(window.location.search);
    paramsFrom(window.location.hash).forEach((value, key) => {
      if (!params.has(key)) params.append(key, value);
    });
    return params.toString();
  }

  window.__hakariApplyHashQueryState = () => {
    const hashParams = paramsFrom(window.location.hash);
    if (Array.from(hashParams.keys()).length === 0) return;
    const queryString = mergedStateQueryString();
    if (!queryString) return;
    const panel = document.getElementById("leaderboard-panel");
    if (panel) panel.setAttribute("hx-get", "/leaderboard?" + queryString);
  };

  window.__hakariSyncHashQueryStateToParent = () => {
    const queryString = mergedStateQueryString();
    const hashValue = queryString ? "#" + queryString : "";
    if (window.parent && window.parent !== window) {
      try {
        window.parent.postMessage({ queryString: "", hash: hashValue }, "https://huggingface.co");
      } catch (_error) {
        // Parent URL synchronization is best-effort for non-HF embeds.
      }
    }
  };

  function leaderboardControlFrom(event) {
    const source = event.detail && event.detail.elt;
    if (!source || !source.closest) return null;
    return source.closest("[data-leaderboard-control='true']");
  }

  window.__hakariSetLeaderboardPending = (event, pending) => {
    const control = leaderboardControlFrom(event);
    if (!control) return;
    if (pending) {
      control.dataset.leaderboardPending = "true";
      control.setAttribute("aria-busy", "true");
    } else {
      delete control.dataset.leaderboardPending;
      control.removeAttribute("aria-busy");
    }
  };

  let tooltipTimer = null;
  let tooltipTrigger = null;
  let tooltipPinned = false;

  function tooltipElement() {
    return document.getElementById("hakari-global-tooltip");
  }

  window.__hakariPositionTooltip = (trigger) => {
    const tooltip = tooltipElement();
    if (!trigger || !tooltip || tooltip.hidden) return;
    const margin = 8;
    const gap = 8;
    const rect = trigger.getBoundingClientRect();
    const tooltipWidth = tooltip.offsetWidth;
    const tooltipHeight = tooltip.offsetHeight;
    const maxLeft = Math.max(margin, window.innerWidth - tooltipWidth - margin);
    const left = Math.min(Math.max(rect.left, margin), maxLeft);
    let top = rect.bottom + gap;
    if (top + tooltipHeight > window.innerHeight - margin) {
      top = Math.max(margin, rect.top - tooltipHeight - gap);
    }
    tooltip.style.left = `${left}px`;
    tooltip.style.top = `${top}px`;
  };

  function showTooltipNow(trigger) {
    const tooltip = tooltipElement();
    const text = trigger && trigger.dataset ? trigger.dataset.tooltip : "";
    if (!tooltip || !text) return;
    window.__hakariHideTooltip();
    tooltipPinned = true;
    tooltipTrigger = trigger;
    tooltip.textContent = text;
    tooltip.hidden = false;
    tooltip.dataset.visible = "true";
    window.__hakariPositionTooltip(trigger);
  }

  window.__hakariShowTooltip = (trigger) => {
    const tooltip = tooltipElement();
    const text = trigger && trigger.dataset ? trigger.dataset.tooltip : "";
    if (!tooltip || !text) return;
    window.__hakariHideTooltip();
    tooltipPinned = false;
    tooltipTrigger = trigger;
    tooltipTimer = setTimeout(() => {
      tooltip.textContent = text;
      tooltip.hidden = false;
      tooltip.dataset.visible = "true";
      window.__hakariPositionTooltip(trigger);
    }, 1000);
  };

  window.__hakariHideTooltip = () => {
    if (tooltipTimer) clearTimeout(tooltipTimer);
    tooltipTimer = null;
    tooltipPinned = false;
    tooltipTrigger = null;
    const tooltip = tooltipElement();
    if (!tooltip) return;
    tooltip.hidden = true;
    delete tooltip.dataset.visible;
    tooltip.textContent = "";
  };

  const modelDetailFields = [
    ["Language", "language_support_label"],
    ["Model type", "model_type"],
    ["Ranking label", "ranking_model_name"],
    ["Variant", "embedding_variant_name"],
    ["Dimensions", "embedding_dim"],
    ["Quantization", "quantization"],
    ["Base delta", "base_score_delta_percent"],
    ["Active params", "active_parameters"],
    ["Total params", "total_parameters"],
    ["Max len", "max_seq_length"],
    ["DType", "dtype"],
    ["Attention", "attention"],
    ["Prompt", "prompt"],
    ["HF trust", "trust_remote_code"],
    ["Query len", "late_interaction_query_length"],
    ["Doc len", "late_interaction_document_length"],
    ["Query expansion", "late_interaction_query_expansion"],
    ["Attend expansion tokens", "late_interaction_attend_to_expansion_tokens"],
    ["Query prefix", "late_interaction_query_prefix"],
    ["Doc prefix", "late_interaction_document_prefix"],
  ];

  function formatModelDetailValue(value) {
    if (value === null || value === undefined || value === "") return "";
    if (typeof value === "boolean") return value ? "true" : "false";
    if (typeof value === "number") return value.toLocaleString();
    return String(value);
  }

  window.__hakariBindModelDetails = () => {
    if (window.__hakariModelDetailsBound) return;
    window.__hakariModelDetailsBound = true;

    document.addEventListener("click", (event) => {
      const trigger = closestElement(event.target, ".doc-summary-trigger");
      if (!trigger) return;
      event.preventDefault();
      event.stopPropagation();
      const modal = document.getElementById("doc-summary-modal");
      const heading = document.getElementById("doc-summary-heading");
      const description = document.getElementById("doc-summary-description");
      const link = document.getElementById("doc-summary-link");
      if (!modal || !heading || !description || !link) return;
      const docTitle = trigger.dataset.docTitle || "Benchmark documentation";
      heading.textContent = docTitle;
      description.textContent = trigger.dataset.docDescription || "";
      link.href = trigger.dataset.docUrl || "#";
      link.textContent = `Read the ${docTitle} overview`;
      if (typeof modal.showModal === "function") modal.showModal();
    });

    document.addEventListener("click", (event) => {
      const trigger = closestElement(event.target, ".help-summary-trigger");
      if (!trigger) return;
      event.preventDefault();
      event.stopPropagation();
      const modal = document.getElementById("help-summary-modal");
      const heading = document.getElementById("help-summary-heading");
      const summary = document.getElementById("help-summary-short");
      const details = document.getElementById("help-summary-details");
      if (!modal || !heading || !summary || !details) return;
      heading.textContent = trigger.dataset.helpTitle || "";
      summary.textContent = trigger.dataset.helpSummary || "";
      details.textContent = trigger.dataset.helpDetails || "";
      if (typeof modal.showModal === "function") modal.showModal();
    });

    document.addEventListener("keydown", (event) => {
      const trigger = closestElement(event.target, ".help-summary-trigger");
      if (!trigger || (event.key !== "Enter" && event.key !== " ")) return;
      event.preventDefault();
      trigger.click();
    });

    document.addEventListener("click", (event) => {
      const trigger = closestElement(event.target, ".model-detail-trigger");
      if (!trigger) return;
      const modal = document.getElementById("model-detail-modal");
      const title = document.getElementById("model-detail-title");
      const list = document.getElementById("model-detail-fields");
      if (!modal || !title || !list) return;
      const metadata = JSON.parse(trigger.dataset.modelMetadata || "{}");
      title.textContent = metadata.model_name || trigger.textContent || "";
      if (metadata.model_url) {
        title.href = metadata.model_url;
      } else {
        title.removeAttribute("href");
      }
      list.replaceChildren();
      for (const [label, key] of modelDetailFields) {
        const value = formatModelDetailValue(metadata[key]);
        if (!value) continue;
        const dt = document.createElement("dt");
        dt.className = "font-medium text-zinc-600";
        dt.textContent = label;
        const dd = document.createElement("dd");
        dd.className = "break-all font-mono text-zinc-900";
        dd.textContent = value;
        list.append(dt, dd);
      }
      if (typeof modal.showModal === "function") modal.showModal();
    });

    document.addEventListener("click", (event) => {
      const modal = event.target && event.target.id === "model-detail-modal" ? event.target : null;
      if (modal) modal.close();
    });

    document.addEventListener("click", (event) => {
      const modal = event.target && event.target.id === "doc-summary-modal" ? event.target : null;
      if (modal) modal.close();
    });

    document.addEventListener("click", (event) => {
      const modal = event.target && event.target.id === "help-summary-modal" ? event.target : null;
      if (modal) modal.close();
    });

    document.addEventListener("submit", (event) => {
      if (!event.target || event.target.id !== "filter-controls") return;
      const activeId = document.activeElement && document.activeElement.id;
      window.__hakariRestoreModelFilterFocus = activeId === "model-filter-input";
      window.__hakariRestoreTaskFilterFocus = activeId === "task-filter-input";
    });

    document.addEventListener("htmx:afterSwap", (event) => {
      if (
        !event.target ||
        event.target.id !== "leaderboard-panel" ||
        (!window.__hakariRestoreModelFilterFocus && !window.__hakariRestoreTaskFilterFocus)
      ) {
        return;
      }
      const inputId = window.__hakariRestoreTaskFilterFocus ? "task-filter-input" : "model-filter-input";
      window.__hakariRestoreModelFilterFocus = false;
      window.__hakariRestoreTaskFilterFocus = false;
      const input = document.getElementById(inputId);
      if (!input) return;
      input.focus();
      const end = input.value.length;
      if (typeof input.setSelectionRange === "function") input.setSelectionRange(end, end);
    });
  };

  document.addEventListener("mouseover", (event) => {
    const trigger = closestElement(event.target, "[data-tooltip]");
    if (trigger) window.__hakariShowTooltip(trigger);
  });
  document.addEventListener("mouseout", (event) => {
    if (!tooltipTrigger || tooltipTrigger.contains(event.relatedTarget)) return;
    if (tooltipPinned) return;
    window.__hakariHideTooltip();
  });
  document.addEventListener("focusin", (event) => {
    const trigger = closestElement(event.target, "[data-tooltip]");
    if (trigger) window.__hakariShowTooltip(trigger);
  });
  document.addEventListener(
    "click",
    (event) => {
      // Let interactive controls nested inside a tooltip target (e.g. the doc
      // modal book icon or the sort button in a two-line task header) handle
      // their own click instead of pinning the hover tooltip.
      if (closestElement(event.target, "a, button, summary, input, select, textarea")) return;
      const trigger = closestElement(event.target, "[data-tooltip]");
      if (!trigger) return;
      event.preventDefault();
      event.stopPropagation();
      showTooltipNow(trigger);
    },
    true,
  );
  document.addEventListener("click", (event) => {
    if (tooltipPinned && !closestElement(event.target, "[data-tooltip]")) window.__hakariHideTooltip();
  });
  document.addEventListener("focusout", () => {
    if (!tooltipPinned) window.__hakariHideTooltip();
  });
  document.addEventListener(
    "scroll",
    () => {
      if (!tooltipPinned) window.__hakariHideTooltip();
    },
    true,
  );
  window.addEventListener("resize", window.__hakariHideTooltip);

  window.__hakariApplyHashQueryState();
  window.__hakariBindThemeToggle();
  window.__hakariBindModelDetails();
  document.addEventListener("DOMContentLoaded", window.__hakariBindThemeToggle, { once: true });
  document.addEventListener("DOMContentLoaded", window.__hakariSyncHashQueryStateToParent, { once: true });
  document.addEventListener("htmx:beforeRequest", (event) => window.__hakariSetLeaderboardPending(event, true));
  document.addEventListener("htmx:afterRequest", (event) => window.__hakariSetLeaderboardPending(event, false));
  document.addEventListener("htmx:sendAbort", (event) => window.__hakariSetLeaderboardPending(event, false));
  document.addEventListener("htmx:pushedIntoHistory", window.__hakariSyncHashQueryStateToParent);
  document.addEventListener("htmx:replacedInHistory", window.__hakariSyncHashQueryStateToParent);
})();
