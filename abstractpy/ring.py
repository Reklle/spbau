from cat import ICat
from cat import finite


#
#   Here is an another sample of creation small categories
#


@finite(supord=2)
class Grp(ICat):
    tags = ['Grp']


def grp(table_0, table_1):
    grp = Grp()
    grp.ord = len(table_0[0, :])
    grp.cayley_table_0 = table_0
    grp.cayley_table_0 = table_1
