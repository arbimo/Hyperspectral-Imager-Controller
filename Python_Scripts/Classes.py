
##class region

class Region:

    def __init__(self,label,size):
        self.label=label
        self.size=size
        self.sections=[]
        self.sections_R=[]
        self.indices_R=[]
        self.nbpix=0
        self.s_maxsize=0

    def add_Section(self,section):
        self.sections.append(section)
        self.nbpix+=section.s_size
        if section.s_size>=self.s_maxsize:
            self.s_maxsize=section.s_size
        self.size = len(self.sections)

    def add_Section_2(self, section, N):
        bs = int(section.s_beg) % N
        es = int(section.s_end) % N
        k = len(self.sections_R)
        new_section = Section(k, bs, es, section.s_line)
        new_section.s_size = section.s_size
        self.sections_R.append(new_section)

        if bs <= es:  # Type1
            self.indices_R.append(1)

        else:  # Type2
            self.indices_R.append(2)

##class section

class Section:

    def __init__(self,label,beg,end,line):
        self.label=label
        self.s_beg=beg
        self.s_end=end
        self.s_size=end-beg+1
        self.s_line=line
