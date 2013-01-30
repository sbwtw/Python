#!/usr/bin/python

import cPickle as p

shoplistfile='/tmp/shoplist.data'

shoplist=['apple','mango','carrot']

f=file(shoplistfile,'w')
p.dump(shoplist,f)
f.close()

del shoplist

f=file(shoplistfile)
storedlist=p.load(f)
print storedlist
