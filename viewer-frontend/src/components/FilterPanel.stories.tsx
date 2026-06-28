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

export const Open: Story = {
  args: {
    result: sampleLeaderboard,
    state: { ...DEFAULT_STATE, filters: true },
    update: () => {},
  },
  render: (args) => {
    const [state, setState] = useState<ViewerState>(args.state);
    return (
      <FilterPanel
        result={args.result}
        state={state}
        update={(patch) => setState((prev) => ({ ...prev, ...patch }))}
      />
    );
  },
};
