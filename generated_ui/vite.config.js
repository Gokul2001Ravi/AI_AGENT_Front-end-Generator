import react from '@vitejs/plugin-react';
import tailwindcss from 'tailwindcss';

export default {
  base: '/',
  build: {
    outDir: 'dist',
    assetsInlineLimit: 0,
  },
  plugins: [
    react(),
    tailwindcss()
  ],
};
