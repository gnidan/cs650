%Must implement:
%CONJ_TRANS
%TRANSPOSE (only deals with scalars... can probably safely be the same as CONJ_TRANS)
%G
%WG -- 
%D -- should take SPL as an argument to call for it's F call
function ans = rader(n, g1, g2)

%0, 1, 3 4 2
%G1 = [ 1 0 0 0 0; 0 1 0 0 0; 0 0 0 1 0; 0 0 0 0 1; 0 0 1 0 0 ];
G1 = G(n, g1);

DFT1 = direct_sum( 1, conj_trans(F(n-1)) );

%The D Matrix takes as parameters g1 and F
D = direct_sum(1, diagonal( scale(compose( F(n-1), WG(n, g1) ), 1/(n-1))));
D(1,2) = 1;
D(2,1) = 1;

DFT2 = direct_sum(1, F(n-1));

%0, 1, 2, 4, 3
%G2 = [1 0 0 0 0; 0 1 0 0 0; 0 0 1 0 0; 0 0 0 0 1; 0 0 0 1 0];
G2 = G(n, g2);

ans = compose(transpose(G1), compose (DFT1, compose (D, compose (DFT2, G2))));
%ans=ws;
