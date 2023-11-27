import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { config } from 'dotenv';

import path from "path";
import { resolve } from 'path';

config({ path: path.join(__dirname, ".env") });

const STATIC_URL = process.env.STATIC_URL;

// https://vitejs.dev/config/
export default defineConfig({
  base: `${STATIC_URL}`,
  clearScreen: false,
  css: {
    devSourcemap: true,
  },
  plugins: [
    vue()
  ],
  build: {
    target: "esnext",
    outDir: resolve("./static/"),
    emptyOutDir: false,
    assetsDir: "",
    manifest: true,
    rollupOptions: {
      input: {
        main: resolve("./gde/js/main.js"),
        gde: resolve("./gde/js/gde.js"),
      },
    },
    root: "."
  },
  server: {
    port: 3333
  }
})
