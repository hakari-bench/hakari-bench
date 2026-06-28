import type { ViewerConfigResponse } from '../lib/api';

const SUITE_NAMES = [
  ['MNanoBEIR:task_mean', 'M-BEIR(task)', 'MNanoBEIR'],
  ['MNanoBEIR:lang_mean', 'M-BEIR(lang)', 'MNanoBEIR'],
  ['NanoMMTEB-v2', 'MMTEB-v2', 'NanoMMTEB-v2'],
  ['NanoRTEB', 'RTEB', 'NanoRTEB'],
  ['NanoMLDR', 'MLDR', 'NanoMLDR'],
  ['NanoMIRACL', 'MIRACL', 'NanoMIRACL'],
  ['NanoCoIR', 'CoIR', 'NanoCoIR'],
  ['NanoBRIGHT', 'BRIGHT', 'NanoBRIGHT'],
  ['NanoIndicQA', 'IndicQA', 'NanoIndicQA'],
  ['NanoCodeRAG', 'CodeRAG', 'NanoCodeRAG'],
];

/** Static config fixture so the ConfigPanel renders without a running API. */
export const sampleConfig: ViewerConfigResponse = {
  overalls: [
    { name: 'Overall', label: 'Overall' },
    { name: 'Overall (EN)', label: 'Overall (EN)' },
  ],
  benchmarks: SUITE_NAMES.filter(([, , b]) => b !== 'MNanoBEIR' || true).map(([, , b]) => ({
    name: b,
    label: b,
  })),
  scope: {
    presets: [
      { name: 'Overall', label: 'Overall', kind: 'overall' },
      { name: 'Overall (EN)', label: 'Overall (EN)', kind: 'overall' },
      { name: 'Clear', label: 'Clear', kind: 'clear' },
    ],
    suites: SUITE_NAMES.map(([selection_key, label, benchmark], index) => ({
      selection_key,
      label,
      benchmark,
      sort_key: index,
    })),
  },
  clear_scope: 'Clear',
  defaults: {
    view: 'Overall',
    sort: 'borda_score',
    direction: 'desc',
    target: 'all',
    score: 'micro',
    metric: 'ndcg@10',
    result_view: 'table',
  },
  footer: {
    latest_update: '2026-06-25T22:34:13(UTC)',
    database_label: 'database: remote / 0123456789ab',
  },
  links: { github: 'https://github.com/hakari-bench/hakari-bench', docs: '/docs/' },
};
