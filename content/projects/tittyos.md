+++
title = "tittyos"
roll = "toys"
order = 4
year = "2025"
kind = "Library"
status = "in progress"
url = "https://github.com/milotek/tittyos"
url_label = "github.com/milotek/tittyos"
blurb = "A deep learning library in C++, with autograd. Unfortunate name, real tensors."
stack = ["C++"]
+++

Tensors, shapes, dtypes and a backward pass, in C++.

```cpp
ty::Tensor result = ty::sum(ty::multiply(tensor1, tensor2));
result.backward();
tensor1.grad(); // [2.0, 3.0, 5.0, 7.0, 11.0]
```

Written with [Samuel Johnson](https://github.com/SJ1727), who started it and owns the copyright. Still under construction.

Yes, I know. He named it.
