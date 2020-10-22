
import Functions as ft
from docplex.mp.model import Model

def Solver_1(Regions,N,Height,Width):

    ##Definition of Main Parameters

    problem = Model(name='HSI_Model')
    problem.time_limit = 600

    Wavelengths = range(0, N)
    NbofRegions = len(Regions)

    ##Definition of Variables

    y=problem.integer_var_matrix(Height, Width, lb=0, ub = N-1, name="lambda_assigned_to_P")
    x=problem.binary_var_matrix(Height, Width, name='x')

    indexes=[(k,s) for k in range(NbofRegions) for s in range(Regions[k].size) ]

    yl=problem.integer_var_dict(indexes,lb=0 , ub = N-1, name="lambda_line")
    lbs=problem.integer_var_dict(indexes,lb=0 , ub = N-1, name="lambda_b_section")

    indexes2=[(k,s,wl) for k in range(NbofRegions) for s in range(Regions[k].size) for wl in Wavelengths ]

    c=problem.integer_var_dict(indexes2, lb= 0, ub = Width + 2*N, name="column")
    g=problem.binary_var_dict(indexes2, name="gamma")
    z=problem.binary_var_dict(indexes2, name="z")

    print('All variables have been defined.')

    ##Definition of Constraints

    ##Constraints for 1st requirement

    problem.add_constraint(y[0,0]==1)

    for i in range(Height):
        for j in range(Width):
            problem.add_constraint(y[i,j] >= (N-1) * x[i,j])
            problem.add_constraint(y[i,j] <= (N-1) * (1 + x[i,j]) - 1)

    for i in range(Height):
        for j in range(Width-1):
            problem.add_constraint(y[i,j+1] == y[i,j] + 1 - x[i,j] * N)

    ##Constraints for 2nd requirement

    for k in range(NbofRegions):
        for s in range(Regions[k].size):
            section=Regions[k].sections[s]

            problem.add_constraint(yl[k,s] == y[section.s_line,0])
            problem.add_constraint(lbs[k,s] == y[section.s_line, section.s_beg])

    M=100000

    for k in range(NbofRegions):
        for s in range(Regions[k].size):
            for wl in Wavelengths:
                problem.add_constraint(wl-lbs[k,s] >= -M * g[k,s,wl])
                problem.add_constraint(wl-lbs[k,s] <= M * (1 - g[k,s,wl]) - 1)

    for k in range(NbofRegions):
        for s in range(Regions[k].size):
            for wl in Wavelengths:
                section=Regions[k].sections[s]
                sumx = sum([x[section.s_line,j] for j in range(0,section.s_beg)])

                problem.add_constraint(c[k,s,wl] == wl - yl[k,s] + N * sumx + N * g[k,s,wl])


    for k in range(NbofRegions):
        for s in range(Regions[k].size):
            for wl in Wavelengths:
                section=Regions[k].sections[s]

                problem.add_constraint(c[k,s,wl] >= section.s_beg - M * (1 - z[k,s,wl]))
                problem.add_constraint(c[k,s,wl] <= section.s_end + M * (1 - z[k,s,wl]))

    for k in range(NbofRegions):
        for wl in Wavelengths:
            region=Regions[k]

            problem.add_constraint(sum([z[k,s,wl] for s in range(region.size)]) >= 1 )

    print('All constraints have been written.')
    print('There are '+ str(problem.number_of_variables) + ' variables and '+ str(problem.number_of_constraints)+' constraints.')

    ##Resolution of the problem

    print('The resolution has started.')
    print('')

    problem.solve()

    lambda_l=[int(y[l,0].solution_value) for l in range(Height)]

    return(lambda_l,problem)

def Solver_2(Regions,N,Height):

    ##Definition of Main Parameters

    problem = Model(name='HSI_Model')
    problem.time_limit = 600

    Wavelengths = range(0, N)
    NbofRegions = len(Regions)

    ##Definition of Variables

    yl=problem.integer_var_list(Height, lb=0, ub = N-1, name="lambda_l")

    indexes = [(wl, line) for wl in Wavelengths for line in range(Height)]

    c=problem.integer_var_dict(indexes, lb= 0 , ub = N-1 , name="column")
    g=problem.binary_var_dict(indexes, name="gamma")

    indexes2 = [(wl, k, s) for wl in Wavelengths for k in range(NbofRegions) for s in range(len(Regions[k].sections))]
    indexes3 = []

    for wl in Wavelengths :
        for k in range(NbofRegions) :
            for s in range(Regions[k].size) :
                if Regions[k].indices_R[s] == 2:
                    indexes3.append((wl,k,s))

    z=problem.binary_var_dict(indexes2, name="z")
    d=problem.binary_var_dict(indexes3, name="delta")

    print('All variables have been defined.')

    ##Definition of Constraints

    problem.add_constraint(yl[0]==1)

    M=100000

    for line in range(Height):
        for wl in Wavelengths :
            problem.add_constraint(wl-yl[line] >= -M * g[wl,line] )
            problem.add_constraint(wl-yl[line] <= M * (1 - g[wl,line]) - 1)

    for line in range(Height):
        for wl in Wavelengths :
            problem.add_constraint(c[wl,line] == wl - yl[line]  + N * g[wl,line])

    for k in range(NbofRegions):
        for s in range(len(Regions[k].sections)):
            for wl in Wavelengths:

                section = Regions[k].sections_R[s]

                if Regions[k].indices_R[s] == 1 :  #Sections of Type 1
                    problem.add_constraint(c[wl, section.s_line] >= section.s_beg - M * (1 - z[wl, k, s]))
                    problem.add_constraint(c[wl, section.s_line] <= section.s_end + M * (1 - z[wl, k, s]))

                else :    #Sections of Type 2
                    problem.add_constraint(c[wl, section.s_line] >= section.s_beg - M * (2 - z[wl, k, s] - d[wl, k, s]))
                    problem.add_constraint(c[wl, section.s_line] <= section.s_end + M * (1 - z[wl, k, s] + d[wl, k, s]))


    for k in range(NbofRegions):
        for l in Wavelengths:
            region = Regions[k]
            problem.add_constraint(sum([z[l,k,s] for s in range(region.size)]) >= 1)

    print('All constraints have been written.')
    print('There are '+ str(problem.number_of_variables) + ' variables and '+ str(problem.number_of_constraints)+' constraints.')

    ##Resolution of the problem

    print('The resolution has started.')
    print('')

    problem.solve()

    lambda_l=[int(yl[l].solution_value) for l in range(Height)]

    return(lambda_l,problem)

def Solver_2_Prim(Regions,N,Height) :

    ##Definition of Main Parameters

    problem = Model(name='HSI_Model')
    problem.time_limit = 600

    Wavelengths = range(0, N)
    NbofRegions = len(Regions)

    ##Definition of Variables

    yl = problem.integer_var_list(Height, lb=0, ub=N - 1, name="lambda_l")

    indexes = [(wl, line) for wl in Wavelengths for line in range(Height)]

    c = problem.integer_var_dict(indexes, lb=0, ub=N - 1, name="column")

    indexes2 = [(wl, k, s) for wl in Wavelengths for k in range(NbofRegions) for s in range(len(Regions[k].sections))]

    z = problem.binary_var_dict(indexes2, name="z")

    print('All variables have been defined.')

    ##Definition of Constraints

    problem.add_constraint(yl[0]==1)

    for line in range(Height):
        for wl in Wavelengths:
            problem.add_if_then(wl >= yl[line], c[wl, line] == wl - yl[line])
            problem.add_if_then(wl + 1 <= yl[line], c[wl, line] == wl - yl[line] + N)

    for k in range(NbofRegions):
        for s in range(len(Regions[k].sections)):
            for wl in Wavelengths:

                S = Regions[k].sections_R[s]

                if Regions[k].indices_R[s] == 1 :  #Sections of Type 1
                    z[wl, k, s] = problem.logical_and(c[wl, S.s_line] >= S.s_beg, c[wl, S.s_line] <= S.s_end)
                else :    #Sections of Type 2
                    z[wl, k, s] = problem.logical_or(c[wl, S.s_line] >= S.s_beg, c[wl, S.s_line] <= S.s_end)

    for k in range(NbofRegions):
        for l in Wavelengths:
            region = Regions[k]
            problem.add_constraint(sum([z[l,k,s] for s in range(region.size)]) >= 1)

    print('All constraints have been written.')
    print('There are '+ str(problem.number_of_variables) + ' variables and '+ str(problem.number_of_constraints)+' constraints.')

    ##Resolution of the problem

    print('The resolution has started.')
    print('')

    problem.solve()

    lambda_l=[int(yl[l].solution_value) for l in range(Height)]

    return(lambda_l,problem)

def Solver_3(Regions,N,Height):

    ##Definition of Main Parameters

    problem = Model(name='HSI_Model')
    problem.time_limit = 600

    Wavelengths = range(0, N)
    NbofRegions = len(Regions)

    decision = 'Objective'

    ##Definition of Variables

    BoundariesInf, BoundariesSup, Indices1, Indices2, Indices_Final_Constraint = ft.Boundaries_of_I(Regions,N)
    Indices_Region=[(wl,k) for wl in Wavelengths for k in range(NbofRegions)]

    yl=problem.integer_var_list(Height, lb=0 , ub = N-1, name="lambda_l")
    z1=problem.binary_var_dict(Indices1,name='z1')
    z2=problem.binary_var_dict(Indices2,name='z2')
    z3=problem.binary_var_dict(Indices2,name='z3')
    Z_Region=problem.binary_var_dict(Indices_Region,name='Z_Region')

    print('All variables have been defined.')

    ##Definition of Constraints

    problem.add_constraint(yl[0]==1)

    M=100000

    for i in Indices2:
        problem.add_constraint(z2[i] + z3[i] <= 1)

    for k in range(NbofRegions):
        for s in range(Regions[k].size):
            for wl in Wavelengths:

                S=Regions[k].sections[s]

                if BoundariesSup[k][s][wl] >= BoundariesInf[k][s][wl]:

                    problem.add_constraint(yl[S.s_line] >= BoundariesInf[k][s][wl] - M * (1 - z1[wl, k, s]))
                    problem.add_constraint(yl[S.s_line] <= BoundariesSup[k][s][wl] + M * (1 - z1[wl, k, s]))

                else:

                    problem.add_constraint(yl[S.s_line] >= BoundariesInf[k][s][wl] - M * (1 - z2[wl, k, s]))
                    problem.add_constraint(yl[S.s_line] <= BoundariesSup[k][s][wl] + M * (1 - z3[wl, k, s]))


    for k in range(NbofRegions):
        for wl in Wavelengths:

            Somme1=sum([z1[wl,k,s] for s in Indices_Final_Constraint[wl][k][0]])
            Somme2=sum([z2[wl,k,s] for s in Indices_Final_Constraint[wl][k][1]])
            Somme3=sum([z3[wl,k,s] for s in Indices_Final_Constraint[wl][k][1]])

            if decision == 'Constraint' :
                problem.add_constraint(Somme1 + Somme2 + Somme3  >= 1 )
            elif decision == 'Objective' :
                problem.add_constraint(Somme1 + Somme2 + Somme3  <= N * Z_Region[wl,k] )
                problem.add_constraint(Somme1 + Somme2 + Somme3  >= Z_Region[wl,k] )

    if decision == 'Objective' :
        problem.maximize(sum([sum([Z_Region[wl,k] for wl in Wavelengths]) for k in range(NbofRegions)]))


    print('All constraints have been written.')

    print('There are '+ str(problem.number_of_variables) + ' variables and '+ str(problem.number_of_constraints)+' constraints.')

    ##Resolution of the problem

    print('The resolution has started.')
    print('')

    problem.solve()

    lambda_l=[int(yl[i].solution_value) for i in range(Height)]

    return(lambda_l,problem)

