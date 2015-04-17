%%-----------------------------------------------------------------------%%
% Description: ctrl.m                                                     %
%   Compute the controller.                                               %
%      joint_velocity = - (L' + 0.5 * C' * delta_n') * k1 * delta_n       %         
%                                                                         %
%   Input:  n               3x1 line feature                              %
%           M               3x4 perspective projection matrix             %                                        %
%           T               4x4 homogeneous transformation from b to e    %
%           point           3x1 point on the 3-D line                     %
%           u               3x1 direction vector of the 3-D line          %
%           J               6x4 Jacobian matrix of the manipulator        %
%           delta_n         3x1 image errors of line feature              %
%   Output: joint_velocity  4x1 joint velocity                            %
%                                                                         %
% Copyright:   Shanghai SJTU Autonomous Robot Lab.                        %
% Author:      Jay Wang                                                   %
% Version:     Beta 1.0.1                                                 %
% Data:        2015.04.16                                                 %
%%-----------------------------------------------------------------------%%

%%
function  joint_velocity = ctrl (n_cur, M_esti, T_cur, point_esti, u_esti, J_cur, delta_n)
L = dpim(n_cur, M_esti, T_cur, point_esti, u_esti, J_cur);
C = c(n_cur, M_esti, T_cur, point_esti, u_esti, J_cur);
joint_velocity = - (L.' + 0.5 * C.' * delta_n.') * delta_n;               %compute the controller (joint velocity)