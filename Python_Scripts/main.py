import sys
import os

import SysPath
sys.path = SysPath.Path

Visual = 1

import time
import Solvers as sv

if Visual == 0 :
    import Functions as ft
elif Visual == 1 :
    import Functions_Visual as ft

##Definition of Main Parameters

start_time = time.time()

Type = int(sys.argv[1])
Number = int(sys.argv[2])

NbofWavelengths = int(input('Number of Wavelengths '))
print('')
Solver = input('Version of the Solver ')
print('')
Pre_Processing = int(input('Are extensive pre-processing steps necessary (Yes=1, No=0) '))
print('')

Initial_Set_of_Regions, Height, Width = ft.Data_Image(Type,Number)
ft.Initial_SofR(Initial_Set_of_Regions)
print('')

[Minimum_Number_of_Pixels, Grouping_Factor, Limiter] = ft.Select_Pre_Processing_Parameters(NbofWavelengths,Pre_Processing)

N = int(NbofWavelengths/Grouping_Factor)
Reduced_Width=int(Width/Grouping_Factor)
Pre_Processing_Parameters = [Minimum_Number_of_Pixels, Grouping_Factor, Limiter]
Already_Satisfied_Regions, Unsolvable_Regions, Regions_To_Satisfy = ft.Pre_Processing(Initial_Set_of_Regions,Pre_Processing,Pre_Processing_Parameters,N)

Regions = Regions_To_Satisfy
ft.Proceed_Resolution(Regions)

[NbofWavelengths, NbofRegions, NbofSections] = ft.Configuration_for_Resolution(Regions,NbofWavelengths)
Configuration = [NbofWavelengths, NbofRegions, NbofSections]
ft.Initial_Configuration(Already_Satisfied_Regions, Unsolvable_Regions, Regions_To_Satisfy, Configuration)


#Problem Resolution

if Solver == '1' :
    lambda_l,problem = sv.Solver_1(Regions,N,Height,Reduced_Width)

elif Solver == '2' :
    ft.Relocation_of_Sections(Regions,N)
    ft.Several_Figures_after_Relocation(Regions,Reduced_Width,Height,N)
    lambda_l,problem = sv.Solver_2(Regions,N,Height)

elif Solver == '2.5' :
    ft.Relocation_of_Sections(Regions,N)
    ft.Several_Figures_after_Relocation(Regions,Height,Reduced_Width,N)
    lambda_l,problem = sv.Solver_2_Prim(Regions,N,Height)

elif Solver == '3' :
    lambda_l,problem = sv.Solver_3(Regions,N,Height)


##Satisfaction Assessment

print('Results')
print('')

Overall_Computing_Time = round(time.time()-start_time)

Lambda_l=[(lambda_l[i]*Grouping_Factor)%NbofWavelengths for i in range(Height)]
Solution=ft.Solution_from_1st_Column(Lambda_l, Height, Width, NbofWavelengths)

Indices_SRegions, Indices_UnsRegions, Missing_Wavelengths = ft.Adequate_Assignment_Regions(Initial_Set_of_Regions, Solution, NbofWavelengths)
Statistics = ft.Statistics(Initial_Set_of_Regions,Indices_SRegions, Indices_UnsRegions, NbofWavelengths, Missing_Wavelengths)
Nb_UnsatisReg = len(Indices_UnsRegions)

SatisfiedRegions=[Initial_Set_of_Regions[k] for k in Indices_SRegions]
UnsatisfiedRegions=[Initial_Set_of_Regions[k] for k in Indices_UnsRegions]
All_Parameters = Configuration + Pre_Processing_Parameters

ft.Display_Results(All_Parameters, problem, Overall_Computing_Time, Nb_UnsatisReg, Pre_Processing)
ft.Display_Statistics(Statistics)

if Visual == 1:
    ft.Draw_Figure(SatisfiedRegions,UnsatisfiedRegions, Height,Width)

ft.Solution_in_text_file(Lambda_l)
ft.Parameters_and_Statistics_in_text_file(All_Parameters, problem, Overall_Computing_Time, Nb_UnsatisReg, Pre_Processing, Statistics)

