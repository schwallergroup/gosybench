"""Build and operate on trees of synthetic procedures."""


from .document import SynthDocument


class SynthTree(SynthDocument):
    """extend synthdoc to represent reaction tree"""

    def __init__(self):
        """init"""
        super(SynthTree, self).__init__()

    # TODO extend functionality for trees. merge, network, etc
