import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite"; /* instead of @tailwindcss/postcss */

// https://vitejs.dev/config/
export default defineConfig({
  base: "/static/", // base path to serve static assets
  build: {
    outDir: "./dist",
    manifest: "manifest.json",
    rollupOptions: {
      input: {
        main: "/src/app/main.js",
      },
    },
  },
  server: {
    host: "localhost",
    port: 5173,
    cors: true,
  },
  plugins: [tailwindcss()],
});
