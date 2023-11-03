from argparse import ArgumentParser, Namespace
from pathlib import Path
from time import monotonic_ns
from unittest.mock import Mock

import pytest
from vedro import Scenario
from vedro.core import (
    Config,
    ConfigType,
    Dispatcher,
    Factory,
    MonotonicScenarioScheduler,
    ScenarioResult,
    ScenarioScheduler,
    VirtualScenario,
)
from vedro.events import (
    ArgParsedEvent,
    ArgParseEvent,
    ConfigLoadedEvent,
    ScenarioFailedEvent,
    StartupEvent,
)

from vedro_lazy_rerunner import LazyRerunner, LazyRerunnerPlugin, LazyScenarioScheduler


@pytest.fixture()
def dispatcher() -> Dispatcher:
    return Dispatcher()


@pytest.fixture()
def rerunner(dispatcher: Dispatcher) -> LazyRerunnerPlugin:
    plugin = LazyRerunnerPlugin(LazyRerunner)
    plugin.subscribe(dispatcher)
    return plugin


@pytest.fixture()
def scheduler() -> LazyScenarioScheduler:
    return LazyScenarioScheduler([])


@pytest.fixture()
def scheduler_() -> LazyScenarioScheduler:
    return Mock(spec=LazyScenarioScheduler)


def make_vscenario() -> VirtualScenario:
    class _Scenario(Scenario):
        __file__ = Path(f"scenario_{monotonic_ns()}.py").absolute()

    return VirtualScenario(_Scenario, steps=[])


def make_scenario_result() -> ScenarioResult:
    return ScenarioResult(make_vscenario())


def make_config() -> ConfigType:
    class TestConfig(Config):
        class Registry(Config.Registry):
            ScenarioScheduler = Factory[ScenarioScheduler](MonotonicScenarioScheduler)

    return TestConfig


async def fire_arg_parsed_event(dispatcher: Dispatcher, lazy_reruns: int) -> None:
    config_loaded_event = ConfigLoadedEvent(Path(), make_config())
    await dispatcher.fire(config_loaded_event)

    arg_parse_event = ArgParseEvent(ArgumentParser())
    await dispatcher.fire(arg_parse_event)

    arg_parsed_event = ArgParsedEvent(Namespace(lazy_reruns=lazy_reruns))
    await dispatcher.fire(arg_parsed_event)


async def fire_startup_event(dispatcher: Dispatcher, scheduler: LazyScenarioScheduler) -> None:
    startup_event = StartupEvent(scheduler)
    await dispatcher.fire(startup_event)


async def fire_failed_event(scenario_result, dispatcher: Dispatcher) -> ScenarioFailedEvent:
    scenario_result.mark_failed()
    scenario_failed_event = ScenarioFailedEvent(scenario_result)
    await dispatcher.fire(scenario_failed_event)
    return scenario_failed_event
