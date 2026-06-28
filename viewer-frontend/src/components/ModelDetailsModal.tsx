import { Info } from 'lucide-react';
import type { ReactNode } from 'react';
import type { LeaderboardRow } from '../lib/api';
import { formatDim, formatMaxLen, formatParams, shortModelTypeLabel } from '../lib/format';
import { Modal } from '../ui/modal';

interface ModelDetailsModalProps {
  row: LeaderboardRow | null;
  onClose: () => void;
}

function Row({ label, value }: { label: string; value: ReactNode }) {
  if (value === null || value === undefined || value === '') return null;
  return (
    <div className="grid grid-cols-[140px_1fr] gap-2 border-b border-border/50 py-1 last:border-0">
      <dt className="text-muted-foreground">{label}</dt>
      <dd className="break-words text-foreground">{value}</dd>
    </div>
  );
}

function githubLabel(url: string): string {
  const match = url.match(/github\.com\/([^/]+\/[^/]+)/i);
  return match ? match[1] : url;
}

export function ModelDetailsModal({ row, onClose }: ModelDetailsModalProps) {
  if (!row) return null;
  const license = row.license;
  const links = row.links;
  const languages = row.language_support_languages?.length
    ? row.language_support_languages.join(', ')
    : row.language_support_category;
  const prompt = (value: string | null, name: string | null): string | null => {
    if (value) return value;
    if (name) return `name: ${name}`;
    return null;
  };

  return (
    <Modal
      open={!!row}
      onClose={onClose}
      icon={<Info className="h-4 w-4 text-accent" strokeWidth={1.75} />}
      title={row.model_name}
    >
      <dl className="text-[12px] tnum">
        <Row label="Language" value={languages} />
        <Row label="Model type" value={shortModelTypeLabel(row.model_type)} />
        <Row label="Active params" value={formatParams(row.active_parameters)} />
        <Row label="Total params" value={formatParams(row.total_parameters)} />
        <Row label="Max tokens" value={formatMaxLen(row.max_seq_length)} />
        <Row label="Dims" value={formatDim(row.embedding_dim)} />
        {row.quantization ? <Row label="Quantization" value={row.quantization} /> : null}
        {row.truncate_dims?.length ? (
          <Row label="Truncate dims" value={row.truncate_dims.join(', ')} />
        ) : null}
        <Row label="Dtype" value={row.dtype ? row.dtype.toUpperCase() : null} />
        <Row label="Attention" value={row.attn_implementation} />
        <Row label="Query Prompt" value={prompt(row.query_prompt, row.query_prompt_name)} />
        <Row label="Doc Prompt" value={prompt(row.document_prompt, row.document_prompt_name)} />
        <Row label="License" value={license?.label ?? license?.id} />
        {links?.huggingface ? (
          <Row
            label="Hugging Face"
            value={
              <a className="text-accent hover:underline" href={links.huggingface} target="_blank" rel="noreferrer">
                {row.model_name}
              </a>
            }
          />
        ) : null}
        {links?.github ? (
          <Row
            label="GitHub"
            value={
              <a className="text-accent hover:underline" href={links.github} target="_blank" rel="noreferrer">
                {githubLabel(links.github)}
              </a>
            }
          />
        ) : null}
        {links?.papers?.length ? (
          <Row
            label="Papers"
            value={
              <ul className="space-y-0.5">
                {links.papers.map((paper) => (
                  <li key={paper.url}>
                    <a className="text-accent hover:underline" href={paper.url} target="_blank" rel="noreferrer">
                      {paper.title}
                    </a>
                  </li>
                ))}
              </ul>
            }
          />
        ) : null}
        {row.notice ? <Row label="Notice" value={row.notice} /> : null}
      </dl>
    </Modal>
  );
}
