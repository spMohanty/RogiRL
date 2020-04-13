from rogi_rl.agent_state import AgentState
from enum import Enum


def test_agent_state_type():
    """
    Ensures that the AgentState is always an Enum
    """
    assert type(AgentState) == type(Enum)


def test_agent_state():
    """
    Tests and ensure that all the states in the AgentState class
    are expected classes.
    """

    EXPECTED_STATE_NAMES = [
        "SUSCEPTIBLE",
        "EXPOSED",
        "INFECTIOUS",
        "SYMPTOMATIC",
        "RECOVERED",
        "VACCINATED"
    ]

    AVAILABLE_STATES = []
    # Check if all states in AgentState are known states
    for _state in AgentState:
        assert _state.name in EXPECTED_STATE_NAMES
        AVAILABLE_STATES.append(_state.name)

    # Check if all states in the EXPECTED_state names are
    # present in the AgentState
    for _state_name in EXPECTED_STATE_NAMES:
        assert _state_name in AVAILABLE_STATES
