from ortools.sat.python import cp_model
from empolyee import Employee, Gender
from soultion_callback import WorkerPartialSolutionPrinter

model = cp_model.CpModel()
workDays = range(5)
shiftsPerDay = range(3)

workers = [
    Employee('Niv', Gender.Male),
    Employee('Ron', Gender.Male),
    Employee('Naomi', Gender.Female)
]

# Create shifts

shifts = {}
for (w, _) in enumerate(workers):
    for d in workDays:
        for s in shiftsPerDay:
            shifts[(w, d, s)] = model.NewBoolVar(f"shift_n{w}_d{d}_s{s}")

# Each shift contains one nurse

for d in workDays:
    for s in shiftsPerDay:
        model.AddExactlyOne(shifts[(w, d, s)] for (w, _) in enumerate(workers))

# Divide shifts evenly if possiable

minShiftsPerWeek = len(shiftsPerDay) * len(workDays) // len(workers)
maxShiftsPerWeek = minShiftsPerWeek + minShiftsPerWeek % len(workers)

for (i, w) in enumerate(workers):
    shiftsWorked = []
    
    for d in workDays:
        for s in shiftsPerDay:
            shiftsWorked.append(shifts[(i, d, s)])
    
    numShiftsWorked = sum(shiftsWorked)
    model.Add(numShiftsWorked <= maxShiftsPerWeek)
    model.Add(numShiftsWorked >= minShiftsPerWeek)

# Solution printer

soultionPrinter = WorkerPartialSolutionPrinter(
    shifts, len(workers), len(workDays), len(shiftsPerDay), 5
)

# Solve model

solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
solver.parameters.enumerate_all_solutions = True
solver.Solve(model, soultionPrinter)