#!/usr/bin/env python
# -*- coding: latin-1 -*-
#-----------------------------------------------------
#
# Open Monte Carlo Engine Client
#
# Author: Rüdiger Kessel
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
# 1.0.0 2011-02-11 Rüdiger Kessel: module created
#-----------------------------------------------------
__version__="1.0.0"
__MODID__="OMCE Client (OMCEclient V:"+__version__+")"
__AUTHOR__="Author: Rüdiger Kessel (ruediger.kessel@nist.gov)"
#-----------------------------------------------------
import warnings
warnings.simplefilter("ignore",DeprecationWarning)
from OMCEbase import *
import rpyc
import os
import tlslite
import tlslite.errors
from tlslite.errors import TLSRemoteAlert

error[251]=["Server service version (%s) does not match client service version (%s)!",['<ver>','<ver>']]

def Client(argv):
    cfg_filename=''
    CP=''
    argv=list(argv)
    for prm in argv:
        if prm[0:6]=="--cfg=":
            o=prm.split('=')
            if len(o)==2:
                cfg_filename=DefConText.PathJoin(get_main_dir(),DefConText.STR(o[1]))
    if cfg_filename=='':
        cfg_filename=os.path.splitext(sys.argv[0])[0]+'.cfg'
    argv=ReadOptionFile(DefConText,cfg_filename,False)+argv
    options=argv
    port=DefServerPort
    server="localhost"
    argv=[]
    user=''
    passw=''
    tls=False
    for opt in options:
        if opt[0:2]=="--":
            if opt[0:7]=="--port=":
                o=opt.split('=')
                if (len(o)==2) and isInt(o[1]):
                    port=int(o[1])
            elif opt[0:9]=="--server=":
                o=opt.split('=')
                if (len(o)==2):
                    server=DefConText.STR(o[1])
            elif opt[0:7]=="--user=":
                o=opt.split('=')
                if (len(o)==2):
                    user=DefConText.STR(o[1])
            elif opt[0:7]=="--pass=":
                o=opt.split('=')
                if (len(o)==2):
                    passw=DefConText.STR(o[1])
        else:
            argv.append(opt)
            if opt[0:3]=="-v=":
                o=opt.split('=')
                if len(o)==2:
                    DefConText.VerboseLevel=int(o[1])
    if (user!='') or (passw!=''):
        tls=True
    DefConText.NOISE('Server-Argv: '+DefConText.STR(argv))
    if not tls:
        DefConText.PRINT('Connecting OMCE-Server on %s port %s...' % (server,str(port)),VL_Info)
        c = rpyc.connect(server, port)
    else:
        DefConText.PRINT('Connecting OMCE-Server via TLS on %s port %s...' % (server,str(port)),VL_Info)
        DefConText.NOISE('User: %s password: "%s"' % (user,passw))
        c = rpyc.tls_connect(server, port, user, passw)
    try:
        SVRSV=c.root.ServiceVersion()
        DefConText.NOISE('ServiceVersion: '+SVRSV)
    except:
        SVRSV='0.0.0'
        DefConText.NOISE('ServiceVersion: *** not available ***')
    if SVRSV!=SERVICEVERSION:
        DefConText.ERROR(251,SVRSV,SERVICEVERSION)
    path=get_main_dir()
    modname=DefConText.PathJoin(path,'OMCE')
    argv[0]=modname+'.py'
    functab={'write':DefConText.WRITE,
             'read':DefConText.READ,
             'isfile':DefConText.IsFile,
             'readfile':DefConText.ReadFile,
             'writefile':DefConText.WriteFile,
             'readbinfile':DefConText.ReadBinFile,
             'joinpath':DefConText.PathJoin,
             'setdeftext':DefConText.SetDefExt,
             'dirpath':DefConText.DirPath,
             'splitext':DefConText.SplitExt}
    DefConText.NOISE('Calling OMCE...')
    try:
        ret = c.root.OMCE(argv,path,modname,functab)
    finally:
        c.close()
    return ret

if __name__=="__main__":
    DefConText.StopQueue()
    ExitCode=run_main(Client,sys.argv)
    sys.exit(ExitCode)

#[EOF]]