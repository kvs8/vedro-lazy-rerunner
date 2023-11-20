# vedro-lazy-rerunner
[![PyPI](https://img.shields.io/pypi/v/vedro-lazy-rerunner.svg?style=flat-square)](https://pypi.org/project/vedro-lazy-rerunner/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-lazy-rerunner.svg?style=flat-square)](https://pypi.org/project/vedro-lazy-rerunner/)

The `vedro-lazy-rerunner` is a plugin for the [Vedro](https://vedro.io/) testing framework. 
It reruns failed scenarios until they pass for the first time. If none of the reruns are successful, the test is marked as failed after the designated number of attempts.

# Installation

1. Install the package using pip:
```shell
$ pip3 install vedro-lazy-rerunner
```

2. Then, activate the plugin in your vedro.cfg.py configuration file:
```python
# ./vedro.cfg.py
import vedro
import vedro_lazy_rerunner

class Config(vedro.Config):

    class Plugins(vedro.Config.Plugins):

        class LazyRerunner(vedro_lazy_rerunner.LazyRerunner):
            enabled = True
```

# Usage
Run Vedro with the `--lazy-reruns` option set to the desired number of reruns:
```shell
$ vedro run --lazy-reruns=5
```

# Examples

- A test will not be rerun further if it passes during one of the reruns:
```shell
$ vedro run --lazy-reruns=5
```
```shell
Scenarios
* 
 ✔ check number
 │
 ├─[1/2] ✗ check number
 │
 ├─[2/2] ✔ check number
 
# 1 scenario, 1 passed, 0 failed, 0 skipped (0.01s)
```
The test passed on the second attempt. The remaining 3 attempts were not needed. The test is considered passed.

- A test is marked as failed if it does not pass in any of the attempts:
```shell
$ vedro run --lazy-reruns=5
```
```shell
Scenarios
* 
 ✗ check number
 │
 ├─[1/5] ✗ check number
 │
 ├─[2/5] ✗ check number
 │
 ├─[3/5] ✗ check number
 │
 ├─[4/5] ✗ check number
 │
 ├─[5/5] ✗ check number

# 1 scenario, 0 passed, 1 failed, 0 skipped (0.02s)
```
The test is considered failed as it did not pass in any of the 5 attempts.
