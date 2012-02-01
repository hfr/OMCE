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
# 1.0.17 2009-03-12 Rüdiger Kessel: "+-" bug in CreateGrammar fixed
# 1.0.17 2009-03-12 Rüdiger Kessel: added option -cg
# 1.0.18 2009-06-08 Rüdiger Kessel: correlation analysis for result data
# 1.0.18 2009-06-08 Rüdiger Kessel: added options -ac, -cl, (-lc modified)
# 1.0.18 2009-06-08 Rüdiger Kessel: bug in random data handling fixed
# 1.0.19 2009-06-08 Rüdiger Kessel: bug for unc to uri conversion fixed
# 1.0.20 2009-06-08 Rüdiger Kessel: added -ac=2
# 1.0.21 2009-09-28 Rüdiger Kessel: added -p1=0.95, -p2=0.99, -p3=0.999
# 1.0.22 2009-09-30 Rüdiger Kessel: added <Ctrapez>, <Exponent> and <Gamma>
# 1.0.23 2009-10-01 Rüdiger Kessel: added exit code 21
# 1.0.24 2009-11-23 Rüdiger Kessel: small bug fixed in reader1
# 1.0.25 2009-12-28 Rüdiger Kessel: check for reserved words added
# 1.0.28 2010-03-01 Rüdiger Kessel: extension of the output file changed to .ohd
# 1.0.29 2010-04-07 Rüdiger Kessel: added <Discrete> and sorted bin format (-wb=3)
# 1.0.29 2010-04-09 Rüdiger Kessel: added nan support
# 1.0.30 2010-04-11 Rüdiger Kessel: added nan support for evaluation of correlations
# 1.0.31 2010-04-12 Rüdiger Kessel: added <Conditions> support
# 1.0.32 2010-04-13 Rüdiger Kessel: added minimum() and maximum()
# 1.0.33 2010-04-13 Rüdiger Kessel: option -cg ignored
# 1.0.34 2010-04-13 Rüdiger Kessel: added iff(cond,T_value,F_value)
# 1.0.35 2010-04-13 Rüdiger Kessel: added symbol name support for binfiles
# 1.0.35 2010-04-13 Rüdiger Kessel: added <Import>
# 1.0.36 2010-04-14 Rüdiger Kessel: option -io added
# 1.0.37 2010-04-19 Rüdiger Kessel: added <Function>
# 1.0.38 2010-04-20 Rüdiger Kessel: added distribution functions (Rectangle, ...)
# 1.0.39 2010-04-20 Rüdiger Kessel: added val() function
# 1.0.40 2010-04-20 Rüdiger Kessel: added u() function, Ctrapez bug fixed
# 1.0.41 2010-04-20 Rüdiger Kessel: min() and max() modified for multiple arguments
# 1.0.42 2010-04-20 Rüdiger Kessel: bug fixed with option -hp=1
# 1.0.43 2010-04-26 Rüdiger Kessel: renamed <Conditions> to <Constrains>
# 1.0.44 2010-04-26 Rüdiger Kessel: bug fixed in ReadXML
# 1.0.45 2010-05-07 Rüdiger Kessel: added <Parameters> and <Simulations>
# 1.1.0  2010-05-07 Rüdiger Kessel: ofd format changed to include the SID
# 1.1.1  2010-05-12 Rüdiger Kessel: Error handling changed
# 1.1.2  2010-05-12 Rüdiger Kessel: -info=5
# 1.1.3  2010-05-12 Rüdiger Kessel: added main_is_frozen(), get_main_dir()
# 1.1.4  2010-06-08 Rüdiger Kessel: split of OMCEbase.py
# 1.1.5  2010-06-08 Rüdiger Kessel: error 64 added
# 1.1.6  2010-10-27 Rüdiger Kessel: added Laplace distribution function
# 1.1.7  2010-10-28 Rüdiger Kessel: fixed memory problem with multiple simulations
# 1.1.8  2010-11-05 Rüdiger Kessel: added Stein 2-Stage adaptive modes (-am=1 and -am=2)
# 1.1.9  2010-11-10 Rüdiger Kessel: added option -at
# 1.1.10 2010-12-06 Rüdiger Kessel: added simple adaptive modes (-am=3 and -am=4)
# 1.1.11 2010-12-10 Rüdiger Kessel: stdevm added to result table (deleted by accident)
# 1.1.12 2010-12-12 Rüdiger Kessel: result['simblocks'] and result['addblocks'] added which
#                                   contains the number of simulation and additional blocks,
#                                   default changed to -v=2, renaming constain to constaint
# 1.1.13 2010-12-16 Rüdiger Kessel: Added WeightedStat(), AdjustPreRuns(), UD()
# 1.1.14 2010-12-16 Rüdiger Kessel: Added Class WeightedStats (replacing WeightedStat())
# 1.2.0  2011-01-13 Rüdiger Kessel: upgraded to Python 2.7, ReadXML() simplified
# 1.2.1  2011-01-18 Rüdiger Kessel: ofd and vfd options added ([], sd(), avg()]
# 1.2.2  2011-01-25 Rüdiger Kessel: -enc added, UNICODE()
# 1.2.3  2011-01-25 Rüdiger Kessel: -cp added
# 1.2.4  2011-02-11 Rüdiger Kessel: added client/server mode (--SERVER, --PORT)
# 1.2.5  2011-02-12 Rüdiger Kessel: improved client/server mode (Service 1.0.0)
# 1.2.6  2011-02-14 Rüdiger Kessel: improved server logging, added security layer
# 1.2.7  2011-02-16 Rüdiger Kessel: improved message filtering for logger
# 1.2.8  2011-02-17 Rüdiger Kessel: OMCEbase bugfix for Python 2.5
# 1.2.9  2011-02-18 Rüdiger Kessel: NOISE output added BeginInfo(context), EndInfo(context)
# 1.2.10 2011-02-20 Rüdiger Kessel: automaic support for amara 1 and 2
# 1.2.11 2011-02-22 Rüdiger Kessel: separating OMCEserver
# 1.2.12 2011-02-23 Rüdiger Kessel: separating OMCEerrors and OMCEmsgs
# 1.2.13 2011-03-02 Rüdiger Kessel: minor bugs fixed
# 1.2.14 2011-05-02 Rüdiger Kessel: added Cauchy() and Lognormal()
# 1.2.14.1 2011-10-15 Rüdiger Kessel: added sgn() and atan2()
# 1.2.14.2 2012-01-23 Rüdiger Kessel: added median()
# 1.2.14.3 2011-01-24 Rüdiger Kessel: added Python coding for user defined functions
#-----------------------------------------------------
__version__="1.2.14.3"
__MODID__="Open Monte Carlo Engine (OMCE V:"+__version__+")"
__AUTHOR__="Author: Ruediger Kessel (ruediger.kessel@nist.gov)"
#-----------------------------------------------------
import warnings
warnings.simplefilter("ignore",DeprecationWarning)
#warnings.simplefilter("error")
from OMCEbase import *
import array
import sys
import math
import os
import re
import imp
#from amara import bindery
import code
import thread as TH
import threading as THG
import time
from lxml import etree
import lxml._elementpath as DONTUSE #workaround for a py2exe bug
import inspect
import scipy.stats as stats
import StringIO
import string
import numpy as Numpy

def BeginInfo(context,Name=None):
    if context.VerboseLevel==0:
        if type(Name)==type(''):
            funcname=Name
        else:
            funcname=inspect.getframeinfo(inspect.currentframe().f_back)[2]
        context.NOISE(funcname+"() begin...")
    return Name

def EndInfo(context,Name=None):
    if context.VerboseLevel==0:
        if type(Name)==type(''):
            funcname=Name
        else:
            funcname=inspect.getframeinfo(inspect.currentframe().f_back)[2]
        context.NOISE("%s() end." % funcname)
    return Name

def STDEV(a):
    return Numpy.array(a).std(ddof=1)

def MEAN(a):
    return Numpy.average(Numpy.array(a))

def WMEAN(a,w):
    w=Numpy.array(w)
    return Numpy.sum(w*Numpy.array(a))/Numpy.sum(w)

def CheckConstParams(*ps):
    for p in ps:
        if not (isinstance(p,float) or isinstance(p,int)):
            funcname=inspect.getframeinfo(inspect.currentframe().f_back)[2]
            raise Error(24,funcname)
    return

class SimContext:
    def __init__(self,context,bs,LOV,seed=None):
        self.DataBlockSize=bs
        self.ListOfVars=LOV
        self.ERROR=context.ERROR
        self.PRINT=context.PRINT
        self.RS=Numpy.random.mtrand.RandomState(seed)
        return
    def reseed(self,seed=None):
        self.RS=Numpy.random.mtrand.RandomState(seed)
        return

    def iff(self,con,T,F):
        return Numpy.ma.where(con,T,F).data

    def Chisquare(self,m,s,dof):
        CheckConstParams(m,s,dof)
        return self.RS.chisquare(dof,self.DataBlockSize)*s+m

    def Cauchy(self,m,s):
        CheckConstParams(m,s)
        return self.RS.standard_cauchy(self.DataBlockSize)*s+m

    def Rectangle(self,m,hw):
        CheckConstParams(m,hw)
        ll=m-hw
        wd=2*hw
        return self.RS.random_sample(self.DataBlockSize)*wd+ll

    def Normal(self,m,s):
        CheckConstParams(m,s)
        return self.RS.normal(m,s,self.DataBlockSize)

    def Lognormal(self,m,s):
        CheckConstParams(m,s)
        return self.RS.lognormal(m,s,self.DataBlockSize)

    def Student(self,m,s,dof):
        CheckConstParams(m,s,dof)
        return self.RS.standard_t(dof,self.DataBlockSize)*s+m

    def Triangle(self,m,hw):
        CheckConstParams(m,hw)
        return self.RS.triangular(m-hw,m,m+hw,self.DataBlockSize)

    def Trapez(self,m,hw,beta):
        CheckConstParams(m,hw,beta)
        b=hw*(1 - beta)
        a=2 * hw - b
        R1=self.RS.random_sample(self.DataBlockSize)*a
        R2=self.RS.random_sample(self.DataBlockSize)*b
        return R1+R2+m-hw

    def Ushape(self,m,hw):
        CheckConstParams(m,hw)
        return Numpy.sin(2 * math.pi * self.RS.random_sample(self.DataBlockSize))*hw + m

    def Poisson(self,m):
        CheckConstParams(m)
        return 1.0*self.RS.poisson(m,self.DataBlockSize)

    def Ctrapez(self,m,hw,beta):
        CheckConstParams(m,hw,beta)
        u=self.RS.random_sample(self.DataBlockSize)
        v=self.RS.random_sample(self.DataBlockSize)
        z=(hw*beta)+u*hw*(1-beta)
        return (m-z)+v*2*z

    def Exponent(self,m):
        CheckConstParams(m)
        return self.RS.exponential(m,self.DataBlockSize)

    def Gamma(self,sh, sc):
        CheckConstParams(sh,sc)
        return self.RS.gamma(sh,sc,self.DataBlockSize)

    def Laplace(self,m,b):
        CheckConstParams(m,b)
        U=self.RS.random_sample(self.DataBlockSize)-0.5
        return m-b*Numpy.sign(U)*Numpy.log(1 - 2*Numpy.fabs(U))

    def maximum(self,*vs):
        if len(vs)==0:
            self.ERROR(25,"maximum()")
        m=vs[0]
        for i in range(1,len(vs)):
            m=Numpy.maximum(m,vs[i])
        return m

    def minimum(self,*vs):
        if len(vs)==0:
            self.ERROR(25,"minimum()")
        m=vs[0]
        for i in range(1,len(vs)):
            m=Numpy.minimum(m,vs[i])
        return m

    def average(self,*vs):
        if len(vs)==0:
            self.ERROR(25,"average()")
        m=0
        for i in range(len(vs)):
            m=m+vs[i]
        return m/len(vs)

    def stdev(self,*vs):
        if len(vs)==0:
            self.ERROR(25,"stdev()")
        if len(vs)<2:
            self.ERROR(53,"stdev()",len(vs))
        q_bar=self.average(*vs)
        n=len(vs)
        s=0
        for i in range(len(vs)):
            s=s+Numpy.square(vs[i]-q_bar)
        return Numpy.sqrt(s/(n**2-n))

    def median(self,*vs):
        if len(vs)==0:
            self.ERROR(25,"median()")
        return Numpy.median(Numpy.array(vs),axis=0)

    def val(self,s):
        found=False
        for v in self.ListOfVars:
            if v['sym']==s:
                L=v['exec']
                if L[0] in [0,1,2,3,4,5,6,7,8,9,13]:
                    found=True
                    V=L[1]
                if L[0]==10:
                    found=True
                    V=L[1]*L[2]
                break
        if not found:
            self.ERROR(26,s)
        return V

    def u(self,s):
        found=False
        for v in self.ListOfVars:
            if v['sym']==s:
                L=v['exec']
                found=True
                if L[0]==0:
                    V=0
                elif L[0]==1:
                    V=L[2]
                elif L[0]==2:
                    V=L[2]/math.sqrt(3)
                elif L[0]==3:
                    V=L[2]/math.sqrt(6)
                elif L[0]==4:
                    V=L[2]*math.sqrt((1+L[3]**2)/6)
                elif L[0]==5:
                    V=L[2]/math.sqrt(2)
                elif L[0]==6:
                    if int(L[3])<3:
                        self.ERROR(27,s)
                    else:
                        f=math.sqrt(L[3]*1.0/(L[3]*1.0-2))
                    V=L[2]*f
                elif L[0]==7:
                    V=math.sqrt(L[1])
                elif L[0]==8:
                    V=L[2]*math.sqrt((L[3]**2+L[3]+1)/9)
                elif L[0]==9:
                    V=L[1]
                elif L[0]==10:
                    V=math.sqrt(L[1])*L[2]
                elif L[0]==13:
                    f=math.sqrt(2*L[3])
                    V=L[2]*f
                else:
                    found=False
                break
        if not found:
            self.ERROR(28,s)
        return V

def GetPredefinedFunc(opts,simcon):
    '''
    creates a dictionary with the predefined functions
    the functions are mappings of the NumPy and SimContext functions
    '''
    glob={}
    glob['sgn']=Numpy.sign
    glob['sqrt']=Numpy.sqrt
    glob['sqr']=Numpy.square
    glob['pow']=Numpy.power
    glob['abs']=Numpy.abs
    glob['exp']=Numpy.exp
    glob['log']=Numpy.log
    glob['log10']=Numpy.log10
    glob['sin']=Numpy.sin
    glob['cos']=Numpy.cos
    glob['tan']=Numpy.tan
    glob['asin']=Numpy.arcsin
    glob['acos']=Numpy.arccos
    glob['atan']=Numpy.arctan
    glob['atan2']=Numpy.arctan2
    glob['sinh']=Numpy.sinh
    glob['cosh']=Numpy.cosh
    glob['tanh']=Numpy.tanh
    glob['minimum']=simcon.minimum
    glob['min']=simcon.minimum
    glob['maximum']=simcon.maximum
    glob['max']=simcon.maximum
    glob['average']=simcon.average
    glob['stdev']=simcon.stdev
    glob['median']=simcon.median
    glob['iff']=simcon.iff
    glob['Rectangle']=simcon.Rectangle
    glob['Normal']=simcon.Normal
    glob['Student']=simcon.Student
    glob['Triangle']=simcon.Triangle
    glob['Trapez']=simcon.Trapez
    glob['Ushape']=simcon.Ushape
    glob['Poisson']=simcon.Poisson
    glob['Ctrapez']=simcon.Ctrapez
    glob['Exponent']=simcon.Exponent
    glob['Gamma']=simcon.Gamma
    glob['Laplace']=simcon.Laplace
    glob['Chisquare']=simcon.Chisquare
    glob['Cauchy']=simcon.Cauchy
    glob['Lognormal']=simcon.Lognormal
    glob['val']=simcon.val
    glob['u']=simcon.u
    return glob

def CheckGrammar(G,equ,promt,name):
    '''
    check of the expression <equ> against the grammar
      <promt> and <name> are used for error handling
    '''
    return G.CheckGrammar(equ,promt,name)

def CreateGrammar(data):
    data['context'].PRINT('Creating Grammar...',VL_Noise)
    data['grammar']=Grammar(data['context'],data['predefsymbols'].keys(),data['predeffunc'].keys(),data['usrfunc'],1)
    return

def CreateConGrammar(data):
    data['context'].PRINT('Creating ConGrammar...',VL_Noise)
    data['congrammar']=Grammar(data['context'],data['predefsymbols'].keys(),data['predeffunc'].keys(),[],2)
    return

def COMPILE(s):
    '''
    compile command used to compile expression <s>
    '''
    return code.compile_command(s,'<input>','eval')

def GetContF(fdefs,f):
    f['usedf']=True
    try:
        CF=set(f['contf'])
        if len(f['contf'])>0:
            for C in f['contf']:
                for F in fdefs:
                    if C==F['sym']:
                        if F['usedf']:
                            raise Error(30,f['name'])
                        CF=CF.union(GetContF(fdefs,F))
    finally:
        f['usedf']=False
    return CF

def ResetUsedF(fdefs):
    for f in fdefs:
        f['usedf']=False
    return

def CompileFuncs(opts,data):
    '''
    compile usr defined functions given in data['funcdefs']'
    '''
    def FuncHeader(F):
        FT='def '+F['sym']+'('+','.join(F['param'])+'):\n'
        if (len(F['global'])>0):
            FT+=I+'global '+','.join(F['global'])+'\n'
        return FT
    def __print_error__(msg):
        raise Error(250,msg)
    def __block_size__():
        return opts['-bs']
    context=opts['CONTEXT']
    FT=''
    PFT=''
    I='    '
    for F in data['funcdefs']:
        if F['coding']=='OMCE':
            GR=CheckGrammar(data['grammar'],F['equ'],"Function",F['name'])
            F['contf']=GR[2]
            F['uglobal']=[]
            for S in GR[1]:
                if S in F['param']:
                    if S in F['global']:
                        context.ERROR(31,S,F['name'])
                    continue
                if S in F['global']:
                    found=False
                    for V in data['vars']:
                        if V['sym']==S:
                            found=True
                            break
                    for E in data['equs']:
                        if E['sym']==S:
                            found=True
                            break
                    if found:
                        F['uglobal'].append(S)
                        continue
                    else:
                        context.ERROR(32,S,F['name'])
                context.ERROR(33,S,F['name'])
            FT+=FuncHeader(F)
            FT+=I+'return '+''.join(GR[0])+'\n'
            FT+='\n'
        elif F['coding']=='PYTHON':
            F['contf']=[]
            F['uglobal']=[]
            for S in F['param']:
                if S in F['global']:
                    context.ERROR(31,S,F['name'])
            for S in F['global']:
                found=False
                for V in data['vars']:
                    if V['sym']==S:
                        found=True
                        break
                for E in data['equs']:
                    if E['sym']==S:
                        found=True
                        break
                if found:
                    F['uglobal'].append(S)
                    continue
                else:
                    context.ERROR(32,S,F['name'])
            PFT+=FuncHeader(F)
            PFT+=I+'import numpy as Numpy\n'
            PFT+=I+'BlockSize=__block_size__\n' #+context.STR(opts['-bs'])+'\n'
            PFT+=I+'Error=__print_error__'+'\n'
            for l in F['equ'].split('\n'):
                PFT+=I+l+'\n'
            PFT+='\n'
        else:
            context.ERROR(94,F['coding'],F['name'])
    for F in data['funcdefs']:
        ResetUsedF(data['funcdefs'])
        F['ccontf']=GetContF(data['funcdefs'],F)
    data['funcdeftext']=FT
    data['pfuncdeftext']=PFT
    SYMS={}
    for v in data['vars']:
        SYMS[v['sym']]=None
    for v in data['equs']:
        SYMS[v['sym']]=None
    CONTEXT=DictMerge(data['predefequs'],SYMS)
    if data['funcdeftext']:
        exec data['funcdeftext'] in CONTEXT
    if data['pfuncdeftext']:
        E={}
        exec '' in E
        CONTEXT['__builtins__']=E['__builtins__']
        CONTEXT['__print_error__']=__print_error__
        CONTEXT['__block_size__']=__block_size__
        exec data['pfuncdeftext'] in CONTEXT
    data['predefequs']=CONTEXT
    for F in data['funcdefs']:
        F['code']=CONTEXT[F['sym']]
        data['predefequs'][F['sym']]=F['code']
    return

class XmlReaderBase:
    '''
    base class for XML input file reader
    '''
    def __init__(self,opts,data):
        self.opts=opts
        self.data=data
        self.context=opts['CONTEXT']
        return
    def ERROR(self,*p):
        self.opts['CONTEXT'].ERROR(*p)
    def PRINT(self,*p):
        self.opts['CONTEXT'].PRINT(*p)
    def STR(self,p):
        return self.opts['CONTEXT'].STR(p)
    def UNICODE(self,p):
        return self.opts['CONTEXT'].UNICODE(p)
    def FILENAME(self,p):
        return self.opts['CONTEXT'].FILENAME(p)
    def STRIPED(self,p):
        return self.STR(self.UNICODE(p).strip())
    def XPATH(self,d,p):
        if amara_version==1:
            return d.xml_xpath(p)
        elif amara_version==2:
            return d.xml_select(p)
        else:
            self.ERROR(82)
    def XNODEN(self,n):
        if amara_version==1:
            return n.nodeName
        elif amara_version==2:
            return n.xml_qname
        else:
            self.ERROR(82)
    def InitParams(self,data,params):
        PL=InitMathSymbols()
        MS=InitMathSymbols()
        PS=[]
        if len(params)>0:
            for p in params:
                Nm,V=p.split('=')
                Ns=Nm.strip()
                Nm=self.ConvSymName(Ns)
                if Nm in PL.keys():
                    V=float(eval(V.strip(),MS,{}))
                    PS.append(Ns+'='+self.STR(V))
                    PL[Nm]=V
                else:
                    self.ERROR(34,Ns)
        data['params']=PL
        data['clparams']=PS
    def GetFuncDefs(self,opts,data):
        FD=[]
        UFL=[]
        data['usrfunc']=UFL
        data['funcdefs']=FD
        return FD,UFL
    def GetFileNames(self,opts,data):
        FL=[]
        data['discretefiles']=FL
        return FL
    def GetSymbolName(self,ent):
        return ''
    def GetStr(self,ent):
        return self.STRIPED(ent)
    def GetFilename(self,ent):
        return self.FILENAME(ent).strip()
    def GetInt(self,ent):
        return int(self.UNICODE(ent).strip())
    def GetIntParameter(self,ent):
        p=self.GetParameter(ent)
        if (abs(p/(int(p)*1.0)-1.0))>1E-14:
            sn=self.GetSymbolName(ent)
            nn=self.XNODEN(ent)
            en=self.STRIPED(ent)
            self.ERROR(35,sn,nn,en)
        else:
            p=int(p)
        return p
    def GetParameter(self,ent):
        MemName=BeginInfo(self.context,'XMLReaderBase.GetParameter')
        try:
            p=float(eval(self.ConvEqu(self.UNICODE(ent).strip()),self.data['params'],{}))
        except Exception,e:
            sn=self.GetSymbolName(ent)
            nn=self.XNODEN(ent)
            en=self.UNICODE(ent).strip()
            if isinstance(e, NameError):
                self.ERROR(36,sn,nn,en)
            if '%' in self.UNICODE(ent):
                self.ERROR(37,sn,nn,en)
            else:
                self.ERROR(38,sn,nn,en)
        EndInfo(self.context,MemName)
        return p
    def GetDistrType(self,d):
        for node in self.XPATH(d,u'*'):
            if self.XNODEN(node[0])=='Comment':
                continue
            else:
                type=self.XNODEN(node[0])
                break
        return type
    def GetFormula(self,formula):
        if hasattr(formula,'Comment'):
            s=[]
            for c in formula.xml_children:
                if isinstance(c,unicode):
                    s.append(c)
            frm=' '.join(s)
        else:
            frm=self.UNICODE(formula)
        frm=frm.replace('\r',' ')
        frm=self.STR(frm.replace('\n',' '))
        frm=frm.strip()
        return frm
    def SubsInExpr(self,expr,SL):
        for r in '+-*/(),=<>!~|&':
            expr=expr.replace(r,' '+r+' ')
        return expr
    def GetContr(self,tl):
        l=[]
        for i in tl:
            if not (i in l):
                l.append(i)
        return l
    def GetVarList(self,opts,data):
        return
    def GetEquList(self,opts,data):
        return
    def GetResultList(self,opts,data):
        return
    def GetCorrList(self,opts,data):
        data['corrs']=[]
        return []
    def GetMCRuns(self,data):
        return 0
    def ConvSymName(self,name):
        name=name.replace('@','__')
        return name
    def ConvSymNames(self,names):
        for name in names:
            name=name.replace('@','__')
        return names
    def ConvEqu(self,text):
        text=text.replace('@','__')
        return text
    def GetConstraintList(self,opts,data):
        CL=[]
        data['constraints']=CL
        return CL
    def CheckSymbolUF(self,data,sym):
        if sym in data['predeffunc'].keys():
            self.ERROR(39,sym)
        if sym in data['predefsymbols'].keys():
            self.ERROR(40,sym)
        if sym in data['reserved']:
            self.ERROR(41,sym)
        return
    def CheckSymbol(self,data,sym):
        self.CheckSymbolUF(data,sym)
        if sym in data['usrfunc']:
            self.ERROR(42,sym)
    def ValidateName(self,Nn,T):
        G=Word(alphas+"_", alphas+nums+"_")
        G.setDebug(False)
        try:
            ps=G.parseString(Nn, parseAll=True)
            Nn=ps[0]
        except ParseException,PE:
            self.PRINT(PE.line)
            self.PRINT(" "*(PE.column-1) + "^")
            self.ERROR(64,T,PE)
        return Nn

class OMCReader(XmlReaderBase):
    '''
    XML file reader class for OMC file format
    '''
    def __init__(self,opts,data):
        XmlReaderBase.__init__(self, opts, data)
        MemName=BeginInfo(self.context,'OMCReader.__init__')
        self.files=[]
        EndInfo(self.context,MemName)
        return
    def InitParams(self,data,params):
        MemName=BeginInfo(self.context,'OMCReader.InitParams')
        PL=InitMathSymbols()
        MS=InitMathSymbols()
        data['prmgrammar']=Grammar(self.context,data['predefsymbols'].keys(),MS.keys(),[],3)
        PS=[]
        if hasattr(data['doc'].Model,'Parameters'):
            for p in data['doc'].Model.Parameters.Parameter:
                Na=self.STRIPED(p.Name)
                Nm=self.ConvSymName(Na)
                Nm=self.ValidateName(Nm,'parameter')
                if Nm in MS.keys():
                    self.ERROR(43,Na)
                if Nm in data['reserved']:
                    self.ERROR(44,Na)
                PL[Nm],Va=GetParam(data,p.Value,MS,Na,[])
        if len(params)>0:
            for p in params:
                Nm,V=p.split('=')
                Ns=Nm.strip()
                Nm=self.ConvSymName(Ns)
                if Nm in PL.keys():
                    PL[Nm],Va=GetParam(data,V,MS,Ns,[])
                    PS.append(Ns+'='+self.STR(V))
                else:
                    self.ERROR(34,Ns)
        data['params']=PL
        data['clparams']=PS
        EndInfo(self.context,MemName)
        return
    def GetFuncDefs(self,opts,data):
        MemName=BeginInfo(self.context,'OMCReader.GetFuncDefs')
        FD=[]
        UFL=[]
        data['usrfunc']=UFL
        if hasattr(data['doc'].Model,'Functions'):
            for f in data['doc'].Model.Functions.Function:
                Nm=self.STRIPED(f.Symbol)
                SN=self.ConvSymName(Nm)
                UFL.append(SN)
            data['usrfunc']=UFL
            for f in data['doc'].Model.Functions.Function:
                F={}
                F['name']=self.STRIPED(f.Symbol)
                F['sym']=self.ValidateName(self.ConvSymName(F['name']),'function')
                self.CheckSymbolUF(data,F['sym'])
                if hasattr(f,'Param'):
                    P=self.STRIPED(f.Param)
                    F['param']=self.ConvSymNames(P.replace(' ','').split(','))
                    for P in F['param']:
                        self.CheckSymbol(data,P)
                else:
                    F['param']=[]
                if hasattr(f,'Global'):
                    G=self.STRIPED(f.Global)
                    F['global']=self.ConvSymNames(G.replace(' ','').split(','))
                    for G in F['global']:
                        self.CheckSymbol(data,G)
                else:
                    F['global']=[]
                if hasattr(f,'Coding'):
                    F['coding']=string.upper(self.STRIPED(f.Coding))
                else:
                    F['coding']='OMCE'
                if F['coding']=='OMCE':
                    F['src']=self.GetFormula(f)
                else:
                    F['src']=self.STR(self.UNICODE(f)).strip('\n')
                F['equ']=self.ConvEqu(F['src'])
                FD.append(F)
        data['funcdefs']=FD
        EndInfo(self.context,MemName)
        return FD,UFL
    def GetFileID(self,filename, idx, q, loc):
        MemName=BeginInfo(self.context,'OMCReader.GetFileID')
        if not loc:
            fn=self.context.PathJoin(self.opts['XMLpath'],filename)
        else:
            if self.context.IsServer:
                if not (re.match(r'^\\|.*:|^/|.*\.\.',filename) is None):
                    raise Error(73,filename)
                impdir=self.context.Imports
            else:
                impdir=os.path.join(get_main_dir(),self.opts['-imp'])
            fn=os.path.join(impdir,filename)
        id=-1
        for i,fi in enumerate(self.files):
            if (fi['filename']==fn) and (fi['loc']==loc):
                id=i
                break
        if id<0:
            if not loc:
                fdata,names=self.context.ReadBinFile(fn)
            else:
                fdata,names=LocReadBinFile(self.context,fn)
            nl=[]
            for name in names:
                nl.append(name)
            fd=[]
            for d in fdata:
                fd.append(Numpy.loads(d))
            self.files.append({'filename':fn, 'loc':loc, 'ids':[], 'data':fd, 'names':nl})
            id=len(self.files)-1
        fi=self.files[id]
        if (q!=''):
            try:
                idx=fi['names'].index(q)
            except:
                raise
                self.ERROR(45,q,filename)
        if (idx>=0) or (not (idx in fi['ids'])):
            fi['ids'].append(idx)
        if idx<0:
            self.ERROR(46)
        EndInfo(self.context,MemName)
        return id,idx
    def GetImportedFileID(self, filename, idx, q, loc):
        return self.GetFileID(filename, idx, q, loc)
    def GetFileNames(self,opts,data):
        MemName=BeginInfo(self.context,'OMCReader.GetFileNames')
        FL=[]
        for fn in self.files:
            FL.append(fn)
        data['discretefiles']=FL
        EndInfo(self.context,MemName)
        return FL
    def GetSymbolName(self,ent):
        MemName=BeginInfo(self.context,'OMCReader.GetSymbolName')
        if self.XNODEN(ent)=='Quantity':
            ret=self.UNICODE(ent.Symbol)
        else:
            try:
                ret=self.GetSymbolName(ent.xml_parent)
            except:
                ret=''
        EndInfo(self.context,MemName)
        return ret
    def GetBinFile(self,t):
        MemName=BeginInfo(self.context,'OMCReader.GetBinFile')
        B=t.Binfile
        if hasattr(B,'Q'):
            q=self.GetStr(B.Q)
            idx=-1
        else:
            q=''
            if hasattr(B,'Index'): idx=self.GetInt(B.Index)
            else: idx=0
        if hasattr(B,'Syspath'): loc=self.GetInt(B.Syspath)!=0
        else: loc=False
        fn=self.GetFilename(B.Filename)
        EndInfo(self.context,MemName)
        return fn,idx,q,loc
    def GetDistrL(self,d):
        MemName=BeginInfo(self.context,'OMCReader.GetDistrL')
        for node in self.XPATH(d,u'*'):
            if self.XNODEN(node[0])=='Comment':
                continue
            else:
                t=node[0]
                FN=self.XNODEN(t)
                break
        if FN=='Constant':
            L=[0, self.GetParameter(t.Value)]
        elif FN=='Normal':
            L=[1, self.GetParameter(t.Mean), self.GetParameter(t.Sigma)]
            if L[2]==0.0:
                L=[0,L[1]]
        elif FN=='Rectangle':
            L=[2, self.GetParameter(t.Mean), self.GetParameter(t.Halfwidth)]
            if L[2]==0.0:
                L=[0,L[1]]
        elif FN=='Triangle':
            L=[3, self.GetParameter(t.Mean), self.GetParameter(t.Halfwidth)]
            if L[2]==0.0:
                L=[0,L[1]]
        elif FN=='Trapez':
            L=[4, self.GetParameter(t.Mean), self.GetParameter(t.Halfwidth), self.GetParameter(t.Beta)]
            if L[2]==0.0:
                L=[0,L[1]]
        elif FN=='Ushape':
            L=[5, self.GetParameter(t.Mean), self.GetParameter(t.Halfwidth)]
            if L[2]==0.0:
                L=[0,L[1]]
        elif FN=='TypeA':
            v=[]
            for vl in t.Value:
                v.append(self.GetParameter(vl))
            n=len(v)
            if n<2:
                E='TypeA n<2'
                self.ERROR(15,E)
            E=MEAN(v)
            S=STDEV(v)/math.sqrt(n)
            DOF=n-1
            L=[6, float(E), float(S), float(DOF)]
        elif FN=='Bayesian':
            if hasattr(t,'Distribution'):
                D=self.STRIPED(t.Distribution)
                if D!="Gauss":
                    E='Bayesian.Distribution='+D
                    self.ERROR(15,E)
            v=[]
            for vl in t.Value:
                v.append(self.GetParameter(vl))
            n=len(v)
            if n<4:
                E='Bayesian n<4'
                self.ERROR(15,E)
            E=MEAN(v)
            S=(n-1)/(n-3)*STDEV(v)/math.sqrt(n)
            L=[1, float(E), float(S)]
        elif FN=='Student':
            L=[6, self.GetParameter(t.Mean), self.GetParameter(t.Scalefactor), self.GetIntParameter(t.Dof)]
            if L[2]==0.0:
                L=[0,L[1]]
        elif FN=='Poisson':
            L=[7, self.GetParameter(t.Mean)]
            if L[1]==0.0:
                L=[0,L[1]]
        elif FN=='Ctrapez':
            L=[8, self.GetParameter(t.Mean), self.GetParameter(t.Halfwidth), self.GetParameter(t.Beta)]
            if L[2]==0.0:
                L=[0,L[1]]
        elif FN=='Exponent':
            L=[9, self.GetParameter(t.Mean)]
            if L[1]==0.0:
                L=[0,L[1]]
        elif FN=='Gamma':
            L=[10, self.GetParameter(t.Shape), self.GetParameter(t.Scale)]
            if L[1]==0.0:
                L=[0,L[1]]
        elif FN=='Discrete':
            fn,idx,q,loc=self.GetBinFile(t)
            if hasattr(t,'Shift'): sh=self.GetParameter(t.Shift)
            else: sh=0.0
            if hasattr(t,'Scale'): sc=self.GetParameter(t.Scale)
            else: sc=1.0
            id,idx=self.GetFileID(fn,idx,q,loc)
            L=[11,id,idx,sh,sc]
        elif FN=='Import':
            fn,idx,q,loc=self.GetBinFile(t)
            id,idx=self.GetImportedFileID(fn,idx,q,loc)
            L=[12,id,idx]
        elif FN=='Chisquare':
            L=[13, self.GetParameter(t.Shift), self.GetParameter(t.Scalefactor), self.GetIntParameter(t.Dof)]
            if L[2]==0.0:
                L=[0,L[1]]
        EndInfo(self.context,MemName)
        return L
    def GetVarList(self,opts,data):
        MemName=BeginInfo(self.context,'OMCReader.GetVarList')
        VL=[]
        doc=data['doc']
        if hasattr(doc.Model,'Quantities'):
            if hasattr(doc.Model.Quantities,'Quantity'):
                for vari in doc.Model.Quantities.Quantity:
                    V={}
                    V['id']=len(VL)
                    V['name']=self.STRIPED(vari.Symbol)
                    V['sym']=self.ValidateName(self.ConvSymName(V['name']),'quantity')
                    self.CheckSymbol(data,V['sym'])
                    V['type']=self.GetDistrType(vari)
                    V['exec']=self.GetDistrL(vari)
                    if hasattr(vari,'Unit'):
                        V['unit']=self.STRIPED(vari.Unit)
                    else:
                        V['unit']=''
                    VL.append(V)
        data['vars']=VL
        EndInfo(self.context,MemName)
        return VL
    def GetEqu(self,opts,data,p,name):
        MemName=BeginInfo(self.context,'OMCReader.GetEqu')
        equ=self.GetFormula(p)
        EndInfo(self.context,MemName)
        return equ
    def GetEquList(self,opts,data):
        MemName=BeginInfo(self.context,'OMCReader.GetEquList')
        EL=[]
        if hasattr(data['doc'].Model,'Equations'):
            if hasattr(data['doc'].Model.Equations,'Equ'):
                for equ in data['doc'].Model.Equations.Equ:
                    E={}
                    E['id']=len(EL)
                    E['name']=self.STRIPED(equ.Symbol)
                    E['sym']=self.ValidateName(self.ConvSymName(E['name']),'equation')
                    self.CheckSymbol(data,E['sym'])
                    E['src']=self.GetEqu(opts,data,equ,E['name'])
                    E['equ']=self.ConvEqu(E['src'])
                    GR=CheckGrammar(data['grammar'],E['equ'],"Equation",E['name'])
                    E['cont']=self.GetContr(GR[1])
                    E['contf']=GR[2]
                    E['code']=COMPILE(''.join(GR[0]))
                    if hasattr(equ,'Unit'):
                        E['unit']=self.STRIPED(equ.Unit)
                    else:
                        E['unit']=''
                    EL.append(E)
        data['equs']=EL
        EndInfo(self.context,MemName)
        return EL
    def GetResultList(self,opts,data):
        MemName=BeginInfo(self.context,'OMCReader.GetResultList')
        RL=[]
        if hasattr(data['doc'].Model.Results,'Result'):
            for result in data['doc'].Model.Results.Result:
                R={}
                R['id']=len(RL)
                R['name']=self.STRIPED(result.Symbol)
                R['sym']=self.ValidateName(self.ConvSymName(R['name']),'result')
                self.CheckSymbol(data,R['sym'])
                R['src']=self.GetFormula(result)
                R['equ']=self.ConvEqu(R['src'])
                GR=CheckGrammar(data['grammar'],R['equ'],"Result",R['name'])
                R['cont']=self.GetContr(GR[1])
                R['code']=COMPILE(''.join(GR[0]))
                for r in RL:
                    if r['sym']==R['sym']:
                        self.ERROR(47,R['name'])
                if hasattr(result,'Unit'):
                    R['unit']=self.STRIPED(result.Unit)
                else:
                    R['unit']=''
                if hasattr(result,'Definition'):
                    R['definition']=self.STRIPED(result.Definition)
                else:
                    R['definition']=''
                RL.append(R)
        else:
            self.ERROR(48)
        data['results']=RL
        EndInfo(self.context,MemName)
        return RL
    def GetCorrList(self,opts,data):
        MemName=BeginInfo(self.context,'OMCReader.GetCorrList')
        CL=[]
        if hasattr(data['doc'].Model,'Correlations'):
            if hasattr(data['doc'].Model.Correlations,'Coefficient'):
                for coeff in data['doc'].Model.Correlations.Coefficient:
                    q1=self.ValidateName(self.ConvSymName(self.STRIPED(coeff.Q1)),'correlation')
                    q2=self.ValidateName(self.ConvSymName(self.STRIPED(coeff.Q2)),'correlation')
                    r=self.UNICODE(coeff.Value)
                    if isFloat(r):
                        r=float(r)
                    else:
                        self.PRINT(self.MSG(100,self.STR(r),VL_Warn))
                        r=0.0
                    C=(q1,q2,r)
                    CL.append(C)
        data['corrs']=CL
        EndInfo(self.context,MemName)
        return CL
    def GetMCRuns(self,data):
        return 0
    def GetConstraintList(self,opts,data):
        MemName=BeginInfo(self.context,'OMCReader.GetConstraintList')
        CL=[]
        if hasattr(data['doc'].Model,'Constraints'):
            if hasattr(data['doc'].Model.Constraints,'Constraint'):
                for con in data['doc'].Model.Constraints.Constraint:
                    C={}
                    C['name']=self.STRIPED(con.Q)
                    C['sym']=self.ValidateName(self.ConvSymName(C['name']),'constraint')
                    C['sym']=self.ConvSymName(C['name'])
                    self.CheckSymbol(data,C['sym'])
                    C['src']=self.GetFormula(con)
                    C['equ']=self.ConvEqu(C['src'])
                    GR=CheckGrammar(data['congrammar'],C['equ'],"Constraint for",C['name'])
                    C['cont']=self.GetContr(GR[1])
                    C['code']=COMPILE(' '.join(GR[0]))
                    CL.append(C)
        data['constraints']=CL
        EndInfo(self.context,MemName)
        return CL

class Reader1(XmlReaderBase):
    '''
    XML file reader class for the alternative xml file format
    '''
    def __init__(self,opts,data):
        XmlReaderBase.__init__(self, opts, data)
        self.TypeMapping={}
        self.TypeMapping=DictMerge(self.TypeMapping,{'constant':'Constant','gauss':'Gauss','rectangle':'Rectangle'})
        self.TypeMapping=DictMerge(self.TypeMapping,{'triangle':'Triangle','trapez':'Trapez','arcsine':'Ushape'})
        self.TypeMapping=DictMerge(self.TypeMapping,{'studentt':'Student','typea':'TypeA'})
        return
    def GetSymbolName(self,ent):
        if ent.nodeName=='variable':
            return self.UNICODE(ent.name)
        else:
            try:
                return self.GetSymbolName(ent.xml_parent)
            except:
                return ''
    def GetType(self,v):
        if hasattr(v,'distribution'):
            type=self.GetDistrType(v.distribution)
        else:
            type='constant'
        if (type=='studentt') and hasattr(v.distribution,'values'):
            type='typea'
        if type in self.TypeMapping.keys():
            type=self.TypeMapping[type]
        return type
    def GetDistrL(self,d):
        t=self.XPATH(d,u'*[1]')[0]
        FN=t.nodeName
        if FN=='constant':
            L=[0, self.GetParameter(t.value)]
        elif FN=='gauss':
            L=[1, self.GetParameter(t.mu), self.GetParameter(t.sigma)]
            if L[2]==0.0:
                L=[0,L[1]]
        elif FN=='rectangle':
            L=[2, self.GetParameter(t.mean), self.GetParameter(t.width)]
            if L[2]==0.0:
                L=[0,L[1]]
        elif FN=='triangle':
            L=[3, self.GetParameter(t.mean), self.GetParameter(t.width)]
            if L[2]==0.0:
                L=[0,L[1]]
        elif FN=='trapez':
            ll=self.GetParameter(t.lower)
            ul=self.GetParameter(t.upper)
            L=[4, (ll+ul)/2, math.fabs(ul-ll), 1/self.GetParameter(t.beta)]
            if L[1]==0.0:
                L=[0,L[1]]
        elif FN=='arcsine':
            ll=self.GetParameter(t.lower)
            ul=self.GetParameter(t.upper)
            L=[5, (ll+ul)/2, math.fabs(ul-ll)]
            if L[2]==0.0:
                L=[0,L[1]]
        elif FN=='studentt':
            if hasattr(t,'values'):
                v=[]
                for vl in t.values.value:
                    v.append(self.GetParameter(vl))
                n=len(v)
                E=MEAN(v)
                S=STDEV(v)/math.sqrt(n)
                DOF=n-1
                L=[6, float(E), float(S), float(DOF)]
            else:
                L=[6, self.GetParameter(t.xbar), self.GetParameter(t.std), self.GetParameter(t.dgf)]
            if L[2]==0.0:
                L=[0,L[1]]
        return L
    def GetL(self,v):
        if hasattr(v,'distribution'):
            L=self.GetDistrL(v.distribution)
        else:
            src=self.UNICODE(v)
            src=src.replace('\r','')
            src=self.STR(src.replace('\n',''))
            L=[0, float(self.UNICODE(src))]
        return L
    def GetVarList(self,opts,data):
        VL=[]
        doc=data['doc']
        for vari in doc.simulation.calculation.variable:
            V={}
            V['id']=len(VL)
            V['name']=self.STRIPED(vari.name)
            V['sym']=V['name'].replace('@','__')
            self.CheckSymbol(data,V['sym'])
            V['type']=self.GetType(vari)
            V['exec']=self.GetL(vari)
            V['unit']=''
            VL.append(V)
        data['vars']=VL
        return VL
    def GetEqu(self,opts,data,p,name):
        equ=self.GetFormula(p.formula)
        equ=equ.replace('@','__')
        return equ
    def GetEquList(self,opts,data):
        EL=[]
        for proc in data['doc'].simulation.processes.process:
            E={}
            E['id']=len(EL)
            E['name']=self.STRIPED(proc.name)
            E['sym']=E['name'].replace('@','__')
            self.CheckSymbol(data,E['sym'])
            E['equ']=self.GetEqu(opts,data,proc,E['name'])
            GR=CheckGrammar(data['grammar'],E['equ'],"Equation",E['name'])
            E['cont']=self.GetContr(GR[1])
            E['contf']=[]
            E['code']=COMPILE(''.join(GR[0]))
            E['unit']=''
            EL.append(E)
        data['equs']=EL
        return EL
    def GetResultList(self,opts,data):
        RL=[]
        for formula in data['doc'].simulation.calculation.uncertainty.formula:
            R={}
            R['id']=len(RL)
            R['name']=self.STRIPED(formula.name)
            R['sym']=R['name'].replace('@','__')
            self.CheckSymbol(data,R['sym'])
            f=self.GetFormula(formula)
            f=f.replace('@','__')
            R['equ']=f
            GR=CheckGrammar(data['grammar'],R['equ'],"Result",R['name'])
            R['cont']=self.GetContr(GR[1])
            R['code']=COMPILE(''.join(GR[0]))
            R['unit']=''
            R['definition']=''
            RL.append(R)
        data['results']=RL
        return RL
    def GetMCRuns(self,data):
        smcs=data['doc'].simulation.calculation.mcsimulations
        if isInt(smcs):
            MCR=int(smcs)
        else:
            if self.STR(smcs)!="a":
                raise Error(7,smcs)
            else:
                MCR=0
        return MCR

def GetParam(data,V,MS,N,us):
    Va=data['context'].STR(data['context'].UNICODE(V))
    V=data['reader'].ConvSymName(Va)
    GR=CheckGrammar(data['prmgrammar'],V,"Parameter",N)
    for idn in GR[1]:
        if not(idn in us):
            raise Error(49,idn,Va)
    try:
        V=float(eval(''.join(GR[0]).strip(),MS,{}))
    except NameError:
        raise Error(50,V)
    return V,Va

class CorrMatrixList:
    '''
    class to handle a correlation matrix in list form
    '''
    def __init__(self):
        self.CorrList=[]
        return
    def CheckValue(self,C):
        if (C[2]<-1) or (C[2]>1):
            raise Error(19,C[0],C[1],C[2])
    def FindSubMatrixId(self,symbol):
        i=-1
        if len(self.CorrList)>0:
            for j, mx in enumerate(self.CorrList):
                if symbol in mx['symbols']:
                    i=j
                    break
        return i
    def AddNewMatrix(self,C):
        self.CheckValue(C)
        if C[0]!=C[1]:
            MX={}
            S=[]
            S.append(C[0])
            S.append(C[1])
            MX['symbols']=S
            MX['coeffs']=[C]
            self.CorrList.append(MX)
        return
    def JoinMatrix(self,f1,f2):
        MX1=self.CorrList[f1]
        MX2=self.CorrList[f2]
        S=MX1['symbols']
        for sym in MX2['symbols']:
            if not (sym in S):
                S.append(sym)
        MX1['coeffs'].extend(MX2['coeffs'])
        MX2['symbols']=[]
        MX2['coeffs']=[]
        return f1
    def AddToMatrix(self,f,C):
        self.CheckValue(C)
        MX=self.CorrList[f]
        S=MX['symbols']
        if not (C[0] in S):
            S.append(C[0])
        if not (C[1] in S):
            S.append(C[1])
        for coeff in MX['coeffs']:
            if ((coeff[0]==C[0]) and (coeff[1]==C[1]))or((coeff[0]==C[1]) and (coeff[1]==C[0])):
                if coeff[2]!=C[2]:
                    raise Error(51,C[0],C[1],coeff[2],C[2])
        MX['coeffs'].append(C)
        return
    def MatrixList(self):
        ML=[]
        for CE in self.CorrList:
            if len(CE['symbols'])>0:
                ME={}
                ME['symbols']=CE['symbols'][:]
                S=ME['symbols']
                l=len(S)
                A=Numpy.zeros((l,l),dtype='float64')
                for coeff in CE['coeffs']:
                    i=S.index(coeff[0])
                    j=S.index(coeff[1])
                    v=coeff[2]
                    A[i,j]=v
                    A[j,i]=v
                for i in xrange(l):
                    A[i,i]=1.0
                ME['matrix']=A
                ME['ismodi']=False
                ME['lmn']=0
                ME['iter']=0
                ML.append(ME)
        return ML
    def AllSymbols(self):
        SL=[]
        for CE in self.CorrList:
            if len(CE['symbols'])>0:
                SL.extend(CE['symbols'])
        return SL

def MakeCorrMatrixList(opts,data):
    '''
    create the correlation sub-matrix list and the list of correlated symbols
      check that only normally distributed quantities are correlated
    '''
    MX=CorrMatrixList()
    if len(data['corrs'])>0:
        for C in data['corrs']:
            if (C[0]==C[1]):
                if (C[2]!=1.0):
                    raise Error(21,C[0],C[1],C[2])
            else:
                i=MX.FindSubMatrixId(C[0])
                j=MX.FindSubMatrixId(C[1])
                if (i<0) and (j<0):
                    MX.AddNewMatrix(C)
                elif (i!=j) and (i>=0) and (j>=0):
                    i=MX.JoinMatrix(i,j)
                    MX.AddToMatrix(i,C)
                else:
                    if i<0:
                        i=j
                    MX.AddToMatrix(i,C)
    data['corrmtx']=MX.MatrixList()
    SL=MX.AllSymbols()
    VL={}
    for v in data['vars']:
        VL[v['sym']]=v['exec']
    for S in SL:
        if not (S in VL.keys()):
            raise Error(17,S)

        if VL[S][0]!=1:
            raise Error(18,S)
    data['corrsyms']=SL
    return MX

def Compose(EW,EV):
    '''
    Spectral decomposition of a correlation matrix from eigenvalues and eigenvectors
    Parameter: EW: array [n] of eigenvalues
               EV: array [n,n] of eigenvectors
    Return: Array[n,n] containing the correlation matrix
    The algorithm is based of the section Spectral decomposition in
        Riccardo Rebonato, Peter Jaeckel: The most general methodology to create a valid
        correlation matrix for risk management and option pricing purposes,
        http://www.quarchome.org/correlationmatrix.pdf
    '''
    n=len(EW)
    L=Numpy.matrix(Numpy.zeros((n,n),dtype='float64'))
    T=Numpy.matrix(Numpy.zeros((n,n),dtype='float64'))
    for i in xrange(n):
        if EW[i]>0:
            L[i,i]=math.sqrt(EW[i])
    for i in xrange(n):
        Ti=0
        for j in xrange(n):
            Ti+=EV[i,j]**2 * EW[j]
        T[i,i]=1/math.sqrt(Ti)
    B=T*EV*L
    M=B*B.T
    for i in xrange(n):
        M[i,i]=1.0
    return Numpy.array(M)

def makeCorr(EW,EV,NR,n,sev):
    PEW=Numpy.maximum(EW+NR,sev)
    s=Numpy.sum(PEW)
    if s==0.0:
        PEW=Numpy.maximum(EW,sev)
    else:
        PEW=PEW/s*n
    RR=Compose(PEW,EV)
    return RR

def EV2ThetaMatrix(EW,EV):
    n=len(EW)
    L=Numpy.matrix(Numpy.zeros((n,n),dtype='float64'))
    T=Numpy.matrix(Numpy.zeros((n,n),dtype='float64'))
    for i in xrange(n):
        if EW[i]>=0:
            L[i,i]=math.sqrt(EW[i])
    for i in xrange(n):
        Ti=0
        for j in xrange(n):
            Ti+=EV[i,j]*EV[i,j]*EW[j]
        T[i,i]=1/math.sqrt(Ti)
    B=T*EV*L
    thmat=Numpy.matrix(Numpy.zeros((n,n-1),dtype='float64'))
    for i in xrange(n):
        for j in xrange(n-1):
            if j==0:
                thmat[i,0]=math.acos(B[i,0])
            else:
                s=1
                for k in xrange(j):
                    s*=math.sin(thmat[i,k])
                p=B[i,j]/s
                if p>1:
                    p=1
                if p<-1:
                    p=-1
                thmat[i,j]=math.acos(p)
        s=1
        for k in xrange(n-1):
            s*=math.sin(thmat[i,k])
        if B[i,n-1]/s<0:
            for j in xrange(n-1):
                if j==0:
                    thmat[i,0]=-math.acos(B[i,0])
                else:
                    s=1
                    for k in xrange(j):
                        s*=math.sin(thmat[i,k])
                    p=B[i,j]/s
                    if p>1:
                        p=1
                    if p<-1:
                        p=-1
                    thmat[i,j]=math.acos(p)
    thmat=Numpy.array(thmat)
    return thmat

def Theta2CorrMatrix(n,thmat):
    if thmat.shape!=(n,n-1):
        raise Error(255,"Theta2CorrMatrix parameter error!")
    B=Numpy.matrix(Numpy.zeros((n,n),dtype='float64'))
    uvec=Numpy.matrix(Numpy.ones((n,1),dtype='float64'))
    cosmat=Numpy.cos(thmat)
    sinmat=Numpy.sin(thmat)
    cosmat=Numpy.concatenate((cosmat,uvec),1)
    sinmat=Numpy.concatenate((uvec,sinmat),1)
    sinmat=Numpy.cumprod(sinmat,1)
    B=Numpy.matrix(Numpy.multiply(cosmat,sinmat))
    R=B*B.T
    return R

def W2Norm(m,M1,M2):
    return LSQN(2,M1,M2)

def RandomDelta(Q,l):
    M=Numpy.zeros(Q.shape,dtype='float64')
    n=len(Q)
    for i in xrange(n):
        M[i,i]=0.0
        for j in range(i+1,n):
            if Q[i,j]!=0.0:
                M[i,j]=(Numpy.random.random(1)-0.5)*l
                M[j,i]=M[i,j]
    return M

def Walk3(Q,eps=0,maxits=0,sev=0):
    '''  Nearest correlation matrix by random walk.
         X = Walk2(Q,EPS,MAXITS,SEV)
         finds the nearest correlation matrix to the symmetric matrix A.
         EPS is a convergence tolerance, which defaults to 1000*EPS.
    '''
    if eps<=0:
        eps = len(Q)*1000*Numpy.finfo(Numpy.double).eps
    m=2
    Lambda=0.01*4
    n=len(Q)
    if maxits==0:
        maxits=n**3+2*n
    EW,EV=Numpy.linalg.eigh(Q)
    MEW=Numpy.min(EW)
    M=Q
    i=0
    while (Lambda>eps) and (MEW<=0):
        isimp=False
        imp=False
        Lambda=Lambda/2.0
        MDS=[]
        for itr in xrange(maxits):
            i+=1
            D=RandomDelta(Q,Lambda)
            MD=M+D
            if LMN(0, MD, Q)<0.005:
                EW,EV=Numpy.linalg.eigh(MD)
                if Numpy.min(EW)>MEW:
                    MDS.append({'MEW':Numpy.min(EW), 'M':MD})
                    isimp=True
                    if Numpy.min(EW)>0:
                        M=MD
                        MEW=Numpy.min(EW)
                        break
        if isimp:
            MW=MEW
            for MDE in MDS:
                if MDE['MEW']>MW:
                    MW=MDE['MEW']
                    MD=MDE['M']
            M=MD
            MEW=MW
    return M,i,MEW>0

def Walk2(Q,eps=0,maxits=0,sev=0):
    '''  Nearest correlation matrix by random walk.
         X = Walk2(Q,EPS,MAXITS,SEV)
         finds the nearest correlation matrix to the symmetric matrix A.
         EPS is a convergence tolerance, which defaults to 1000*EPS.
    '''
    if eps<=0:
        eps = len(Q)*1000*Numpy.finfo(Numpy.double).eps
    m=20
    Lambda=math.pi/4
    n=len(Q)
    if maxits==0:
        maxits=n**2*4
    EW,EV=Numpy.linalg.eigh(Q)
    TH0=EV2ThetaMatrix(EW,EV)
    r0=makeCorr(EW,EV,0,n,sev)
    F0=W2Norm(m,Q,r0)
    F=F0
    TH=TH0
    il1=True
    isimp=False
    while il1:
        imp=False
        Lambda=Lambda/2.0
        for itr in xrange(maxits):
            R=2*(Numpy.random.random(TH.shape)-0.5)
            NR=math.sqrt(Numpy.sum(R**2))
            R=R/NR
            THR=TH+R*Lambda
            r=Theta2CorrMatrix(n,THR)
            F1=W2Norm(m,Q,r)
            if F1<F:
                TH=THR
                F=F1
                imp=True
                isimp=True
        il1=Lambda>eps
    if isimp:
        QR=Theta2CorrMatrix(n,TH)
    else:
        QR=r0
    return QR

def Walk1(Q,eps=0,maxits=200,sev=0):
    '''  Nearest correlation matrix by random walk.
         X = Walk1(Q,EPS,MAXITS,SEV)
         finds the nearest correlation matrix to the symmetric matrix A.
         EPS is a convergence tolerance, which defaults to 1000*EPS.

    '''
    if eps<=0:
        eps = len(Q)*1000*Numpy.finfo(Numpy.double).eps
    Lambda=2
    n=len(Q)
    #start value
    EW,EV=Numpy.linalg.eigh(Q)
    r=makeCorr(EW,EV,0,n,sev)
    F0=LMN(0,Q,r)
    F=F0
    il1=True
    imp=False
    while il1:
        imp=False
        Lambda=Lambda/2.0
        for itr in xrange(maxits):
            R=2*(Numpy.random.random(n)-0.5)
            NR=math.sqrt(Numpy.sum(R**2))
            R=R/NR
            r=makeCorr(EW,EV,R*Lambda,n,sev)
            F1=LMN(0,Q,r)
            if F1<F:
                EW=Numpy.maximum(EW+R*Lambda,sev)
                EW=EW/Numpy.sum(EW)*n
                F=F1
                imp=True
        il1=Lambda>eps
    QR=makeCorr(EW,EV,0,n,sev)
    return QR

inf=10E38

def Near4(A,tol=0,maxits=1000,sev=0):
    NORM = Numpy.linalg.norm
    '''  Nearest correlation matrix.
         X, iter = Near4(A,tol,maxits,sev)
         finds the nearest correlation matrix to the symmetric matrix A.
         tol is a convergence tolerance, which defaults to 16*EPS.
         maxits is the maximum number of iterations, which defaults to 1000.
         sev is the value which negative eigenvalues are shifted to, which defaults to 0.

         The implemetation follows the amgorithm published by N. J. Higham.
         Reference:  N. J. Higham, Computing the nearest correlation
         matrix---A problem from finance. IMA J. Numer. Anal.,
         22(3):329-343, 2002.
    '''
    if tol<=0:
        tol = len(A)*1000*Numpy.finfo(Numpy.double).eps
    X = A
    Y = A
    iter = 1

    rel_diffX = inf

    rel_diffY = inf
    rel_diffXY = inf

    dS = Numpy.zeros(A.shape);

    while (rel_diffX>tol) or (rel_diffY>tol) or (rel_diffXY>tol):
        Xold = X
        R = X - dS
        X = Near4ProjSpd(R,sev)
        dS = X - R
        Yold = Y
        Y = Near4ProjUnitDiag(X)
        rel_diffX = NORM(X-Xold)/NORM(X)
        rel_diffY = NORM(Y-Yold)/NORM(Y)
        rel_diffXY = NORM(Y-X)/NORM(Y)
        iter = iter + 1
        if iter > maxits:
            raise Error(52,maxits)
        X = Y;
    return X, iter

def isequal(A,B):
    T=Numpy.equal(A,B)
    return Numpy.alltrue(T)

def Near4ProjSpd(A,sev=0):
    if not isequal(A,A.T):
        raise Error(255,'Internal, spd - matrix is not symmetric!')
    EW,EV=Numpy.linalg.eigh(A)
    PEW=Numpy.maximum(EW,sev)
    PEWM=Numpy.matrix(Numpy.diag(PEW))
    A=EV*PEWM*EV.T
    A=(A+A.T)/2
    return A

def Near4ProjUnitDiag(A):
    n = len(A)
    B = Numpy.copy(A)
    for i in xrange(n):
        B[i,i]=1
    return B

def LMN(m,M1,M2):
    '''
    Modified Least Maximum Norm
    Parameter: m: 0 - standard least maximum norm, 1 - weighted least maximum norm
               M1, M2: array [n,n] or matrix [n,n] matrix to compare
    Return: float containing the least maximum norm
    LMN will calculate the larges component wise difference between M1 and M2
    '''
    n1,m1=M1.shape
    n2,m2=M2.shape
    if (n1!=n2) or (m1!=m2) or (n1!=m1):
        raise Error(254)
    max=0
    f=1
    for i in xrange(n1):
        for j in xrange(n1):
            if m==1:
                if M1[i,j]>=M2[i,j]:
                    f=math.fabs(M1[i,j])
                else:
                    f=math.fabs(M2[i,j])
                if f<0.1:
                    f=0.1
            d=math.fabs(M1[i,j]-M2[i,j])*f
            if d>max:
                max=d
    return max

def LSQN(m,M1,M2):
    '''
    Least Squares Norm
    '''
    if m<=0:
        m=2
    n1,m1=M1.shape
    n2,m2=M2.shape
    if (n1!=n2) or (m1!=m2) or (n1!=m1):
        raise Error(254)
    Nn=0
    for i in xrange(n1):
        for j in xrange(n1):
            Nn+=math.fabs(M1[i,j]-M2[i,j])**m
    return Nn

def CheckMatrix(M,e1=-0.1,sev=1E-10,lmn=1,cm=0):
    '''
    Check Correlation Matrix
    Parameter: M: correlation matrix as array
               e1: smallest eigenvalue which could be shifted
               sev: small positive value used for shifting negative eigenvalues
               lmn: 0 - standard least maximum norm, 1 - modified least maximum norm
               cm: 0 - Spectral decomposition
                   1 - Near4
                   2 - Walk1
                   3 - Walk2
    Return: psd: flag indicating that the matrix is positive semi definite
            ismodi: flag indication if the matrix needed to be modified
            norm: calculated norm of the modification
            MM: modified correlation matrix, ready to be used
    '''
    ismodi=False
    norm=0
    MM=M
    iter=0
    try:
        CM=Numpy.linalg.cholesky(M)
        psd=True
    except Numpy.linalg.LinAlgError, e:
        EW,EV=Numpy.linalg.eigh(M)
        psd=True
        for W in EW:
            if W<0:
                psd=False
        if not psd:
            m=True
            for i,W in enumerate(EW):
                if W<e1:
                    m=False
                elif W<sev:
                    EW[i]=sev
            if m:
                if cm==0:
                    EW=EW/Numpy.sum(EW)*len(EW)
                    MM=Compose(EW,EV)
                elif cm==1:
                    MM,iter=Near4(M,sev=sev)
                elif cm==2:
                    MM=Walk1(M,sev=sev)
                elif cm==3:
                    MM=Walk2(M,sev=sev)
                elif cm==4:
                    MM,i,psd=Walk3(M,sev=sev)
                    if not psd:
                        iter=1
                        EW=EW/Numpy.sum(EW)*len(EW)
                        MM=Compose(EW,EV)
                    else:
                        iter=0
                try:
                    CM=Numpy.linalg.cholesky(MM)
                    psd=True
                except Numpy.linalg.LinAlgError, e:
                    EW,EV=Numpy.linalg.eigh(MM)
                    psd=True
                    for W in EW:
                        if W<0:
                            psd=False
                if psd:
                    ismodi=True
                    norm=LMN(lmn,M,MM)
    return psd, ismodi, norm, MM, iter

def CheckCorrMatrix(opts,data):
    '''
    Check all Correlation Sub-Matrices
    Parameter: opts: program options
               data: global model data
    Return: tpsd: flag indicating that all sub-matrices are positive semi definite
    '''
    ML=data['corrmtx']
    tpsd=True
    for ME in ML:
        psd,ismodi,lmn,MM,iter = CheckMatrix(ME['matrix'],opts['-e1'],opts['-sev'],opts['-lmn'],opts['-mcp'])
        if psd:
            ME['ismodi']=ismodi
            if ismodi:
                ME['lmn']=lmn
                ME['matrix']=MM
                ME['iter']=iter
            else:
                ME['lmn']=0
        tpsd=tpsd and psd
    return tpsd

def IsCorrModi(opts,data):
    f=False
    for ME in data['corrmtx']:
        if ME['ismodi']:
            f=True
    return f

def MakeCovMatrix(opts,data):
    '''
    Make Covariance Matrix from Correlation Matrix
    Parameter: opts: program options
               data: global model data
    Return: CL: covariance matrix list
      take the correlation sub-matices in data['corrmtx'] and
      create a list of covariance matrices in data['covmtx']
      An entry in data['covmtx'] is dictionary containg:
        ['symbols']: list of symbols the sub matrix is used for
        ['means']: the mean values of the symbols
        ['matrix']: array of (len(['symbols']),len(['symbols'])) containing the covariances
    '''
    CL=[]
    VL={}
    for v in data['vars']:
        VL[v['sym']]=v['exec']
    for ME in data['corrmtx']:
        CE={}
        S=ME['symbols']
        CM=ME['matrix']
        l=len(S)
        A=Numpy.zeros((l,l),dtype='float64')
        for i in xrange(l):
            for j in range(i,l):
                q1=S[i]
                q2=S[j]
                s1=VL[q1][2]
                s2=VL[q2][2]
                v=CM[i,j]*s1*s2
                A[i,j]=v
                A[j,i]=v
        CE['symbols']=ME['symbols'][:]
        VS=[]
        for s in CE['symbols']:
            VS.append(VL[s][1])
        CE['means']=VS
        CE['matrix']=A
        CL.append(CE)
    data['covmtx']=CL
    return CL

def CheckMonotone(data):
    s=len(data)
    warnings.simplefilter("ignore",UserWarning)
    data, ind=Numpy.unique1d(data,True)
    warnings.resetwarnings()
    diff=Numpy.setdiff1d(Numpy.arange(s),ind)
    return data, diff

def MakeMonotone(opts,idata,name):
    context=opts['CONTEXT']
    data, diff=CheckMonotone(idata)
    if len(diff)>0:
        context.PRINT('Warning: The data for '+name+' contains '+context.STR(len(diff))+' duplicate values!')
    if len(diff)>0.1*len(idata):
        context.PRINT('Warning: The elimination of more than 10% duplicate values is not possible!')
        data=idata
    else:
        d=1
        for k in range(len(diff)):
            if d>1:
                d-=1
                continue
            j=diff[k]
            d=1
            while (k+d<len(diff)) and (diff[k+d]==j+d):
                d+=1
            if d>2:
                context.PRINT('Warning: The elimination of a sequence of more than 2 duplicate values is not possible!')
                data=idata
                break
            l=data[j-1]
            if j<len(data):
                r=data[j]
            else:
                r=data[j-1]*1.0000000001
            delta=(r-l)/(d+100)
            for m in range(d):
                v=l+(m+1)*delta
                data=Numpy.insert(data,j+m,v)
        tmp, diff=CheckMonotone(data)
        if len(diff)>0:
            context.PRINT('Warning: The duplicate values in the data for '+name+' cannot be corrected!')
    return data

def CanExec(equ,evl):
    _v=''
    f=True
    for v in equ['cont']:
        if not (v in evl):
            _v=v
            f=False
            break
    return f, _v

def FindExecOrder(opts,data):
    '''
    Find Execution Order
    Parameter: opts: program options
               data: global model data
    Return: EXO: execution order (list of indexes in data['equs'])
      Tries to find a linear execution order of the set of
      equations given in <data['equs']>
      Does also some consistency checks
      EVL is a dictionary of symbols evaluated so far
    '''
    def FindID(i,exo):
        f=False
        for j in exo:
            if j==i:
                f=True
                break
        return f

    def FindSym(opts,s,D):
        found=False
        FS=None
        for S in D:
            if s==S['sym']:
                found=True
                FS=S
                break
        if not found:
            opts['CONTEXT'].ERROR(255,'Internal, Symbol "'+s+'" not found!')
        return FS
    context=opts['CONTEXT']
    for equ in data['equs']:
        CS=set(equ['cont'])
        for uf in equ['contf']:
            f=FindSym(opts,uf,data['funcdefs'])
            CS=CS.union(set(f['uglobal']))
            for cf in f['ccontf']:
                f1=FindSym(opts,cf,data['funcdefs'])
                CS=CS.union(set(f1['uglobal']))
        equ['cont']=list(CS)
    EXO=[]
    EXON=[]
    EVL={}
    for v in data['vars']:
        if v['sym'] in EVL.keys():
            context.ERROR(12,v['sym'])
        else:
            EVL[v['sym']]=None
    for j in range(0,len(data['equs'])):
        for i in range(0,len(data['equs'])):
            if not FindID(i,EXO):
                ce,v = CanExec(data['equs'][i],EVL)
                if ce:
                    EXO.append(i)
                    Nm=data['equs'][i]['sym']
                    if Nm in EVL.keys():
                        context.ERROR(12,Nm)
                    else:
                        EVL[Nm]=None
                    EXON.append(Nm)
                    break
                else:
                    f=False
                    for k  in range(0,len(data['equs'])):
                        if data['equs'][k]['sym']==v:
                            f=True
                            break
                    if not f:
                        context.ERROR(11,v)
    if len(EXO)!=len(data['equs']):
        msg='\n'
        msg+='Execution Order: ['+(', '.join(EXON))+']\n'
        msg+='Valid Symbols: ['+(', '.join(EVL))+']\n'
        for k in range(0,len(data['equs'])):
            if not FindID(k,EXO):
                msg+='Unknown: '+data['equs'][k]['sym']+': '+context.STR(data['equs'][k]['cont'])+'\n'
        context.ERROR(10,msg)
    data['exo']=EXO
    data['evl']=EVL
    return EXO

def CheckResultContributer(opts,data):
    EVL=data['evl']
    RL=data['results']
    for R in RL:
        ce,v = CanExec(R,EVL)
        if not ce:
            opts['CONTEXT'].ERROR(14,v,R['name'])
    return

def GetValues(data,L,n):
    '''
    Returns a vector of sampling values (size n) based on the specification
    given in L. L[0] defines the shape of the pdf to sample the data from.
    '''
    simcon=data['simcon']
    if L[0]==0:    #constant (value=L[1])
        R=L[1]#*Numpy.ones(n)
    elif L[0]==1:  #gauss (mu=L[1], sigma=L[2])
        R=simcon.RS.normal(L[1],L[2],n)
    elif L[0]==2:  #rectangular (mean=L[1], halfwidth=L[2])
        ll=L[1]-L[2]
        wd=2*L[2]
        R=simcon.RS.random_sample(n)*wd+ll
    elif L[0]==3:  #triangular (mean=L[1], halfwidth=L[2])
        R=simcon.RS.triangular(L[1]-L[2],L[1],L[1]+L[2],n)
    elif L[0]==4:  #trapezoidal  (mean=L[1], halfwidth=L[2], beta=L[3])
        HW=L[2]
        b=HW*(1 - L[3])
        a=2 * HW - b
        R1=simcon.RS.random_sample(n)*a
        R2=simcon.RS.random_sample(n)*b
        R=R1+R2+L[1]-HW
    elif L[0]==5:  #U-shape (mean=L[1], halfwidth=L[2])
        pi2=2 * math.pi
        R=Numpy.sin(simcon.RS.random_sample(n) * pi2)*L[2] + L[1]
    elif L[0]==6:  #student-t (mean=L[1], sigma=L[2], degrees of freedom=l[3])
        R=simcon.RS.standard_t(L[3],n)*L[2]+L[1]
    elif L[0]==7:  #poisson (mean=L[1])
        R=1.0*simcon.RS.poisson(L[1],n)
    elif L[0]==8:  #curvilinear trapezoidal (mean=L[1], halfwidth=L[2], beta=L[3])
        u=simcon.RS.random_sample(n)
        v=simcon.RS.random_sample(n)
        z=L[2]*L[3]+u*L[2]*(1-L[3])
        R=L[1]-z+v*2*z
    elif L[0]==9:  #exponential (mean=L[1])
        R=simcon.RS.exponential(L[1],n)
    elif L[0]==10:  #gamma (shape=L[1], scale=L[2])
        R=simcon.RS.gamma(L[1],L[2],n)
    elif L[0]==11:  #discrete (fileID=L[1], idx=L[2], shift=L[3], scale=L[4])
        id=L[2]
        RD=data['discretefiles'][L[1]]['data'][id]
        R0=simcon.RS.randint(0,len(RD),n)
        R=RD[R0]*L[4]+L[3]
    elif L[0]==12:  #import (fileID=L[1], idx=L[2])
        id=L[2]
        RD=data['discretefiles'][L[1]]['data'][id]
        R0=simcon.RS.randint(0,len(RD),n)
        R=RD[R0]
    elif L[0]==13:  #Chi square (mean=L[1], sigma=L[2], degrees of freedom=l[3])
        R=simcon.RS.chisquare(L[3],n)*L[2]+L[1]
    return R

def InitResult(file,runs,id,name,unit,definition):
    result={}
    result['NULL']=0
    result['filename']=file
    result['version']=__version__
    result['name']=name
    result['runs']=runs
    result['unit']=unit
    result['definition']=definition
    result['simblocks']=0
    result['addblocks']=0
    result['trials']=0
    result['id']=id
    result['No']=id+1
    result['blocksize']=[]
    result['sortblocksizes']=[]
    result['datablocks']=[]
    result['sortdatablocks']=[]
    result['commonratios']=[]
    result['averages']=[]
    result['stddevs']=[]
    result['subaverages']=[]
    result['subsizes']=[]
    result['substddevs']=[]
    result['low95s']=[]
    result['high95s']=[]
    result['low99s']=[]
    result['high99s']=[]
    result['low999s']=[]
    result['high999s']=[]
    result['lowbinlimits']=[]
    result['highbinlimits']=[]
    result['lowadaptlimits']=[]
    result['highadaptlimits']=[]
    result['medians']=[]
    result['tol']=0.0
    result['tolah']=0.0
    result['tolal']=0.0
    result['minruns0']=1
    result['minruns1']=1
    result['minruns2']=1
    result['tol0']=0.0
    result['tol1']=0.0
    result['tol2']=0.0
    result['s0']=0.0
    result['s1']=0.0
    result['s2']=0.0
    result['average']=0.0
    result['stddev']=0.0
    result['stdavg']=0.0
    result['lowstd']=0.0
    result['highstd']=0.0
    result['low95']=0.0
    result['high95']=0.0
    result['low99']=0.0
    result['high99']=0.0
    result['low999']=0.0
    result['high999']=0.0
    result['median']=0.0
    result['corrs']=[]
    result['corr']=Numpy.array([1])
    result['ircorrs']={}
    result['ircorr']={}
    result['Taverage']=0.0
    result['Tstddev']=0.0
    result['Tlow95']=0.0
    result['Thigh95']=0.0
    result['Tlow99']=0.0
    result['Thigh99']=0.0
    result['Tlow999']=0.0
    result['Thigh999']=0.0
    result['Tmedian']=0.0
    result['corr']=Numpy.array([1])
    result['ircorr']={}
    return result

def AddDataBlock(opts,result,datablock,size):
    MD=Numpy.ma.masked_invalid(datablock)
    if MD.count()<size:
        DB=MD.compressed()
        SC=MD.count()
    else:
        DB=datablock
        SC=size
    if (1.0*SC)/(1.0*size)<opts['-nl']:
        opts['CONTEXT'].ERROR(56,int((1.0*SC)/(1.0*size)*100))
    result['datablocks'].append(datablock)
    result['blocksize'].append(size)
    result['sortdatablocks'].append(Numpy.sort(DB))
    result['sortblocksizes'].append(SC)
    result['averages'].append(0.0)
    result['stddevs'].append(0.0)
    result['subaverages'].append(0.0)
    result['subsizes'].append(0.0)
    result['substddevs'].append(0.0)
    result['low95s'].append(0.0)
    result['high95s'].append(0.0)
    result['low99s'].append(0.0)
    result['high99s'].append(0.0)
    result['low999s'].append(0.0)
    result['high999s'].append(0.0)
    result['lowbinlimits'].append(0.0)
    result['highbinlimits'].append(0.0)
    result['lowadaptlimits'].append(0.0)
    result['highadaptlimits'].append(0.0)
    result['medians'].append(0.0)
    return len(result['datablocks'])-1,SC,MD

def AnalyseDB(opts,db,bs,p,fs=False):
    '''
    calculates the limits of a coverage interval of a given
    probability p in a sorted data block.
    if not fs (force symmetric) checks the shortest interval option and
    searches for the shortest interval if option -i=1
    '''
    def pdf(db,bs,i,j):
        return 1.0*j/(bs*(db[i+j]-db[i]))

    def interpolate(h,bs,db):
        hi=int(math.floor(h))
        if hi>bs-2:
            limit=db[bs-1]
        elif hi<0:
            limit=db[0]
        else:
            limit=db[hi]+(h-hi)*(db[hi+1]-db[hi])
        return limit

    if p<0.001:
        return 0,0
    o=opts['-pq']
    p1=(1-p)/2
    p2=(1+p)/2
    if (o==0):
        q=int(math.floor(p * bs))
        r=int(math.floor((bs-q)/2))
        if q>bs-1:
            q=bs-1
        low=db[r]
        high=db[r+q]
        d=high-low
        if (opts['-i']==1) and (not fs):
            for i in xrange(bs-q):
                if db[i+q]-db[i]<d:
                    low=db[i]
                    high=db[i+q]
                    d=high-low
    elif (o==1):
        low=interpolate(p1 * bs + 0.5,bs,db)
        high=interpolate(p2 * bs + 0.5,bs,db)
    elif (o==2):
        low=interpolate(p1 * (bs+1.0/3.0) + 1.0/3.0,bs,db)
        high=interpolate(p2 * (bs+1.0/3.0) + 1.0/3.0,bs,db)
    elif (o==3):
        low=interpolate(p1 * (bs+1.0/4.0) + 3.0/8.0,bs,db)
        high=interpolate(p2 * (bs+1.0/4.0) + 3.0/8.0,bs,db)
    elif (o==4):
        low=interpolate(p1 * (bs+2) - 0.5,bs,db)
        high=interpolate(p2 * (bs+2) - 0.5,bs,db)
    else:
        opts['CONTEXT'].ERROR(65,o);
    return low,high

def DoAnalyzeResultDataBlock(opts,result,j):
    bin_p=opts['-hp']
    adapt_p=opts['-ap']
    bs=result['sortblocksizes'][j]
    p1=opts['-p1']
    p2=opts['-p2']
    p3=opts['-p3']
    result['low95s'][j], result['high95s'][j]=AnalyseDB(opts,result['sortdatablocks'][j],bs,p1)
    result['low99s'][j], result['high99s'][j]=AnalyseDB(opts,result['sortdatablocks'][j],bs,p2)
    result['low999s'][j], result['high999s'][j]=AnalyseDB(opts,result['sortdatablocks'][j],bs,p3)
    result['lowbinlimits'][j], result['highbinlimits'][j]=AnalyseDB(opts,result['sortdatablocks'][j],bs,bin_p,True)
    result['lowadaptlimits'][j], result['highadaptlimits'][j]=AnalyseDB(opts,result['sortdatablocks'][j],bs,adapt_p)
    result['medians'][j]=result['sortdatablocks'][j][math.floor(bs/2)]
    return

def Tfactor(p,nu):
    T=1.0*stats.t.ppf(1-(1-p)/2,nu)
    return T

def GetKfactor(opts,nu):
    k=opts['-k']
    if k>0:
        return k
    p=opts['-af']
    k=Tfactor(p,nu)
    return k

def SetTolleranz(opts,data,results):
    for i in range(0,len(results)):
        WS=WeightedStats(results[i]['averages'],results[i]['stddevs'],results[i]['sortblocksizes'])
        results[i]['tol']=5*math.pow(10,MAGNITUDE(WS.Stdev_tot)-opts['-sd'])/opts['-ad']
        alal=WMEAN(results[i]['lowadaptlimits'],results[i]['sortblocksizes'])
        results[i]['tolal']=5*math.pow(10,MAGNITUDE(WS.Mean-alal)-opts['-sd'])/opts['-ad']
        ahal=WMEAN(results[i]['highadaptlimits'],results[i]['sortblocksizes'])
        results[i]['tolah']=5*math.pow(10,MAGNITUDE(ahal-WS.Mean)-opts['-sd'])/opts['-ad']

def CheckResults(opts,data,results,j):
    F=True
    cb=opts['-at']
    n=len(results[0]['stddevs'])
    k=GetKfactor(opts,n-1)
    sn=math.sqrt(n)
    for i in range(0,len(results)):
        tol=results[i]['tol']/k
        tolal=results[i]['tolal']/k
        tolah=results[i]['tolah']/k
        WSM=WeightedStats(results[i]['averages'],results[i]['stddevs'],results[i]['sortblocksizes'])
        if ((cb & 1)>0) and (WSM.Stdev_eff/sn>=tol):
            F=False
            break
        WSV=WeightedStats(results[i]['stddevs'],None,results[i]['sortblocksizes'])
        if ((cb & 2)>0) and (WSV.Stdev_eff/sn>=tol):
            F=False
            break
        WSL=WeightedStats(results[i]['lowadaptlimits'],None,results[i]['sortblocksizes'])
        WSH=WeightedStats(results[i]['highadaptlimits'],None,results[i]['sortblocksizes'])
        if ((cb & 4)>0) and ((WSH.Stdev_eff/sn>=tolah) or (WSL.Stdev_eff/sn>=tolal)):
            F=False
            break
    return F

def SaveValidationData(opts,results,validation,EVL,rcount,block,vars):
    for i in xrange(len(vars)):
        validation['inputs'][i]['data'].append(EVL[vars[i]['sym']])
        pass
    for i in xrange(len(results)):
        validation['results'][i]['data'].append(results[i]['datablocks'][block])
        validation['results'][i]['sorted'].append(results[i]['sortdatablocks'][block])
        pass
    return

def InitValidation(data,results,validation):
    for v in data['vars']:
        validation['inputs'].append({'name':v['sym'], 'data':[]})
    for r in results:
        validation['results'].append({'name':r['name'], 'data':[], 'sorted':[]})
    return

def getValidationID(validation,name):
    j=-1
    for i in xrange(len(validation['results'])):
        if validation['results'][i]['name']==name:
            j=i
            break
    return j

def AnalyzeValidation(opts,results,validation):
    for result in results:
        i=getValidationID(validation,result['name'])
        validation['results'][i]['data']=Numpy.ma.masked_invalid(Numpy.concatenate((validation['results'][i]['data'][:]))).compressed()
        validation['results'][i]['sorted']=Numpy.sort(Numpy.ma.masked_invalid(Numpy.concatenate((validation['results'][i]['sorted'][:]))).compressed())
        tmp, diff=CheckMonotone(validation['results'][i]['sorted'])
        if len(diff)>0:
            opts['CONTEXT'].PRINT('Warning: The simulation results for '+result['name']+' contain '+opts['CONTEXT'].STR(len(diff))+' duplicate values!')
        result['Taverage']=Numpy.average(validation['results'][i]['data'])
        result['Tstddev']=validation['results'][i]['data'].std(ddof=1)
        bs=len(validation['results'][i]['sorted'])
        p1=opts['-p1']
        p2=opts['-p2']
        p3=opts['-p3']
        result['Tlow95'], result['Thigh95']=AnalyseDB(opts,validation['results'][i]['sorted'],bs,p1)
        result['Tlow99'], result['Thigh99']=AnalyseDB(opts,validation['results'][i]['sorted'],bs,p2)
        result['Tlow999'], result['Thigh999']=AnalyseDB(opts,validation['results'][i]['sorted'],bs,p3)
        result['Tmedian']=validation['results'][i]['sorted'][math.floor(bs/2)]
        result['Tcorr']=Numpy.array([1])
        result['Tircorr']={}
    return

def DoAnalyzeCorr(opts,results,EVL,rcount,block,vars):
    if opts['-ac']>0:
        MM=False
        EVLR={}
        AVGI={}
        STDI={}
        R=[]
        AVGR=[]
        STDR=[]
        if (opts['-ac'] & 2)!=0:
            for va in vars:
                v=va['sym']
                MD=Numpy.ma.masked_invalid(EVL[v])
                MM=Numpy.ma.mask_or(MM,Numpy.ma.getmask(MD))
        for i in xrange(rcount):
            MD=Numpy.ma.masked_invalid(results[i]['datablocks'][block])
            MM=Numpy.ma.mask_or(MM,Numpy.ma.getmask(MD))
        n=results[0]['blocksize'][block]
        c=n-Numpy.sum(MM)
        cr=(1.0*c)/(1.0*n)
        for i in xrange(rcount):
            results[i]['commonratios'].append(cr)
        if cr>opts['-nc']:
            dof=c-1
            if (opts['-ac'] & 2)!=0:
                for va in vars:
                    v=va['sym']
                    if c<n:
                        D=Numpy.ma.array(EVL[v],mask=MM).compressed()
                    else:
                        D=EVL[v]
                    EVLR[v]=D
                    if isinstance(D,float):
                        AVGI[v]=D
                        STDI[v]=0
                    else:
                        AVGI[v]=Numpy.average(D)
                        STDI[v]=D.std(ddof=1)
            for i in xrange(rcount):
                if c<n:
                    D=Numpy.ma.array(results[i]['datablocks'][block],mask=MM).compressed()
                    R.append(D)
                    AVGR.append(Numpy.average(D))
                    STDR.append(D.std(ddof=1))
                else:
                    R.append(results[i]['datablocks'][block])
                    AVGR.append(results[i]['averages'][block])
                    STDR.append(results[i]['stddevs'][block])
        if (opts['-ac'] & 1)!=0:
            cm=Numpy.zeros((rcount,rcount))*Numpy.nan
            if cr>opts['-nc']:
                for i in xrange(rcount):
                    cm[i,i]=1.0
                    dq1=R[i]-AVGR[i]
                    s1=STDR[i]
                    for j in range(i+1,rcount):
                        dq2=R[j]-AVGR[j]
                        s2=STDR[j]
                        rs=(dq1*dq2).sum()/dof
                        if (rs==0) or (s1==0) or (s2==0):
                            r=0
                        else:
                            r=rs/(s1 * s2)
                        cm[i,j]=r
                        cm[j,i]=r
            for i in xrange(rcount):
                results[i]['corrs'].append(cm[i])
        if (opts['-ac'] & 2)!=0:
            if cr>opts['-nc']:
                for va in vars:
                    v=va['sym']
                    dq1=EVLR[v]-AVGI[v]
                    s1=STDI[v]
                    for j in xrange(rcount):
                        dq2=R[j]-AVGR[j]
                        s2=STDR[j]
                        rs=(dq1*dq2).sum()/dof
                        if (rs==0) or (s1==0) or (s2==0):
                            r=0
                        else:
                            r=rs/(s1 * s2)
                        results[j]['ircorrs'][v].append(r)
            else:
                for va in vars:
                    for j in xrange(rcount):
                        results[j]['ircorrs'][va['sym']].append(Numpy.nan)
    return

def ApplyConstraints(data,EVL,isInput):
    for C in data['constraints']:
        if C['inp']==isInput:
            MM=~eval(C['code'],data['predefequs'],EVL)
            if Numpy.ma.all(MM):
                data['context'].ERROR(57,C['name'],C['src'])
            if Numpy.ma.any(MM):
                MA=Numpy.ma.array(EVL[C['sym']],mask=MM)
                EVL[C['sym']]=MA.filled(Numpy.nan)
    return

def PrepareImports(opts,data):
    MemName=BeginInfo(opts['CONTEXT'],'PrepareImports')
    IL=[]
    IFS=[]
    for v in data['vars']:
        if v['exec'][0]==12:
            IL.append(v['sym'])
            id=-1
            for i,IF in enumerate(IFS):
                if IF['fid']==v['exec'][1]:
                    id=i
                    break
            if id<0:
                IFS.append({'fid':v['exec'][1], 'syms':[], 'data':[], 'length':len(data['discretefiles'][v['exec'][1]]['data'][0])})
                id=len(IFS)-1
            IF=IFS[id]
            IF['syms'].append(v['sym'])
            IF['data'].append(data['discretefiles'][v['exec'][1]]['data'][v['exec'][2]])
            IF['pos']=0
    data['importsyms']=IL
    data['importfiles']=IFS
    EndInfo(opts['CONTEXT'],MemName)
    return

def RunSimulation(opts,data,results,validation,k):
    context=opts['CONTEXT']
    simcon=data['simcon']
    MemName=BeginInfo(context,'RunSimulation')
    if (k % 79 == 0) and (k!=0):
        context.WRITE('\n',VL_Progress)
    context.WRITE('.',VL_Progress)
    n=opts['-bs']
    simcon.DataBlockSize=n
    ones=Numpy.ones(n)
    ecount=len(data['equs'])
    rcount=len(data['results'])
    #R=Numpy.empty(n*rcount, dtype='float64').reshape(n,rcount)
    VL=[]
    for v in data['vars']:
        if not (v['sym'] in data['corrsyms']) and not (v['sym'] in data['importsyms']):
            VL.append([v['sym'],v['exec']])
    EVL=data['predefequs']
    R=1.0
    for CX in data['covmtx']:
        RD=simcon.RS.multivariate_normal(CX['means'],CX['matrix'],n).T
        CS=CX['symbols']
        for i in xrange(len(CS)):
            EVL[CS[i]]=RD[i]
    for IF in data['importfiles']:
        if opts['-io']==1:
            if IF['pos']+n>IF['length']:
                n1=IF['length']-IF['pos']
                if n1>0:
                    R0=Numpy.concatenate(Numpy.arange(n1)+IF['pos'],Numpy.arange(n-n1))
                else:
                    R0=Numpy.arange(n)
                IF['pos']=n-n1
            else:
                R0=Numpy.arange(n)+IF['pos']
                IF['pos']=IF['pos']+n
        else:
            R0=simcon.RS.randint(0,IF['length']-1,n)
        for j,iv in enumerate(IF['syms']):
            EVL[iv]=IF['data'][j][R0]
    for v in VL:
        EVL[v[0]]=GetValues(data,v[1],n)
    ApplyConstraints(data,EVL,True)
    for j in range(0,ecount):
            EVL[data['equs'][j]['sym']]=None
    for j in data['exo']:
        EVL[data['equs'][j]['sym']]=eval(data['equs'][j]['code'],EVL)
    ApplyConstraints(data,EVL,False)
    for j in range(0,rcount):
        RR=eval(data['results'][j]['code'],EVL)
        if type(RR)!=type(ones):
            RR=RR*ones
        i,sc,md=AddDataBlock(opts,results[j],RR,n)
        results[j]['runs']=results[j]['runs']+sc
        results[j]['trials']=results[j]['trials']+n
        results[j]['averages'][i]=Numpy.average(results[j]['sortdatablocks'][i])
        results[j]['stddevs'][i]=results[j]['sortdatablocks'][i].std(ddof=1)
        if opts['-sbs']>0:
            DBS=Numpy.reshape(md,(opts['-sbs'],simcon.DataBlockSize/opts['-sbs']))
            results[j]['subsizes'][i]=DBS.count(axis=0)
            results[j]['subaverages'][i]=Numpy.ma.average(DBS,axis=0)
            results[j]['substddevs'][i]=Numpy.ma.std(DBS,axis=0,ddof=1)
    if opts['-ac']!=0:
        DoAnalyzeCorr(opts,results,EVL,rcount,i,data['vars'])
    if opts['-vm']!=0:
        SaveValidationData(opts,results,validation,EVL,rcount,i,data['vars'])
    for j in range(0,rcount):
        DoAnalyzeResultDataBlock(opts,results[j],i)
    EndInfo(context,MemName)
    return

def OsPathToUri(filename):
    return filename

def ReadXML(opts,data,filename):
    context=opts['CONTEXT']
    MemName=BeginInfo(context,'ReadXML')
    xf=None
    if (opts['-fi']==0) and (opts['-xsd']=='-'):
        data['xsdfile']=[get_main_dir(),'OMCE.xsd']
        CheckFile(opts['CONTEXT'],data['xsdfile'])
        context.NOISE('Reading xsdfile begin...')
        xf=file(os.path.join(*data['xsdfile']),'r')
        context.NOISE('Reading xsdfile end...')
    else:
        if opts['-fi']==1:
            data['xsdfile']=''
        if opts['-xsd']!='-':
            data['xsdfile']=opts['CONTEXT'].PathJoin(opts['PATH'],opts['-xsd'])
        if data['xsdfile']!='':
            xsd=context.ReadFile(data['xsdfile'])
            xf=StringIO.StringIO(xsd)
    context.NOISE('Start ReadFile')
    xml=context.ReadFile(filename)
    context.NOISE('End ReadFile')
    if not (xf is None):
        if type(data['xsdfile'])==type([]):
            xsd_name=data['xsdfile'][-1]
        else:
            xsd_name=data['xsdfile']
        opts['CONTEXT'].PRINT("Validating against XML Schema (%s)" % xsd_name,VL_Info)
        xmlschemadoc=etree.parse(xf)
        xf.close()
        xmlschema=etree.XMLSchema(xmlschemadoc)
        xmldoc=etree.XML(xml)
        xmlschema.assertValid(xmldoc)
    doc=None
    if amara_version==1:
        doc = amara.parse(xml)
    elif amara_version==2:
        doc = bindery.parse(xml,standalone=True,validate=False)
    else:
        context.ERROR(82)
    data['doc']=doc
    EndInfo(context,MemName)
    return

def DoBinaryWrite(opts,results,binname,info,ThdCtrl=None):
    '''
    info: list with two elements
        info[0] data block pointer points to the datablock that is currently written
        info[1] terminate flag, set when data in results is complete
        info[2] buffer status list contains a status word for every block in results
            info[2][i]==0: data block exists
            info[2][i]==1: data block is processed and ready
            info[2][i]==2: data block is written
            info[2][i]==3: data block is purged
    '''
    try:
        context=opts['CONTEXT']
        MemName=BeginInfo(context,'DoBinaryWrite')
        dbp=0
        rcount=len(results)
        wb=opts['-wb']
        if (wb!=0):
            RL=[]
            for R in results:
                RL.append(R['name'])
            RT=StringList2Bytes(RL)
            RT=PadZeros(RT,8)
            cbw=0
            longA = array.array('l')
            if wb==2:
                longA.append(0)
                longA.append(rcount)
            elif (wb==1) or (wb==3):
                longA.append(-1330463557)   # identifier for OMCE format
                longA.append(rcount)        # no of results
                longA.append(0)             # total number of runs
                longA.append(0)             # block size
                longA.append(len(RT))       # no of skip bytes
                longA.append(1)             # flags bit 0 if symbol list is present
                longA.append(0)             # not used
                longA.append(0)             # not used
            else:
                context.ERROR(8,wb)
            if (wb==3):
                terminate=False
                while not terminate:
                    if ThdCtrl!=None:
                        ThdCtrl[0].acquire()
                        terminate=info[1]
                        ThdCtrl[0].release()
                    else: terminate=True
            fdo = file(binname, mode='wb')
            fdo.write(longA)
            if (wb==1) or (wb==3):
                fdo.write(RT)
            ds=0
            C=0
            while True:
                if ThdCtrl!=None:
                    ThdCtrl[1].wait()
                    ThdCtrl[1].clear()
                    ThdCtrl[0].acquire()
                    terminate=info[1]
                    lbw=info[0]
                    bul=info[2]
                    ThdCtrl[0].release()
                else:
                    terminate=True
                    lbw=info[0]
                    bul=info[2]
                C+=1
                while (lbw>cbw) and (bul[cbw]==1):
                    bs=results[0]['blocksize'][cbw]
                    ds+=bs
                    if wb==2:
                        bl=Numpy.empty(bs*rcount, dtype='float64').reshape(bs,rcount)
                        for j in range(0,rcount):
                            bl[:,j]=results[j]['datablocks'][cbw]
                        bl=bl.reshape(rcount*bs)
                        fdo.write(bl)
                    elif wb==1:
                        for j in range(0,rcount):
                            db=Numpy.empty(bs, dtype='float64')
                            db[:]=results[j]['datablocks'][cbw]
                            fdo.write(db)
                    elif wb==3:
                        for j in range(0,rcount):
                            fdo.write(results[j]['sortdatablocks'][cbw])
                    if ThdCtrl!=None:
                        ThdCtrl[0].acquire()
                        info[2][cbw]=2
                        ThdCtrl[0].release()
                    else:
                        info[2][cbw]=2
                    cbw+=1
                while (len(bul)>dbp) and (bul[dbp]==2):
                    for j in range(0,rcount):
                        results[j]['datablocks'][dbp]=None
                        results[j]['sortdatablocks'][dbp]=None
                    if ThdCtrl!=None:
                        ThdCtrl[0].acquire()
                        info[2][dbp]=3
                        ThdCtrl[0].release()
                    else:
                        info[2][dbp]=3
                    dbp+=1
                if terminate and (cbw==lbw) and (dbp==lbw):
                    break
            fdo.close()
            fdo = file(binname, mode='rb+')
            if wb==2:
                longA[0]=ds
            elif (wb==1) or (wb==3):
                longA[2]=ds
                longA[3]=results[0]['blocksize'][0]
            fdo.write(longA)
            fdo.close()
            context.PRINT('Write Process Cyles: %d' % C,VL_Noise)
        else:
            C=0
            while True:
                if ThdCtrl!=None:
                    ThdCtrl[1].wait()
                    ThdCtrl[1].clear()
                    ThdCtrl[0].acquire()
                    terminate=info[1]
                    lbw=info[0]
                    bul=info[2]
                    ThdCtrl[0].release()
                else:
                    terminate=True
                    lbw=info[0]
                    bul=info[2]
                C+=1
                while (len(bul)>dbp) and (bul[dbp]==1):
                    for j in range(0,rcount):
                        results[j]['datablocks'][dbp]=None
                        results[j]['sortdatablocks'][dbp]=None
                    if ThdCtrl!=None:
                        ThdCtrl[0].acquire()
                        info[2][dbp]=2
                        ThdCtrl[0].release()
                    else:
                        info[2][dbp]=2
                    dbp+=1
                if terminate and (dbp==lbw):
                    break
            context.PRINT('Write Process Cyles: %d' % C,VL_Noise)
    except Error,er:
        ThdCtrl[0].acquire()
        info[3]=[er.number,er.params,TRACEINFO()]
        info[1]=True
        ThdCtrl[0].release()
    except (Exception,KeyboardInterrupt),e:
        ThdCtrl[0].acquire()
        if isinstance(e,KeyboardInterrupt):
            info[3]=[-1,context.MSG(5),'']
        else:
            info[3]=[255,context.STR(e),TRACEINFO()]
        info[1]=True
        ThdCtrl[0].release()
    EndInfo(context,MemName)
    return

def PrepareBinning(opts,data):
    bincount=opts['-hc']
    f=opts['-hf']
    data['lowbinlimit']=Numpy.average(data['lowbinlimits'])
    data['highbinlimit']=Numpy.average(data['highbinlimits'])
    data['average']=Numpy.average(data['averages'])
    data['pdf']=[]
    data['bins']=[]
    if data['lowbinlimit']!=data['highbinlimit']:
        if f!=1.0:
            data['lowbinlimit']=(1-f)*data['average']+f*data['lowbinlimit']
            data['highbinlimit']=(1-f)*data['average']+f*data['highbinlimit']
        data['binwidth']=abs(data['highbinlimit']-data['lowbinlimit'])/bincount
        data['bincount']=bincount
        for j in range(0,bincount):
            data['bins'].append(0)
            data['pdf'].append(0)
    else:
        data['binwidth']=0
        data['bincount']=bincount
        for j in range(0,bincount):
            data['bins'].append(0)
            data['pdf'].append(0)
        data['bins'][0]=len(data['datablocks'][0])
        data['pdf'][0]=1.0
    return

def PrepareAllBinning(opts,data):
    MemName=BeginInfo(opts['CONTEXT'],'PrepareAllBinning')
    for i in range(0,len(data)):
        PrepareBinning(opts,data[i])
    EndInfo(opts['CONTEXT'],MemName)
    return

def BinDataBlock(datablock,bins,bincount,binlimits):
    db=datablock.searchsorted(binlimits)
    for k in range(0,bincount):
        bins[k] =bins[k]+db[k+1]-db[k]
    return

def BinDataBlockResults(opts,data,i,bins,bincount,binlimits):
    for j in range(0,len(data)):
        BinDataBlock(data[j]['sortdatablocks'][i],bins[j],bincount[j],binlimits[j])
    return

def FinalizeBinning(opts,data):
    f=data['runs']*data['binwidth']
    bincount=data['bincount']
    if bincount>1:
        for j in range(0,bincount):
            data['pdf'][j]=data['bins'][j]/f
    return

def FinalizeAllBinning(opts,data):
    MemName=BeginInfo(opts['CONTEXT'],'FinalizeAllBinning')
    for i in range(0,len(data)):
        FinalizeBinning(opts,data[i])
    EndInfo(opts['CONTEXT'],MemName)
    return

def PowAverage(exp,data,ref1,ref2):
    if exp!=1.0:
        dat=Numpy.array(data)
        d=dat-Numpy.array(ref1)
        s=Numpy.sign(d)
        dd=s*Numpy.power(Numpy.abs(d),exp)
        av=Numpy.average(dd)
        s=Numpy.sign(av)
        av=s*Numpy.power(Numpy.abs(av),1.0/exp)+ref2
    else:
        av=Numpy.average(data)
    return av

class WeightedStats:
    '''
    class for weighted statistics
    '''
    def __init__(self,means,stdevs,weights):
        self.Mean=0.0
        self.Stdev_eff=Numpy.NaN
        self.N_eff=-1
        self.N=-1
        self.Stdev_tot=Numpy.NaN
        self.Avg_Stdev=Numpy.NaN

        self.means=Numpy.array(means)
        self.weights=1.0*Numpy.array(weights)
        sh=Numpy.shape(self.weights)
        m=1.0
        for p in sh:
            m*=p
        self.n_r=m
        self.N_eff=Numpy.average(self.weights)
        self.N=Numpy.sum(self.weights)

        self.Mean=Numpy.sum((self.means*self.weights))/self.N

        wd2=Numpy.sum(self.weights*Numpy.square(self.means-self.Mean))
        if self.n_r>1:
            self.Stdev_eff=math.sqrt(1.0/(self.N_eff * (self.n_r-1))*wd2)

        if not(stdevs is None):
            sds=Numpy.array(stdevs)
            wvs=Numpy.sum(self.weights*Numpy.square(sds))
            self.Avg_Stdev=Numpy.sqrt(wvs/self.N)
            self.Stdev_tot=math.sqrt((wvs+wd2)/(self.N-1))
        return

def DoAnalyzeResults(opts,data,MCruns,addruns):
    context=opts['CONTEXT']
    MemName=BeginInfo(context,'DoAnalyzeResults')
    crm=1.0
    ex=opts['-pa']
    nbs=opts['-bs']
    for i in range(0,len(data)):
        data[i]['simblocks']=MCruns
        data[i]['addblocks']=addruns
        WS=WeightedStats(data[i]['averages'],data[i]['stddevs'],data[i]['sortblocksizes'])
        data[i]['avgsize']=WS.N_eff
        data[i]['average']=WS.Mean
        if WS.Stdev_eff == Numpy.NaN:
            data[i]['stdavg']=Numpy.NaN
        else:
            data[i]['stdavg']=WS.Stdev_eff *math.sqrt(WS.N_eff/nbs)
        data[i]['avgstd']=WS.Avg_Stdev
        data[i]['stddev']=WS.Stdev_tot
        data[i]['stdevm']=WS.Stdev_tot/math.sqrt(WS.N)
        data[i]['low95']=PowAverage(ex,data[i]['low95s'],data[i]['averages'],data[i]['average'])
        data[i]['high95']=PowAverage(ex,data[i]['high95s'],data[i]['averages'],data[i]['average'])
        data[i]['low99']=PowAverage(ex,data[i]['low99s'],data[i]['averages'],data[i]['average'])

        data[i]['high99']=PowAverage(ex,data[i]['high99s'],data[i]['averages'],data[i]['average'])
        data[i]['low999']=PowAverage(ex,data[i]['low999s'],data[i]['averages'],data[i]['average'])
        data[i]['high999']=PowAverage(ex,data[i]['high999s'],data[i]['averages'],data[i]['average'])
        data[i]['median']=Numpy.average(data[i]['medians'])
        data[i]['lowstd']=data[i]['average']-data[i]['stddev']
        data[i]['highstd']=data[i]['average']+data[i]['stddev']
        if (opts['-ac'] & 1)>0:
            bc=len(data[i]['corrs'])
            cm=Numpy.zeros(len(data))
            for j in xrange(bc):
                cm+=data[i]['corrs'][j]
            cm/=bc
            data[i]['corr']=cm
        if (opts['-ac'] & 2)>0:
            for k in data[i]['ircorrs'].keys():
                cm=Numpy.average(data[i]['ircorrs'][k])
                data[i]['ircorr'][k]=cm
        if data[i]['runs'] < data[i]['trials']:
            R=(1.0*(data[i]['runs']))/(1.0*(data[i]['trials']))
            context.PRINT('Warning: About '+context.STR(100-int(R*100))+'% of the simulated results for "'+data[i]['name']+'" are not valid and have been discarded!',VL_Warn)
        if opts['-ac']>0:
            crm=min(crm,min(data[i]['commonratios']))
    if crm<=opts['-nc']:
        context.PRINT('Warning: Less than '+context.STR(int(crm*100))+'% of the common data is valid!\n         The correlation coefficients are not evaluated!',VL_Warn)
    EndInfo(context,MemName)
    return

def ReadOFD(opts,fn,s,hf,e,qc):
    context=opts['CONTEXT']
    H=[]
    K=[]
    FC=[]
    ofd=context.ReadFile(fn)
    f=StringIO.StringIO(ofd)
    while True:
        line=f.readline().strip()
        if line=="":
            break
        if line=="\n":
            continue
        if line.find("#")==0:
            continue
        if line.find("-")==0:
            opt=line.split('=')
            if opt[0]=='-separator':
                s=opt[1].strip('"''').replace('\\t','\t')
            elif opt[0]=='-quotechar':
                qc=opt[1].strip()
            elif opt[0]=='-header':
                hf=(opt[1]!='0')
            elif opt[0]=='-extension':
                e=opt[1].strip('"''')
                if e.find(".")!=0:
                    e='.'+e
            continue
        if line.find("=")>=0:
            E=line.split('=')
            df=''
            if (E[1][0]=='"') or (E[1][0]=="'"):
                pass
            elif E[1].find('(')>=0:
                try:
                    n,k,x=re.split('[(]|[)]',E[1])
                    if x!='':
                        raise Exception
                except:
                    context.ERROR(54,fn,line)
                E[1]=k
                df=n
            elif E[1].find('[')>=0:
                try:
                    n,k,x=re.split('\[|\]',E[1])
                    if (x!=''):
                        raise Exception
                except:
                    context.ERROR(54,fn,line)
                E[1]=n
                df=k
            H.append(E[0].strip())
            K.append(E[1].strip())
            FC.append(df.strip())
    f.close()
    return H,K,FC,s,hf,e,qc

def contains(achrs,da):
    f=False
    for c in achrs:
        if c in da:
            f=True
            break
    return f

def CreateDataFile(opts,results,file,fmt):
    context=opts['CONTEXT']
    MemName=BeginInfo(context,'CreateDataFile')
    Header, Keys, fc, sep, hf, ext, qc=opts[fmt]
    H=[]
    bc=opts['-hc']
    if hf:
        for j in xrange(len(Keys)):
            if (Keys[j].find('"')==0) or (Keys[j].find("'")==0):
                H.append(Header[j])
            elif Keys[j]=='BINS':
                for i in xrange(bc):
                    H.append(Header[j] % context.STR(i))
            elif (Keys[j]=='CORR'):
                if ((opts['-ac'] & 1)!=0):
                    cc=len(results[0]['corr'])
                    for i in xrange(cc):
                        H.append(Header[j] % context.STR(i))
            elif (Keys[j]=='IRCORR'):
                if  ((opts['-ac'] & 2)!=0):
                    for k in results[0]['ircorr'].keys():
                        H.append(Header[j] % k)
            elif (Keys[j]=='SID'):
                H.append(Header[j])
            else:
                if not (Keys[j] in results[0].keys()):
                    if fmt=='format-ohd':
                        context.ERROR(68,Keys[j])
                    else: # 'format-var'
                        context.ERROR(69,Keys[j])
                if (type(results[0][Keys[j]])==type([])) and ('[' in Header[j]):
                    if fc[j]=='':
                        for i in xrange(len(results[0][Keys[j]])):
                            H.append(Header[j] % context.STR(i))
                    else:
                        ps=fc[j].split(':')
                        if len(ps)==1:
                            if not isInt(ps[0]):
                                context.ERROR(55,Header[j],Keys[j])
                            H.append(Header[j] % ps[0])
                        elif len(ps)==2:
                            if not isInt(ps[0]) or not isInt(ps[1]):
                                context.ERROR(55,Header[j],Keys[j])
                            n1=int(ps[0])
                            n2=int(ps[1])
                            if n1>n2: n1,n2=n2,n1
                            if n1<0: n1=0
                            if n2>len(results[0][Keys[j]]): n2=len(results[0][Keys[j]])
                            for i in xrange(n1,n2):
                                H.append(Header[j] % context.STR(i))
                        else:
                            context.ERROR(55,Header[j],Keys[j])
                else:
                    H.append(Header[j])
    H=sep.join(H)
    if H!='':
        H+='\n'
    context.WriteFile(file,H,"w")
    EndInfo(context,MemName)
    return

def WriteResults2DataFile(opts,data,file,fmt,sid):
    context=opts['CONTEXT']
    MemName=BeginInfo(context,'WriteResults2DataFile')
    Header, Keys, fc, sep, hf, ext, qc=opts[fmt]
    bc=opts['-hc']
    pdf=opts['-pdf']
    dss=['bins','pdf']
    od=[]
    for i in xrange(len(Header)):
        context.PRINT('HD: '+Header[i]+', KEY: '+Keys[i]+', FC: '+fc[i],VL_Noise)
    for i in xrange(len(data)):
        D=[]
        for j in xrange(len(Keys)):
            if (Keys[j].find('"')==0) or (Keys[j].find("'")==0):
                D.append(Keys[j].strip('"'''))
            elif Keys[j]=='BINS':
                for k in range(0,bc):
                    D.append(context.STR(data[i][dss[pdf]][k]))
            elif (Keys[j]=='CORR'):
                if ((opts['-ac'] & 1)!=0):
                    cc=len(data[i]['corr'])
                    for k in range(0,cc):
                        D.append(context.STR(data[i]['corr'][k]))
            elif (Keys[j]=='IRCORR'):
                if ((opts['-ac'] & 2)!=0):
                    for k in data[0]['ircorr'].keys():
                        D.append(context.STR(data[i]['ircorr'][k]))
            elif (Keys[j]=='SID'):
                D.append(context.STR(sid))
            elif (type(data[i][Keys[j]])==type([])) and ('[' in Header[j]):
                da=data[i][Keys[j]]
                if fc[j]=='':
                    for k in xrange(len(da)):
                        D.append(context.STR(da[k]))
                else:
                    ps=fc[j].split(':')
                    if len(ps)==1:
                        n=int(ps[0])
                        if n<0: n=0
                        if n>=len(da): n=len(da)-1
                        D.append(context.STR(da[n]))
                        context.PRINT('Appending Data['+ps[0]+']',VL_Noise)
                    elif len(ps)==2:
                        n1=int(ps[0])
                        n2=int(ps[1])
                        if n1>n2: n1,n2=n2,n1
                        if n1<0: n1=0
                        if n2>len(da): n2=len(da)
                        context.PRINT('Appending Data['+context.STR(n1)+':'+context.STR(n2)+']',VL_Noise)
                        for k in xrange(n1,n2):
                            D.append(context.STR(da[k]))
                    else:
                        context.ERROR(55,Header[j],Keys[j],fc[j])
            else:
                if not (Keys[j] in data[i].keys()):
                    if fmt=='format-ohd':
                        context.ERROR(68,Keys[j])
                    else: # 'format-var'
                        context.ERROR(69,Keys[j])
                da=data[i][Keys[j]]
                if type(da)==type([]):
                    if (fc[j]=='') or (fc[j]=='sd'):
                        context.PRINT('Appending sd('+Keys[j]+')',VL_Noise)
                        da=STDEV(da)
                    elif (fc[j]=='avg'):
                        context.PRINT('Appending avg('+Keys[j]+')',VL_Noise)
                        da=MEAN(da)
                    else:
                        if isInt(fc[j]):
                            n=int(fc[j])
                            if n<0: n=0
                            if n>=len(da): n=len(da)-1
                            da=da[n]
                        else:
                            context.ERROR(55,Header[j],Keys[j],fc[j])
                elif type(da)==type(''):
                    if contains(' ,;\t',da):
                        da=qc+da.strip('"''')+qc
                D.append(context.STR(da))
        od.append(sep.join(D)+"\n")
    context.WriteFile(file,''.join(od),"a")
    EndInfo(context,MemName)
    return

def WriteDataFile(sid1,opts,results,file,fmt,sid):
    if (sid1==opts['-sid']) and (opts['-da']==0):
        CreateDataFile(opts,results,file,fmt)
    WriteResults2DataFile(opts,results,file,fmt,sid)
    return

def DoOneRun(opts,data,results,validation,i,info,ThdCtrl):
    RunSimulation(opts,data,results,validation,i)
    ThdCtrl[0].acquire()
    info[0]+=1
    info[2].append(0)
    ThdCtrl[0].release()
    return

def AllRunsDone(info,ThdCtrl):
    ThdCtrl[0].acquire()
    info[1]=True
    ThdCtrl[0].release()
    ThdCtrl[1].set()
    return

def BlockIsProcessed(i,info,ThdCtrl):
    ThdCtrl[0].acquire()
    info[2][i]=1
    ThdCtrl[0].release()
    ThdCtrl[1].set()
    return

def FirstRuns(n,MCruns,opts,data,results,validation,info,ThdCtrl):
    MemName=BeginInfo(opts['CONTEXT'],'FirstRuns')
    for i in range(0,n):
        DoOneRun(opts,data,results,validation,i,info,ThdCtrl)
    PrepareAllBinning(opts, results)
    Rbins=[]
    RbinCounts=[]
    RbinLimits=[]
    for j in range(0,len(results)):
        Rbins.append(results[j]['bins'])
        RbinCounts.append(results[j]['bincount'])
        bw=results[j]['binwidth']
        lbl=results[j]['lowbinlimit']
        hbl=results[j]['highbinlimit']
        RbinLimits.append(Numpy.linspace(lbl, hbl+bw, num=RbinCounts[j]+1,endpoint=False))
    for i in range(0,n):
        BinDataBlockResults(opts,results,i,Rbins,RbinCounts,RbinLimits)
        BlockIsProcessed(i,info,ThdCtrl)
    EndInfo(opts['CONTEXT'],MemName)
    return Rbins, RbinCounts, RbinLimits

def SortAll(opts,results):
    bsa=Numpy.cumsum(Numpy.array(results[0]['blocksize'])[:-1])
    for i in range(0,len(results)):
        S=Numpy.sort(Numpy.concatenate((results[i]['sortdatablocks'][:])))
        S=MakeMonotone(opts,S,results[i]['name'])
        results[i]['sortdatablocks']=Numpy.split(S,bsa)
    return

def TotalRunCnt(s,k,d,f=1.0):
    n=max(int(f*s*s*k*k/(d*d)+0.5),1)
    return n

def EvalRunCnt(opts,result,k):
    cb=opts['-at']
    mr=[0,0]
    tol=[0,0]
    s=[0,0]
    if opts['-sbs']>0:
        Rstddevs=Numpy.array(result['substddevs'])
        Ravgs=Numpy.array(result['subaverages'])
        Rweights=Numpy.array(result['subsizes'])
        f=opts['-sbs']*1.0/opts['-bs']
    else:
        Rstddevs=Numpy.array(result['stddevs'])
        Ravgs=Numpy.array(result['averages'])
        Rweights=Numpy.array(result['sortblocksizes'])
        f=1.0
    vy=Numpy.square(Rstddevs)
    WSM=WeightedStats(Ravgs,Rstddevs,Rweights)
    WSS=WeightedStats(vy,None,Rweights)
    s[0]=WSM.Stdev_eff
    s[1]=WSS.Stdev_eff
    if (s[0] is None) or (s[1] is None):
        raise Error(91)
    if (opts['-am']==2) or (opts['-am']==4):
        tol[0]=5/(math.pow(10,opts['-sd']+1)*opts['-ad'])*WSM.Stdev_tot
    else:
        tol[0]=5*math.pow(10,MAGNITUDE(WSM.Stdev_tot)-opts['-sd'])/opts['-ad']
    tol[1]=2*WSM.Stdev_tot*tol[0]
    if ((cb & 1)>0):
        mr[0]=TotalRunCnt(s[0],k,tol[0],f)
    else:
        mr[0]=1
    if ((cb & 2)>0):
        mr[1]=TotalRunCnt(s[1],k,tol[1],f)
    else:
        mr[1]=1
    R=max(mr)
    return R,mr,tol,s

def EvalKFactor(opts,n):
    if opts['-sbs']>0:
        nu=n*opts['-bs']/opts['-sbs']-1
    else:
        nu=n-1
    k=Tfactor(opts['-af'],nu)
    return k


def CheckStatParams(opts,MCruns,data,results,validation,info,ThdCtrl,Rbins,RbinCounts,RbinLimits):
    addruns=0
    while True:
        k=EvalKFactor(opts,MCruns)
        R=MCruns
        for i in range(0,len(results)):
            nr,mr,tol,s=EvalRunCnt(opts,results[i],k)
            R=max(R,nr)
        if (R>MCruns) and (MCruns<opts['-mr']):
#            for i in range(MCruns,MCruns+1):
            i=MCruns
            DoOneRun(opts,data,results,validation,i,info,ThdCtrl)
            BinDataBlockResults(opts,results,i,Rbins,RbinCounts,RbinLimits)
            BlockIsProcessed(i,info,ThdCtrl)
            MCruns+=1
            addruns+=1
        else:
            break
    return MCruns,addruns


def AdjustPreRuns(opts,data,results,validation,MCruns,Rbins,RbinCounts,RbinLimits,info,ThdCtrl):
    vds=MCruns*opts['-bs']
    for result in results:
        vds=min(vds,Numpy.sum(result['sortblocksizes']))
    if vds < MCruns*opts['-bs']:
        PreRuns=int(((1.0*(MCruns*opts['-bs'])**2)/vds+opts['-bs']-1)/opts['-bs'])
        deltaPr=PreRuns-MCruns
        for i in range(MCruns,PreRuns):
            DoOneRun(opts,data,results,validation,i,info,ThdCtrl)
            BinDataBlockResults(opts,results,i,Rbins,RbinCounts,RbinLimits)
            BlockIsProcessed(i,info,ThdCtrl)
    else:
        PreRuns=MCruns
        deltaPr=0
    return PreRuns,deltaPr

def UD(results):
    sy=0
    for i in range(0,len(results)):
        WS=WeightedStats(results[i]['averages'],results[i]['stddevs'],results[i]['sortblocksizes'])
        sy=max(sy,WS.Stdev_tot)
    return sy/math.pow(10,MAGNITUDE(sy)-1)

def DoSimulations(MCruns,opts,data,results,validation,info,ThdCtrl):
    MemName=BeginInfo(opts['CONTEXT'],'DoSimulations')
    '''
    Simulation task
    '''
    try:
        context=opts['CONTEXT']
        cb=opts['-at']
        PreRuns=opts['-pr']
        addruns=0
        if MCruns>0:
            context.PRINT('Mode: non adaptive',VL_Details)
            context.PRINT('Blocksize: %d' % opts['-bs'],VL_Details)
            if MCruns<PreRuns:
                PreRuns=MCruns
            Rbins, RbinCounts, RbinLimits = FirstRuns(PreRuns,MCruns,opts,data,results,validation,info,ThdCtrl)
            if MCruns>PreRuns:
                for i in range(PreRuns,MCruns):
                    DoOneRun(opts,data,results,validation,i,info,ThdCtrl)
                    BinDataBlockResults(opts,results,i,Rbins,RbinCounts,RbinLimits)
                    BlockIsProcessed(i,info,ThdCtrl)
            vds=MCruns*opts['-bs']
            for result in results:
                vds=min(vds,Numpy.sum(result['sortblocksizes']))
            if vds < MCruns*opts['-bs']:
                Runs0=MCruns
                MCruns=int(((1.0*(MCruns*opts['-bs'])**2)/vds+opts['-bs']-1)/opts['-bs'])
                adj=True
                if MCruns>Runs0:
                    for i in range(Runs0,MCruns):
                        DoOneRun(opts,data,results,validation,i,info,ThdCtrl)
                        BinDataBlockResults(opts,results,i,Rbins,RbinCounts,RbinLimits)
                        BlockIsProcessed(i,info,ThdCtrl)
            else:
                adj=False
            context.WRITE('\n',VL_Progress)
            if adj:
                context.PRINT("The number of simulation blocks have been adjusted to: %s" % (context.STR(MCruns)),VL_Warn)
            else:
                context.PRINT("Number of simulation blocks: %s" % (context.STR(MCruns)),VL_Details)
        else:
            context.PRINT('Mode: adaptive mode %s' % context.STR(opts['-am']),VL_Details)
            nbs=int(math.floor(100/(1-opts['-ap'])+0.5))
            if (opts['-sbs']>0) and (nbs % opts['-sbs']!=0):
                nbs=((nbs/opts['-sbs'])+1)*opts['-sbs']

            bs=max(opts['-bs'],nbs)
            if bs!=opts['-bs']:
                opts['-bs']=bs
                context.PRINT('Blocksize: %d' % opts['-bs'],VL_Info)
            else:
                context.PRINT('Blocksize: %d' % opts['-bs'],VL_Details)
            if opts['-am']==4:
                f=10**opts['-sd']*opts['-ad']
                Runs0=int(((f*stats.norm.ppf(1-(1-opts['-af'])/2))**2+(bs-1))/bs)
                Rbins, RbinCounts, RbinLimits = FirstRuns(Runs0,MCruns,opts,data,results,validation,info,ThdCtrl)
                MCruns=Runs0
                vds=MCruns*opts['-bs']
                for result in results:
                    vds=min(vds,Numpy.sum(result['sortblocksizes']))
                total=(2*f*stats.norm.ppf(1-(1-opts['-af'])/2))**2
                if vds < MCruns*opts['-bs']:
                    total=((1.0*total*MCruns*opts['-bs']**2)/vds+opts['-bs']-1)/opts['-bs']
                Runs1=(int(total+0.5)+bs-1)/bs
                if Runs1>opts['-mr']:
                    Runs1=opts['-mr']
                for i in range(MCruns,Runs1):
                    DoOneRun(opts,data,results,validation,i,info,ThdCtrl)
                    BinDataBlockResults(opts,results,i,Rbins,RbinCounts,RbinLimits)
                    BlockIsProcessed(i,info,ThdCtrl)
                MCruns=Runs1
                MCruns, addruns = CheckStatParams(opts,MCruns,data,results,validation,info,ThdCtrl,Rbins,RbinCounts,RbinLimits)
                context.WRITE("\n",VL_Progress)
            elif opts['-am']==3:
                f=10**opts['-sd']*opts['-ad']
                lim=10.0/f
                Runs0=int(((f*stats.norm.ppf(1-(1-opts['-af'])/2))**2+(bs-1))/bs)
                Rbins, RbinCounts, RbinLimits = FirstRuns(Runs0,MCruns,opts,data,results,validation,info,ThdCtrl)
                Runs0,deltaR0=AdjustPreRuns(opts,data,results,validation,Runs0,Rbins,RbinCounts,RbinLimits,info,ThdCtrl)
                MCruns=Runs0
                ud=UD(results)
                if (ud<(10+lim)) or (ud>=(50-lim)):
                    for i in range(MCruns,MCruns+Runs0):
                        DoOneRun(opts,data,results,validation,i,info,ThdCtrl)
                        BinDataBlockResults(opts,results,i,Rbins,RbinCounts,RbinLimits)
                        BlockIsProcessed(i,info,ThdCtrl)
                    MCruns +=Runs0
                    ud=UD(results)
                    if (ud<(10+lim)) or (ud>(70-lim)):
                        for i in range(MCruns,MCruns+Runs0):
                            DoOneRun(opts,data,results,validation,i,info,ThdCtrl)
                            BinDataBlockResults(opts,results,i,Rbins,RbinCounts,RbinLimits)
                            BlockIsProcessed(i,info,ThdCtrl)
                        MCruns +=Runs0
                        ud=UD(results)
                        if (ud<(10+lim)) or (ud>(85-lim)):
                            for i in range(MCruns,MCruns+Runs0):
                                DoOneRun(opts,data,results,validation,i,info,ThdCtrl)
                                BinDataBlockResults(opts,results,i,Rbins,RbinCounts,RbinLimits)
                                BlockIsProcessed(i,info,ThdCtrl)
                            MCruns +=Runs0
                MCruns,addruns=CheckStatParams(opts,MCruns,data,results,validation,info,ThdCtrl,Rbins,RbinCounts,RbinLimits)
                context.WRITE("\n",VL_Progress)
                context.PRINT('Number of prerun blocks: %s (+%s)' % (context.STR(Runs0),context.STR(deltaR0)),VL_Details)
            elif (opts['-am']==1) or (opts['-am']==2):
                Rbins, RbinCounts, RbinLimits = FirstRuns(PreRuns,MCruns,opts,data,results,validation,info,ThdCtrl)
                PreRuns,deltaPr=AdjustPreRuns(opts,data,results,validation,PreRuns,Rbins,RbinCounts,RbinLimits,info,ThdCtrl)
                MCruns=PreRuns
                k=EvalKFactor(opts,MCruns)
                for i in range(0,len(results)):
                    R,mr,tol,s=EvalRunCnt(opts,results[i],k)
                    MCruns=max(MCruns,R)
                    if ((cb & 1)>0):
                        results[i]['tol0']=tol[0]
                        results[i]['s0']=s[0]
                        results[i]['minruns0']=mr[0]
                    else:
                        results[i]['tol0']=0.0
                        results[i]['s0']=0.0
                        results[i]['minruns0']=1
                    if ((cb & 2)>0):
                        results[i]['tol1']=tol[1]
                        results[i]['s1']=s[1]
                        results[i]['minruns1']=mr[1]
                    else:
                        results[i]['tol1']=0.0
                        results[i]['s1']=0.0
                        results[i]['minruns1']=1
                if MCruns>opts['-mr']:
                    MCruns=opts['-mr']
                if (MCruns>PreRuns):
                    for i in range(PreRuns,MCruns):
                        DoOneRun(opts,data,results,validation,i,info,ThdCtrl)
                        BinDataBlockResults(opts,results,i,Rbins,RbinCounts,RbinLimits)
                        BlockIsProcessed(i,info,ThdCtrl)
                    MCruns,addruns=CheckStatParams(opts,MCruns,data,results,validation,info,ThdCtrl,Rbins,RbinCounts,RbinLimits)
                context.WRITE("\n",VL_Progress)
                context.PRINT('Number of prerun blocks: %s (+%s)' % (context.STR(PreRuns),context.STR(deltaPr)),VL_Details)
            else: # -am=0
                Rbins, RbinCounts, RbinLimits = FirstRuns(PreRuns,MCruns,opts,data,results,validation,info,ThdCtrl)
                PreRuns,deltaPr=AdjustPreRuns(opts,data,results,validation,PreRuns,Rbins,RbinCounts,RbinLimits,info,ThdCtrl)
                MCruns=PreRuns
                while MCruns<opts['-mr']:
                    DoOneRun(opts,data,results,validation,MCruns,info,ThdCtrl)
                    SetTolleranz(opts,data,results)
                    BinDataBlockResults(opts,results,MCruns,Rbins,RbinCounts,RbinLimits)
                    BlockIsProcessed(MCruns,info,ThdCtrl)
                    MCruns+=1
                    if CheckResults(opts,data,results,MCruns):
                        break
                context.WRITE("\n",VL_Progress)
                context.PRINT('Number of prerun blocks: %s (+%s)' % (context.STR(PreRuns),context.STR(deltaPr)),VL_Details)
            context.PRINT("Number of simulation blocks: %s (+%s)" % (context.STR(MCruns),context.STR(addruns)),VL_Info)
        if opts['-wb']==3:
            SortAll(opts,results)
        AllRunsDone(info,ThdCtrl)
        for j in range(0,len(results)):
            results[j]['bins']=Rbins[j]
        FinalizeAllBinning(opts,results)
        DoAnalyzeResults(opts,results,MCruns,addruns)
    except Error,er:
        ThdCtrl[0].acquire()
        info[3]=[er.number,er.params,TRACEINFO()]
        info[1]=True
        ThdCtrl[0].release()
        ThdCtrl[1].set()
    except (Exception,KeyboardInterrupt),e:
        ThdCtrl[0].acquire()
        if e is KeyboardInterrupt:
            info[3]=[-1,context.MSG(5),'']
        else:
            info[3]=[255,context.STR(e),TRACEINFO()]
        info[1]=True
        ThdCtrl[0].release()
        ThdCtrl[1].set()
    EndInfo(opts['CONTEXT'],MemName)
    return

def DefaultCSVFmt():
    Header=['Filename','Symbol','ID','Runs','Mean','StdUnc','Low95','High95','BinCount','LowBinLimit','BinWidth','Bin[%s]']
    Keys=['filename','name','id','runs','average','stddev','low95','high95','bincount','lowbinlimit','binwidth','BINS']
    sep=','
    hf=True
    ext='.ohd'
    qc='"'
    return Header, Keys, sep, hf, ext, qc

def DefaultFmt():
    Header=[]
    Keys=[]
    sep='\t'
    hf=False
    ext='.sta'
    qc=''
    return Header, Keys, sep, hf, ext, qc

def GetOFD(opts,key,ex,fmt,GetDefaults):
    fn=opts[key]
    fn=opts['CONTEXT'].SetDefExt(fn,ex)
    fn=opts['CONTEXT'].PathJoin(opts['PATH'],fn)
    if not opts['CONTEXT'].IsFile(fn):
        opts['CONTEXT'].ERROR(58,fn)
    Header, Keys, sep, hf, ext, qc=GetDefaults()
    if fn!='':
        Header, Keys, fc, sep, hf, ext, qc=ReadOFD(opts,fn,sep,hf,ext, qc)
    opts[fmt]=[Header, Keys, fc, sep, hf, ext, qc]
    return

def ListCorrMatrix(opts,MX):
    context=opts['CONTEXT']
    n=[]
    for s in MX['symbols']:
        n.append("%-17s" % s)
    context.PRINT("%17s" % 'r(x_i,x_j)'+" "+'  '.join(n))
    for i in xrange(len(MX['symbols'])):
        l=[]
        for j in xrange(len(MX['symbols'])):
            l.append("%0.15f" % MX['matrix'][i,j])
        context.PRINT("%17s" % MX['symbols'][i]+" "+'  '.join(l))
    return

def ListAllCorrMatrix(opts,data):
    for MX in data['corrmtx']:
        ListCorrMatrix(opts,MX)
    return

def ListOutCorrMatrix(opts,results):
    context=opts['CONTEXT']
    n=[]
    for r in results:
        n.append("%-17s" % r['name'])
    context.PRINT("%17s" % 'r(y_i,y_j)'+" "+'  '.join(n))
    for i in xrange(len(results)):
        l=[]
        for j in xrange(len(results)):
            l.append("%0.15f" % results[i]['corr'][j])
        context.PRINT("%17s" % results[i]['name']+" "+'  '.join(l))
    return

def ListInOutCorrMatrix(opts,results):
    context=opts['CONTEXT']
    n=[]
    for v in results[0]['ircorr'].keys():
        n.append("%-17s" % v)
    context.PRINT("%17s" % 'r(y_j,x_i)'+" "+'  '.join(n))
    for i in xrange(len(results)):
        l=[]
        for v in results[0]['ircorr'].keys():
            l.append("%0.15f" % results[i]['ircorr'][v])
        context.PRINT("%17s" % results[i]['name']+" "+'  '.join(l))
    return

def ListTolerances(opts,results,MCruns):
    context=opts['CONTEXT']
    if (MCruns==0):
        if (opts['-am']==1) or (opts['-am']==2):
            pass
            k=Tfactor(opts['-af'],opts['-pr']-1)
            n=[]
            m=[]
            sm=[]
            nm=[]
            v=[]
            sv=[]
            nv=[]
            u=[]
            su=[]
            nu=[]
            for r in results:
                n.append("%-17s" % r['name'])
                m.append(context.context.STR("%0.15f" % r['tol0']))
                v.append(context.STR("%0.15f" % r['tol1']))
                u.append(context.STR("%0.15f" % r['tol2']))
                sm.append(context.STR("%0.15f" % r['s0']))
                sv.append(context.STR("%0.15f" % r['s1']))
                su.append(context.STR("%0.15f" % r['s2']))
                nm.append(context.STR("%d" % r['minruns0']))
                nv.append(context.STR("%d" % r['minruns1']))
                nu.append(context.STR("%d" % r['minruns2']))
            context.PRINT("%17s" % 't-factor('+context.STR(opts['-af'])+") = "+context.STR(k),VL_Info)
            context.PRINT("%17s" % 'Result'+" "+'  '.join(n),VL_Info)
            context.PRINT("%17s" % 'Tol(mean)'+" "+'  '.join(m),VL_Info)
            context.PRINT("%17s" % 's(mean)'+" "+'  '.join(sm),VL_Info)
            context.PRINT("%17s" % 'n(mean)'+" "+'  '.join(nm),VL_Info)
            context.PRINT("%17s" % 'Tol(variance)'+" "+'  '.join(v),VL_Info)
            context.PRINT("%17s" % 's(variance)'+" "+'  '.join(sv),VL_Info)
            context.PRINT("%17s" % 'n(variance)'+" "+'  '.join(nv),VL_Info)
        elif opts['-am']==0:
            at=opts['-at']
            tl=[]
            tlh=[]
            tll=[]
            n=[]
            ss=[]
            sm=[]
            sv=[]
            hadapt=[]
            ladapt=[]
            k=GetKfactor(opts,len(results[0]['stddevs'])-1)
            sn=math.sqrt(len(results[0]['stddevs']))/k
            ap=context.STR(opts["-ap"]*100)
            for r in results:
                sm.append(context.STR("%0.15f" % (STDEV(r['averages'])/sn)))
                ss.append(context.STR("%0.15f" % (STDEV(r['stddevs'])/sn)))
                sv.append(context.STR("%0.15f" % (STDEV(Numpy.square(r['stddevs']))/sn)))
                hadapt.append(context.STR("%0.15f" % (STDEV(r['highadaptlimits'])/sn)))
                ladapt.append(context.STR("%0.15f" % (STDEV(r['lowadaptlimits'])/sn)))
                tl.append(context.STR("%0.15f" % r['tol']))
                tlh.append(context.STR("%0.15f" % r['tolah']))
                tll.append(context.STR("%0.15f" % r['tolal']))
                n.append("%-17s" % r['name'])
            context.PRINT("%17s" % 'k-factor ('+context.STR(opts['-af'])+") = "+context.STR(k),VL_Info)
            context.PRINT("%17s" % 'Result'+" "+'  '.join(n),VL_Info)
            if (at & 1)>0:
                context.PRINT("%17s" % 'Tol(mean)'+" "+'  '.join(tl),VL_Info)
                context.PRINT("%17s" % 'k*s(mean)'+" "+'  '.join(sm),VL_Info)
            if (at & 2)>0:
                context.PRINT("%17s" % 'Tol(stddev)'+" "+'  '.join(tl),VL_Info)
                context.PRINT("%17s" % 'k*s(stddev)'+" "+'  '.join(ss),VL_Info)
            if (at & 4)>0:
                context.PRINT("%17s" % ('Tol(high '+ap+'%)')+" "+'  '.join(tlh),VL_Info)
                context.PRINT("%17s" % ('k*s(high '+ap+'%)')+" "+'  '.join(hadapt),VL_Info)
                context.PRINT("%17s" % ('Tol(low '+ap+'%)')+" "+'  '.join(tlh),VL_Info)
                context.PRINT("%17s" % ('k*s(low '+ap+'%)')+" "+'  '.join(ladapt),VL_Info)
        else:
            pass
    return

def ReRaiseError(opts,info,where):
    opts['CONTEXT'].NOISE('Exception in %s' % where)
    if info[2]!='':
        opts['CONTEXT'].NOISE(info[2])
    if info[0]!=0:
        if type(info[1])==type(''):
            raise Error(info[0],info[1])
        else:
            raise Error(info[0],*info[1])
    return

def InitOptions(opts,specs,filename=''):
    #specs: [<type>,<min>,<max>,<default>,<comment>]
    #       type: 'i'|'f'|'s'  (integer, float, string)
    #       min: minimum value or number of char
    #       max: maximum value or number of char
    maxi=sys.maxint
    maxf=10E38
    specs['-a']=['i',0,1,1,          'analyze data and write statistic data file']
    specs['-ac']=['i',0,3,0,         'analyze correlation 1=results/results 2=inputs/results 3=all']
    specs['-ad']=['f',1,10,1.0,      'adaptive mode tolerance divisor']
    specs['-af']=['f',0.001,1,0.9545,'probability level of the decision in adaptive mode']
    specs['-am']=['i',0,4,0,         'adaptive mode (0=GUM S1, 1=Stein 2-stage scheme, 2=simple, 3=fixed accuracy)']
    specs['-ap']=['f',0,1.0,0.95,    'probability of the interval tested in adaptive mode (S1)']
    specs['-at']=['i',1,7,7,         'controls the adaptive test (bit 0: mean, bit 1:std.dev., bit 2: interval']
    specs['-bs']=['i',100,1000000,10000,'controls the block size for the processing']
    specs['-cfg']=['s',0,255,'OMCE.cfg','config file name']
    specs['-cg']=['i',0,1,1,         'unused, ignored']
    specs['-cl']=['f',0.0,1.0,0.001, 'lower correlation limit']
    specs['-cp']=['s',0,255,'cp850', 'code page character encoding for console output']
    specs['-da']=['i',0,1,0,         'append to an existing output file']
    specs['-de']=['i',0,1,1,         'deletes the .omc section in the output filename if -de=1']
    specs['-e1']=['f',-maxf,0,-0.1,  'limit for negative eigenvalues in the correlation matrix']
    specs['-e2']=['f',0,1,0.01,      'maximum value for the norm of the correlation matix correction']
    specs['-enc']=['s',0,255,'iso_8859_1', 'character encoding for unicode chars']
    specs['-fi']=['i',0,1,0,         'input file format (0=OMCS, 1=other)']
    specs['-fo']=['s',0,255,'',      'name of the output file if not empty']
    specs['-hp']=['f',0.001,1.0,0.99,'probability of the histogram interval']
    specs['-hc']=['i',1,100000,200,  'count of histogram bars']
    specs['-hf']=['f',0.1,100.0,1.2, 'factor to extend the histogram interval']
    specs['-i']=['i',0,1,0,          'coverage intervals (0=probabilistic symmetric, 1=shortest)']
    specs['-imp']=['s',0,255,'imports', 'sub directory for binary imports if Syspath="1"']
    specs['-info']=['i',0,5,0,       'prints details (1=model, 2=predefined symbols, 3=result values, 4= reserved words, 5=Error messages)']
    specs['-io']=['i',0,1,0,         'Sampling mode for imported quantities -io=0 random sampling -io=1 linear sampling']
    specs['-k']=['f',0,100,2.0,      'k-factor for the adaptive mode']
    specs['-l']=['i',1,maxi,0,       'number of repeated simulations']
    specs['-lc']=['i',0,3,0,         'lists the correlation matrix 1=input 2=output']
    specs['-lmn']=['i',0,1,1,        'matix norm type (-lmn=0: plain, -lmn=1: weighted)']
    specs['-lt']=['i',0,1,0,         'lists the tolerances used for the adaptive mode if -lt=1']
    specs['-mcp']=['i',0,4,0,        'matix correction procedure (-mcp=0: spectral comp., -mcp=1: Near4, -mcp=2: Walk)']
    specs['-mcs']=['i',0,maxi,-1,    'number of Monte Carlo simulation blocks, see -bs (0,-1=adaptive)']
    specs['-mr']=['i',1,maxi,10000,  'maximum number of runs * -bs in the adaptive mode']
    specs['-nc']=['f',0,1.0,0.5,     'limit on the tolerated fraction of not valid common data for correlation analysis']
    specs['-nl']=['f',0,1.0,0.5,     'limit on the tolerated fraction of not valid data']
    specs['-ofd']=['s',0,255,'OMCE', 'file name for the output format definition']
    specs['-p1']=['f',0.001,1.0,0.95,'probability of the the 95% interval']
    specs['-p2']=['f',0.001,1.0,0.99,'probability of the the 99% interval']
    specs['-p3']=['f',0.001,1.0,0.999,'probability of the the 99.9% interval']
    specs['-pa']=['f',1.0,99.0,2.0,  'Exponent for averaging the quantiles']
    specs['-pdf']=['i',0,1,1,        'sampling of the pdf instead of counts (histogram values)']

    specs['-po']=['i',0,1,0,         'print all options and exit if -po=1']
    specs['-pq']=['i',0,4,0,         'quantile estimation method (0..4)']
    specs['-pr']=['i',1,100,10,      'number of of initial runs used to establish the histogram bounds']
    specs['-sbs']=['i',100,10000,-1, 'controls the sub block size for the processing']
    specs['-sd']=['i',1,4,2,         'number of significant digits for adaptive mode']
    specs['-seed']=['i',0,maxi,0,    'sets the seed of the random generator if nonzero']
    specs['-sev']=['f',0,maxf,1E-7,  'smallest eigenvalue of the correlation matix after correction']
    specs['-sid']=['i',0,maxi,0,     'start value for the simulation id (inc. after every simulation']
    specs['-t']=['i',0,2,1,          'measure and print elapsed time if -t=1 or -t=2']
    specs['-v']=['i',0,10,2,         'verbose level 0..10: all..nothing']
    specs['-vfd']=['s',0,255,'OMCE', 'file name for the var-file format definition']
    specs['-vm']=['i',0,1,0,         'validation mode']
    specs['-wb']=['i',0,3,0,         'write binary data file(1=OMCE format, 2=simple format, 3=sorted OMCE format)']
    specs['-wv']=['i',0,1,0,         'write var file']
    specs['-xsd']=['s',0,255,'-',    'path to xsd-file for xml validation']
    for skey in specs.keys():
        opts[skey]=specs[skey][3]
    if not (filename == ''):
        SetOptionsOf(opts,specs,ReadOptionFile(opts['CONTEXT'],filename))
    return

def GetInfo(opts,specs):
    L=[]
    L.append("Error: missing omc-file name\n")
    L.append("Usage: OMCE <omc-filename> [Options] [Parameters]")
    L.append("Options:")
    M='\n'.join(L)+'\n'
    L=[]
    M+=GetOptionInfo(opts,specs)
    L.append("")
    L.append("Parameters:")
    L.append('         The Parameter names are defined in the section <Parameters>')
    L.append('         in the omc-file. The format is <param>=<value>.')
    L.append("")
    L.append("Exit Codes:")
    M+='\n'.join(L)+'\n'
    L=[]
    M+=GetErrors()
    M+="\n"
    M+=GetDisclaimer()
    M+="\nPress Enter..."
    return M

def Init(filename,path,data,options,opts,specs,params):
    context=data['context']
    SetOptionsOf(opts,specs,options)
    data['simcon']=SimContext(data['context'],0,[])
    data['reserved']=GetReservedWords(opts)
    data['predeffunc']=GetPredefinedFunc(opts,data['simcon'])
    data['predefsymbols']=GetPredefinedSymbols(opts)
    data['predef']=DictMerge(data['predeffunc'],data['predefsymbols'])
    opts['PATH']=path
    if (opts['-i']==1) and (opts['-pq']>0):
        context.PRINT('Warning: Option -pq need to be 0 to make option -i=1 effective!',VL_Warn)
    if opts['-info']==2:
        context.PRINT('Predefined Functions and Symbols',VL_Info)
        prefs=data['predef'].keys()
        prefs.sort()
        context.PRINT('\n'.join(prefs),VL_Info)
        context.PRINT('Operators : '+"['+', '-', '*', '/', '**', '(', ')', ',']",VL_Info)
        Exit()
    if opts['-info']==3:
        context.PRINT('Data File Symbols:',VL_Info)
        Results=InitResult('',0,0,'','','')
        prefs=Results.keys()
        for i in xrange(len(prefs)):
            if type(Results[prefs[i]])==type([]):
                prefs[i]=prefs[i]+'[]'
        prefs.append('BINS')
        prefs.append('CORR')
        prefs.append('SID')
        prefs.sort()
        context.PRINT('\n'.join(prefs),VL_Info)
        Exit()
    if opts['-info']==4:
        context.PRINT('Reserved words:',VL_Info)
        res=data['reserved']
        res.sort()
        context.PRINT('\n'.join(res),VL_Info)
        Exit()
    if opts['-info']==5:
        context.PRINT(GetErrorsTeX(),VL_Info)
        Exit()
    if len(filename) == 0:
        context.PRINT(GetInfo(opts,specs),VL_Info)
        context.READ(1)
        Exit()
    data['predefequs']=DictMerge({"__builtins__":None},(data['predef']))
    CreateConGrammar(data)
    opts['XMLpath']=context.DirPath(filename)
    context.PRINT("Reading XML ("+filename+")",VL_Info)
    ReadXML(opts,data,filename)
    context.PRINT("XML-file read.",VL_Noise)
    GetOFD(opts,'-ofd','.ofd','format-ohd',DefaultCSVFmt)
    GetOFD(opts,'-vfd','.vfd','format-var',DefaultFmt)
    context.PRINT("ofd/vfd-file read.",VL_Noise)
    if opts['-fi']==0:
        data['reader']=OMCReader(opts,data)
    elif opts['-fi']==1:
        data['reader']=Reader1(opts,data)
    else:
        context.FormatError(opts['-fi'])
    context.PRINT("reader created.",VL_Noise)
    data['reader'].InitParams(data,params)
    if len(data['clparams'])>0:
        context.PRINT('Command line parameter: '+', '.join(data['clparams']),VL_Info)
    context.PRINT("Init() complete.",VL_Noise)
    return

def MonteCarlo(sid,filename,path,data,results,options,SimOptStr,opts,specs):
    '''
    Runs a Monte Carlo simulation on a model in xml-format
      filename: model definition file
      path: path to the OMCE directory
      data: dictionary for the model data
      results: list for the result data
      options: list of options
      SimOptStr: additional options string
      opts: list of active options
      specs: list of specifications for all options
    '''
    context=data['context']
    MemName=BeginInfo(context,'MonteCarlo')
    data['SID']=sid
    if (opts['-fi']==0) and (hasattr(data['doc'].Model,'Options')):
        foptions=context.STR(context.UNICODE(data['doc'].Model.Options)).split()
        SetOptionsOf(opts,specs,foptions)
    if SimOptStr!="":
        foptions=SimOptStr.split()
        SetOptionsOf(opts,specs,foptions)
    SetOptionsOf(opts,specs,options)
    context.NOISE("Options setup complete.")
    if opts['-sbs']>0:
        if opts['-sbs']%10>0:
            context.ERROR(66,opts['-sbs'])
        if opts['-bs']%opts['-sbs']>0:
            context.ERROR(67,opts['-bs'],opts['-sbs'])
    validation={}
    validation['results']=[]
    validation['inputs']=[]
    tic1 = time.clock()
    if opts['-po']!=0:
        context.PRINT("Effective Options:",VL_Info)
        ol=opts.keys()
        ol.sort()
        for o in ol:
            context.PRINT(o+'='+context.STR(opts[o]),VL_Info)
        Exit()
    if ('seed' in opts):
        opts['seed']=int(opts['seed'])
        context.PRINT('Set Seed='+context.STR(opts['seed']),VL_Info)
        data['simcon'].reseed(opts['seed'])
    elif opts['-seed']!=0:
        data['simcon'].reseed(opts['-seed'])
    FD, UFL=data['reader'].GetFuncDefs(opts,data)
    CreateGrammar(data)
    data['simcon'].ListOfVars=data['reader'].GetVarList(opts,data)
    CL=data['reader'].GetCorrList(opts,data)
    EL=data['reader'].GetEquList(opts,data)
    CDL=data['reader'].GetConstraintList(opts,data)
    DL=[]
    for i,C in enumerate(CDL):
        C['inp']=False
        for V in data['simcon'].ListOfVars:
            if C['sym']==V['sym']:
                C['inp']=True
                break
        if not C['inp']:
            found=False
            for E in EL:
                if C['sym']==E['sym']:
                    found=True
                    break
            if not found:
                context.PRINT('Warning: Constraint for '+C['name']+': '+C['src']+' is ignored',VL_Warn)
                DL.append(i)
    d=0
    for i in DL:
        C=CDL.pop(i-d)
        d+=1
    for C in CDL:
        for S in C['cont']:
            found=False
            for V in data['simcon'].ListOfVars:
                if S==V['sym']:
                    found=True
                    break
            if (not C['inp']) and (not found):
                for E in EL:
                    if S==E['sym']:
                        found=True
                        break
            if not found:
                context.ERROR(59,C['name'],C['src'])
                DL.append(i)
    RL=data['reader'].GetResultList(opts,data)
    FL=data['reader'].GetFileNames(opts,data)
    FT=CompileFuncs(opts,data)
    PrepareImports(opts,data)
    CX=MakeCorrMatrixList(opts,data)
    if not CheckCorrMatrix(opts,data):
        context.ERROR(16)
    if IsCorrModi(opts,data):
        context.PRINT('Warning: Correlation matrix needs modification, use:',VL_Warn)
        for MX in data['corrmtx']:
            if MX['ismodi']:
                ListCorrMatrix(MX)
                context.PRINT("Norm: "+context.STR(MX['lmn']),VL_Warn)
                if MX['iter']>0:
                    context.PRINT("Interations: "+context.STR(MX['iter']),VL_Warn)
    elif opts['-lc']&1>0:
        ListAllCorrMatrix(opts,data)
    for MX in data['corrmtx']:
        if MX['ismodi'] and (MX['lmn']>opts['-e2']):
            context.ERROR(20,opts['-e2'])
    COV=MakeCovMatrix(opts,data)
    exo=FindExecOrder(opts,data)
    CheckResultContributer(opts,data)
    toc = time.clock()
    context.SHOWTIME(opts,toc-tic1)
    outname=filename
    if opts['-de']!=0:
        outname=context.SplitExt(outname)[0]
    if opts['-fo']!='':
        outname=opts['-fo']
    data['binname']=outname+".bin"
    data['varfile']=outname+opts['format-var'][5]
    data['ohdfile']=outname+opts['format-ohd'][5]
    if opts['-info']==1:
        if len(data['simcon'].ListOfVars)>0:
            context.PRINT('Input Quantities:',VL_Info)
            for v in data['simcon'].ListOfVars:
                context.WRITE("%2s" % context.STR(v['id']),VL_Info)
                context.PRINT(': '+v['name']+' ('+v['type']+') '+context.STR(v['exec']),VL_Info)
        if len(EL)>0:
            context.PRINT('Equations:',VL_Info)
            for E in EL:
                context.WRITE("%2s" % context.STR(E['id']),VL_Info)
                context.PRINT(': '+E['name']+' = '+E['equ']+';',VL_Info)
                context.PRINT('    dependency: '+context.STR(E['cont']),VL_Info)
            context.PRINT('Execution Order: '+context.STR(exo),VL_Info)
        if len(RL)>0:
            context.PRINT('Results:',VL_Info)
            for R in RL:
                context.WRITE("%2s" % context.STR(R['id']),VL_Info)
                context.PRINT(': '+R['name']+' = '+R['equ']+'; '+R['unit']+'; '+R['definition']+';',VL_Info)
        Exit()
    tic = time.clock()
    if opts['-mcs']>=0:
        MCruns=opts['-mcs']
    else:
        MCruns=data['reader'].GetMCRuns(data)
    rcount=len(data['results'])
    for i in range(0,rcount):
        R=InitResult(data['binname'],0,i,data['results'][i]['name'],data['results'][i]['unit'],data['results'][i]['definition'])
        for va in data['vars']:
            v=va['sym']
            R['ircorrs'][v]=[]
        results.append(R)
    for i in range(0,rcount):
        results[i]['corr']=Numpy.zeros(rcount)
        results[i]['corr'][i]=1.0
    if (opts['-wb']!=0):
        if opts['IsServer']:
            context.PRINT(context.MSG(101),VL_Warn)
            opts['-wb']=0
        else:
            context.PRINT("Writing BIN-File ("+data['binname']+")",VL_Info)
    InitValidation(data,results,validation)
    if data['SID']>=0:
        sSID="SID="+context.STR(data['SID'])
    else:
        sSID=''
    context.PRINT(' '.join(["Running Simulation",sSID,data['simname']]),VL_Info)
    info=[0 , False, [],[0,'',''],[0,'','']]
    # info structure
    # [<block-rdy-cnt>,<sim-terminated>,[<block-status>,[<DoSim-Err>],[DoBinWrt-Err>]]
    DATA_READY=THG.Event()
    DATA_READY.clear()
    DATA_LOCK=TH.allocate_lock()
    ThdCtrl=(DATA_LOCK,DATA_READY)
    SimThd=THG.Thread(target=DoSimulations,args=(MCruns,opts,data,results,validation,info,ThdCtrl))
    BinThd=THG.Thread(target=DoBinaryWrite,args=(opts,results,data['binname'],info,ThdCtrl))
    try:
        BinThd.start()
        SimThd.start()
        SimThd.join()
        BinThd.join()
    except KeyboardInterrupt,e:
        raise Error(-1,context.MSG(5))
    ReRaiseError(opts,info[3],'Simulation')
    ReRaiseError(opts,info[4],'Binary write')
    if opts['-vm']!=0:
        AnalyzeValidation(opts,results,validation)
    toc = time.clock()
    context.SHOWTIME(opts,toc-tic)
    if (opts['-lt']!=0):
        ListTolerances(opts, results, MCruns)
    if (opts['-ac']&1>0) and (opts['-lc']&2>0):
        ListOutCorrMatrix(opts,results)
    if (opts['-ac']&2>0) and (opts['-lc']&3==3):
        ListInOutCorrMatrix(opts,results)
    toc = time.clock()
    context.SHOWTIME(opts,toc-tic1,1,'Total time: ')
    tic = time.clock()
    if (len(results)>0) and (opts['-wv']!=0):
        context.PRINT("Writing data to VAR-file ("+data['varfile']+")",VL_Info)
        WriteDataFile(sid,opts,results,data['varfile'],'format-var',data['SID'])
    toc = time.clock()
    context.SHOWTIME(opts,toc-tic)
    if (len(results)>0) and (opts['-a']!=0):
        context.PRINT("Writing data to OHD-file ("+data['ohdfile']+")",VL_Info)
        tic = time.clock()
        WriteDataFile(sid,opts,results,data['ohdfile'],'format-ohd',data['SID'])
        toc = time.clock()
        context.SHOWTIME(opts,toc-tic)
    EndInfo(context,MemName)
    return

def Simulator(argv,context,path=get_main_dir(),modname=os.path.splitext(sys.argv[0])[0],IsServer=False):
#    path=get_main_dir()
    data={}
    data['context']=context
    cfg_filename=''
    CP=''
    for prm in argv[1:]:
        if prm[0:3]=="-v=":
            o=prm.split('=')
            if len(o)==2:
                context.VerboseLevel=int(o[1])
        elif prm[0:5]=="-cfg=":
            o=prm.split('=')
            if len(o)==2:
                cfg_filename=context.PathJoin(path,context.STR(o[1]))
        elif prm[0:4]=="-cp=":
            o=prm.split('=')
            if len(o)==2:
                CP=context.STR(o[1])
    if cfg_filename=='':
        cfg_filename=modname+'.cfg'
    if CP=='':
        cfg=ReadOptionFile(context,cfg_filename)
        for Opt in cfg:
            o=Opt.split('=')
            if (len(o)==2) and (o[0]=="-cp"):
                CP=context.STR(o[1])
    if CP!='':
        context.CodePage=CP
    context.PRINT(__MODID__,VL_Startup)
    context.PRINT(__AUTHOR__,VL_Startup)
    context.PRINT('Config file: '+cfg_filename,VL_Noise)
    options=[]
    params=[]
    filename=""
    for prm in argv[1:]:
        if prm[0:1]=="-":
            options.append(prm)
        else:
            if filename=="":
                filename=prm
            else:
                if "=" in prm:
                    params.append(prm)
                else:
                    context.ERROR(60,prm)
    opts={}
    opts['CONTEXT']=context
    opts['IsServer']=IsServer
    specs={}
    InitOptions(opts,specs,cfg_filename)
    Init(filename,path,data,options,opts,specs,params)
    context.EncodingOption=opts['-enc']
    if (opts['-fi']==0) and (hasattr(data['doc'].Model,'Simulations')):
        i=opts['-sid']
        SC=data['reader'].XPATH(data['doc'].Model.Simulations,u'*')
        for S in SC:
            SimOptStr=""
            if S[0].nodeName=='Simulation':
                R=S
                MS=InitMathSymbols()
                data['reader'].InitParams(data,params)
                if hasattr(R,'Name'):
                    data['simname']=context.STR(context.UNICODE(R.Name))
                else:
                    data['simname']=''
                if hasattr(R,'Options'):
                    SimOptStr=context.STR(context.UNICODE(R.Options))
                PS=[]
                if hasattr(R,'Parameter'):
                    for P in R.Parameter:
                        Ns=context.STR(context.UNICODE(P.Name))
                        Nm=data['reader'].ConvSymName(Ns)
                        if not(Nm in data['params'].keys()):
                            context.ERROR(61,Ns)
                        if Nm in MS.keys():
                            context.ERROR(44,Ns)
                        data['params'][Nm],Va=GetParam(data,P.Value,MS,Ns,[])
                        PS.append(Ns+'='+context.STR(data['params'][Nm]))
                if len(PS)>0:
                    context.PRINT('Set parameter: '+', '.join(PS),VL_Info)
                results=[]
                InitOptions(opts,specs,cfg_filename)
                if hasattr(R,'Seed'):
                    opts['seed'],Va=GetParam(data,R.Seed,MS,'Seed',[])
                MonteCarlo(i,filename,path,data,results,options,SimOptStr,opts,specs)
                i+=1
            if S[0].nodeName=='Loop':
                MS=InitMathSymbols()
                Fr=float(eval(context.STR(context.UNICODE(S.From)).strip(),MS,{}))
                To=float(eval(context.STR(context.UNICODE(S.To)).strip(),MS,{}))
                if hasattr(S,'Step'):
                    Ic=math.fabs(float(eval(context.STR(context.UNICODE(S.Inc)).strip(),MS,{})))
                    if Ic==0:
                        context.ERROR(62)
                else:
                    Ic=1
                if hasattr(S,'Enum'):
                    ENa=context.STR(context.UNICODE(S.Enum))
                    Na=data['reader'].ConvSymName(ENa)
                else:
                    Na=None
                if hasattr(S,'Name'):
                    NT=context.STR(context.UNICODE(S.Name))
                else:
                    NT='loop'
                if (Fr>To):
                    Ic=-Ic
                if hasattr(S,'Options'):
                    SimOptStr=context.STR(context.UNICODE(R.Options))
                while (Fr==To) or ((Fr<To) and (Ic>0))or ((Fr>To) and (Ic<0)):
                    MS=InitMathSymbols()
                    if Na<>None:
                        MS[Na]=Fr
                        Frs=ENa+'='+context.STR(Fr)
                    else:
                        Frs=context.STR(Fr)
                    data['reader'].InitParams(data,params)
                    data['simname']=' '.join([NT,Frs])
                    PS=[]
                    if hasattr(S,'Parameter'):
                        for P in S.Parameter:
                            Ns=context.STR(context.UNICODE(P.Name))
                            Nm=data['reader'].ConvSymName(Ns)
                            if not(Nm in data['params'].keys()):
                                context.ERROR(63,Ns)
                            if Nm in MS.keys():
                                context.ERROR(44,Ns)
                            data['params'][Nm],Nx=GetParam(data,P.Value,MS,Ns,[Na])
                            PS.append(Ns+'='+context.STR(data['params'][Nm]))
                        if len(PS)>0:
                            context.PRINT('Set parameter: '+', '.join(PS),VL_Info)
                    results=[]
                    InitOptions(opts,specs,cfg_filename)
                    if hasattr(S,'Seed'):
                        opts['seed'],Va=GetParam(data,S.Seed,MS,'Seed',[Na])
                    MonteCarlo(i,filename,path,data,results,options,SimOptStr,opts,specs)
                    i+=1
                    Fr+=Ic
    else:
        SimOptStr=""
        if opts['-l']>0:
            for i in xrange(opts['-l']):
                results=[]
                data['simname']=''
                MonteCarlo(i+opts['-sid'],filename,path,data,results,options,SimOptStr,opts,specs)
        else:
            results=[]
            data['simname']=''
            MonteCarlo(opts['-sid'],filename,path,data,results,options,SimOptStr,opts,specs)
    context.PRINT('Done.',VL_Finish)
    return data,results

if __name__=="__main__":
    ExitCode=run_main(Simulator,sys.argv,DefConText)
    sys.exit(ExitCode)

