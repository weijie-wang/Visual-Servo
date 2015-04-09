%%-----------------------------------------------------------------------%%
% Description: main.m                                                     %
%   An adaptive controller for image-based KINEMATIC control of a robot   %
%   manipulator using a eye-in-hand camera whose intrinsic and extrinsic  %
%   parameters are not known using one point feature.The controller       %
%   controls the pose(position and orientation(YPR)) of end-effectors     %
%   and updata the point estimated positon.                               %
%   Refer to peper: Wang H, Liu Y H, Zhou D.                              %
%   Adaptive visual servoing using point and line features with an        %
%   uncalibrated eye-in-hand camera[J]. Robotics, IEEE Transactions on,   %
%   2008,24(4): 843-857. Note: It uses DYNAMICS.                          %
%                                                                         %
% Copyright:   Shanghai SJTU Autonomous Robot Lab.                        %
% Author:      Jay Wang                                                   %
% Version:     Beta 1.0.1                                                 %
% Data:        2015.04.08                                                 %
%%-----------------------------------------------------------------------%%

%% Initialize Variables
M = [630 0 250 0;0 630 250 0;0 0 1 0];                                      %camera perspective projection matrix KNOWN consist of intrinsic parameters matrix
point_esti = [2; 2; 2];                                                     %point estimated position with respect to base frame
point_real = [1; 1; 0];                                                     %point real position with respect to base frame
endeffector_des = [1.5; 0.9;   1; 3.14; 0.5; 0];                           	%endeffector (frame) desired pose([x y z y p r]) with respect to base frame 
endeffector_cur = [1.1; 1.2; 0.8;  3.2; 0.1; 2];                            %endeffector (frame) current pose([x y z y p r]) with respect to base frame 
t=0.01;                                                                     %interval
k1=0.00001;                                                                 %positive difinite gain matrix
k2=10000;                                                                   %positive difinite gain matrix
k=1;                                                                        %cycle index

temp = M * trans(endeffector_des) * [point_real;1];
yd = [temp(1)/temp(3);temp(2)/temp(3)];                                     %desired position(coordinates) of the feature point on the image plane
plot(yd(1),yd(2),'r*');                                                     %mark it with red *
hold on

temp = M*trans(endeffector_cur)*[point_real;1];
y = [temp(1)/temp(3);temp(2)/temp(3)];                                      %current position(coordinates) of the feature point on the image plane
delta_y = y-yd;                                                             %image error

%% Iteration
while delta_y.'*delta_y > 0.000001
    %% control
    endeffector_trans = trans(endeffector_cur);                             %endeffector (frame) current homogenous transform matrix with respect to base frame
    endeffector_velocity = -k1*ctrl(delta_y, M, endeffector_trans, y, point_esti);%compute the controller (end-effector velocity)                                                                                   
    endeffector_cur = endeffector_cur + endeffector_velocity .* t;          %updata endeffector (frame) current pose          
    %% parameter estimatin
    Y = regressor(delta_y, M, endeffector_trans, y);                        %compute  Y
    gtv = -1/k2 * Y.' * endeffector_velocity;                               %the adaptive rule for the estimation of point position
    point_esti = point_esti + gtv .* t; %WRONG!                             %updata point estimated position
    %% image error
    temp = M * trans(endeffector_cur) * [point_real;1];
    y = [temp(1)/temp(3); temp(2)/temp(3)];                                 %current position(coordinates) of the feature point on the image plane
    plot(y(1), y(2), '.');                                                    
    hold on                                                                 %plot it
    delta_y = y - yd                                                        %image error
    pause(0.1);
    k = k + 1;
end



