%%-----------------------------------------------------------------------%%
% Description: err.m                                                      %
%   Compute the error vector for parameters estimation.                   %
%     E = b_esti - (b_esti' * n) * n                                     % 
%                                                                         %
%   Input:  M_esti      3x4 ESTIMATED perspective projection matrix       %
%           T           4x4 homogeneous transformation from b to e        %
%           point_esti  3x1 ESTIMATED point on the 3-D line               %
%           u_esti      3x1 ESTIMATED direction vector of the 3-D line    %
%           n           3x1 line feature from the image                   %
%   Output: E           3x1                                               %
%                                                                         %
% Copyright:   Shanghai SJTU Autonomous Robot Lab.                        %
% Author:      Jay Wang                                                   %
% Version:     Beta 1.0.1                                                 %
% Data:        2015.04.16                                                 %
%%-----------------------------------------------------------------------%%

%%
function E = err(b_esti, n)
E = b_esti - (b_esti.' * n) * n;