from nal.truth import TruthValue as Truth
from nal.budget import BudgetValue as Budget

from .Position import Position
from .DataStructures import Task, Mirror, Prototype
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from typing import Callable
import random
from .reward_function import reward
from nal.ExtendedBooleanFunctions import Or

seed = 42
np.random.seed(seed)
random.seed(seed)

SCALE = 10
DURATION = 5
DISTURB = 0.2
DURATION_BUDGET = DURATION  # 10
RADIUS = 0.3

a1 = 0.8 # mirror priority inhibition
a2_exh = 2 # task priority exhibition
a2_inh = 2 # task priority inhibition

def create_prototype(locations: list[tuple[float, float]], scale=10, radius=0.3):
    """
    Suppose all features are the same
    """
    locations = [(loc[0]/scale, loc[1]/scale) for loc in locations]
    
    curr_loc = Position(locations[0])
    tasks = OrderedDict()
    for loc in locations:
        dx, dy = curr_loc - Position(loc)
        # loc_task = locations[0]
        for loc_task in locations:
            task = Task([Mirror(Position(loc)) for loc in locations], Position((loc_task)))
            task.gaze_point.move(dx, dy) 
            x, y = task.gaze_point.center
            tasks[f"{x:.3f}, {y:.3f}"] = task

            task.budget.d = 1-Budget.get_decay_factor(DURATION_BUDGET)
            for mirror in task.mirrors:
                mirror.position.radius = radius/scale
                mirror.position.sharpness = mirror.position.radius*20*5
                mirror.budget.d = 1-Budget.get_decay_factor(DURATION_BUDGET)
    return Prototype(list(tasks.values()), scale), curr_loc

def take(proto: Prototype):
    task: Task = max(proto.tasks, key =lambda task: task.budget.p)
    mirror: Mirror = max(task.mirrors, key = lambda mirror: mirror.budget.p)
    return task, mirror

def move(proto: Prototype, dx, dy):
    for task in proto.tasks:
        task.gaze_point.move(dx, dy)

def decay_truth(proto: Prototype, ts_now: int, duration: int):
    alpha = Truth.get_decay_factor(duration)
    for task in proto.tasks:
        for mirror in task.mirrors:
            mirror.truth.decay(alpha, ts_now)
            mirror.anticipation.decay(alpha, ts_now)

def decay_budget(proto: Prototype, ts_now: int):
    for task in proto.tasks:
        task.budget.decay(ts_now)
        for mirror in task.mirrors:
            mirror.budget.decay(ts_now)

def update_task(task: Task, gazed_mirror: Mirror, feat_locs: list[tuple[float, float]], ts_now):
    for mirror in task.mirrors:
        mirror.novelty = None
        mirror.matched_value = None
        if gazed_mirror == mirror: # only if the mirror is gazed, the anticipated truth should be considered
            # 1. revise the truth of the mirror
            if len(feat_locs) > 0:
                closeness = max([mirror.position.match(feat_loc) for feat_loc in feat_locs]) # closeness between the feature and the mirror
                # truth_observed = Truth.from_w(closeness**2, closeness, 1)
                truth_observed = Truth(closeness, min(closeness, 0.75), 1)
            else:
                closeness = 0
                truth_observed = Truth(0.0, 0.0, 1)
            truth_observed.ts_update = ts_now

            truth_anticipated = mirror.anticipation
            # 1.1. temporal projection
            # 1.2. compute truth through induction function
            # 1.3. revision
            truth_anticipated.projection(ts_now, DURATION)

            s = abs(truth_anticipated.e - truth_observed.e)
            w = Or(s, abs(truth_anticipated.e-0.5))
            w_p = truth_observed.f*w
            truth_observed.revise_w(w_p, w, ts_now)
            # 1.4 reset the anticipation
            mirror.anticipation.reset(0.0, 0.0)
            # 2. inhibit the priority of the gazed mirror
            mirror.budget.inhibit_p(a1, stubbornness=0.9)
            # 3. novelty and matched value
            mirror.novelty = abs(truth_observed.e - mirror.truth.e)
            mirror.matched_value = (truth_observed.e - 0.5)
            # 4. task reward & priority
            task.reward = reward(mirror.matched_value, mirror.novelty)
            if task.reward > 0:
                task.budget.exhibit_p(abs(a2_exh*task.reward))
            else:
                task.budget.inhibit_p(abs(a2_inh*task.reward))

            mirror.truth.revise(truth_observed, ts_now, DURATION)
        else:
            # ??? What should be done if the mirror is not a gazed one?
            # mirror.truth.revise(truth_observed, ts_now, DURATION)
            # To be considered
            pass

def update_proto(proto: Prototype, gazed_mirror: Mirror, feat_locs: list[tuple[float, float]], ts_now):
    for task in proto.tasks:
        update_task(task, gazed_mirror, feat_locs, ts_now)

