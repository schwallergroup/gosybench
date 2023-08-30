"""Build and operate on trees of synthetic procedures."""


from .document import SynthDocument


class SynthTree(SynthDocument):
    def __init__(self):
        super(SynthTree, self).__init__()

    # TODO extend functionality for trees. merge, network, etc
