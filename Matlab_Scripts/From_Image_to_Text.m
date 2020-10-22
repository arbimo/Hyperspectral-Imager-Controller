function[]=From_Image_to_Text(Type, Number)

%With this function we get from the type and number of the image the
%characterization of homogeneous areas and height/width of image

[S_Image, Image_Directory] = Segmented_Image(Type, Number); %segmentation

Filename1 = strcat(Image_Directory,'Regions_and_Sections_',num2str(Number),'.txt');
Filename2 = strcat(Image_Directory,'Size_Image_',num2str(Number),'.txt');

[Regions] = Characterization_Regions_and_Sections(S_Image); %definition of set of homogeneous regions with sections
NbofRegions = length(Regions);

fileID=fopen(Filename1,'w'); %creation of text files with pertinent data
formatSpec1= 'Region %d  Size : %d\n';
formatSpec2= 'Section %d  beginning: %d  end: %d  size: %d  line: %d\n'; 

for i = 1:NbofRegions
    region=Regions{1,i};
    fprintf(fileID,formatSpec1,region.label,region.size);
    for j = 1:region.size
        section=region.sections{1,j};
        fprintf(fileID, formatSpec2, section.s_label, section.s_beg, section.s_end, section.s_size, section.s_line);
    end
    fprintf(fileID, '\n');
end
fclose(fileID);

fileID2=fopen(Filename2,'w');

Nbline = length(S_Image(:,1));
Nbcolumn = length(S_Image(1,:));

fprintf(fileID2, "Nb of lines = %d\n", Nbline);
fprintf(fileID2, "Nb of columns = %d", Nbcolumn);

fclose(fileID2);
end
