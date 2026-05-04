% clear all
% close all
% clc
% 
% % size
% Nr = 1024;
% Nc = 1024;
% Np = Nr*Nc;
% 
% dimr = 5;
% dimc = 5;
% 
% snr_min = 0;
% snr_max = 1;
% 
% % number of iterations
% Nmc = 30;
% 
% % parameters of the field (to be empirically adjusted)
% gran = 60;
% p = 0.8; P = [1/p p];



% initialization 
Z_ext = rand(Nr+2, Nc+2)<1/2;

isdisplay = 0;
for i=1:Nmc
    for i=2:Nr+1
        for j=2:Nr+1
            %%% Proba of having 0
            % nb of neighbors with 0
            nb0 = (Z_ext(i-1,j)==0) + (Z_ext(i+1,j)==0) + (Z_ext(i,j-1)==0) + (Z_ext(i,j+1)==0);
            Pij0 = exp(gran*nb0+log(P(1)));
            
            % Proba of having 1
            % nb of neighbors with 1
            nb1 = 4-nb0;
            Pij1 = exp(gran*nb1+log(P(2)));
            
            Pij1norm = Pij1/(Pij0+Pij1);
            Z_ext(i,j) = (rand<Pij1norm);
        end
    end
    
    if isdisplay
        figure(11);
        imagesc(Z_ext);
       drawnow
    end
    
end
Z_out = Z_ext(2:end-1,2:end-1);

if isdisplay
    figure(1); imshow(Z_out,[])
    title(['\beta = ' num2str(gran),  '  Iteration= ',num2str(Nmc), '  p= ',num2str(p)],'fontsize',14)
end

center = find(Z_out==1);
maptmp = zeros(Nr,Nc);
mapres = zeros(Nr,Nc);

L = length(center);
for i = 1:L 
    ii = center(i);
    maptmp(ii) = 1;
    % randomly choose size of rfi
    % dimr = 10, paramr = [1,11]
    paramr = 2*unidrnd(dimr)+1;
    paramc = 2*unidrnd(dimc)+1;

    %building psf
    %fspecial('type', size, sigma)

    psftmp = newfspecial('gaussian', paramr, unifrnd(0.8,paramr/2));
    psfr = psftmp(1+(paramr-1)/2,:);

    psftmp = newfspecial('gaussian', paramc, unifrnd(0.8,paramc/2));
    psfc = psftmp(1+(paramc-1)/2,:);
    
    %snr of rfi 0-1
    snr = (snr_max-snr_min)*rand+snr_min;
    psf = snr*psfr(:)*psfc(:)';
    
    %imagesc(psf);
    mapres = mapres + conv2(maptmp, psf, 'same');

    maptmp(ii)=0;
end

% if isdisplay
%     figure; imshow(mapres,[]);
%     title(['\beta = ' num2str(gran),  '  Iteration= ',num2str(Nmc), '  p= ',num2str(p)],'fontsize',14);
% end




