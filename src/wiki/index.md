---
title: Wiki
layout: wiki
---

How to install, run and use each part of ezp2p.

{% for w in site.wikis -%}
- **[{{ w.title }}]({{ '/wiki/' | append: w.id | append: '/' | relative_url }})**
{% endfor %}

## Editing the wiki

The wiki lives in the [`website`](https://github.com/ezp2p/website) repository, under `src/wiki/`, with one folder per
program. Every page has an **Edit this page on GitHub** link at the bottom.

When a change to Puddle, Pond or Levee changes how people install or use it, update the matching page in the same
piece of work.

To add a page, make a Markdown file in the program's folder with a title at the top:

```markdown
---
title: Backups
nav_order: 30
---

Text of the page.
```

`nav_order` sets where it sits in the sidebar (lower comes first). Link to other pages by their address, such as
`/wiki/puddle/installation/`.
