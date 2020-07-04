class Statistics:
    """Provide a statistics keeper and provider"""
    def __init__(self):
        self.Susceptible = 0
        self.Infected = 0
        self.Recovered = 0
        self.Dead = 0

        self.Hospitalised = 0