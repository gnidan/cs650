from icodes import *
from options import *

x = VarIn()
y = VarOut()

icode = F(x, y, 4)
il = ICodeList(icode)

il.unroll()

for i in il.icodes:
    print i
