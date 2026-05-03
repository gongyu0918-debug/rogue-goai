import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/static/react/",
  plugins: [react()],
  build: {
    outDir: "../static/react",
    emptyOutDir: true,
    sourcemap: false,
    target: ["chrome109", "edge109"],
    cssTarget: ["chrome109", "edge109"]
  },
  server: {
    host: "127.0.0.1",
    port: 5173
  }
});
