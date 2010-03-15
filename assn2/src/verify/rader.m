%Must implement:
%CONJ_TRANS -- this is just a conjugate(transpose(A))... no need for new symbol
%TRANSPOSE (only deals with scalars... can probably safely be the same as CONJ_TRANS)
%G -- this can be implemented in the SPL generator ... it is just a permutation array
%WG -- 
%E -- should take SPL as input, call it, and add the 3 1's.
function ans = rader(n, g1, g2)

DFT1 = direct_sum( 1, transpose(conj((F(n-1)))) );

e = E(diagonal(scale(compose( F(n-1), WG(n, g1) ), 1/(n-1))) );

DFT2 = direct_sum(1, F(n-1));

ans = compose(rpermutation(G(n, g1)), compose(DFT1, compose(e, compose(DFT2, permutation(G(n, g2))))));
