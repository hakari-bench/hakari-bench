import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import { DocsApp } from './DocsApp.tsx';

const isDocs = window.location.pathname.startsWith('/docs');

createRoot(document.getElementById('root')!).render(
  <StrictMode>{isDocs ? <DocsApp /> : <App />}</StrictMode>,
);
