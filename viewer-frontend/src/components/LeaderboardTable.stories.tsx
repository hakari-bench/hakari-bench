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

export const Default: Story = {
  args: {
    result: sampleLeaderboard,
    sort: 'borda_score',
    direction: 'desc',
    onSort: () => {},
  },
  render: (args) => {
    const [sort, setSort] = useState(args.sort);
    const [direction, setDirection] = useState(args.direction);
    return (
      <LeaderboardTable
        result={args.result}
        sort={sort}
        direction={direction}
        onSort={(column) => {
          if (column === sort) setDirection(direction === 'desc' ? 'asc' : 'desc');
          else {
            setSort(column);
            setDirection(column === 'model_name' ? 'asc' : 'desc');
          }
        }}
      />
    );
  },
};
