(() => {
  if (window.__hakariViewerInitialized) return;
  window.__hakariViewerInitialized = true;

  function closestElement(target, selector) {
    if (!target || !target.closest) return null;
    return target.closest(selector);
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

  window.__hakariShowTooltip = (trigger) => {
    const tooltip = tooltipElement();
    const text = trigger && trigger.dataset ? trigger.dataset.tooltip : "";
    if (!tooltip || !text) return;
    window.__hakariHideTooltip();
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
    tooltipTrigger = null;
    const tooltip = tooltipElement();
    if (!tooltip) return;
    tooltip.hidden = true;
    delete tooltip.dataset.visible;
    tooltip.textContent = "";
  };

  const modelDetailFields = [
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
      const trigger = closestElement(event.target, ".model-detail-trigger");
      if (!trigger) return;
      const modal = document.getElementById("model-detail-modal");
      const title = document.getElementById("model-detail-title");
      const list = document.getElementById("model-detail-fields");
      if (!modal || !title || !list) return;
      const metadata = JSON.parse(trigger.dataset.modelMetadata || "{}");
      title.textContent = metadata.model_name || trigger.textContent || "";
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

    document.addEventListener("submit", (event) => {
      if (!event.target || event.target.id !== "display-controls") return;
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
    window.__hakariHideTooltip();
  });
  document.addEventListener("focusin", (event) => {
    const trigger = closestElement(event.target, "[data-tooltip]");
    if (trigger) window.__hakariShowTooltip(trigger);
  });
  document.addEventListener("focusout", window.__hakariHideTooltip);
  document.addEventListener("scroll", window.__hakariHideTooltip, true);
  window.addEventListener("resize", window.__hakariHideTooltip);

  window.__hakariApplyHashQueryState();
  window.__hakariBindModelDetails();
  document.addEventListener("DOMContentLoaded", window.__hakariSyncHashQueryStateToParent, { once: true });
  document.addEventListener("htmx:beforeRequest", (event) => window.__hakariSetLeaderboardPending(event, true));
  document.addEventListener("htmx:afterRequest", (event) => window.__hakariSetLeaderboardPending(event, false));
  document.addEventListener("htmx:sendAbort", (event) => window.__hakariSetLeaderboardPending(event, false));
  document.addEventListener("htmx:pushedIntoHistory", window.__hakariSyncHashQueryStateToParent);
  document.addEventListener("htmx:replacedInHistory", window.__hakariSyncHashQueryStateToParent);
})();
