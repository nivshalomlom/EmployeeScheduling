from ortools.sat.python.cp_model import CpSolverSolutionCallback, IntVar
from typing import TypeVar, Generic, List, Dict, Tuple
from abc import ABC
from scheduler import SchedulerConfig

T = TypeVar('T')

class SchedulerSoultionCallback(ABC, CpSolverSolutionCallback, Generic[T]):
    
    def __init__(self):
        super().__init__()
        
    def SetModelData(self, shifts: Dict[Tuple[int, int, int], IntVar], config: SchedulerConfig, workers: List[T]):
        self._config = config
        self._workers = workers
        self._shifts = shifts
