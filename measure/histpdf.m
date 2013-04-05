run=load('run.dat');
ct=run(:,1);
plot_counts_instead_of_frequencies = 1;
nb_bar = 11;
m=mean(ct);
s=std(ct);
h=hist(ct, nb_bar); 
t = linspace(min(ct), max(ct), nb_bar);
tlarge = linspace(min(ct), max(ct), 4*nb_bar);
freq_scale = normpdf(m, m, s)/max(h);
count_scale = 1/freq_scale;
if plot_counts_instead_of_frequencies
	sv = [t' count_scale*normpdf(t,m,s)' h'];
	svpdf = [tlarge' count_scale*normpdf(tlarge,m,s)'];
else
	sv = [t' normpdf(t,m,s)' freq_scale*h'];
	svpdf = [tlarge' normpdf(tlarge,m,s)'];
end
name_num = '1.dat';%strcat(int2str(randi(2**17)), '.dat');
save('-ascii', strcat('hist-', name_num), 'sv');
save('-ascii', strcat('pdf-', name_num), 'svpdf');
%if plot_counts_instead_of_frequencies
%	bar(t, h); 
%else
%	bar(t, freq_scale*h);
%end
%hold on; 
%if plot_counts_instead_of_frequencies
%	plot (t, count_scale*normpdf(t,m,s)); 
%else
%	plot (t, normpdf(t,m,s)); 
%end
%hold off;
