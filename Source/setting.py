class Setting:
    """Provide the simulation setting keeper"""
    def __init__(self, **kwargs) -> None:
        # Pre-set keys
        self.Population: int = None
        self.ZeroPatient: int = None
        self.BaseInfectionRate: float = None
        self.BaseAlpha: float = None
        self.MASK: float = None
        self.HYGIENE: float = None
        self.GROUP: int = None

        # Set keys
        for key in kwargs:
            setattr(self, key, kwargs[key])

        self.CheckSimulationSettings()
        self.CheckScenerioSettings()
        self.ReloadAdaptiveInfectionRate()

    def CheckSimulationSettings(self):
        """Check for compulsory keys

        Raises:
            NameError: One (or more) of the keys is not available
        """

        # The set of compulsory keys
        compulsory_key = (
            "Population",           # Simulation population
            "ZeroPatient",          # Number of Patient Zero, i.e. initial number of infected people
            "BaseInfectionRate",    # Basic infection rate (one susceptible near one infected, per hour)           
        )

        # Iterate through every compulsory keys
        for key in compulsory_key:
            # Check for non-None key
            if getattr(self, key) != None:
                continue
            # Raise NameError on non-existing keys
            raise NameError(f"'{key}' is a required parameter but not found")

        return

    def CheckScenerioSettings(self):
        """Check for compulsory scenerio keys

        Raises:
            NameError: One (or more) of the keys is not available
        """

        # The set of compulsory keys
        compulsory_key = (
            "BaseAlpha",            # Infection rate modifier
            "MASK",                 # Percentage of population wearing masks
            "HYGIENE",              # Percentage of population with good personal hygiene
            "DISTANCING",           # Percentage of population practising social distancing
            "GROUP",                # Maximum number of people with close contact
        )

        # Iterate through every compulsory keys
        for key in compulsory_key:
            # Check for non-None key
            if getattr(self, key) != None:
                continue
            # Raise NameError on non-existing keys
            raise NameError(f"'{key}' is a required parameter but not found")

        # Set initial adaptive alpha
        self.Alpha = self.BaseAlpha

        return
        
    def CalculateAlpha(self):
        """Calculate adaptive alpha value on-demand"""

        # Adaptive alpha = Base Alpha * Mask modifer * Hygiene modifie * Distancing modifier
        self.Alpha = self.BaseAlpha
        self.Alpha *= (1 - self.MASK * 0.3)
        self.Alpha *= (1 - self.HYGIENE * 0.8)
        self.Alpha *= (1 - self.DISTANCING * 0.7)

        return

    def ReloadAdaptiveInfectionRate(self):
        """Recalculate adaptive infection rate function"""

        self.CalculateAlpha()

        # Set aliases
        x, y = self.BaseInfectionRate, self.Alpha

        # Define lambda
        self.AdaptiveInfectionRate = lambda n: x+(1-x)*(1-1/(1+y*(n-1)))

        return
  
class ParameterProvider:
    """Provides some default scenerio presets"""
    
    # Normal condition, without any uncontrolled diseases
    NORMAL = {
        "Population": 100000,
        "ZeroPatient": 1,
        "BaseInfectionRate": 0.05,
        "BaseAlpha": 0.01,
        "MASK": 0,
        "HYGIENE": 0.8,
        "DISTANCING": 0,
        "GROUP": 20,
    }

    # During a pandemic, but no safety measures in place
    FREE_PANDEMIC = {
        "Population": 100000,
        "ZeroPatient": 4,
        "BaseInfectionRate": 0.05,
        "BaseAlpha": 0.01,
        "MASK": 0.2,
        "HYGIENE": 0.9,
        "DISTANCING": 0.1,
        "GROUP": 20,
    }

    # During a pandemic, multiple safety measures in place
    FORCED_PANDEMIC = {
        "Population": 100000,
        "ZeroPatient": 10,
        "BaseInfectionRate": 0.01,
        "BaseAlpha": 0.01,
        "MASK": 1,
        "HYGIENE": 0.9,
        "DISTANCING": 0.7,
        "GROUP": 5,
    }