import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://hongping-zh.github.io',
  base: '/circular-bias-detection/',
  integrations: [tailwind({ applyBaseStyles: true }), sitemap()],
  output: 'static'
});
