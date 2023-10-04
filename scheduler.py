from ortools.sat.python.cp_model import CpModel, CpSolver, CpSolverSolutionCallback, IntVar
from typing import TypeVar, Generic, List, Dict, Tuple, Callable
from scheduler_soultion_callback import SchedulerSoultionCallback

T = TypeVar('T')
ShiftFilter = Callable[[Tuple[int, int, int], T], bool]
ShiftConstraint = Callable[[List[IntVar]], bool]

class SchedulerConfig:
    
    def __init__(self, numWorkDays: int, shiftsPerDay: int, workersPerShift: int):
        self.numWorkDays = numWorkDays
        self.shiftsPerDay = shiftsPerDay
        self.workersPerShift = workersPerShift

class Scheduler(Generic[T]):
    
    def __init__(self, config: SchedulerConfig, workers: List[T]):
        self._model = CpModel()
        self._config = config
        self._workers = workers
        self._shifts = self._GenerateShifts()
        self._AddGlobalConstaints()
        
    def AddConstraint(self, shiftFilter: ShiftFilter[T], constraint: ShiftConstraint):
        shifts = [
            self._shifts[shift] 
                for shift in self._shifts 
                if shiftFilter(shift, self._workers[shift[0]])
        ]
        
        self._model.Add(constraint(shifts))
        
    def AddWorkerConstaint(self, constraint: ShiftConstraint):
        [
            self.AddConstraint(
                lambda shift_id, _: w == shift_id[0], 
                constraint
            )
                for w in range(len(self._workers))
        ]
        
    def AddDayConstaint(self, constraint: ShiftConstraint):
        [
            self.AddConstraint(
                lambda shift_id, _: d == shift_id[1], 
                constraint
            )
                for d in range(self._config.numWorkDays)
        ]
        
    def AddShiftConstaint(self, constraint: ShiftConstraint):
        [
            self.AddConstraint(
                lambda shift_id, _: d == shift_id[1] and s == shift_id[2], 
                constraint
            )
                for d in range(self._config.numWorkDays)
                for s in range(self._config.shiftsPerDay)
        ]
        
    def Solve(self, soultionCallback: SchedulerSoultionCallback[T], parameters: Dict[str, any] = {}):
        soultionCallback.SetModelData(
            self._shifts,
            self._config, 
            self._workers
        )
        
        solver = CpSolver()
        solver.parameters |= parameters
        solver.Solve(self._model, soultionCallback)

    def _GenerateShifts(self):
        return {
            (w, d, s): self._model.NewBoolVar(f"shift_w{w}_d{d}_s{s}")
                for w in range(len(self._workers))
                for d in range(self._config.numWorkDays)
                for s in range(self._config.shiftsPerDay)
        }
        
    def _AddGlobalConstaints(self):
        self.AddShiftConstaint(lambda shifts: sum(shifts) == self._config.workersPerShift)
