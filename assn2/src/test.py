#!/usr/bin/env python
# encoding: utf-8

from icode import *
from symbols import *
from options import *
from templates import *
from icodelist import *
import unparser

x = VarIn()
y = VarOut()

icode = F(x, y, 4)
il = ICodeList(icode)

il.unroll()

il.constprop()

print il

opt = Options(unparser.C99())
func = opt.unparser.write_function(opt, il)

print func
