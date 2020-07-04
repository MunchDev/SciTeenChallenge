from objects import *
from setting import *
from statistics import *
from typing import List
import random as rd

class Simulation:
    def __init__(self, setting: Setting, statistics: Statistics):
        self.Setting = setting
        self.Statistics = statistics
        Person.DataProvider = self.Statistics
        Person.DataProvider.Susceptible = self.Setting.Population

        self.Everyone: List[Person] = []
        self.Places: List[Entity] = []

    def Run(self):
        # Alias for population
        pop = self.Setting.Population

        # Add a number of people
        for i in range(pop):
            self.Everyone.append(Person())

        # Calculate the number of entity needed to accommodate everyone
        # Add 1 if not enough (due to flooring of 'int')
        ent = int(pop / self.Setting.GROUP)
        if self.Setting.GROUP * ent < pop:
            ent += 1

        # Add a number of entities
        for i in range(ent):
            self.Places.append(Entity(self.Setting))

        # Create patient zero
        for i in range(self.Setting.ZeroPatient):
            self.Everyone[i].State = "Infected"
            self.Everyone[i].NoOfDaysInfected = 0
            self.Statistics.Infected += 1
            self.Statistics.Susceptible -= 1

        # Initial assignment
        self.MixPopulation()

        while self.Statistics.Infected != 0:
            for hour in range(24):
                for ent in self.Places:
                    ent.Run(hour)
            self.MixPopulation()
            print(self.Statistics.Susceptible, self.Statistics.Infected, self.Statistics.Recovered, self.Statistics.Dead)

    def MixPopulation(self):
        # Random order distribution of population
        randomOrder = list(range(len(self.Everyone)))
        rd.shuffle(randomOrder)

        count = 0
        # Iterate over each entity
        for ent in self.Places:
            # Remove existings occupants
            ent.Empty()

            # Add people
            for i in range(self.Setting.GROUP):
                ent.Assign(self.Everyone[randomOrder[count]])
                count += 1

        return