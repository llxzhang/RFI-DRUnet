% clear all
% close all
% clc

% size
Nr = 1024;
Nc = 1024;
Np = Nr*Nc;

dimr = 10;
dimc = 10;

snr_min = 0;
snr_max = 10;

p = 0.00001;
Z_out = rand(Nr, Nc)<p;

isdisplay = 0;
if isdisplay
    figure(1); imshow(Z_out,[])
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

if isdisplay
    figure; imshow(mapres,[]);
    title(['\beta = ' num2str(gran),  '  Iteration= ',num2str(Nmc), '  p= ',num2str(p)],'fontsize',14);
end




