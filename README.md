# vedro-lazy-rerunner
[![PyPI](https://img.shields.io/pypi/v/vedro-lazy-rerunner.svg?style=flat-square)](https://pypi.org/project/vedro-lazy-rerunner/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-lazy-rerunner.svg?style=flat-square)](https://pypi.org/project/vedro-lazy-rerunner/)

Rerunner plugin for the [Vedro](https://vedro.io/) testing framework.  
Reruns failed scenarios until the first pass. If there is no successful execution, the test will fail after the specified number of attempts.

# Installation

1. Install the package using pip:
```shell
$ pip3 install vedro-lazy-rerunner
```

2. Next, activate the plugin in your vedro.cfg.py configuration file:
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
```shell
$ vedro run --lazy-reruns=5
```

# Examples

- Test will not be reruned further if it is passed during one of the rerun  
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
> Test was passed on the second attempt, the remaining 3 attempts will not be performed. Test is considered passed  

- Test is considered failed if it failed during all attempts
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
> Test is considered failed
