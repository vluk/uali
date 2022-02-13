from game import Game
from policy import Policy


class MCTS():
    def __init__(self):
        pass

    def select(self):
        pass

    def expand(self, leaf):
        child = leaf.random_child()
        return child

    def simulate(self, child):
        node = child
        while not Game.game_over(node):
            action = Policy.get_action(node)
            new_child = Game.apply(node.state, action)
            node.add_child(new_child)
            node = new_child

    def backprop(self, child, result):
        node = child
        while node.parent:
            node.parent.update(result)

    def run(self):
        leaf = self.select()
        child = self.expand(leaf)
        result = self.simulate(child)
        self.backprop(child, result)
