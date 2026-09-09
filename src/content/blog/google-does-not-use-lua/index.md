---
title: "Google Does Not Use Lua"
published: 2026-08-25
draft: false
---
I started scripting in Lua when I was 11.

If you're not familiar with Lua, it is a neat and weird scripting language. It has:
- 1-indexed arrays (wtf?)
- no concept of OOP (double wtf??)
- one single data structure - a table (triple wtf???)
- Makes you write end at the end of every function. So your code ends up looking like this

```lua
local function kill_everything_ever(x)
	for i=1, n = n + 2, 2:
```

## Lua's practical use fate

Aside from the fun applications, it would appear we have two main remaining Lua users still active out in the wild.

![lua_users_in_2026.png](./lua_users_in_2026.png)

Let's choose to not talk about the weirdos using [LÖVE2D](https://love2d.org/) and [Pico8](https://www.lexaloffle.com/pico-8.php).

ROBLOX, a platform that was once filled with young pioneers, future engineers, and men destined to go on to do great things, is turning into a vibe-coding haven for agents of m s a to create gslop for prepubescent iPad kids. Thank you, private equity! irregardless, Roblox has made a dedicated commitment to stick with Lua, or rather, their fork of the language - Luau.

Luau is a modern tbc