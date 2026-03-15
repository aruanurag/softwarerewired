import { defineConfig } from "astro/config";
import rss from "@astrojs/rss";
import adapter from "@astrojs/adapter-static";

export default defineConfig({
  site: "https://softwarerewired.com",
  output: "static",
  adapter: adapter(),
  integrations: [rss()]
});
