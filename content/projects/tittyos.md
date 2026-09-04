+++
title   = "tittyos"
group   = "apps"
year    = "2025"
role    = "solo"
tagline = "A deep learning library in C++. Tensors, autograd, terrible name."
stack   = ["C++", "CMake"]
thumb   = "img/proj/tittyos-thumb.webp"
order   = 23
[[links]]
label = "source"
url   = "https://github.com/milotek/tittyos"
[[images]]
src = "img/proj/tittyos-1.webp"
alt = "The tittyos logo, a gold sculpture"
+++

Tensors with shapes and dtypes, elementwise ops, and `backward()` walking the graph to fill in gradients. You write `ty::sum(ty::multiply(a, b))` and it does the calculus for you.

Written to find out what PyTorch is doing under the hood, which turns out to be the only way I ever properly learn anything. Still unfinished, plenty missing.
