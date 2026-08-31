---
publish: true
type: note
title: Wikilink Torture Test
date: 2026-08-01
tags: [meta]
---

## Resolution cases

- Published target: [[Google Does Not Use Lua]]
- With an alias: [[Google Does Not Use Lua|this post about Lua]]
- With a heading: [[Google Does Not Use Lua#Resolution cases]]
- Unpublished target must degrade to plain text: [[My Private Journal]]
- Nonexistent target: [[Does Not Exist At All]]

## Embeds

![[Pasted image 20260830.png]]

Ordinary markdown image: ![a square](Attachments/Pasted%20image%2020260830.png)

Inline `[[not a link]]` inside code must survive untouched.

    [[also not a link]] in a code block
