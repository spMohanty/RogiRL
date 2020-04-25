from rogi_rl.agent import DiseaseSimAgent
from rogi_rl.model import DiseaseSimModel


def test_prob_movement_0():
    """
    Tests that prob_agent_movement works as
    expected when set to 0.

    Setting it to 0, should forbid movement
    """
    # Initialize a model with a single agent
    model = DiseaseSimModel(
        width=50,
        height=50,
        population_density=1.0/50
    )

    unique_id = "uid"
    agent = DiseaseSimAgent(
                unique_id,
                model,
                prob_agent_movement=0.0,
                moore=True
    )
    agent.pos = (0, 0)
    for k in range(100):
        agent.random_move()
        assert agent.pos == (0, 0)


def test_prob_movement_1():
    """
    Tests that prob_agent_movement works as
    expected when set to 1.

    Setting it to 1, should guarantee movement
        (if relevant cells exist)
    """
    # Initialize a model with a single agent
    model = DiseaseSimModel(
        width=50,
        height=50,
        population_density=1.0/50
    )

    unique_id = "uid"
    agent = DiseaseSimAgent(
                unique_id,
                model,
                prob_agent_movement=1.0,
                moore=True
    )
    agent.pos = (0, 0)
    for k in range(100):
        previous_position = agent.pos
        agent.random_move()
        assert agent.pos != previous_position
