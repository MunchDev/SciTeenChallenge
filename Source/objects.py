import random as rd
from setting import Setting
from statistics import Statistics
from typing import Optional, List

class Person:
    """Represents each individual of the simulation"""
    DataProvider: Optional[Statistics] = None
    FatalityChance: float = 0.04

    def __init__(self, statistics = None):
        if statistics:
            Person.DataProvider = statistics

        self.State = "Susceptible"
        self.NoOfDaysInfected: Optional[int] = None
        self.IsHospitalised: Optional[bool] = None
        self.Infectious: Optional[bool] = None

        self.Thresholds = {
            "BeforeInfectious": rd.randint(5, 6),
            "BeforeHospitalised": rd.randint(6, 8),
            "BeforeRecoveredOrDead": rd.randint(18, 24),
        }

    def Run(self):
        """Calculate disease outcome at the begining of the day

        Args:
            currentTime (int): The hour of the day (24-hour scale)
        """

        # Infected for 28 days -> Die or recover
        if self.IsHospitalised and self.NoOfDaysInfected == self.Thresholds["BeforeRecoveredOrDead"]:
            self.NoOfDaysInfected = None
            self.IsHospitalised = None
            Person.DataProvider.Hospitalised -= 1
            Person.DataProvider.Infected -= 1
            if rd.random() <= Person.FatalityChance:           
                Person.DataProvider.Dead += 1
                self.State = "Dead"              
            else:
                Person.DataProvider.Recovered += 1
                self.State = "Recovered"

        # While hospitalising
        elif self.IsHospitalised:
            self.NoOfDaysInfected += 1
        
        elif self.State == "Infected":
            # Infected for 5 days (incubation)
            if self.NoOfDaysInfected == self.Thresholds["BeforeInfectious"]:
                self.Infectious = True

            # Infected for 11 days -> Hospitalise
            elif self.NoOfDaysInfected == self.Thresholds["BeforeHospitalised"]:
                Person.DataProvider.Hospitalised += 1
                self.IsHospitalised = True
                self.Infectious = False
            self.NoOfDaysInfected += 1
            
        return

class Entity:
    """Represents each entity (place, destination)"""
    def __init__(self, setting: Setting):
        self.Setting = setting

        self.Occupants: List[Person] = []
        self.RealInfectionRate: float = 0
        
    def Assign(self, person):
        """Assign a person to this entity

        Args:
            person (Person): A lay person
        """
        self.Occupants.append(person)

        return
    
    def Empty(self):
        self.Occupants = []

    def Run(self, currentTime):
        """Run simulation at this entity for all occupants"""

        # Calculate real infection rate at the beginning of the day
        if currentTime == 0:
            # Reload adaptive infection rate calculation
            self.Setting.ReloadAdaptiveInfectionRate()

            # Get the number of infected occupants
            # Using list comprehension, check for state "Infected" -> Iterators of (True, False, ...)
            # Using sum to count the number of True: int(True) == 1, int(False) == 0
            self.NoOfInfected: int = sum(person.Infectious == True for person in self.Occupants)

            if self.NoOfInfected > 0:
                # Calculate real infection rate based on the number of infected occupants
                self.RealInfectionRate = self.Setting.AdaptiveInfectionRate(self.NoOfInfected)
            else:
                self.RealInfectionRate = 0

            for person in self.Occupants:
                person.Run()

        if self.RealInfectionRate == 0:
            return

        # Apply infection rate
        for i in range(len(self.Occupants)):
            person = self.Occupants[i]
            if person.State == "Susceptible":
                state = "Infected" if rd.random() <= self.RealInfectionRate else "Susceptible"
                if state == "Infected":
                    Person.DataProvider.Infected += 1
                    Person.DataProvider.Susceptible -= 1

                    person.NoOfDaysInfected = 0
                person.State = state
            self.Occupants[i] = person

        return