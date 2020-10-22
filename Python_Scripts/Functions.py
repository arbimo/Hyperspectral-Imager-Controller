import os
import copy
import Classes as cl

def Adequate_Assignment_Regions(Regions,Solution,NbofWavelengths):

    Unsolved_Regions=[]
    Solved_Regions=[]

    Missing_Wavelengths=[]

    NbofRegions=len(Regions)


    for k in range(NbofRegions):

        Region=Regions[k]
        Present_Wavelengths=set()

        for s in range(Region.size):
            Section=Region.sections[s]
            for j in range(Section.s_size):
                integer=Solution[Section.s_line][Section.s_beg+j]
                Present_Wavelengths.add(integer)

        if len(Present_Wavelengths)<NbofWavelengths:
            Unsolved_Regions.append(k)
            Missing_Wavelengths.append(NbofWavelengths-len(Present_Wavelengths))

        else :
            Solved_Regions.append(k)

    return Solved_Regions,Unsolved_Regions, Missing_Wavelengths

def Average_Sizes_of_Sections(Regions):

    Average_Sizes = []

    for Region in Regions:

        Sizes = [Section.s_size for Section in Region.sections]
        Average_Sizes.append(int(sum(Sizes)/Region.size))

    return Average_Sizes

def Bip():
    duration=0.3
    freq=300
    os.system('play -nq -t alsa synth {} sine {}'.format(duration,freq))

def Boundaries(bs,es,wl,N):

    Specific_Lambda_l1 = int((wl-bs)%N)
    Specific_Lambda_l2 = int((wl-es)%N)
    return Specific_Lambda_l1, Specific_Lambda_l2

def Boundaries_of_I(Regions,N):
    Max = Max_Size_Regions(Regions)
    NbofRegions = len(Regions)

    BoundariesInf=[[[ 0 for _ in range(N)] for _ in range(Max)] for _ in range(NbofRegions)]
    BoundariesSup=[[[ 0 for _ in range(N)] for _ in range(Max)] for _ in range(NbofRegions)]

    Indices1=[]
    Indices2=[]

    Indices_Final_Constraint = [[[[] for _ in range(2)] for _ in range(NbofRegions)] for _ in range(N)]

    for k in range(NbofRegions):
        for wl in range(N):

            for s in range(Regions[k].size) :

                S=Regions[k].sections[s]
                Superior_Boundary, Inferior_Boundary = Boundaries(S.s_beg,S.s_end,wl,N)
                BoundariesInf[k][s][wl]=Inferior_Boundary
                BoundariesSup[k][s][wl]=Superior_Boundary

                if Inferior_Boundary <= Superior_Boundary :

                    Indices1.append((wl,k,s))
                    Indices_Final_Constraint[wl][k][0].append(s)

                else :

                    Indices2.append((wl,k,s))
                    Indices_Final_Constraint[wl][k][1].append(s)

    return BoundariesInf, BoundariesSup, Indices1, Indices2, Indices_Final_Constraint

def Configuration_for_Resolution(Regions,NbofWavelengths):
    Configuration = [NbofWavelengths, len(Regions), sum([region.size for region in Regions])]
    return Configuration

def Data_Image(Type,Number):

    if Type == 1:
        string = 'Test_Easy'
    if Type == 2:
        string = 'Test_Medium'
    if Type == 3:
        string = 'Aerial_Scene'

    Dir = Images_Directory()

    Filepath1 = Dir + '/{}/Regions_and_Sections_{}.txt'.format(string,Number)
    Filepath2 = Dir + '/{}/Size_Image_{}.txt'.format(string,Number)

    Initial_Set_of_Regions = Extraction(Filepath1)
    Height, Width = Extraction2(Filepath2)

    return Initial_Set_of_Regions, Height, Width

def Display_Regions(Regions):
    for k in range(len(Regions)):
        R=Regions[k]
        print('Region '+str(R.label)+', size = '+str(R.size)+', Nb of Pixels = '+str(R.nbpix)+', Smax = '+str(R.s_maxsize))
        print('\n')
        for s in range(len(R.sections)):
            S=R.sections[s]
            print('Section ' + str(S.label) + ', size = ' + str(S.s_size) + ', beginning = ' + str(S.s_beg)+ ', end = ' + str(S.s_end) + ', line = ' + str(S.s_line))
        print('\n')

def Display_Results(Parameters,problem,Overall_Computing_Time, Nb_UnsatisfiedRegions, Pre_Processing, output = 'print'):

    min = Overall_Computing_Time // 60
    sec = Overall_Computing_Time % 60
    string = []

    if Pre_Processing == 1 :
        string.append('- For pre-processing, regions with a number of pixels < {} have been removed'.format(Parameters[3]))
        string.append('- Pixels have been fused in groups of {} pixels '.format(Parameters[4]))
        string.append('- The limiter for the size of the regions has been set to {} pixels'.format(Parameters[5]))

    string.append('- We have {} variables and {} constraints'.format(problem.number_of_variables, problem.number_of_constraints))
    string.append('- The overall computing time is {} min(s) and {} second(s)'.format(min, sec))
    string.append('- {} region(s) have not been satisfied'.format(Nb_UnsatisfiedRegions))

    if output == 'print' :
        for i in range(len(string)):
            print(string[i])

    else :
        return string

def Display_Statistics(Statistics, output = 'print'):

    string = []

    string.append('- Number of Satisfied Regions : {}'.format(Statistics[0]))
    string.append('- Satisfaction Percentage of the Regions : {}'.format(round(Statistics[1],2)))
    string.append('- Satisfaction Percentage of the Wavelengths (Distinct Wavelengths Available in Regions) : {}'.format(round(Statistics[2],2)))
    string.append('- Average Number of Missing Wavelengths in Unsatisfied Regions : {}'.format(Statistics[3]))
    string.append('- Number of pixels in Satisfied Regions : {}'.format(Statistics[4]))
    string.append('- Percentage of pixels in Satisfied Regions : {}'.format(round(Statistics[5],2)))

    if output == 'print':
        print('')
        print('Statistics')
        print('')
        for i in range(len(string)):
            print(string[i])

    else :
        return string

def Extraction(filepath):
    file=open(filepath,"r")
    Regions=[]
    for row in file.readlines():
        line=row.split()
        if len(line)>0:

            if line[0]=="Region": #New Region
                label, size = int(line[1]) - 1 , int(line[4])
                region=cl.Region(label,size)
                Regions.append(region)

            elif line[0]=="Section": #New Section
                label, beginning, ending, section_line= int(line[1]), int(line[3]), int(line[5]) ,int(line[9])
                section=cl.Section(label-1, beginning-1, ending-1, section_line-1) #lists start with index 0, not 1 (as in Matlab)
                Regions[-1].add_Section(section)

    file.close()
    return Regions

def Extraction2(filepath):
    file=open(filepath,"r")
    line=file.readlines(1)[0] #line 1 of txtfile
    Height=int(line.split()[4])
    line=file.readlines(1)[0]  #line 2 of txtfile
    Width=int(line.split()[4])
    return Height, Width

def Grouping_of_Pixels(Section,Grouping_Factor):
    GF = Grouping_Factor
    if Section.s_size<=GF-1:
        return None

    else :
        if (Section.s_beg % GF) == 0:
            New_Section_Beginning = Section.s_beg / GF
        else:
            New_Section_Beginning = (Section.s_beg // GF) + 1

        if ((Section.s_end + 1) % GF) == 0:
            New_Section_End = ((Section.s_end + 1) / GF) - 1
        else:
            New_Section_End = (Section.s_end // GF) - 1

    if New_Section_Beginning>New_Section_End :
        return None

    else :
        return int(New_Section_Beginning),int(New_Section_End)

def Grouping_of_Pixels2(Regions,GF):

    Regions2=[]
    k2=0

    for k in range(len(Regions)):

        Region2=cl.Region(k2,0)
        s2=0

        for Section in Regions[k].sections:

            if Grouping_of_Pixels(Section,GF) != None :

                New_Section_Beginning, New_Section_End = Grouping_of_Pixels(Section,GF)
                Section2 = cl.Section(s2, New_Section_Beginning, New_Section_End, Section.s_line)
                Region2.add_Section(Section2)
                s2 += 1

        if Region2.size > 0:
            Regions2.append(Region2)
            k2+=1

    return Regions2

def Images_Directory():
    return os.getcwd() + '/Images'

def Initial_Configuration(Already_Satisfied_Regions, Unsolvable_Regions, Regions_To_Satisfy, Parameters):

    Nb_of_Already_Satisfied_Regions = len(Already_Satisfied_Regions)
    Nb_of_Unsolvable_Regions = len(Unsolvable_Regions)
    Nb_of_Regions_To_Satisfy = len(Regions_To_Satisfy)

    NbofRegions = Nb_of_Already_Satisfied_Regions + Nb_of_Unsolvable_Regions + Nb_of_Regions_To_Satisfy

    print('For the resolution, the new set of homogeneous regions is comprised of ' + str(NbofRegions) + ' areas. After the sorting of the areas, there are :')

    if Nb_of_Unsolvable_Regions>=1 :
        print('- ' + str(Nb_of_Unsolvable_Regions) + ' region(s) unsolvable,')

    if Nb_of_Already_Satisfied_Regions>=1 :
        print('- ' + str(Nb_of_Already_Satisfied_Regions) + ' region(s) already satisfied,')

    print('- ' + str(Nb_of_Regions_To_Satisfy) + ' region(s) to solve.')

    print('- We consider {} wavelengths and {} sections'.format(Parameters[0], Parameters[2]))
    print('')

def Initial_SofR(Initial_Set):
    print('Initially, there are {} regions and {} sections in the image.'.format(len(Initial_Set),sum([region.size for region in Initial_Set])))

def Limitation(Regions,limiter):
    Indices_Section=[]

    for region in Regions:

        list_of_Section_sizes_and_labels=[[section.s_size,section.label] for section in region.sections]

        list_of_Section_sizes_and_labels.sort(key = lambda x: (x[0]), reverse=True)

        sum=0

        for s in range(len(list_of_Section_sizes_and_labels)):
            sum+=list_of_Section_sizes_and_labels[s][0]
            if sum >= limiter:

                Subset_Sections = list_of_Section_sizes_and_labels[0:s+1]
                Indices_Section.append(Subset_Sections)
                break


        if sum < limiter :
            Indices_Section.append(list_of_Section_sizes_and_labels)

    return Indices_Section

def Max_Size_Regions(Regions):
    sizes=[region.size for region in Regions]
    return max(sizes)

def Parameters_and_Statistics_in_text_file(Parameters, problem, Overall_Computing_Time, Nb_UnsatisfiedRegions, Pre_Processing, Statistics):
    Fpath = Results_Directory() + '/Parameters_and_Statistics.txt'
    file=open(Fpath,"w")
    file.write('Parameters \n')
    file.write('\n')

    string = Display_Results(Parameters, problem, Overall_Computing_Time, Nb_UnsatisfiedRegions, Pre_Processing, 'return')


    for str in string :
        file.write(str + '\n')

    file.write('\n')
    file.write('Statistics \n')
    file.write('\n')

    string2 = Display_Statistics(Statistics, 'return')

    for str in string2 :
        file.write(str + '\n')

    file.close()

def Pre_Processing(Initial_Set_of_Regions,Pre_Processing, Parameters,N):

    limiter = int(Parameters[2]/Parameters[1])
    Regions_aux1 = Removing_Smallest_Regions(Initial_Set_of_Regions,Parameters[0])
    Regions_aux2 = Grouping_of_Pixels2(Regions_aux1, Parameters[1])
    Regions_aux3 = Subset_of_Sections(Regions_aux2, limiter)

    if Pre_Processing == 0:
        Already_Satisfied_Regions, Unsolvable_Regions, Regions_To_Satisfy = Sort_Regions(Initial_Set_of_Regions, N)
    else :
        Already_Satisfied_Regions, Unsolvable_Regions, Regions_To_Satisfy = Sort_Regions(Regions_aux3, N)

    return Already_Satisfied_Regions, Unsolvable_Regions, Regions_To_Satisfy

def Proceed_Resolution(Regions):

    if len(Regions) == 0:
        print('No Region to solve for these parameters')
        exit()

def Python_Directory():
    return os.getcwd()

def Relocation_of_Sections(Regions,N):
    for k in range(len(Regions)):
        for s in range(len(Regions[k].sections)):
            section=Regions[k].sections[s]
            Regions[k].add_Section_2(section,N)
    return(Regions)

def Removing_Smallest_Regions(Regions, Minimum_Number_of_Pixels) :

    Regions2 = []
    for region in Regions :
        if region.nbpix >= Minimum_Number_of_Pixels :
            Regions2.append(region)

    return Regions2

def Results_Directory():
    return os.getcwd() + '/Results'

def Sections_of_Minimum_Size(Regions):

    Minimum_Sizes = []

    for Region in Regions:

        Sizes = [Section.s_size for Section in Region.sections]
        Minimum_Sizes.append(min(Sizes))

    return Minimum_Sizes

def Select_Pre_Processing_Parameters(NbofWavelengths, pre_processing):

    if pre_processing == 0 :
        return [1,1,1]
    else :
        Minimum_Number_of_Pixels = int(input('Minimum Number of Pixels ? '))
        Grouping_Factor = int(input('Grouping Factor ? '))
        Limiter = int(input('Limiter (how many times N) ? '))
        print('')
        return [Minimum_Number_of_Pixels, Grouping_Factor, NbofWavelengths * Limiter]

def Several_Figures_after_Relocation(Regions,Height,Width,N):

    Fpath= Results_Directory() + '/Relocation_of_Sections.txt'
    file=open(Fpath,'w')

    #Width must be > to N

    for k in range(len(Regions)):
        file.write('[')
        Figure=[[ 0 for _ in range(N)] for _ in range(Height)]

        for s in range(len(Regions[k].sections_R)):
            section = Regions[k].sections_R[s]

            if Regions[k].indices_R[s] == 1 :
                for l in range(section.s_size):
                    Figure[section.s_line][section.s_beg + l] = 1

            else :
                for c in range(N):
                    if c<=section.s_end or c>=section.s_beg :
                        Figure[section.s_line][c] = 1

        for row in Figure :
            file.write(' [')
            for i in row:
                file.write(' ' + str(int(i))+ ',')
            file.write('] \n')
        file.write('] \n \n')

    file.close()

def Solution_from_1st_Column(list, Height, Width, N):  #Lambda = 0,.., N-1
    Solution=[[ 0 for _ in range(Width)] for _ in range(Height)]
    for i in range(Height):
        for j in range(Width):
            Solution[i][j]=(list[i] + j)%N
    return Solution

def Solution_in_text_file(lambda_l_s) :

    Fpath = Results_Directory() + '/Solution.txt'
    file=open(Fpath,"w")
    file.write('[')
    for lambda_l in lambda_l_s :
        file.write(str(lambda_l))
        file.write(', ')
    file.write('] \n')
    file.close()

def Sort_Regions(Regions,N):
    Satis_Regions=[]       #already satisfied regions
    Unsol_Regions=[]       #unsolvable regions
    Tosol_Regions=[]       #to solve regions
    k1=0
    k2=0
    k3=0

    for k in range(len(Regions)):
        if Regions[k].s_maxsize>=N :
            region=copy.deepcopy(Regions[k])
            region.label=k1
            Satis_Regions.append(region)
            k1 +=1
        elif Regions[k].nbpix<N :
            region=copy.deepcopy(Regions[k])
            region.label = k2
            Unsol_Regions.append(region)
            k2 += 1
        else :
            region=copy.deepcopy(Regions[k])
            region.label = k3
            Tosol_Regions.append(region)
            k3 += 1

    return Satis_Regions, Unsol_Regions, Tosol_Regions

def Statistics(Regions,Indices_Solved_Regions,Indices_Unsolved_Regions,NbofWavelengths, Missing_Wavelengths):

    Nb_Satisfied_Regions=len(Indices_Solved_Regions)
    Nb_Unsatisfied_Regions=len(Indices_Unsolved_Regions)

    Total_Number_of_Pixels = sum([region.nbpix for region in Regions])
    Total_Satis_Assign_of_Pixels = sum([Regions[k].nbpix for k in Indices_Solved_Regions])

    Total_Missing_Wavelengths=sum(Missing_Wavelengths)

    Satis_Percent_Regions=(Nb_Satisfied_Regions/len(Regions))*100
    Satis_Percent_Wavelengths=(1-(Total_Missing_Wavelengths/(len(Regions)*NbofWavelengths)))*100
    Satis_Percent_Pixels=(Total_Satis_Assign_of_Pixels/Total_Number_of_Pixels)*100

    if Nb_Unsatisfied_Regions == 0 :
        Average_Number_of_Missing_Wavelenghts = 0
    else :
        Average_Number_of_Missing_Wavelenghts = round(Total_Missing_Wavelengths/Nb_Unsatisfied_Regions)

    Statistics=[Nb_Satisfied_Regions,Satis_Percent_Regions,Satis_Percent_Wavelengths, Average_Number_of_Missing_Wavelenghts,Total_Satis_Assign_of_Pixels,Satis_Percent_Pixels]

    return Statistics

def Subset_of_Sections(Regions,limiter):
    NbRegions=len(Regions)

    Indices_Section=Limitation(Regions,limiter)
    Regions2=[]

    for k in range(NbRegions):
        Region2=cl.Region(k,0)

        for s in range(len(Indices_Section[k])):

            section_label=Indices_Section[k][s][1]
            Section=Regions[k].sections[section_label]

            Region2.add_Section(Section)

        Regions2.append(Region2)

    return Regions2





















