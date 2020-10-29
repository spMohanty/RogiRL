from rog_rl.agent_event import AgentEvent
from rog_rl.agent_state import AgentState


class DiseasePlannerBase:
    """
    This class plans the schedule of different state transitions for a disease
    """

    def __init__(self, random=False):
        pass

    def sample_disease_progression(self):
        pass

    def get_disease_plan(self, base_timestep=0):
        """
            Plans out the schedule of the state transitions for a
            particular agent using a particular disease model.

            It returns a list of AgentEvent objects which have to be
            "executed" by the Agent at the right moment.
        """
        return []


class SEIRDiseasePlanner(DiseasePlannerBase):
    """
    This class plans the schedule of different state transitions for a disease
    """

    def __init__(self,
                 latent_period_mu=2 * 4,
                 latent_period_sigma=1 * 4,
                 incubation_period_mu=5 * 4,
                 incubation_period_sigma=3 * 4,
                 recovery_period_mu=14 * 4,
                 recovery_period_sigma=1 * 4,
                 random=False
                 ):

        self.latent_period_mu = latent_period_mu
        self.latent_period_sigma = latent_period_sigma
        self.incubation_period_mu = incubation_period_mu
        self.incubation_period_sigma = incubation_period_sigma
        self.recovery_period_mu = recovery_period_mu
        self.recovery_period_sigma = recovery_period_sigma

        variable_list = [
            latent_period_mu,
            incubation_period_mu,
            recovery_period_mu]
        assert latent_period_mu != incubation_period_mu, \
            "latent_period_mu cannot be equal to incubation_period_mu"
        assert incubation_period_mu != recovery_period_mu, \
            "incubation_period_mu cannot be equal to recovery_period_mu"

        if not(variable_list == sorted(variable_list)):
            """
            Cases arises when the provided latent, incubation and
            recovery period are not in increasing order.
            """
            raise Exception(
                "Invalid Values Provided to Disease Planner."
                "Expected : Latent Period < Incubation Period < Recover Period"
            )

        self.random = random
        if not self.random:
            import random
            self.random = random

    def get_disease_plan(self, base_timestep=0):
        """
        It returns a list of AgentEvent objects which have to be
        "executed" by the Agent at the right moment.
        """
        disease_progression = self.sample_disease_progression()
        return self.build_disease_plan(
            disease_progression,
            base_timestep
        )

    def sample_disease_progression(self):
        """
            Plans out the schedule of the state transitions for a
            particular agent using a particular disease model.
        """

        # Case when the patient gets an infection

        #############################################
        #############################################
        # Compute Latent Period
        # - Conditions :
        #  - Latent Period has to be >= 0.
        #############################################
        #############################################
        latent_period = -1
        while True:
            latent_period = round(self.random.normalvariate(
                self.latent_period_mu, self.latent_period_sigma))
            if latent_period >= 0:
                break

        #############################################
        #############################################
        # Compute Incubation Period
        #
        # - Conditions :
        #  - Incubation Period has to be greater than
        #    the latent period.
        #############################################
        #############################################
        incubation_period = -1
        while True:
            incubation_period = round(self.random.normalvariate(
                self.incubation_period_mu, self.incubation_period_sigma))
            if incubation_period > latent_period:
                break

        #############################################
        #############################################
        # Compute Recovery Period
        #
        # - Conditions :
        #  - Recovery Period has to be greater than
        #    the Incubation period.
        #############################################
        #############################################
        recovery_period = -1
        while True:
            recovery_period = round(self.random.normalvariate(
                self.recovery_period_mu, self.recovery_period_sigma))
            if recovery_period > incubation_period:
                break

        return latent_period, incubation_period, recovery_period

    def build_disease_plan(self, disease_progression, base_timestep=0):
        #############################################
        #############################################
        #
        # Build AgentEvents
        #
        #############################################
        #############################################
        latent_period, incubation_period, recovery_period = \
            self.sample_disease_progression()
        disease_plan = []

        # Susceptible -> Exposed | Now
        timestep = base_timestep
        _event = AgentEvent(
            previous_state=AgentState.SUSCEPTIBLE,
            new_state=AgentState.EXPOSED,
            update_timestep=timestep
        )
        disease_plan.append(_event)

        # Exposed -> Infectious | Now + latent_period
        timestep = base_timestep + latent_period
        _event = AgentEvent(
            previous_state=AgentState.EXPOSED,
            new_state=AgentState.INFECTIOUS,
            update_timestep=timestep
        )
        disease_plan.append(_event)

        # Infectious -> Symptomatic | Now + incubation_period
        timestep = base_timestep + incubation_period
        _event = AgentEvent(
            previous_state=AgentState.INFECTIOUS,
            new_state=AgentState.SYMPTOMATIC,
            update_timestep=timestep
        )
        disease_plan.append(_event)

        # Symptomatic -> Recovered | Now + recovery_period
        timestep = base_timestep + recovery_period
        _event = AgentEvent(
            previous_state=AgentState.SYMPTOMATIC,
            new_state=AgentState.RECOVERED,
            update_timestep=timestep
        )
        disease_plan.append(_event)

        return disease_plan


class SimpleSEIRDiseasePlanner(SEIRDiseasePlanner):
    """
    This class plans the schedule of different state transitions for a disease
    """

    def __init__(self,
                 latent_period=2 * 1,
                 incubation_period=5 * 1,
                 recovery_period=14 * 1,
                 random=False
                 ):
        self.latent_period_mu = latent_period
        self.latent_period_sigma = 0

        self.incubation_period_mu = incubation_period
        self.incubation_period_sigma = 0

        self.recovery_period_mu = recovery_period
        self.recovery_period_sigma = 0

        self.random = random
        if not self.random:
            import random
            self.random = random


if __name__ == "__main__":
    disease_scheduler = SEIRDiseasePlanner()
    disease_scheduler = SimpleSEIRDiseasePlanner()
    for k in range(100):
        print(disease_scheduler.get_disease_plan())
