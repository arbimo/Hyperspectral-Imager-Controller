function[]=Save_Image(Image,Filepath,Color)

maximum = max(Image(:));
Image8Bit = uint8((255 * Image) / maximum); %We create the 8Bit-equivalent of the image we want to save

if strcmp(Color,'Panchromatic') %The first saved image is the panchromatic
    Pan_Image = ind2gray(Image8Bit, gray(256));
    imwrite(Pan_Image, Filepath);
    
elseif strcmp(Color,'Segmented') %The second is the segmented version
    Seg_Image = ind2rgb(Image8Bit, jet(256));
    imwrite(Seg_Image, Filepath);
    
end
end

