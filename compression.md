

% Yada Pruksachatkkun 
% Code skeleton from Marcos Bolanos
%Compressive Sensing Example

%This very simple example of L1 minimization is reproduced for
%implementation on matlab. The original example was posted on Rip's Applied
%Mathematics Blog on March 28, 2011 entitled "Compressed Sensing: the L1
%norm finds sparse solutions". 
import l1magic.*
K = 2;
fs = 44100; % Hz
t = 0:1/fs:5; % seconds
f1 = 697;
f2 = 1336;
f4 = 400;
y1 = sin(2.*pi.*f1.*t) + sin(2.*pi.*f2.*t);
y2 =  sin(2.*pi.*f4.*t);
disp(t(1:1000));
s=RandStream('mt19937ar');
len = int64(length(x)/2);
x = cat(1, y1, y2);
A=randn(s,2, K);
 B=A'*x;
 
 new_sound_1 = [];
 new_sound_2 = [];
 for n =1:1000
    b1 = B(1:K,n+1)'; % does not work when b1 is 0 0
    x1 = [0.1, 0.1];
    xp = l1eq_pd(x1', A', 1, b1');   %l1 minimization using L1-MAGIC
    new_sound_1 = [new_sound_1, xp(1)];
    new_sound_2 = [new_sound_2, xp(2)];
 end
subplot(2,2,1);
plot(t(1:1000), y1(1:1000))

subplot(2,2,2);
plot(t(1:1000), new_sound_1(1:1000))


subplot(2,2,3); 
plot(t(1:1000),y2(1:1000));

subplot(2,2,4); 
plot(t(1:1000),new_sound_2(1:1000));

