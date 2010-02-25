from icode import *
from ivars import *
from options import *

x = VarIn()
y = VarOut()

icode = F(x, y, 4)
il = ICodeList(icode)

il.unroll()

il.constprop()

for i in il.icodes:
    print i
