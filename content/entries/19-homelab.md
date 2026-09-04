+++
title = "Self-hosting"
slug = "self-hosting"
lane = "systems"
when = "2022 -"
sort = "2022-06"
tags = ["linux", "caddy", "tailscale", "servers"]
blurb = "Three years of running my own boxes. Started as a free VPS and a game server, ended as most of a house."
+++
It started with a free Oracle Cloud VPS hosting a website and some game servers, which taught me more about
networking, ports, SSH and what a firewall is for than school ever did.

Now it's a mini PC at home doing files, music, DNS, home automation and game servers, a VPS holding the
public ingress because I'd rather own my front door, and Tailscale gluing the two together.

All of it is declared in [nixeljam](../nixeljam/), so the interesting question stopped being "how do I set
this up" and became "what happens when this disk dies".
