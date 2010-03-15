a = [1 0 0; 0 1 0; 0 0 1]
  b = direct_sum ([1], conj_trans (F(2)))
  D = compose (F(2), [W(3,1); W(3,2)])
  D = D / 2
  c = direct_sum ([1 1; 1 (D (1))], [(D (2))])
  d = direct_sum ([1], F(2))
  e = [1 0 0; 0 1 0; 0 0 1]

  compose (a, compose (b, compose (c, compose (d, e))))

  
