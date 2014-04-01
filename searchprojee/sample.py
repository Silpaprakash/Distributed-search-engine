from models import *

lookup=raw_input("enter a lookup keyword")

print index_tbl.objects.filter(key__startswith=lookup)
