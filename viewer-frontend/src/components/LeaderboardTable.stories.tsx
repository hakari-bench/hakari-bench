import type { Meta, StoryObj } from '@storybook/react-vite';
import { useState } from 'react';
import { LeaderboardTable } from './LeaderboardTable';
import { sampleLeaderboard } from '../fixtures/leaderboard';

const meta = {
  title: 'Leaderboard/LeaderboardTable',
  component: LeaderboardTable,
} satisfies Meta<typeof LeaderboardTable>;

export default meta;
type Story = StoryObj<typeof meta>;

function LeaderboardTableDemo() {
  const [sort, setSort] = useState('borda_score');
  const [direction, setDirection] = useState<'asc' | 'desc'>('desc');
  return (
    <LeaderboardTable
      result={sampleLeaderboard}
      sort={sort}
      direction={direction}
      onSelectModel={() => {}}
      onSort={(column) => {
        if (column === sort) setDirection(direction === 'desc' ? 'asc' : 'desc');
        else {
          setSort(column);
          setDirection(column === 'model_name' ? 'asc' : 'desc');
        }
      }}
    />
  );
}

export const Default: Story = {
  args: {
    result: sampleLeaderboard,
    sort: 'borda_score',
    direction: 'desc',
    onSort: () => {},
    onSelectModel: () => {},
  },
  render: () => <LeaderboardTableDemo />,
};
