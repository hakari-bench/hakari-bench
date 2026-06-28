import type { Meta, StoryObj } from '@storybook/react-vite';
import { useState } from 'react';
import { FilterPanel } from './FilterPanel';
import { sampleLeaderboard } from '../fixtures/leaderboard';
import { DEFAULT_STATE, type ViewerState } from '../lib/urlState';

const meta = {
  title: 'Leaderboard/FilterPanel',
  component: FilterPanel,
} satisfies Meta<typeof FilterPanel>;

export default meta;
type Story = StoryObj<typeof meta>;

function FilterPanelDemo({ initial }: { initial: ViewerState }) {
  const [state, setState] = useState<ViewerState>(initial);
  return (
    <FilterPanel
      result={sampleLeaderboard}
      state={state}
      update={(patch) => setState((prev) => ({ ...prev, ...patch }))}
    />
  );
}

export const Open: Story = {
  args: {
    result: sampleLeaderboard,
    state: { ...DEFAULT_STATE, filters: true },
    update: () => {},
  },
  render: () => <FilterPanelDemo initial={{ ...DEFAULT_STATE, filters: true }} />,
};
