#!/usr/bin/env python
# -*- coding: latin-1 -*-
#-----------------------------------------------------
#
# Open Monte Carlo Engine
#
# Author: Ruediger Kessel
#         National Institute of Standards and Technology (NIST)
#
# Disclaimer:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the
# course of their official duties. Pursuant to title 17 Section 105
# of the United States Code this software is not subject to
# copyright protection and is in the public domain. This software is
# experimental. NIST assumes no responsibility whatsoever for its
# use by other parties, and makes no guarantees, expressed or
# implied, about its quality, reliability, or any other
# characteristic. We would appreciate acknowledgement if the
# software is used.
#-----------------------------------------------------
#-----------------------------------------------------
# 1.0.0  2011-02-18 Rüdiger Kessel: Module created
#-----------------------------------------------------
VERSION="1.0.0"
PROGID="OMCE Result Compare Tool (OMCEcomp V:"+VERSION+")"
AUTHOR="Author: Ruediger Kessel (ruediger.kessel@nist.gov)"
#-----------------------------------------------------
from OMCEbase import *

def InitOptions():
    opts={}
    specs={}
    #specs: [<type>,<min>,<max>,<default>,<comment>]
    #       type: 'i'|'f'|'s'  (integer, float, string)
    #       min: minimum value or number of char
    #       max: maximum value or number of char
    maxi=sys.maxint
    maxf=10E38
    specs['-sid']=['s',0,255,':', 'range of simulation ID values which should be plotted']
    specs['-sym']=['s',0,255,'*', 'filter of symbols which should be plotted']
    specs['-v'  ]=['i',0,10,2,    'verbose level 0..10: all..nothing']
    specs['-asc']=['s',0,255,     'SID,ID,Symbol,Unit,Definition', 'Text only columns definition']
    specs['-cfg']=['s',0,255,'OMCEcomp.cfg','name of the configuration file']
    specs['-lim']=['f',0,1,1E-11, 'numerical tolerance for comparison']
    for skey in specs.keys():
        opts[skey]=specs[skey][3]
    return opts,specs

def Info(opts,specs):
    PRINT("Error: missing input file names!\n")
    PRINT("Usage: OMCEcomp <ohd-filename-1> <ohd-filename-2> [Options]")
    PRINT("Options:")
    PRINT(GetOptionInfo(opts,specs))
    PRINT("")
    PRINT("Exit Codes:")
    PRINT(GetErrors())
    PRINT("")
    PRINT(GetDisclaimer())
    PRINT("\nPress Enter...")
    sys.stdin.read(1)
    sys.exit()
    return

def CompRel(a,b):
    if a==b:
        return 0.0
    if a>b:
        b,a = a,b
    return (float(b)/float(a))-1

def IsEqLim(opts,a,b):
    return CompRel(a,b) < opts['-lim']

def Compare(filenames,exepath,options):
    opts,specs=InitOptions()
    SetOptionsOf(opts,specs,options)
    opts['-sym']=opts['-sym'].split(',')
    for i in xrange(len(opts['-sym'])):
        opts['-sym'][i]=opts['-sym'][i].strip()
    opts['-asc']=opts['-asc'].split(',')
    for i in xrange(len(opts['-asc'])):
        opts['-asc'][i]=opts['-asc'][i].strip()
    if len(filenames) != 2:
        Info(opts,specs)
    opts['PATH']=exepath
    for fn in filenames:
        CheckFile(DefConText,fn)
    opts['filenames']=filenames
    rdata=[]
    for i in xrange(len(filenames)):
        rdata.append(ResultDataClass())
        PRINT('Reading data file: '+filenames[i])
        rdata[i].readCSV(filenames[i])
        rdata[i].setsidfilter(opts['-sid'])
    for i in xrange(1,len(filenames)):
        if rdata[0].rowcount != rdata[i].rowcount:
            ERROR(83,rdata[0].rowcount,rdata[i].rowcount)
        if rdata[0].colcount != rdata[i].colcount:
            ERROR(84,rdata[0].colcount,rdata[i].colcount)
        for row in xrange(rdata[0].rowcount):
            for col in xrange(rdata[0].colcount):
                cn=rdata[0].colnames[col]
                if cn in opts['-asc']:
                    eq=rdata[0].entry(row,cn)==rdata[i].entry(row,cn)
                else:
                    if rdata[0].entry(row,cn)!=rdata[i].entry(row,cn):
                        PRINT('Warning: Content Column %s, Row %s does not match ("%s" != "%s")' % (rdata[0].colnames[col],row,rdata[0].entry(row,cn),rdata[i].entry(row,cn)))
                    eq=IsEqLim(opts,rdata[0].entryf(row,cn),rdata[i].entryf(row,cn))
                    rdiff=CompRel(rdata[0].entryf(row,cn),rdata[i].entryf(row,cn))
                    if rdiff != 0.0:
                        PRINT('Warning: Values Column %s, Row %s differ relative by %s)' % (rdata[0].colnames[col],row,rdiff))
                if not eq:
                    ERROR(85,rdata[0].colnames[col],row,rdata[0].entry(row,cn),rdata[i].entry(row,cn))
    PRINT('Files match.')

def MAIN(argv):
    INIT_IO()
    path=get_main_dir()
    cfgfile=''
    for prm in argv[1:]:
        if prm[0:3]=="-v=":
            o=prm.split('=')
            if len(o)==2:
                DefConText.VerboseLevel=int(o[1])
        elif prm[0:5]=="-cfg=":
            o=prm.split('=')
            if len(o)==2:
                cfgfile=os.path.join(path,o[1])
    if cfgfile=='':
        cfgfile=os.path.splitext(argv[0])[0]+'.cfg'
    PRINT(PROGID)
    PRINT(AUTHOR)
    PRINT('Config file: '+cfgfile,VL_Noise)
    options=ReadOptionFile(DefConText,cfgfile,False)
    filenames=[]
    for prm in argv[1:]:
        if prm[0:1]=="-":
            options.append(prm)
        else:
            filenames.append(prm)
    exepath=get_main_dir()
    Compare(filenames,exepath,options)
    return

if __name__=="__main__":
    DefConText.StopQueue()
    ExitCode=run_main(MAIN,sys.argv)
    sys.exit(ExitCode)
