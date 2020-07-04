from simulation import Simulation
from setting import *
from statistics import *

if __name__ == "__main__":
    params = ParameterProvider.NORMAL

    sim = Simulation(
        Setting(**params),
        Statistics(),
    )

    sim.Run()