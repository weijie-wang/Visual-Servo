%%-----------------------------------------------------------------------%%
% Description: skewsymmetric.m                                            %
%   Compute the skew-symmetric matrix of a vector                         %
%                                                                         %
%    p(t) = R(t) * q                 q ---- a constant vector             %
%                                    R(t) ---- a rotation matrix          %
%    d[p(t)]/dt = d[R(t)]/dt * q                                          %
%    d[p(t)]/dt = sk(t) * R(t) * q                                        %
%    d[p(t)]/dt = w(t) x R(t) * q                                         %
%    w(t) = [wx; wy; wz] donates the angular velocity of frame R(t)       %
%    justify the expression:                                              %
%    sk(t) = sk(w(t)) = |  0 -wz   wy|                                    %
%                       | wz   0  -wx|                                    %
%                       |-wy  wx    0|                                    %
%                                                                         %
%   Input:  w = [wx; wy; wz]   3x1                                        %
%           A vector donates the angular velocity of frame R(t)           %                                            
%   Output: sk              3x3 skew-symmetric matrix of a vector         %
%                                                                         %
% Copyright:   Shanghai SJTU Autonomous Robot Lab.                        %
% Author:      Jay Wang                                                   %
% Version:     Release 1.0.1                                              %
% Data:        2015.04.12                                                 %
%%-----------------------------------------------------------------------%%

%%
function sk = skewsymmetric( w )
x=w(1);y=w(2);z=w(3);
sk = [ 0, -z,  y;
       z,  0, -x;
      -y,  x,  0];