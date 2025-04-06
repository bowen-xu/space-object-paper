from nal.truth import TruthValue
from .link import Link
from ordered_set import OrderedSet

class Node:
    def __init__(self):
        self.lower_links = OrderedSet[Link]()
        self.higher_links = OrderedSet[Link]()
        self.truth_value = TruthValue(0.0, 0.0, 1.0)
        self.truth_value_back = TruthValue(0.0, 0.0, 1.0)
    
    def connect_to(self, other: 'Node'):
        link = Link(self, other)
        self.higher_links.add(link)
        other.lower_links.add(link)
