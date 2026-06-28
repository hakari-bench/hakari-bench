import type { Meta, StoryObj } from '@storybook/react-vite';
import { useState } from 'react';
import { Chart } from './Chart';
import { sampleLeaderboard } from '../fixtures/leaderboard';
import { DEFAULT_STATE, type ViewerState } from '../lib/urlState';

const meta = {
  title: 'Leaderboard/Chart',
  component: Chart,
} satisfies Meta<typeof Chart>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    result: sampleLeaderboard,
    state: { ...DEFAULT_STATE, resultView: 'chart' },
    update: () => {},
  },
  render: (args) => {
    const [state, setState] = useState<ViewerState>(args.state);
    return (
      <Chart result={args.result} state={state} update={(patch) => setState((prev) => ({ ...prev, ...patch }))} />
    );
  },
};
