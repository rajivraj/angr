
from .base import SimSootExpr

class SimSootExpr_ThisRef(SimSootExpr):
    def __init__(self, expr, state):
        super(SimSootExpr_ThisRef, self).__init__(expr, state)

    def _execute(self):
        # Parse the expr to get a SimSootValue_ParamRef instance
        ref = self._translate_value(self.expr)
        self.expr = self.state.memory.load(ref)

