%%-----------------------------------------------------------------------%%
% Description: main.m                                                     %
%   An adaptive controller for image-based KINEMATIC control of a robot   %
%   manipulator using a eye-in-hand camera whose intrinsic and extrinsic  %
%   parameters are not known using 2 line features.The controller         %
%   controls the pose(position and orientation(YPR)) of end-effectors     %
%   and updata the point estimated positon.                               %
%   Refer to peper: Wang H, Liu Y H, Zhou D.                              %
%   Adaptive visual servoing using point and line features with an        %
%   uncalibrated eye-in-hand camera[J]. Robotics, IEEE Transactions on,   %
%   2008,24(4): 843-857. Note: It uses DYNAMICS.                          %
%                                                                         %
% Copyright:   Shanghai SJTU Autonomous Robot Lab.                        %
% Author:      Jay Wang                                                   %
% Version:     realse 1.0.1                                               %
% Data:        2015.04.19                                                 %
%%-----------------------------------------------------------------------%%

%% Initialize Variables
omega_real = [630 0 250 0;0 630 250 0;0 0 1 0];                             %camera intrinsic parameters matrix REAL
T_real = [1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1];                              %camera extrinsic parameters matrix REAL
M_real = omega_real * T_real;                                               %camera perspective projection matrix REAL consist of extrinsic and intrinsic parameters matrix

omega_esti = [600 0 200 0;0 600 200 0;0 0 1 0];                             %camera intrinsic parameters matrix ESTIMATED
% omega_esti = [630 0 250 0;0 630 250 0;0 0 1 0];
T_esti = [1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1];                              %camera extrinsic parameters matrix ESTIMATED
% T_esti = [1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1];
M_esti = omega_esti * T_esti;                                               %camera perspective projection matrix ESTIMATED consist of extrinsic and intrinsic parameters matrix

L(1) = Link([0 0.7   0   pi/2   0]);
L(2) = Link([0   0  -1      0   0]);
L(3) = Link([0   0   0  -pi/2   0]);
L(4) = Link([0 0.3   0      0   0]);
Doves = SerialLink(L, 'name', 'Doves');
Doves.base = transl([0 0 0.7])*trotx(pi);
Doves.offset = [0 -pi 0 0];                                                 %initialize the robot kinectics

joint_des = [0; 0; 0; 0];                                                   %joint (frame) current pose 
joint_cur = [pi/6; -pi/6; pi/6; 0];                                         %joint (frame) current pose
u_real = [1; 0; 0];                                                         %unit direction vector of line REAL
point_real = [1; 0; 2];                                                     %one point on the line REAL
u_esti = [cos(pi/18); 0; sin(pi/18)];                                       %unit direction vector of line ESTIMATED
% u_esti = [1; 0; 0];  
point_esti = [1; 0; 2];                                                     %one point on the line ESTIMATED

b_des = cross(M_real / Doves.fkine(joint_des') * [point_real; 1], M_real / Doves.fkine(joint_des') * [u_real; 0]); 
n_des = b_des/sqrt(sum(b_des' * b_des));                                    %perspective projecion of line DESIRED 
figure(1);
plot3(n_des(1), n_des(2), n_des(3), 'r*');       
hold on                                                                     %plot it
b_cur = cross(M_real / Doves.fkine(joint_cur') * [point_real; 1], M_real / Doves.fkine(joint_cur') * [u_real; 0]); 
n_cur = b_cur/sqrt(sum(b_cur' * b_cur));                                    %perspective projecion of line CURRENT 
delta_n = n_cur - n_des;                                                    %image error

t=0.01;                                                                     %interval
k1=1;                                                                       %positive difinite gain matrix for joint_velocity                                                             
k3=100000;                                                                  %positive difinite gain matrix for Theta_integral   
k4=100000;                                                                  %positive difinite gain matrix for Theta_velocity
time=0;                                                                     %cycle index
k = 1;

Theta_esti = theta(M_esti, point_esti, u_esti);                             %parameters ESTIMATED
Theta_real = theta(M_real, point_real, u_real);                             %parameters REAL

E_esti = zeros(3,1);                                                        %e(tj)
E_coe = zeros(3,216);                                                       %e(tj) = E_coe * Theta_esti
W = zeros(3,216);                                                           %e(tj) = W * Theta_delta
Theta_integral = zeros(216,1);                                              %Theta_integral =  W.' * k3 * E_esti;

j_velocity = [];                                                            %for plot
T_velocity = [];                                                            %for plot
E_velocity = [];                                                            %for plot

%% Iteration
while delta_n.'*delta_n > 0.00000000001
    %% control
    T_cur = Doves.fkine(joint_cur');
    T_cur = inv(T_cur);                                                     %homogenous transformation from base to end_effertor
    J_cur = Doves.jacob0(joint_cur');                                       %Jacobian now
    Y = regressor(n_cur, T_cur, J_cur, delta_n);                            %negative regressor matrix
    joint_velocity = - k1 * Y * Theta_esti;                                 %joint velocity
    j_velocity =  [j_velocity, joint_velocity];                             %for plot
    joint_cur = joint_cur + joint_velocity .* t;                            %updata endeffector (frame) current pose          
    %% parameter estimatin    
    Theta_delta = Theta_esti - Theta_real;                                  %delta unknown parameters
    if k == 10
        W = w(T_cur, n_cur);
        E_coe = err(T_cur, n_cur);
    end                                                                     %get a image for error vector e
    E_esti = E_coe * Theta_esti;                                            %e(tj)
    E_velocity = [E_velocity, E_esti];                                      %for plot
    E1 = W * Theta_delta;                                                   %test e(tj) is right?  In theory : E1 = E_esti 
    Theta_integral =  W.' * k3 * E_esti;    
    Theta_velocity = - 1 / k4 * ((-Y).' * joint_velocity + Theta_integral); %the adaptive rule for the estimation of point position      
    T_velocity = [T_velocity,Theta_velocity];                               %for plot
    Theta_esti = Theta_esti + Theta_velocity .* t;                          %updata parameters estimated     
    %% image error
    b_cur = cross(M_real / Doves.fkine(joint_cur') * [point_real; 1], M_real / Doves.fkine(joint_cur') * [u_real; 0]);  
    n_cur = b_cur/sqrt(sum(b_cur' * b_cur));                                %perspective projecion of line CURRENT 
    figure(1);
    plot3(n_cur(1), n_cur(2), n_cur(3), '.');       
    hold on;                                                                %plot it
    delta_n = n_cur - n_des;                                                %image error
    pause(0.1);
    time = time + t;
    k = k + 1;
end



