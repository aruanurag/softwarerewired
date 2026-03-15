# Software Rewired

A clean, minimal Astro blog built for GitHub Pages.

## Quick start

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
npm run preview
```

## Content

Add Markdown posts in `src/content/posts/` with frontmatter:

```md
---
title: "Your Title"
date: "2026-03-15"
author: "Software Rewired"
tags: ["AI", "SaaS"]
summary: "Short summary."
---
```

## Deploy to GitHub Pages

1. Update `astro.config.mjs` `site` to your custom domain.
2. Update `public/CNAME` to your custom domain.
3. Push to `main`. The GitHub Actions workflow in `.github/workflows/deploy.yml` will build and deploy.
4. In GitHub repo settings, enable Pages and set the custom domain.

## Notes

- RSS feed at `/rss.xml`
- Dark mode is automatic based on system preference
