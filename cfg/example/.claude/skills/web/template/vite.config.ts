import { defineConfig } from "vite";
import { existsSync } from "fs";
import { join } from "path";

export default defineConfig({
  appType: "mpa",
  server: {
    port: 49165,
    host: "0.0.0.0",
    watch: { usePolling: false },
  },
  plugins: [
    {
      name: "trailing-slash-rewrite",
      configureServer(server) {
        server.middlewares.use((req, _res, next) => {
          const url = req.url || "";
          if (
            !url.endsWith("/") &&
            !url.includes(".") &&
            !url.startsWith("/@")
          ) {
            const indexPath = join(__dirname, url, "index.html");
            if (existsSync(indexPath)) {
              req.url = url + "/";
            }
          }
          next();
        });
      },
    },
  ],
});
