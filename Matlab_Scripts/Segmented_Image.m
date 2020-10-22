function[Segmented_Image, Image_Directory] = Segmented_Image(Type, Number)

%We use the provided segmentation function to define the
%panchromatic and segmented renderings of the hyperspectral scene

[Image, Image_Directory] = Get_Image(Type, Number);

Name_Pan = strcat(Image_Directory,num2str(Number),'_panchromatic.png'); %Name and Location of saved Image
Name_Seg = strcat(Image_Directory,num2str(Number),'_segmented.png');

grayscale_image=sum(Image, 3); %sum RGB to get grayscale image, corresponds to panchromatic

Save_Image(grayscale_image, Name_Pan, 'Panchromatic');

%% Segmentation Code

[Seuil_grad, Seuil_taille] = Define_Segmentation_Parameters(Type, Number); 
%we get some of the segmentation parameters for the image

kappa = 100;
num_iter = 20;
delta_t = 1/7; 
option = 2;  
largeur_contour = 1;

% Anisodiff2D segmentation 
[Im_label, ~]=segmentation(grayscale_image,Seuil_grad,num_iter,delta_t,kappa,option,Seuil_taille,largeur_contour);

Nblines = length(Im_label(:,1));
Nbcolumns = length(Im_label(1,:));

Segmented_Image = Im_label(3:Nblines-2 , 3:Nbcolumns-2); %borders are removed because the segmentation creates supplimentary 
                                                         %regions in these
                                                         %areas

Save_Image(Segmented_Image, Name_Seg, 'Segmented');

end

