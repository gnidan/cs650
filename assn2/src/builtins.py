#!/usr/bin/env python
#

def f_icode(S, n, out_v, in_v):
  # S is the symbol collection
  # n is a free variable
  # out_v is the output vector
  # in_v is the input vector
  
  return [
    Do(n), # should this append a loop onto the symbol table?
      Assn(out_v[S.i[0]], 0),
      Do(n),
        Mult(S.r[0], S.i[0], S.i[1]),
        Call(S.f[0], "W", [n, S.r[0]]),
        Mult(S.f[1], S.f[0], in_v[S.i[0]]),
        Mult(out_v[S.i[1]], out_v[S.i[1]], S.f[1]),
      EndDo(),
    EndDo()
    ]





