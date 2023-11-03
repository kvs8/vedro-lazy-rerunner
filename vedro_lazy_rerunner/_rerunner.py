from typing import Type, Union

from vedro.core import ConfigType, Dispatcher, Plugin, PluginConfig, ScenarioScheduler
from vedro.events import (
    ArgParsedEvent,
    ArgParseEvent,
    ConfigLoadedEvent,
    ScenarioFailedEvent,
    ScenarioPassedEvent,
    StartupEvent,
)

from ._scheduler import LazyScenarioScheduler


class LazyRerunnerPlugin(Plugin):
    def __init__(self, config: Type["LazyRerunner"]) -> None:
        super().__init__(config)
        self._reruns: int = 0
        self._global_config: Union[ConfigType, None] = None
        self._scheduler: Union[ScenarioScheduler, None] = None
        self._rerun_scenario_id: Union[str, None] = None
        self._current_rerun = 0

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ConfigLoadedEvent, self.on_config_loaded) \
            .listen(ArgParseEvent, self.on_arg_parse) \
            .listen(ArgParsedEvent, self.on_arg_parsed) \
            .listen(StartupEvent, self.on_startup) \
            .listen(ScenarioPassedEvent, self.on_scenario_end) \
            .listen(ScenarioFailedEvent, self.on_scenario_end)

    def on_config_loaded(self, event: ConfigLoadedEvent) -> None:
        self._global_config = event.config

    def on_arg_parse(self, event: ArgParseEvent) -> None:
        group = event.arg_parser.add_argument_group("Rerunner")
        group.add_argument("--lazy-reruns", type=int, default=0,
                           help="Number of times to rerun failed scenarios (default: 0)")

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        self._reruns = event.args.lazy_reruns
        if self._reruns < 0:
            raise ValueError("--lazy-reruns must be >= 0")

        if self._reruns == 0:
            return

        assert self._global_config is not None  # for type checking
        self._global_config.Registry.ScenarioScheduler.register(LazyScenarioScheduler, self)

    def on_startup(self, event: StartupEvent) -> None:
        self._scheduler = event.scheduler

    def on_scenario_end(self, event: Union[ScenarioPassedEvent, ScenarioFailedEvent]) -> None:
        if self._reruns == 0:
            return

        if event.scenario_result.is_failed():
            if self._rerun_scenario_id == event.scenario_result.scenario.unique_id:
                if self._reruns > self._current_rerun:
                    self._current_rerun += 1
                    self._scheduler.schedule(event.scenario_result.scenario)  # type: ignore
            else:
                self._rerun_scenario_id = event.scenario_result.scenario.unique_id
                self._current_rerun = 1
                self._scheduler.schedule(event.scenario_result.scenario)  # type: ignore


class LazyRerunner(PluginConfig):
    plugin = LazyRerunnerPlugin
    description = "Reruns failed scenarios until the first pass otherwise the specified number of times"
