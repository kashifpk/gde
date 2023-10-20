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
        vuehello: resolve("./gde/js/index.js"),
        // auth: resolve("./src/sensorhub/auth/js/index.js"),
        // dashboard: resolve("./src/sensorhub/dashboard/js/index.js"),
        // admin: resolve("./src/sensorhub/admin/js/index.js"),
        // devices: resolve("./src/sensorhub/devices/js/index.js"),
        // tags: resolve("./src/sensorhub/tags/js/index.js"),
        // notifications: resolve("./src/sensorhub/notifications/js/index.js"),
        // partner: resolve("./src/sensorhub/partner/js/index.js"),
        // alerts: resolve("./src/sensorhub/alerts/js/index.js")
      },
    },
    root: "."
  },
  server: {
    port: 3333
  }
})
