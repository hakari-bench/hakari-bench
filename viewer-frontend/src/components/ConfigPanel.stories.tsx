import type { Meta, StoryObj } from '@storybook/react-vite';
import { useState } from 'react';
import { ConfigPanel } from './ConfigPanel';
import { sampleConfig } from '../fixtures/config';
import { sampleLeaderboard } from '../fixtures/leaderboard';
import { DEFAULT_STATE, type ViewerState } from '../lib/urlState';

const meta = {
  title: 'Leaderboard/ConfigPanel',
  component: ConfigPanel,
} satisfies Meta<typeof ConfigPanel>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    config: sampleConfig,
    result: sampleLeaderboard,
    state: DEFAULT_STATE,
    update: () => {},
  },
  render: (args) => {
    const [state, setState] = useState<ViewerState>(args.state);
    return (
      <ConfigPanel
        config={args.config}
        result={args.result}
        state={state}
        update={(patch) => setState((prev) => ({ ...prev, ...patch }))}
      />
    );
  },
};
