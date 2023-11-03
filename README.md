# vedro-lazy-rerunner
Rerunner plugin for the [Vedro](https://vedro.io/) testing framework.  
Reruns failed scenarios until the first pass otherwise the specified number of times.

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
