from ortools.sat.python import cp_model
from typing import TypeVar, Generic

T = TypeVar('T');

class ConstaintScheduler(Generic(T)):
    
    def __init__(self, workers: list[T], numWorkDays: int, shiftsPerDay: int):
        self._model = cp_model.CpModel()
        self._numWorkDays = numWorkDays
        self._shiftsPerDay = shiftsPerDay
        
        self._blockedShifts = set()
        self._InitializeShifts(workers, numWorkDays, shiftsPerDay)
                
    def SetNumShiftWorkers(self, day: int, shift: int, numWorkers: int):
        self._workersPerShift[(day, shift)] = numWorkers
      
    def _ShiftValid(self, worker: int, day: int, shift: int):
        return (worker, day, shift) not in self._blockedShifts
        
    def _InitializeShifts(self, workers: list[T]):
        self._shifts = {}
        self._workersPerShift = {}
        
        for d in range(0, self._numWorkDays):
            for s in range(0, self._shiftsPerDay):
                self._workersPerShift[(d, s)] = 1
                shiftWorkers = []
                
                for (i, _) in enumerate(workers):
                    self._shifts[(i, d, s)] = self._model.NewBoolVar(f"shift_n{i}_d{d}_s{s}")
                    shiftWorkers.append(self._shifts[(i, d, s)])
                    
                    # A worker should work a shift only if he is able to
                    self._model.Add(self._ShiftValid(i, d, s))
                
                # The amount of workers in a shift should be the required amount
                self._model.Add(sum(shiftWorkers) == self._workersPerShift[(d, s)])