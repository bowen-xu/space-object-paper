from nal.truth import TruthValue as Truth
from nal.budget import BudgetValue as Budget
from .Location import Location
import random

class Mirror:
    truth: Truth
    anticipation: Truth
    budget: Budget
    location: Location
    novelty: float = 0.5
    matched_value: float = 0.0
    reward: float = 0.0
    def __init__(self, location) -> None:
        self.truth = Truth(0.0, 0.0)
        self.anticipation = Truth(0.0, 0.0)
        self.budget = Budget(0.1*random.random(), 0.0, 0.0)
        self.location = location
    
class Task:
    mirrors: list[Mirror]
    gaze_point: Location
    budget: Budget
    novelty: float = 0.5
    reward: float = 0.0
    def __init__(self, mirrors: list[Mirror], gaze_point: Location) -> None:
        self.truth = Truth(0.0, 0.0)
        self.budget = Budget(0.1*random.random(), 0.0, 0.0)
        self.mirrors = mirrors
        self.gaze_point = gaze_point

class Prototype:
    tasks: list[Task]
    scale: float
    def __init__(self, tasks: list[Task], scale: float) -> None:
        self.tasks = tasks
        self.scale = scale