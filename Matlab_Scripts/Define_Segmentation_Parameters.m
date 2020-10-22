function[Seuil_grad, Seuil_taille] = Define_Segmentation_Parameters(Type, Number)

%We select parameters for the segmentation based on the image we wish to
%process. For a custom image, custom parameters must be defined in this function.

if Type == 1
    
    Seuil_grad = 30;
    Seuil_taille = 100;
    
elseif Type == 2
    
    if Number == 2
        Seuil_grad = 10; 
    elseif Number == 3
        Seuil_grad = 12; 
    else
        Seuil_grad = 7; 
    end
    
    Seuil_taille = 60;
    
else   
    
    if Number == 2
        Seuil_grad = 7;
    else
        Seuil_grad = 15;
    end
    
    Seuil_taille = 200;
end
end