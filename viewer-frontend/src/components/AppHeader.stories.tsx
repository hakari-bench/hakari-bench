import type { Meta, StoryObj } from '@storybook/react-vite';
import { AppHeader } from './AppHeader';

const meta = {
  title: 'Leaderboard/AppHeader',
  component: AppHeader,
} satisfies Meta<typeof AppHeader>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    githubUrl: 'https://github.com/hakari-bench/hakari-bench',
    docsUrl: '/docs/',
  },
};
