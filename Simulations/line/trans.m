%%-----------------------------------------------------------------------%%
% Description: trans.m                                                    %
%   Compute the homogeneous transformation matrix from base frame to      %
%   end-effect frame                                                      %
%               T = | R'   -R'*t |   R ---- rotation matrix(trans b to e) %
%                   | 0'      1  |   t ---- transplational vector         %
%                                                                         %
%   Input:  X = [x y z y p r]   6x1                                       %
%           A vector consist of Pose position and orientation(YPR)        %                                            
%   Output: T           4x4 homogeneous transformation matrix             %
%                                                                         %
% Copyright:   Shanghai SJTU Autonomous Robot Lab.                        %
% Author:      Jay Wang                                                   %
% Version:     Release 1.0.1                                              %
% Data:        2015.04.09                                                 %
%%-----------------------------------------------------------------------%%

%%
function T=trans(X)
x=X(1);y=X(2);z=X(3);a=X(4);b=X(5);c=X(6);
T=[                        cos(b)*cos(c),                        cos(b)*sin(c),       -sin(b),                                                          z*sin(b) - x*cos(b)*cos(c) - y*cos(b)*sin(c);
    cos(c)*sin(a)*sin(b) - cos(a)*sin(c), cos(a)*cos(c) + sin(a)*sin(b)*sin(c), cos(b)*sin(a), x*cos(a)*sin(c) - y*cos(a)*cos(c) - z*cos(b)*sin(a) - x*cos(c)*sin(a)*sin(b) - y*sin(a)*sin(b)*sin(c);
    sin(a)*sin(c) + cos(a)*cos(c)*sin(b), cos(a)*sin(b)*sin(c) - cos(c)*sin(a), cos(a)*cos(b), y*cos(c)*sin(a) - z*cos(a)*cos(b) - x*sin(a)*sin(c) - x*cos(a)*cos(c)*sin(b) - y*cos(a)*sin(b)*sin(c);
    0,                                                                       0,             0,                                                                                                     1];

