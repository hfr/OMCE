#!/usr/bin/env python
# -*- coding: latin-1 -*-
#-----------------------------------------------------
#
# Open Monte Carlo Engine Daemon wrapper
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
# 1.0.0  2011-02-15 Rüdiger Kessel: module creation
#-----------------------------------------------------
VERSION="1.0.0"
PROGID="OMCE Daemonn (OMCEd V:"+VERSION+")"
AUTHOR="Author: Ruediger Kessel (ruediger.kessel@nist.gov)"
#-----------------------------------------------------
OMCED_PID_FILE = 'omced.pid'
OMCED_CONFIG_FILE = 'OMCEd_config'

import warnings
warnings.simplefilter("ignore",DeprecationWarning)
import sys
import os
from OMCEserver import ServerMain
from OMCEbase import UnQuote, get_main_dir, run_main

def ReadOptionFile(fn,warn=True):
    '''
    Reads a list of options from a text file
      fn: file name
      return: list of well formed option strings
    '''
    L=[]
    if os.path.isfile(fn):
        f=open(fn,'r')
        while True:
            line=f.readline().strip()
            if line=="":
                break
            if line=="\n":
                continue
            if line.find("#")==0:
                continue
            if line.find("-")==0:
                L=L+list(UnQuote(line))
                continue
            print 'Warning: option line ""%s"" ("%s") not well formed, line is ignored!' % (line,fn)
        f.close()
    else:
        if warn and (fn!=''):
            print 'Warning: config file "%s" cannot be found!' % fn
    return L

def main():
    cmdargv=list(sys.argv[1:])
    cfg=''
    if '--config' in cmdargv:
        i=cmdargv.index('--config')
        if len(cmdargv)>i+1:
            cfg=cmdargv[i+1]
            del cmdargv[i]
        else:
            print 'Warning: config file is not given after option --config'
        del cmdargv[i]
    if cfg=='':
        cfg=os.path.join(get_main_dir(),OMCED_CONFIG_FILE)
    argv=sys.argv[0:1]+['--Q']+ReadOptionFile(cfg)
    argv = argv + cmdargv
    pidfile = open(OMCED_PID_FILE, 'w')
    pidfile.write("%s" % os.getpid())
    pidfile.write("%s" % os.getcwd())
    ExitCode=run_main(ServerMain,argv,False)
    return ExitCode

if __name__ == "__main__":
    if os.name=='nt':
        main()
        sys.exit()
    else:
        import daemon
        context = daemon.DaemonContext(stdout=sys.stdout,
                                       stderr=sys.stderr,
                                       working_directory=os.getcwd()
                                       )
        with context:
            main()
        sys.exit()
#[EOF]

