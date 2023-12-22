import cplex

cpx = cplex.Cplex()
cpx.parameters.threads.set(1)
cpx.objective.set_sense(cpx.objective.sense.maximize)

I_n = 3
J_n = 4
sallary = [
    [10, 12, 13, 9],
    [5, 6, 3, 8],
    [4, 1, 8, 9],
]

# adding variables
for i in range(I_n):
    for j in range(J_n):
        # obj is the coef in the objective function
        cpx.variables.add(obj = [sallary[i][j]], types=[cpx.variables.type.binary], names=[f"X{i}{j}"])

# adding constrains
#lin_expr = cplex.SparsePair(ind = ["X00", "X01", "X02", "X03"], val = [1, 1, 1, 1])
#cpx.linear_constraints.add(lin_expr = [lin_expr], senses=["L"], rhs = [1])


