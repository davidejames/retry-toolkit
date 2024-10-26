# retry_toolkit

[![PyPI - Version](https://img.shields.io/pypi/v/retry-toolkit.svg)](https://pypi.org/project/retry-toolkit)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/retry-toolkit.svg)](https://pypi.org/project/retry-toolkit)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
-----

(Yet Another) Retry implementation for python.

Do you have code that may be subjected to intermittent failures? Then you should
have a retry wapper for it. This module includes a simple retry decorator
(factory) you can use. Or peek inside and copy the implementation into your own
project where you can make your own tweaks.

*No dependencies outside of standard python libraries*


## Table of Contents

- [Installation](#installation)
- [Examples](#examples)
- [License](#license)

## Installation

```console
pip install retry-toolkit
```

## Examples

Defaults to 3 tries, no delays between, retry all exceptions:

```python
from retry.simple import retry

@retry()
def foo():
    some_networking_stuff()
```

Customize the basic behaviors like so:

```python
from retry.simple import retry

@retry(tries=4, backoff=1, exceptions=SomeConnectionError)
def foo():
    some_other_networking_stuff()
```
The arguments can take callables for more customization.

## License

`retry-toolkit` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
