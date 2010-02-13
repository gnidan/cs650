##### ICodes Module #####
def F(out_v, in_v, vars=("i0","i1","r0","f0","f1")):

  return [Do(n, i0),
          Do(n, i1),
          Assn(out_v[i0]),
            in_loop,
            Mult(r, i0, i1),
            Call(f0, W(n, r)),
            Mult(f1, f0, in_v[i1]),
            Mult(out_v[i0], out_v[i0], f1),
            EndDo(),
            EndDo()]
        return icode
