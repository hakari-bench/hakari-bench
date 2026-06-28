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

function ChartDemo({ initial }: { initial: ViewerState }) {
  const [state, setState] = useState<ViewerState>(initial);
  return (
    <Chart
      result={sampleLeaderboard}
      state={state}
      update={(patch) => setState((prev) => ({ ...prev, ...patch }))}
    />
  );
}

export const Default: Story = {
  args: {
    result: sampleLeaderboard,
    state: { ...DEFAULT_STATE, resultView: 'chart' },
    update: () => {},
  },
  render: () => <ChartDemo initial={{ ...DEFAULT_STATE, resultView: 'chart' }} />,
};
