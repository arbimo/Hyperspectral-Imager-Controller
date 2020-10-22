
function [Im_label, TEND] = segmentation(panchro, Seuil_grad, num_iter, delta_t, kappa, option, Seuil_taille, largeur_contour)
%segmentation   Region-oriented segmentation according to the watershed method
%   [Im_label, TEND] = segmentation(panchro, Seuil_grad, num_iter, delta_t, kappa, option, Seuil_taille, largeur_contour)
%
% Tony Rouvier, IRAP, Jul 2018

TSTART = tic;
% filtre�P&M
panchro_img_PM = double(anisodiff2D(panchro, num_iter, delta_t, kappa, option));

%figure(5)
%colours denote region label, edges have value=1;
%imagesc(panchro_img_PM);colorbar

%title('Anisodiff2D')

% element structurant gradient beucher
se = strel(ones(3,3));
G = imdilate(panchro_img_PM, se) - imerode(panchro_img_PM, se);
% seuillage gradient pour enlever faibles variations
GS = G.*(G>Seuil_grad);
% ligne de partage des eaux par matlab, renvoie une image labelisee. label
% 0 = contour de largeur 1 pixel
Im_label = double(watershed(GS));
% dilatation des contours de largeur 1 pixel � largeur_contour pixel.
E = zeros(largeur_contour,largeur_contour);
E(floor(largeur_contour/2)+1,:) = 1;
E(:,floor(largeur_contour/2)+1) = 1;
Im_label = Im_label .* ~imdilate(Im_label==0,E);

% Si besoin on enleve les petites regions de la segmentation
% exemple : on regarde la reconstruciton seulement sur des r�gions de plus
% de 100 pixels.
if Seuil_taille~=0
  Nb_P = regionprops(Im_label,'Area'); Nb_P = struct2table(Nb_P); Nb_P = table2array(Nb_P);
  P_ind = regionprops(Im_label,'PixelIdxList'); P_ind = struct2table(P_ind); P_ind = table2array(P_ind);
  ind_label_keep = nonzeros((1:length(Nb_P))'.*(Nb_P>=Seuil_taille));
  Im_label_new = zeros(size(Im_label));
  for i=1:length(ind_label_keep)
    Im_label_new(P_ind{ind_label_keep(i)}) = ind_label_keep(i);
  end
  Im_label = Im_label_new;
end

TEND = toc(TSTART);
% sprintf ('Segmentation time = %.2f s', TEND)
