from unittest.mock import Mock, call

import pytest
from baby_steps import given, then, when
from pytest import raises
from vedro.core import Dispatcher
from vedro.events import ScenarioFailedEvent, ScenarioPassedEvent, ScenarioSkippedEvent

from ._utils import (
    dispatcher,
    fire_arg_parsed_event,
    fire_failed_event,
    fire_startup_event,
    make_scenario_result,
    rerunner,
    scheduler_,
)

__all__ = ("rerunner", "scheduler_", "dispatcher")  # fixtures


@pytest.mark.asyncio
@pytest.mark.usefixtures(rerunner.__name__)
async def test_rerun_validation(dispatcher: Dispatcher):
    with when, raises(BaseException) as exc_info:
        await fire_arg_parsed_event(dispatcher, lazy_reruns=-1)

    with then:
        assert exc_info.type is ValueError
        assert str(exc_info.value) == "--lazy-reruns must be >= 0"


@pytest.mark.asyncio
@pytest.mark.parametrize("lazy_reruns", [0, 1, 3])
@pytest.mark.usefixtures(rerunner.__name__)
async def test_rerun_failed(lazy_reruns: int, *, dispatcher: Dispatcher, scheduler_: Mock):
    with given:
        await fire_arg_parsed_event(dispatcher, lazy_reruns)
        await fire_startup_event(dispatcher, scheduler_)

        scenario_result = make_scenario_result().mark_failed()
        scenario_failed_event = ScenarioFailedEvent(scenario_result)

    with when:
        await dispatcher.fire(scenario_failed_event)

    with then:
        assert scheduler_.mock_calls == [call.schedule(scenario_result.scenario)] * 0 if not lazy_reruns else 1


@pytest.mark.asyncio
@pytest.mark.parametrize("reruns", [0, 1, 3])
@pytest.mark.usefixtures(rerunner.__name__)
async def test_dont_rerun_passed(reruns: int, *, dispatcher: Dispatcher, scheduler_: Mock):
    with given:
        await fire_arg_parsed_event(dispatcher, reruns)
        await fire_startup_event(dispatcher, scheduler_)

        scenario_result = make_scenario_result().mark_passed()
        scenario_passed_event = ScenarioPassedEvent(scenario_result)

    with when:
        await dispatcher.fire(scenario_passed_event)

    with then:
        assert scheduler_.mock_calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize("repeats", [0, 1, 3])
@pytest.mark.usefixtures(rerunner.__name__)
async def test_dont_repeat_skipped(repeats: int, *, dispatcher: Dispatcher, scheduler_: Mock):
    with given:
        await fire_arg_parsed_event(dispatcher, repeats)
        await fire_startup_event(dispatcher, scheduler_)

        scenario_result = make_scenario_result().mark_skipped()
        scenario_skipped_event = ScenarioSkippedEvent(scenario_result)

    with when:
        await dispatcher.fire(scenario_skipped_event)

    with then:
        assert scheduler_.mock_calls == []


@pytest.mark.asyncio
@pytest.mark.usefixtures(rerunner.__name__)
async def test_rerun_rerunned(dispatcher: Dispatcher, scheduler_: Mock):
    with given:
        await fire_arg_parsed_event(dispatcher, lazy_reruns=3)
        await fire_startup_event(dispatcher, scheduler_)

        scenario_result = make_scenario_result()
        scenario_failed_event = await fire_failed_event(scenario_result, dispatcher)
        scheduler_.reset_mock()

    with when:
        await dispatcher.fire(scenario_failed_event)

    with then:
        assert scheduler_.mock_calls == [call.schedule(scenario_result.scenario)]


@pytest.mark.asyncio
@pytest.mark.usefixtures(rerunner.__name__)
async def test_dont_rerun_more_than_specified_in_argument(dispatcher: Dispatcher, scheduler_: Mock):
    with given:
        await fire_arg_parsed_event(dispatcher, lazy_reruns=1)
        await fire_startup_event(dispatcher, scheduler_)

        scenario_result = make_scenario_result()
        scenario_failed_event = await fire_failed_event(scenario_result, dispatcher)
        scheduler_.reset_mock()

    with when:
        await dispatcher.fire(scenario_failed_event)

    with then:
        assert scheduler_.mock_calls == []
