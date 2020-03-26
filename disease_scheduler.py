import numpy as np

from agent_event import AgentEvent
from agent_state import AgentState


class DiseaseSchedulerBase:
    """
    This class plans the schedule of different state transitions for a disease
    """
    def __init__(self, np_random=False):
        pass

    def get_disease_schedule(self, base_timestep=0):
        """
            Plans out the schedule of the state transitions for a 
            particular agent using a particular disease model.

            It returns a list of AgentEvent objects which have to be
            "executed" by the Agent at the right moment.
        """
        return []

class SEIRDiseaseScheduler(DiseaseSchedulerBase):
    """
    This class plans the schedule of different state transitions for a disease
    """
    def __init__(   self,
                    latent_period_mu = 2 * 4,
                    latent_period_sigma = 1 * 4,
                    incubation_period_mu = 5 * 4,
                    incubation_period_sigma = 3 * 4,
                    recovery_period_mu = 14 * 4,
                    recovery_period_sigma = 1 * 4,
                    np_random = False
                ):

        self.latent_period_mu = latent_period_mu
        self.latent_period_sigma = latent_period_sigma
        self.incubation_period_mu = incubation_period_mu
        self.incubation_period_sigma = incubation_period_sigma
        self.recovery_period_mu = recovery_period_mu
        self.recovery_period_sigma = recovery_period_sigma

        self.np_random = np_random
        if not self.np_random:
            self.np_random = np.random

    def get_disease_schedule(self, base_timestep=0):
        """
            Plans out the schedule of the state transitions for a 
            particular agent using a particular disease model.

            It returns a list of AgentEvent objects which have to be
            "executed" by the Agent at the right moment.
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
            latent_period = np.around(self.np_random.normal(self.latent_period_mu, self.latent_period_sigma))
            if latent_period >= 0 :
                break
            print(latent_period)
        
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
            incubation_period = np.around(self.np_random.normal(self.incubation_period_mu, self.incubation_period_sigma))
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
            recovery_period = np.around(self.np_random.normal(self.recovery_period_mu, self.recovery_period_sigma))
            if recovery_period > incubation_period:
                break

        #############################################
        #############################################
        # 
        # Build AgentEvents
        #
        #############################################
        #############################################
        disease_schedule = []

        # Susceptible -> Exposed | Now
        timestep = base_timestep
        _event = AgentEvent(
            previous_state=AgentState.SUSCEPTIBLE,
            new_state=AgentState.EXPOSED,
            update_timestep=timestep
        )
        disease_schedule.append(_event)

        # Exposed -> Infectious | Now + latent_period
        timestep = base_timestep + latent_period
        _event = AgentEvent(
            previous_state=AgentState.EXPOSED,
            new_state=AgentState.INFECTIOUS,
            update_timestep=timestep
        )
        disease_schedule.append(_event)

        # Infectious -> Symptomatic | Now + incubation_period
        timestep = base_timestep + incubation_period
        _event = AgentEvent(
            previous_state=AgentState.INFECTIOUS,
            new_state=AgentState.SYMPTOMATIC,
            update_timestep=timestep
        )
        disease_schedule.append(_event)

        # Symptomatic -> Recovered | Now + recovery_period
        timestep = base_timestep + recovery_period
        _event = AgentEvent(
            previous_state=AgentState.SYMPTOMATIC,
            new_state=AgentState.RECOVERED,
            update_timestep=timestep
        )
        disease_schedule.append(_event)

        return disease_schedule


class SimpleSEIRDiseaseScheduler(SEIRDiseaseScheduler):
    """
    This class plans the schedule of different state transitions for a disease
    """
    def __init__(   self,
                    latent_period = 2 * 4,
                    incubation_period = 5 * 4,
                    recovery_period = 14 * 4,
                    np_random = False
                ):
        self.latent_period_mu = latent_period
        self.latent_period_sigma = 0

        self.incubation_period_mu = incubation_period
        self.incubation_period_sigma = 0

        self.recovery_period_mu = recovery_period
        self.recovery_period_sigma = 0

        self.np_random = np_random
        if not self.np_random:
            self.np_random = np.random


if __name__ == "__main__":
    disease_scheduler = SEIRDiseaseScheduler()
    disease_scheduler = SimpleSEIRDiseaseScheduler()
    for k in range(100):
        print(disease_scheduler.get_disease_schedule())