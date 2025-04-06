from nal.truth import TruthValue
from .node import *

class Link:
    def __init__(self, lower_node: 'Node', higher_node: 'Node', ):
        self.higher_node = higher_node
        self.lower_node = lower_node
        self.truth_value = TruthValue(0.0, 0.0, 1.0)
