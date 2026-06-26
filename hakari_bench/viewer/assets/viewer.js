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
    const delay = trigger.dataset.tooltipDelay === "0" ? 0 : 1000;
    tooltipTimer = setTimeout(() => {
      tooltip.textContent = text;
      tooltip.hidden = false;
      tooltip.dataset.visible = "true";
      window.__hakariPositionTooltip(trigger);
    }, delay);
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
    ["Active params", "active_parameters"],
    ["Total params", "total_parameters"],
    ["Max Tokens", "max_seq_length"],
    ["Dimensions", "embedding_dim"],
    ["Truncate dims", "truncate_dims"],
  ];

  const modelDetailFieldsAfterLinks = [
    ["DType", "dtype"],
    ["Attention", "attention"],
    ["Query Prompt", "query_prompt"],
    ["Query Prompt", "query_prompt_name"],
    ["Doc Prompt", "document_prompt"],
    ["Doc Prompt", "document_prompt_name"],
    ["Prompt", "prompt"],
    ["HF trust", "trust_remote_code"],
    ["Variant", "embedding_variant_name"],
    ["Quantization", "quantization"],
    ["Base delta", "base_score_delta_percent"],
    ["Query len", "late_interaction_query_length"],
    ["Doc len", "late_interaction_document_length"],
    ["Query expansion", "late_interaction_query_expansion"],
    ["Attend expansion tokens", "late_interaction_attend_to_expansion_tokens"],
    ["Query prefix", "late_interaction_query_prefix"],
    ["Doc prefix", "late_interaction_document_prefix"],
  ];

  function formatModelDetailValue(value) {
    if (value === null || value === undefined || value === "") return "";
    if (Array.isArray(value)) {
      if (value.length === 0) return "";
      return value.map((item) => formatModelDetailValue(item)).filter(Boolean).join(", ");
    }
    if (typeof value === "boolean") return value ? "true" : "false";
    if (typeof value === "number") return value.toLocaleString();
    return String(value);
  }

  function shouldShowUnknownModelDetailValue(key, value) {
    if (value !== null && value !== undefined && value !== "") return false;
    return key === "active_parameters" || key === "total_parameters";
  }

  function createModelDetailLink(url, text) {
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.target = "_blank";
    anchor.rel = "noopener noreferrer";
    anchor.className = "break-all text-cyan-700 underline underline-offset-2";
    anchor.textContent = text || url;
    return anchor;
  }

  function appendModelDetailRow(list, label, node) {
    const dt = document.createElement("dt");
    dt.className = "font-medium text-zinc-600";
    dt.textContent = label;
    const dd = document.createElement("dd");
    dd.className = "break-all font-mono text-zinc-900";
    dd.append(node);
    list.append(dt, dd);
  }

  function appendModelDetailLicense(list, license) {
    if (!license || typeof license !== "object") return;
    const label = license.label || license.id;
    if (!label) return;
    appendModelDetailRow(list, "License", document.createTextNode(label));
  }

  function appendModelDetailLinks(list, links) {
    if (!links || typeof links !== "object") return;
    if (typeof links.huggingface === "string" && links.huggingface) {
      const repoId = links.huggingface.replace(/^https?:\/\/huggingface\.co\//, "").replace(/\/+$/, "");
      appendModelDetailRow(list, "Hugging Face", createModelDetailLink(links.huggingface, repoId || "Model page"));
    }
    if (typeof links.github === "string" && links.github) {
      const repoId = links.github.replace(/^https?:\/\/github\.com\//, "").replace(/\/+$/, "");
      appendModelDetailRow(list, "GitHub", createModelDetailLink(links.github, repoId || links.github));
    }
    const papers = Array.isArray(links.papers) ? links.papers : [];
    if (papers.length === 0) return;
    const dt = document.createElement("dt");
    dt.className = "font-medium text-zinc-600";
    dt.textContent = papers.length > 1 ? "Papers" : "Paper";
    const dd = document.createElement("dd");
    dd.className = "flex flex-col gap-1 break-all font-mono text-zinc-900";
    for (const paper of papers) {
      if (!paper || typeof paper.url !== "string" || !paper.url) continue;
      dd.append(createModelDetailLink(paper.url, paper.title || paper.url));
    }
    if (dd.childElementCount > 0) list.append(dt, dd);
  }

  function appendModelDetailNotice(list, notice) {
    const value = formatModelDetailValue(notice);
    if (!value) return;
    appendModelDetailRow(list, "Notice", document.createTextNode(value));
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
      const tableContainer = document.getElementById("help-summary-table-container");
      if (!modal || !heading || !summary || !details || !tableContainer) return;
      heading.textContent = trigger.dataset.helpTitle || "";
      summary.textContent = trigger.dataset.helpSummary || "";
      details.textContent = trigger.dataset.helpDetails || "";
      renderHelpSummaryTable(tableContainer, trigger.dataset.helpTable || "");
      if (typeof modal.showModal === "function") modal.showModal();
    });

    document.addEventListener("keydown", (event) => {
      const trigger = closestElement(event.target, ".help-summary-trigger");
      if (!trigger || (event.key !== "Enter" && event.key !== " ")) return;
      event.preventDefault();
      trigger.click();
    });

    document.addEventListener("click", (event) => {
      const trigger = closestElement(event.target, ".leaderboard-status-count-trigger");
      if (!trigger) return;
      event.preventDefault();
      event.stopPropagation();
      const modal = document.getElementById("count-breakdown-modal");
      const title = document.getElementById("count-breakdown-title");
      if (!modal) return;
      const selectedSection = trigger.dataset.countBreakdownTrigger || "";
      let activeTitle = "Result breakdown";
      for (const section of document.querySelectorAll("[data-count-breakdown-section]")) {
        const isActive = section.dataset.countBreakdownSection === selectedSection;
        section.hidden = !isActive;
        if (isActive) activeTitle = section.dataset.countBreakdownTitle || activeTitle;
      }
      if (title) title.textContent = activeTitle;
      if (typeof modal.showModal === "function") modal.showModal();
    });

    document.addEventListener("click", (event) => {
      const link = closestElement(event.target, ".count-breakdown-task-link");
      if (!link || !link.href) return;
      event.preventDefault();
      event.stopPropagation();
      window.open(link.href, "_blank", "noopener,noreferrer");
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
        const rawValue = metadata[key];
        const value = shouldShowUnknownModelDetailValue(key, rawValue) ? "Unknown" : formatModelDetailValue(rawValue);
        if (!value) continue;
        const dt = document.createElement("dt");
        dt.className = "font-medium text-zinc-600";
        dt.textContent = label;
        const dd = document.createElement("dd");
        dd.className = "break-all font-mono text-zinc-900";
        dd.textContent = value;
        list.append(dt, dd);
      }
      appendModelDetailLicense(list, metadata.license);
      appendModelDetailLinks(list, metadata.links);
      const renderedLabels = new Set();
      for (const [label, key] of modelDetailFieldsAfterLinks) {
        const rawValue = metadata[key];
        const value = shouldShowUnknownModelDetailValue(key, rawValue) ? "Unknown" : formatModelDetailValue(rawValue);
        if (!value || renderedLabels.has(label)) continue;
        renderedLabels.add(label);
        const dt = document.createElement("dt");
        dt.className = "font-medium text-zinc-600";
        dt.textContent = label;
        const dd = document.createElement("dd");
        dd.className = "break-all font-mono text-zinc-900";
        dd.textContent = value;
        list.append(dt, dd);
      }
      appendModelDetailNotice(list, metadata.notice);
      if (typeof modal.showModal === "function") modal.showModal();
    });

    document.addEventListener("click", (event) => {
      const modal = event.target && event.target.id === "model-detail-modal" ? event.target : null;
      if (modal) modal.close();
    });

    document.addEventListener("click", (event) => {
      const modal = event.target && event.target.id === "count-breakdown-modal" ? event.target : null;
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
      if (trigger.dataset.tooltipHoverOnly === "true") return;
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

  function parseOptionalNonNegativeInteger(value) {
    const trimmed = String(value || "").trim();
    if (trimmed === "") return null;
    const parsed = Number.parseInt(trimmed, 10);
    if (!Number.isFinite(parsed)) return null;
    return Math.max(0, parsed);
  }

  function syncDimBoundControl(input) {
    if (!input || !input.dataset || !input.dataset.dimBoundInput) return;
    const container = input.closest(".dim-bounds-filter");
    if (!container) return;
    const minInput = container.querySelector("[data-dim-bound-input='min']");
    const maxInput = container.querySelector("[data-dim-bound-input='max']");
    if (!minInput || !maxInput) return;
    let minValue = parseOptionalNonNegativeInteger(minInput.value);
    let maxValue = parseOptionalNonNegativeInteger(maxInput.value);
    if (minValue !== null) minInput.value = String(minValue);
    if (maxValue !== null) maxInput.value = String(maxValue);
    if (minValue !== null && maxValue !== null && minValue > maxValue) {
      if (input.dataset.dimBoundInput === "min") {
        maxValue = minValue;
        maxInput.value = String(maxValue);
      } else {
        minValue = maxValue;
        minInput.value = String(minValue);
      }
    }

    const hiddenContainer = document.getElementById(input.dataset.dimBoundHiddenTarget || "");
    if (!hiddenContainer) return;
    hiddenContainer.replaceChildren();
    const hiddenValues = [];
    if (minValue !== null && minValue > 32) hiddenValues.push(`gte:${minValue}`);
    if (maxValue !== null) hiddenValues.push(`lte:${maxValue}`);
    for (const value of hiddenValues) {
      const hidden = document.createElement("input");
      hidden.type = "hidden";
      hidden.name = "dim_filter";
      hidden.value = value;
      hiddenContainer.appendChild(hidden);
    }
  }

  document.addEventListener(
    "input",
    (event) => {
      const input = closestElement(event.target, "[data-dim-bound-input]");
      if (input) syncDimBoundControl(input);
    },
    true,
  );

  // Floating sticky column header. Horizontal scrolling lives inside the table's
  // overflow container, so CSS sticky cannot pin the header on page scroll; this
  // mirrors a copy of the header row at the viewport top instead, synced to the
  // table's horizontal scroll and column widths, keeping the pinned-left columns.
  function initStickyLeaderboardHeader() {
    const existing = document.getElementById("hakari-sticky-head");
    if (existing) existing.remove();
    window.__hakariStickyHead = null;
    const container = document.querySelector(".leaderboard-table-scroll");
    const table = container && container.querySelector(".leaderboard-table");
    const thead = table && table.querySelector("thead");
    if (!container || !table || !thead) return;

    const floater = document.createElement("div");
    floater.id = "hakari-sticky-head";
    floater.className = "leaderboard-sticky-head";
    floater.setAttribute("aria-hidden", "true");
    floater.hidden = true;
    const cloneTable = document.createElement("table");
    cloneTable.className = table.className;
    cloneTable.style.tableLayout = "fixed";
    const cloneThead = thead.cloneNode(true);
    cloneTable.appendChild(cloneThead);
    floater.appendChild(cloneTable);
    container.appendChild(floater);

    function syncWidths() {
      if (floater.hidden) return;
      const realThs = thead.querySelectorAll("tr > th");
      const cloneThs = cloneThead.querySelectorAll("tr > th");
      let total = 0;
      realThs.forEach((th, index) => {
        const width = th.getBoundingClientRect().width;
        total += width;
        if (cloneThs[index]) cloneThs[index].style.width = `${width}px`;
      });
      cloneTable.style.width = `${total}px`;
    }

    function update() {
      const rect = container.getBoundingClientRect();
      const headHeight = thead.getBoundingClientRect().height;
      const shouldShow = rect.top < 0 && rect.bottom > headHeight + 4;
      if (!shouldShow) {
        if (!floater.hidden) floater.hidden = true;
        return;
      }
      if (floater.hidden) {
        floater.hidden = false;
        syncWidths();
      }
      floater.style.left = `${rect.left}px`;
      floater.style.width = `${container.clientWidth}px`;
      floater.scrollLeft = container.scrollLeft;
    }

    container.addEventListener(
      "scroll",
      () => {
        if (!floater.hidden) floater.scrollLeft = container.scrollLeft;
      },
      { passive: true },
    );

    window.__hakariStickyHead = { update, syncWidths };
    update();
  }
  window.__hakariInitStickyHeader = initStickyLeaderboardHeader;

  window.addEventListener(
    "scroll",
    () => {
      if (window.__hakariStickyHead) window.__hakariStickyHead.update();
    },
    { passive: true },
  );
  window.addEventListener("resize", () => {
    if (!window.__hakariStickyHead) return;
    window.__hakariStickyHead.syncWidths();
    window.__hakariStickyHead.update();
  });
  document.addEventListener("htmx:afterSwap", (event) => {
    if (event.target && event.target.id === "leaderboard-panel") window.__hakariInitStickyHeader();
  });

  function renderHelpSummaryTable(container, tableJson) {
    container.replaceChildren();
    container.hidden = true;
    if (!tableJson) return;

    let rows = [];
    try {
      rows = JSON.parse(tableJson);
    } catch (_error) {
      return;
    }
    if (!Array.isArray(rows) || rows.length === 0) return;

    const table = document.createElement("table");
    table.className = "w-full border-collapse text-sm";
    const thead = document.createElement("thead");
    const headRow = document.createElement("tr");
    ["Facet", "Full name", "Tasks"].forEach((label) => {
      const th = document.createElement("th");
      th.scope = "col";
      th.className = "border-t px-2 py-1 text-left font-semibold text-zinc-800";
      th.textContent = label;
      headRow.appendChild(th);
    });
    thead.appendChild(headRow);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    rows.forEach((row) => {
      const tr = document.createElement("tr");
      ["code", "name", "tasks"].forEach((key) => {
        const td = document.createElement("td");
        td.className = "border-t px-2 py-1 text-left text-zinc-700";
        td.textContent = row && row[key] != null ? String(row[key]) : "";
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    container.appendChild(table);
    container.hidden = false;
  }

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
