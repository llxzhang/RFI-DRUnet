clear all
close all
clc

% 1 = MRF, 0 = independt
generate_mode = 1;

% size
Nr = 1024;
Nc = 1024;
Np = Nr*Nc;

if generate_mode
    %MRF:
    % parameters of the field (to be empirically adjusted)
    gran = 40;
    p = 0.8; P = [1/p p];
    % number of iterations
    Nmc = 30;
    %kernel
    dimr =5;
    dimc =5;

    snr_min = 0;
    snr_max = 1;
else
    %Independent
    p = 0.0001;
    dimr = 10;
    dimc = 10;

    snr_min = 0;
    snr_max = 1;
end






Nb = 20;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

savedir =  '/home/xiao/Documents/Simulation/generateRfi/simulation_map/';
if ~exist(savedir, 'dir')
    % Folder does not exist so create it.
    mkdir(savedir);
end


for n = 1:Nb
    nn = n;
    generation_Ising;

%     generation_indep;
    savepath = [savedir , 'sim_map_', num2str(nn),  '.mat'];
    save(savepath,'mapres','L');
end

fig = fopen([savedir + "sim_info.txt"], 'wt');
fprintf(fig, 'generation parameter:\n');
fprintf(fig, 'gran = %g \n', gran);
fprintf(fig, 'p= %f\n' , p);
fprintf(fig, 'Number of iteration = %g\n' , Nmc);
fprintf(fig, 'Dimsion = %g * %g \n' ,Nr,Nc);
fprintf(fig, 'kernel size = %g, %g \n', dimr, dimc);
fprintf(fig, 'snr of kernel = [%g, %g]\n', snr_min, snr_max);
fprintf(fig, 'Numer of sample = %g\n', Nb);
fprintf(fig, 'rfi info: \n');
fclose(fig);



