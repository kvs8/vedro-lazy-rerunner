from typing import List

from vedro.core import AggregatedResult, MonotonicScenarioScheduler, ScenarioResult


class LazyScenarioScheduler(MonotonicScenarioScheduler):
    def aggregate_results(self, scenario_results: List[ScenarioResult]) -> AggregatedResult:
        assert len(scenario_results) > 0

        for scenario_result in scenario_results:
            if scenario_result.is_passed():
                return AggregatedResult.from_existing(scenario_result, scenario_results)

        return AggregatedResult.from_existing(scenario_results[-1], scenario_results)
