  a = [1 0 0 0 0; 0 1 0 0 0; 0 0 0 0 1; 0 0 1 0 0; 0 0 0 1 0]
  b = direct_sum ([1], conj_trans (F(4)))
  D = compose (F(4), [W(5,1); W(5,3); W(5,4); W(5,2)])
  D = D / 4
  c = direct_sum ([1 1; 1 (D (1))], [(D (2)) 0 0; 0 (D (3)) 0; 0 0 (D (4))])
  d = direct_sum ([1], F(4))
  e = [1 0 0 0 0; 0 1 0 0 0; 0 0 1 0 0; 0 0 0 0 1; 0 0 0 1 0]

  compose (a, compose (b, compose (c, compose (d, e))))

  
