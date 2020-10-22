function [Regions] = Characterization_Regions_and_Sections(Image)

%We define the set of homogeneous regions obtained after segmentation of
%the image

Nbline = length(Image(:,1));
Colors = [];
Regions = {};
NbofRegions = 1;


for k =1:Nbline
    line=Image(k,:);
    [I_beg, I_end]=Partitioning_Rows(line); %we partition each row of the image independently
    S_nber = length(I_beg);
        
    for j = 1:S_nber %for each new section we ascertain if it belongs to a known region 
                      %or if it defines a new region
        
        color = line(I_beg(j));
        index = find(Colors == color); 
        
            if isempty(index) %the color has not been encountered yet
                
                Regions{NbofRegions} = region(NbofRegions); %we create a new region of label NbOfRegions
                Colors=[Colors color];
                label = NbofRegions;
                NbofRegions = NbofRegions+1;
                
            else 
                
                label = index; %an index in Colors corresponds exactly to the label of the region which contains the 'color'
                
            end
        
        Regions{label}.size = Regions{label}.size + 1;     
        Section = section(Regions{label}.size, I_beg(j),I_end(j),k); %we create a new section with our data 
        Regions{label}.sections{end+1} = Section; %a new section is added to sections of considered region
        
    end
end
end




