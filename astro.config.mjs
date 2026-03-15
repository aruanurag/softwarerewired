import { defineConfig } from "astro/config";
import rss from "@astrojs/rss";

export default defineConfig({
  site: "https://softwarerewired.com",
  output: "static",
  integrations: [rss()]
});
