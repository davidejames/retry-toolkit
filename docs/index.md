
# retry-toolkit

(Yet Another) Retry implementation for python.

Do you have code that may be subjected to intermittent failures? Then you should
have a retry wapper for it. This module includes a simple retry decorator
(factory) you can use. Or peek inside and copy the implementation into your own
project where you can make your own tweaks.

*No dependencies outside of standard python libraries*


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


## API Reference

### `retry_toolkit.simple.retry`

::: retry_toolkit.simple.retry
    options:
        heading_level: 0


### `retry_toolkit.simple.GiveUp`

::: retry_toolkit.simple.GiveUp
    options:
        heading_level: 0


### `retry_toolkit.simple.Defaults`

::: retry_toolkit.simple.Defaults
    options:
        heading_level: 0
        members_order: source

### Backoff Functions

#### `retry_toolkit.simple.constant`

::: retry_toolkit.simple.constant
    options:
        heading_level: 0

#### `retry_toolkit.simple.linear`

::: retry_toolkit.simple.linear
    options:
        heading_level: 0

#### `retry_toolkit.simple.exponential`

::: retry_toolkit.simple.exponential
    options:
        heading_level: 0



