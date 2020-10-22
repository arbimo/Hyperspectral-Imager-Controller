function[Image, Image_Directory] = Get_Image(Type, Number)

%From the type and number of the image we deduce its location in the
%directory Solver

DirectoryPath = erase(pwd,'/Matlab_Scripts'); 

if Type == 1
    Image_Type = 'Test_Easy';
elseif Type == 2
    Image_Type = 'Test_Medium';
else 
    Image_Type = 'Aerial_Scene';
end    

Image_Directory = strcat(DirectoryPath,'/Images/',Image_Type,'/');
Image = imread(strcat(Image_Directory,num2str(Number),'.png'));

end

