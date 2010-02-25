from icode import *
from symbols import *
from options import *
from templates import *
from icodelist import *

x = VarIn()
y = VarOut()

icode = F(x, y, 4)
il = ICodeList(icode)

il.unroll()

il.constprop()

for i in il.icode:
    print i

opt = Options()
lang = opt.language()

func = lang.write_function(opt, il)
