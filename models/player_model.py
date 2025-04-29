class Player:
    def __init__(self, name, minutes, goals, assists):
        self.name = name
        self.minutes = minutes
        self.goals = goals
        self.assists = assists

    def goals_per_90(self):
        return (self.goals / self.minutes) * 90 if self.minutes else 0

    def involvement(self):
        return self.goals + self.assists
