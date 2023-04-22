from data.load_profiles import PV_GENERATION

class SolarFarm:
    def __init__(self, max_power) -> None:
        self.max_power = max_power
        self.P = self.max_power
        self.power_reduction = 0.0

    def step(self, time: int) -> None:
        try:
            generation = PV_GENERATION[time] * self.max_power
        except IndexError:
            print(f"The time must be in the range of [, {len(PV_GENERATION)-1}]. Time passed was {time}.")
            
        self.P = generation - self.power_reduction