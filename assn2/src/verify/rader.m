%Must implement:
%CONJ_TRANS
%TRANSPOSE (only deals with scalars... can probably safely be the same as CONJ_TRANS)
%G
%WG --
%D -- can be SPL or icode
%E -- should take SPL as input, call it, and add the 3 1's.
function ans = rader(n, g1, g2)

%0, 1, 3 4 2
%G1 = [ 1 0 0 0 0; 0 1 0 0 0; 0 0 0 1 0; 0 0 0 0 1; 0 0 1 0 0 ];

DFT1 = direct_sum( 1, conj_trans(F(n-1)) );

%The D Matrix takes as parameters g1 and F
D = diagonal( scale(compose( F(n-1), WG(n, g1) ), 1/(n-1)));

%This should be in icode... easy to write up!
E = direct_sum(1, D);
E(1,2) = 1;
E(2,1) = 1;

DFT2 = direct_sum(1, F(n-1));

%0, 1, 2, 4, 3
%G2 = [1 0 0 0 0; 0 1 0 0 0; 0 0 1 0 0; 0 0 0 0 1; 0 0 0 1 0];

ans = compose(rpermutation(G(n, g1)), compose(DFT1, compose(E, compose(DFT2, permutation(G(n, g2))))));
%ans=ws;
