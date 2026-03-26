---
name: software-rewired-blog-drafter
description: "Prepares a new Software Rewired blog branch and post path, then uses OpenClaw's configured model to draft the post in src/content/posts."
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins: ["git", "python3"]
---

# Software Rewired Blog Drafting Skill

Use this skill when the user shares the topic, message, audience, or source notes for a new Software Rewired blog post.
## Workflow

1. Work from the repository root that contains `src/content/posts`.
2. If the git worktree is dirty, stop unless the user explicitly approves continuing.
3. Run the helper to sync the default branch, create a new blog branch, and emit the target post path plus style context from recent posts.
4. Use OpenClaw's configured model to draft the blog post directly. Do not call a provider API from the helper script.
5. Write a markdown file to the emitted `post_path` with frontmatter keys: `title`, `date`, `author`, `tags`, `summary`.
6. Match the tone of recent Software Rewired posts: practical, optimistic but grounded, and easy to scan.
7. Report the branch name and saved post path.
## Command

Run the helper from the repo root:

```bash
python3 openclaw/scripts/create_blog_post.py \
  --brief "Your blog brief goes here"
```

Useful optional flags:

```bash
--title "Optional title"
--tags "AI,Software Architecture"
--author "Anurag Mohan"
--date "2026-03-26"
--slug "optional-slug"
--brief-file /absolute/path/to/brief.txt
--skip-git
--allow-dirty
```
## Expected Helper Output

The helper prints JSON containing:

- `branch`
- `post_path`
- `slug`
- `date`
- `author`
- `title_hint`
- `tags_hint`
- `brief`
- `style_samples`

Use that JSON as the drafting context, then write the final markdown post yourself.

## Notes

- This skill should rely on OpenClaw's configured model provider.
- No `OPENAI_API_KEY` is required for this skill.
- `REPO_PATH`, `BLOG_AUTHOR`, and `BLOG_DEFAULT_BRANCH` can still be used as defaults.
