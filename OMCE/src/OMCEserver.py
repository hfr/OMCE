#!/usr/bin/env python
# -*- coding: latin-1 -*-
#-----------------------------------------------------
#
# Open Monte Carlo Engine Server wrapper
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
# 1.0.0  2011-02-22 Rüdiger Kessel: module creation
#-----------------------------------------------------
#
__version__="1.0.0"
__MODIDstr__="OMCE Server (OMCE V:%s)"
__MODID__=__MODIDstr__ % __version__
__AUTHOR__="Author: Ruediger Kessel (ruediger.kessel@nist.gov)"
#-----------------------------------------------------
import warnings
warnings.simplefilter("ignore",DeprecationWarning)
import sys
import os
from OMCEbase import UnQuote, get_main_dir, SERVICE_VERSION, ConText, DefConText
from OMCEbase import Error, Terminate, SERVICEVERSION, MSG, DefServerPort, run_main
from OMCEbase import VL_Error, VL_Warn, VL_Startup, VL_Finish, VL_Progress, VL_Time
from OMCEbase import VL_Info, VL_Default, VL_Details, VL_Noise
from OMCEbase import OMCEAuthenticator, OMCEForkingServer, OMCEThreadedServer, OMCElogger
from OMCEbase import isInt, msg, ReadOptionFile
import tlslite.api
import tlslite
import rpyc
if False:
    import dbhash
    import dumbdbm
import anydbm
import thread as TH
import re
Simulator=None

class OMCEService(rpyc.Service):
    ALIASES = ["OMCE-"+SERVICE_VERSION, "OMCE"]
    _ClientID=0
    SimulationID=0
    RunningSimulations=0
    LOCK=TH.allocate_lock()
    Server=None
    Fork=False
    Imports="imports"
    def IncClientID(self):
        OMCEService.LOCK.acquire()
        OMCEService._ClientID+=1
        self._ClientID=OMCEService._ClientID
        OMCEService.LOCK.release()
        return
    def SetSimIDStr(self):
        if OMCEService.Fork:
            self.SimIDStr=''
        else:
            self.SimIDStr=str(self.SimulationID)+' '
        return
    def on_connect(self):
        self.IncClientID()
        self.exposed_namespace = {}
        return

    def on_disconnect(self):
        pass

    def exposed_OMCE(self,argv,path,modname,functab):
        OMCEService.LOCK.acquire()
        OMCEService.RunningSimulations+=1
        OMCEService.SimulationID+=1
        self.SimulationID=OMCEService.SimulationID
        self.SetSimIDStr()
        OMCEService.LOCK.release()
        self.Server.logger.info("starting simulation %s", self.SimIDStr)
        context=ConText(functab)
        context.IsServer=True
        context.Imports=os.path.join(get_main_dir(),OMCEService.Imports)
        ExitCode=0
        try:
            try:
                try:
                    Simulator(argv,context,path,modname,True)
                except Error,er:
                    errmsg=DefConText.ERRORMSG(er.number,*er.params)
                    self.Server.logger.info("simulation %sterminated with Error %s", self.SimIDStr,errmsg)
                    context.ERROR(er.number,*er.params)
            except Terminate,te:
                ExitCode = te.code
        except Exception,e:
            context.PRINT(context.ERRORMSG(255,'\nFatal Error: '+context.STR(e)+"!"),VL_Error)
            context.PRINT(context.MSG(1,'Service'),VL_Error)
            self.Server.logger.info("simulation %sterminated with exception %s", self.SimIDStr,str(e))
            ExitCode=255
        context.EmptyQueue()
        OMCEService.LOCK.acquire()
        OMCEService.RunningSimulations-=1
        OMCEService.LOCK.release()
        self.Server.logger.info("completing simulation %s(exit code: %s)", self.SimIDStr,ExitCode)
        return ExitCode

    def exposed_RunningSimulations(self):
        OMCEService.LOCK.acquire()
        rs=OMCEService.RunningSimulations
        OMCEService.LOCK.release()
        return rs

    def exposed_TotalSimulations(self):
        OMCEService.LOCK.acquire()
        ts=OMCEService.SimulationID
        OMCEService.LOCK.release()
        return ts

    def exposed_ClientID(self):
        OMCEService.LOCK.acquire()
        cid=self._ClientID
        OMCEService.LOCK.release()
        return cid

    def exposed_ServiceVersion(self):
        return SERVICEVERSION

def StartServer(port, ar=False, host='0.0.0.0', fork=False, quiet=False, vdbn='', tls=False):
    global Simulator
    from OMCE import Simulator
    from OMCE import __version__ as OMCEversion
    if quiet:
        console=None
    else:
        DefConText.PRINT(__MODIDstr__  % OMCEversion,VL_Startup)
        DefConText.PRINT(__AUTHOR__,VL_Startup)
        console = sys.stderr
    at=None
    if (vdbn!='') or tls:
        if vdbn=='':
            UL={tls[0]:tls[1]}
            DefConText.NOISE('Using simple TLS with user "'+UL.keys()[0]+'" and password "'+UL[UL.keys()[0]]+'"')
            at = OMCEAuthenticator.from_dict(UL)
        else:
            DefConText.NOISE('Using VDB ('+vdbn+')')
            at = OMCEAuthenticator.from_file(vdbn,'r')
        at.bypass_known_ip=True
    DefConText.NOISE(DefConText.MSG(104))
    logger=OMCElogger(OMCEService.ALIASES[0],show_tid = True,console = console,file=DefConText.logfile)
    DefConText.logfile=None
    if fork:
        OMCEService.Server = OMCEForkingServer(OMCEService, port = port, auto_register = ar, hostname=host, logger = logger, authenticator = at)
    else:
        OMCEService.Server = OMCEThreadedServer(OMCEService, port = port, auto_register = ar, hostname=host, logger = logger, authenticator = at)
    if DefConText.VerboseLevel>VL_Details:
        logger.filter=set(["TRACEBACK"])
    if DefConText.VerboseLevel>VL_Info:
        logger.filter=set(["TRACEBACK","INFO"])
    if DefConText.VerboseLevel>VL_Warn:
        logger.filter=set(["TRACEBACK","INFO","WARNING"])
    OMCEService.Fork=fork
    try:
        OMCEService.Server.start()
    finally:
        DefConText.logfile=logger.file
        logger.file=None
    return

def EditVDB(vdbn,um,usefile=True):
    def DoEdit(um):
        if um[1]=='list':
            at = OMCEAuthenticator.from_file(vdbn,'r')
            DefConText.PRINT('Users in "%s":' % vdbn)
            for un in at.list_users():
                DefConText.PRINT(un)
        else:
            at = OMCEAuthenticator.from_file(vdbn,'w')
            if um[1]=='addfile':
                if len(um)!=3:
                    DefConText.ERROR(76,'addfile')
                fn=um[2]
                if not os.path.isfile(fn):
                    DefConText.ERROR(2,fn)
                DefConText.PRINT('Processing "%s":' % fn)
                unf=open(fn,'r')
                cs=unf.read()
                ls=cs.split('\n')
                for cl in ls:
                    un=cl.split(' ')[0]
                    pssw=cl[len(un):].strip()
                    try:
                        pssw=UnQuote(pssw)[0]
                    except:
                        raise Error(81,pssw)
                    if un!='':
                        if pssw=='':
                            DefConText.PRINT(MSG(105,un))
                        DefConText.PRINT("Adding %s" % un)
                        at.set_user(un,pssw)
            elif um[1]=='add':
                if len(um)!=4:
                    DefConText.ERROR(76,'add')
                if (um[2].strip()=='') or (um[3]==''):
                    DefConText.ERROR(80)
                at.set_user(um[2].strip(),um[3])
            elif um[1]=='del':
                if len(um)!=3:
                    DefConText.ERROR(76,'del')
                try:
                    at.del_user(um[2].strip())
                except:
                    DefConText.ERROR(79,um[2],vdbn)
            else:
                DefConText.ERROR(78,um[1])
            at.sync()
        return
    if vdbn=='':
        DefConText.ERROR(75)
    if len(um)<2:
        DefConText.ERROR(77,'--USER')
    DoEdit(um)
    return

def ServerMain(argv=[],usecfg=True):
    cfg_filename=''
    CP=''
    argv=list(argv)
    if usecfg:
        for prm in argv[1:]:
            if prm[0:6]=="--CFG=":
                o=prm.split('=')
                if len(o)==2:
                    cfg_filename=DefConText.PathJoin(get_main_dir(),DefConText.STR(o[1]))
        if cfg_filename=='':
            cfg_filename=os.path.splitext(sys.argv[0])[0]+'.cfg'
        argv=argv[0:1]+ReadOptionFile(DefConText,cfg_filename)+argv[1:]
    for prm in argv[1:]:
        if prm[0:5]=="--CP=":
            o=prm.split('=')
            if len(o)==2:
                CP=str(o[1])
    if CP!='':
        DefConText.CodePage=CP
    DefConText.PRINT('Config file: '+cfg_filename,VL_Noise)
    um=[]
    ar=False
    port = DefServerPort
    host='0.0.0.0'
    fork=False
    quiet=False
    vdbn=''
    tls=None
    oo=[]
    skip=1 #skip argv[0]
    for i,prm in enumerate(argv):
        if skip>0:
            skip-=1
            continue
        elif len(um)==0:
            if prm=="--THREAD":
                fork=False
            elif prm[0:7]=="--PORT=":
                o=prm.split('=')
                if (len(o)==2) and isInt(o[1]):
                    port=int(o[1])
            elif prm[0:7]=="--HOST=":
                o=prm.split('=')
                if len(o)==2:
                    host=o[1]
            elif prm=="--AUTOREGISTER":
                ar=True
            elif prm=="--NOREGISTER":
                ar=False
            elif prm=="--NOAUTH":
                vdbn=''
                tls=None
            elif prm=="--FORK":
                fork=True
            elif prm=="--Q":
                quiet=True
            elif prm=="--Q-":
                quiet=False
            elif prm[0:10]=="--IMPORTS=":
                o=prm.split('=')
                if len(o)==2:
                    OMCEService.Imports=o[1]
            elif prm[0:4]=="--V=":
                o=prm.split('=')
                if len(o)==2:
                    DefConText.VerboseLevel=int(o[1])
            elif prm[0:6]=="--LOG=":
                o=prm.split('=')
                if len(o)==2:
                    if o[1]!="":
                        fn=os.path.join(get_main_dir(),'logs',o[1])
                        DefConText.logfile=open(fn,'a')
            elif prm[0:6]=="--VDB=":
                o=prm.split('=')
                if len(o)==2:
                    if o[1]!="":
                        vdbn=os.path.join(get_main_dir(),o[1])
                        tls=None
            elif prm=="--TLS":
                skip=2
                if len(argv)>i+2:
                    tls=(argv[i+1].strip(),argv[i+2])
                    vdbn=''
                else:
                    msg[1][0]=''
                    DefConText.ERROR(77,'--TLS')
            elif prm=="--USER":
                um.append('USER')
            else:
                oo.append(prm)
        else:
            um.append(prm)
    if (len(um)>0):
        msg[1][0]=''
        EditVDB(vdbn,um)
    else:
        msg[1][0]=''
        for prm in oo:
            DefConText.PRINT(DefConText.MSG(102,prm),VL_Warn)
        wf=False
        for prm in sys.argv[1:]:
            if not (re.match('^-(?!-).*',prm) is None):
                wf=True
        if wf:
            DefConText.PRINT(DefConText.MSG(103,prm),VL_Warn)
        StartServer(port,ar,host,fork,quiet,vdbn,tls)
    return

if __name__=="__main__":
    ExitCode=run_main(ServerMain,sys.argv,True)
    sys.exit(ExitCode)
