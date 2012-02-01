#!/usr/bin/env python
# -*- coding: latin-1 -*-
#-----------------------------------------------------
#
# OMCE Result Analyser
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
# 1.0.0 2011-02-23 RKe: module creation
# 1.0.2 2011-03-04 RKe: parameter support
#-----------------------------------------------------
__version__="1.0.2"
__MODID__="OMCE Result Analyser (OMCEanalyser V:"+__version__+")"
__AUTHOR__="Author: Ruediger Kessel (ruediger.kessel@nist.gov)"
#-----------------------------------------------------
import warnings
warnings.simplefilter("ignore",DeprecationWarning)
import numpy as np
import matplotlib
#matplotlib.rc('text', usetex = True)
matplotlib.rc('mathtext', fontset='stix')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.backends.backend_pdf as pdf
import sys
import os
from OMCEbase import ResultDataClass, SetOptionsOf, ReadOptionFile, get_main_dir, \
        MSG, STR, PRINT, ERROR, WRITE, FATALERROR, DefConText, GetOptionInfo, GetErrors, \
        GetDisclaimer, CheckFile, isFloat, isInt, VL_Error, VL_Warn, VL_Startup, \
        VL_Finish, VL_Progress, VL_Time, VL_Info, VL_Default, VL_Details, VL_Noise, \
        FilterSymbol, run_main, InitStdMainSingle, ReadCmdFile, Exit, MAGNITUDE, \
        InitMathSymbols, amara_version, amara, bindery, GetReservedWords, Grammar, \
        GetPredefinedSymbols, Error, TypeByName, MakeFilename, Abort, Terminate, Str2ParamList
import re
from collections import deque
import math
import code
import thread as TH
import threading as THG
import datetime

def InitOptions():
    opts={}
    opts['CONTEXT']=DefConText
    specs={}
    #specs: [<type>,<min>,<max>,<default>,<comment>]
    #       type: 'i'|'f'|'s'  (integer, float, string)
    #       min: minimum value or number of char
    #       max: maximum value or number of char
    maxi=sys.maxint
    maxf=10E38
    specs['-v']=['i',0,10,2,       'verbose level 0..10: all..nothing']
    specs['-fo']=['s',0,255,'',    'name of the output file for plots']
    specs['-pdf']=['i',0,1,0,      'save plots as pdf, if set']
    specs['-mm']=['i',0,1,1,       'use fancy symbols']
    specs['-it']=['i',0,1,1,       'use italic for symbols']
    specs['-rm']=['i',0,1,1,       'use serif font']
    specs['-sht']=['i',0,1,1,      'show x-label']
    specs['-shx']=['i',0,1,1,      'show y-label']
    specs['-shy']=['i',0,1,1,      'show title']
    specs['-ttl']=['s',0,255,'',   'diagram title']
    specs['-xl']=['s',0,255,'',    'x-label']
    specs['-yl']=['s',0,255,'',    'y-label']
    specs['-h']=['f',0.0,maxf,150.0,    'diagram height in mm']
    specs['-w']=['f',0.0,maxf,200.0,    'diagram width in mm']
    specs['-cfg']=['s',0,255,'OMCEanalyser.cfg','name of the configuration file']
    specs['-xls']=['fs',1,100,16.0,    'x-label font size']
    specs['-yls']=['fs',1,100,16.0,    'y-label font size']
    specs['-tls']=['fs',1,100,16.0,    'title font size']
    specs['-xts']=['fs',1,100,12.0,    'x-axis ticks font size']
    specs['-yts']=['fs',1,100,12.0,    'y-axis ticks font size']
    specs['-run']=['s',0,255,'',    'run commands from file']
    specs['-rundir']=['s',0,255,'cmds',    'default directory for command files']
    specs['-iam']=['i',0,1,1,  'enter interactive mode after running a script']
    specs['-info']=['i',0,1,0,       'prints program info (1=usage)']
    specs['-log']=['s',0,255,'analyser_%date%.log',    'log commands to file']
    specs['-logdir']=['s',0,255,'logs',    'default directory for log files']
    specs['-xsd']=['s',0,255,'-',    'path to xsd-file for xml validation']
    for skey in specs.keys():
        opts[skey]=specs[skey][3]
    return opts,specs

def Info(opts,specs):
    PRINT("Usage: OMCEanalyser [<ohd-filename-1> [<ohd-filename-2> ...]] [Options] [parameters]")
    PRINT("Options:")
    PRINT(GetOptionInfo(opts,specs))
    PRINT("")
    PRINT("Exit Codes:")
    PRINT(GetErrors())
    PRINT("")
    PRINT(GetDisclaimer())
    Exit()
    return

from lxml import etree
import lxml._elementpath as DONTUSE #workaround for a py2exe bug
import StringIO

class XmlReader(object):
    def __init__(self,opts):
        self.opts=opts
        self.context=opts['CONTEXT']
        self.cmdctx=opts['CMDCTX']
        self.ParamList=[]
        return
    def Set_xml(self,xmlstr):
        self.xml=xmlstr
        xf=None
        if (self.opts['-xsd']=='-'):
            xsdfile=[get_main_dir(),'OMCEanalyser.xsd']
            CheckFile(self.context,xsdfile)
            self.context.NOISE('Reading xsdfile begin...')
            xf=file(os.path.join(*xsdfile),'r')
            self.context.NOISE('Reading xsdfile end...')
        else:
            xsdfile=self.context.PathJoin(get_main_dir(),self.opts['-xsd'])
            if xsdfile!='':
                xsd=self.context.ReadFile(xsdfile)
                xf=StringIO.StringIO(xsd)
        if not (xf is None):
            if type(xsdfile)==type([]):
                xsd_name=MakeFilename(xsdfile)
            else:
                xsd_name=xsdfile
            self.context.PRINT("Validating against XML Schema (%s)" % xsd_name,VL_Info)
            xmlschemadoc=etree.parse(xf)
            xf.close()
            xmlschema=etree.XMLSchema(xmlschemadoc)
            xmldoc=etree.XML(self.xml)
            xmlschema.assertValid(xmldoc)
        doc=None
        if amara_version==1:
            doc = amara.parse(xmlstr)
        elif amara_version==2:
            doc = bindery.parse(xmlstr,standalone=True,validate=False)
        else:
            self.context.ERROR(82)
        self.doc=doc
        return
    def ConvSymName(self,name):
        name=name.replace('@','__')
        return name
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
    def ValidateName(self,Nn,T):
        from pyparsing import Word,alphas,nums,ParseException
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
    def GetParam(self,V,MS,N,_type):
        Va=self.STR(self.UNICODE(V))
        V=self.ConvSymName(Va)
        try:
            Vn=eval(V,MS,self.cmdctx)
        except NameError:
            if _type==str:
                Vn=V
            else:
                raise Error(50,V)
        V=Vn
        if (_type==int):
            if type(V)==int:
                V=int(V)
            else:
                raise Error(92,N,Va)
        elif (_type==float):
            if isFloat(V):
                V=float(V)
            else:
                raise Error(93,N,Va)
        else:
            V=str(V)
        return V,Va
    def Set_params(self,params):
        PL={}
        MS=InitMathSymbols()
        PS=[]
        if hasattr(self.doc.Script,'Parameters'):
            if hasattr(self.doc.Script.Parameters,'Parameter'):
                for p in self.doc.Script.Parameters.Parameter:
                    if hasattr(p,'Type'):
                        ty=self.STR(self.UNICODE(p.Type))
                    else:
                        ty='s'
                    Na=self.STRIPED(p.Name)
                    Nm=self.ConvSymName(Na)
                    Nm=self.ValidateName(Nm,'parameter')
                    if Nm in MS.keys():
                        self.ERROR(43,Na)
                    if Nm in GetReservedWords(self.opts):
                        self.ERROR(44,Na)
                    PL[Nm],Va=self.GetParam(p.Value,MS,Na,TypeByName(ty)())
        if type(params)==type(''):
            params=Str2ParamList(params)()
        if len(params)>0:
            for p in params:
                Nm,V=p.split('=')
                Ns=Nm.strip()
                Nm=self.ConvSymName(Ns)
                if Nm in PL.keys():
                    PL[Nm],Va=self.GetParam(V,MS,Ns,type(PL[Nm]))
                    PS.append(Ns+'='+self.STR(V))
                else:
                    self.ERROR(34,Ns)
        self.ParamList=PL
        self.PS=PS
        return

def TexSymbol(opts,s):
    if opts['-mm']!=0:
        ss=s.replace('^','_')
        T=ss.split('_')
        K=[]
        p=0
        sub=False
        sup=False
        K.append(0)
        for i in xrange(len(T)-1):
            p=p+len(T[i])
            if ((not sub) or sup) and (s[p+i]=='_'):
                K.append(-1)
                sub=True
                sup=False
            elif ((not sup) or sub) and (s[p+i]=='^'):
                K.append(1)
                sup=True
                sub=False
            else:
                K.append(0)
                sub=False
                sup=False
        s=''
        for i,t in enumerate(T):
            if len(t)>0:
                if K[i]==0:
                    s+=t
                elif K[i]>0:
                    s+=r'^{'+t+r'}'
                else:
                    s+=r'_{'+t+r'}'
    return s

def MakeTeXSym(opts,ttl):
    if opts['-mm']!=0:
        if opts['-it']!=0:
            ttl=r'$'+ttl+r'$'
        else:
            ttl=r'$\mathregular{'+ttl+r'}$'
        PRINT('MakeTeXSym: '+ttl,VL_Noise)
    return ttl

def MakeTeX(opts,ttl):
    if opts['-mm']!=0:
        ttl=r'$\mathregular{'+ttl+r'}$'
        PRINT('MakeTeX: '+ttl,VL_Noise)
    return ttl


def VarConv(opts,D,ttl):
    try:
        if not (D is None):
            if ttl.find('%def%')>=0:
                ttl=ttl.replace(r'%def%',MakeTeX(opts,TexSymbol(opts,D['Def'])))
            if ttl.find('%fp%')>=0:
                ttl=ttl.replace(r'%fp%',os.path.splitext(D['File'])[0])
            if ttl.find('%fn%')>=0:
                ttl=ttl.replace(r'%fn%',os.path.splitext(os.path.basename(D['File']))[0])
            if ttl.find('%sym%')>=0:
                ttl=ttl.replace(r'%sym%',MakeTeXSym(opts,TexSymbol(opts,D['Sym'])))
            if ttl.find('%unit%')>=0:
                ttl=ttl.replace(r'%unit%',MakeTeX(opts,TexSymbol(opts,D['Unit'])))
            if ttl.find('%unit-1%')>=0:
                if D['Unit']!='':
                    ttl=ttl.replace(r'%unit-1%',MakeTeX(opts,'('+TexSymbol(opts,D['Unit'])+')^{-1}'))
                else:
                    ttl=ttl.replace(r'%unit-1%','')
            if ttl.find('%phi%')>=0:
                ttl=ttl.replace(r'%phi%',MakeTeXSym(opts,r'\phi('+TexSymbol(opts,D['Sym'])+r')'))
    except: pass
    if ttl.find('%date%')>=0:
        ttl=ttl.replace(r'%date%',str(datetime.date.today()))
    return ttl

def getBinData(bincount,lowbin,binwidth,abins):
    bins=np.zeros(bincount+1)
    for i in xrange(bincount+1):
        bins[i]=lowbin+(i*binwidth)
    return abins,bins

class MyPath(path.Path):
    @classmethod
    def make_compound_path_from_polys(cls, XY):
        """
        (static method) Make a compound path object to draw a number
        of polygons with equal numbers of sides XY is a (numpolys x
        numsides x 2) numpy array of vertices.  Return object is a
        :class:`Path`

        .. plot:: mpl_examples/api/histogram_path_demo.py

        """

        # for each poly: 1 for the MOVETO, (numsides-1) for the LINETO, 1 for the
        # CLOSEPOLY; the vert for the closepoly is ignored but we still need
        # it to keep the codes aligned with the vertices
        numpolys, numsides, two = XY.shape
        assert(two==2)
        stride = numsides + 1
        nverts = numpolys * stride
        verts = np.zeros((nverts, 2))
        codes = np.ones(nverts, int) * cls.LINETO
        codes[0::stride] = cls.MOVETO
        codes[numsides::stride] = cls.CLOSEPOLY
        for i in range(numsides):
            verts[i::stride] = XY[:,i]

        return cls(verts, codes)

def MakeUniqueFile(fn):
    i=0
    fnN=fn
    while os.path.exists(fnN):
        fnL=os.path.splitext(fn)
        fnN=fnL[0]+'(%d)' % i+fnL[1]
        i+=1
    return fnN

def WriteLog(opts,s,mode='a'):
    if opts['-log']!='':
        DefConText.WriteFile(opts['-log'],s,mode)
    return

import traceback
class AnalyserInteractiveConsole(code.InteractiveConsole):
    def __init__(self,locals,opts):
        code.InteractiveConsole.__init__(self,locals)
        self.opts=opts
        self._buffer=[]
        self.iserror=False
    def push(self,line):
        if line in self.locals.keys():
            if type(self.locals[line])==type(self.__init__):
                line=line+'()'
        self.iserror=False
        self._buffer.append(line)
        ret=code.InteractiveConsole.push(self,line)
        if not ret:
            line='\n'.join(self._buffer)
            self._buffer=[]
#            if not self.iserror and not line.startswith('Quit()') and not line.startswith('Run('):
            if not self.iserror and not line.startswith('Quit()'):
                WriteLog(self.opts,line+'\n')
        return ret
    def showsyntaxerror(self, *args):
        code.InteractiveConsole.showsyntaxerror(self, *args)
        self.iserror=True
    def showtraceback(self, *args):
        """Display the exception that just occurred.

        We remove the first stack item because it is our own code.

        The output is written by self.write(), below.

        """
        try:
            type, value, tb = sys.exc_info()
            sys.last_type = type
            sys.last_value = value
            sys.last_traceback = tb
            tblist = traceback.extract_tb(tb)
            del tblist[:1]
            fn, lineno, name, line = tblist[0]
            list=['  File "%s", line %d\n' % (self.filename,lineno)]
            if list:
                list.insert(0, "Traceback (most recent call last):\n")
            list[len(list):] = traceback.format_exception_only(type, value)
        finally:
            tblist = tb = None
        map(self.write, list)
        self.iserror=True
        return
    def runcode(self, xcode):
        """Execute a code object.

        When an exception occurs, self.showtraceback() is called to
        display a traceback.  All exceptions are caught except
        SystemExit, which is re-raised.

        A note about KeyboardInterrupt: this exception may occur
        elsewhere in this code, and may not always be caught.  The
        caller should be prepared to deal with it.

        """
        try:
            exec xcode in self.locals
        except SystemExit:
            raise
        except (Abort, Terminate):
            raise
        except:
            self.showtraceback()
        else:
            if code.softspace(sys.stdout, 0):
                print

import scipy.stats as stats
class CmdInterpreter(object):
    def __init__(self,opts,specs):
        def Cmd_Options(self):
            PRINT(Cmd_Options.__doc__)
        Cmd_Options.__doc__="Options:\n"+GetOptionInfo(opts,specs,2)
        Cmd_Options.__name__="Cmd_Options"
        setattr(CmdInterpreter,Cmd_Options.__name__,Cmd_Options)
        self.opts=opts
        self.specs=specs
        self.cmdctx={}
        opts['CMDCTX']=self.cmdctx
        self.XR=XmlReader(opts)
        self.Prp_PlotParams={'Title':opts['-ttl'],'Bars':100,'Pdf':False,'Color':'gray',
                             'Xlabel':opts['-xl'],'Ylabel':opts['-yl'],'Alpha':1.0,
                             'File':'','Def':'', 'Sym':'','Unit':'', 'Lcolor':'b',
                             'Lwidth':1.0, 'Lstyle':'solid'}
        self.Prp_DataFiles=opts['RD']
        self.Prp_stats=stats
        self.Prp_plt=plt
        self.Prp_np=np
        self.Prp_math=math
        self.Prp_Params={}
        self.Cls_ResultDataClass=ResultDataClass
        D=dir(self)
        for pn in D:
            if pn.startswith('Cmd_') or pn.startswith('Prp_') or pn.startswith('Fct_') or pn.startswith('Cls_'):
                self.cmdctx[pn[4:]]=getattr(self, pn)
        self.cmdctx['sqrt']=np.sqrt
        self.cmdctx['sqr']=np.square
        self.cmdctx['pow']=np.power
        self.cmdctx['abs']=np.abs
        self.cmdctx['exp']=np.exp
        self.cmdctx['log']=np.log
        self.cmdctx['log10']=np.log10
        self.cmdctx['sin']=np.sin
        self.cmdctx['cos']=np.cos
        self.cmdctx['tan']=np.tan
        self.cmdctx['asin']=np.arcsin
        self.cmdctx['acos']=np.arccos
        self.cmdctx['atan']=np.arctan
        self.cmdctx['sinh']=np.sinh
        self.cmdctx['cosh']=np.cosh
        self.cmdctx['tanh']=np.tanh
        #self.Cmd_Options.__doc__="Options:\n"+GetOptionInfo(opts,specs)
        self.IC=AnalyserInteractiveConsole(self.cmdctx,opts)
        self._isshown=False
        self.Cmd_OpenPlot()
        return
    def SetParams(self,prms):
        for p in prms.keys():
            self.Prp_Params[p]=prms[p]
    def WriteLog(self,cmd):
        WriteLog(self.opts,cmd)
    def RunSource(self,srclist,fn):
        self.IC.filename=fn
        try:
            code=compile('\n'.join(srclist), '','exec') 
            self.IC.runcode(code)
        except Abort:
            pass
        except Terminate:
            if self.opts['-iam']==0:
                self.opts['-pdf']=0
                raise
        except Exception,e:
            PRINT('Error in %s: ' % fn+STR(e))
        return
    def RunInteractive(self):
        self.IC.filename='<input>'
        plt.ion()
        self.Cmd_Show()
        sys.ps1='$> '
        sys.ps2='.. '
        while True:
            try:
                sys.exc_clear()
                self.IC.interact('')
                break
            except Terminate:
                pass
    def Cmd_Print(self,s):
        '''
Print(s)
    Prints the string s+'\\n'. 
'''
        PRINT(STR(s),VL_Default)
    def Cmd_Write(self,s):
        '''
Write(s)
    Prints the string s (without extra newline). 
'''
        WRITE(STR(s),VL_Default)
    def Cmd_OpenPlot(self,n=None):
        '''
OpenPlot(n=None)
    Opens an existing or new plot as the active plot. 
'''
        if (n<=0) or (n is None):
            n=None
            newplt=True
        else:
            newplt=not plt.fignum_exists(n)
        figure = plt.figure(n,figsize=(self.opts['-w']/25.4,self.opts['-h']/25.4))
        if newplt:
            figure.add_subplot(1,1,1)
            self.Prp_PlotParams['Xlabel']=self.opts['-xl']
            self.Prp_PlotParams['Ylabel']=self.opts['-yl']
            self.Prp_PlotParams['Title']=self.opts['-ttl']
        else:
            ax=plt.gca()
            self.Prp_PlotParams['Xlabel']=ax.get_xlabel()
            self.Prp_PlotParams['Ylabel']=ax.get_ylabel()
            self.Prp_PlotParams['Title']=ax.get_title()
        self.Cmd_UpdatePlot()
    def Cmd_Show(self):
        if not self._isshown:
            plt.show()
            self._isshown=True
        plt.draw_if_interactive()
        return
    def Fct_Histogram(self,data,normed=True,range=None):
        '''
bin_limits,bin_heights = Histogram(data,normed=True,range=None)
    Plots the given data as a histogram. By default (normed=True)
    the heights will be normed (pdf-sample) and the full range of
    the data will be used.
    The function returns the bin limits and the bin heights as 
    arrays of length len(data)+1.  
'''
        # the histogram of the data
        nob=self.Prp_PlotParams['Bars']
        color=self.Prp_PlotParams['Color']
        alpha=self.Prp_PlotParams['Alpha']
        n, bins, patches = plt.gca().hist(data, nob,range=range, normed=normed, facecolor=color, edgecolor=color, alpha=alpha)
        n1=np.hstack((n,np.zeros(1)))
        plt.draw_if_interactive()
        return bins,n1
    def Cmd_UpdatePlot(self):
        '''
UpdatePlot()
    Updates the active plot after changes in the plotting parameters. 
'''
        plt.title(VarConv(self.opts,self.Prp_PlotParams,self.Prp_PlotParams['Title']),fontsize=self.opts['-tls'],x=0.5,y=1.01)
        ax=plt.gca()
        ax.set_xlabel(VarConv(self.opts,self.Prp_PlotParams,VarConv(self.opts,self.Prp_PlotParams,self.Prp_PlotParams['Xlabel'])),size=self.opts['-xls'])
        ax.set_ylabel(VarConv(self.opts,self.Prp_PlotParams,VarConv(self.opts,self.Prp_PlotParams,self.Prp_PlotParams['Ylabel'])),size=self.opts['-yls'])
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(self.opts['-xts'])
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(self.opts['-yts'])
        plt.grid(False)
        plt.draw_if_interactive()
        return
    def Cmd_Set(self,param=None,value=None):
        '''
Set(param=None,value=None)
    Sets the value of a plotting parameter. 
'''
        def PrintParam(p):
            v=self.Prp_PlotParams[p]
            if type(v)==type(''):
                v='"'+v+'"'
            else:
                v=str(v)
            PRINT('%s = %s' % (p,v))
            return
        if param is None:
            prms=self.Prp_PlotParams.keys()
            prms.sort()
            for p in prms:
                PrintParam(p)
        else:
            param=param.capitalize()
            if not (param in self.Prp_PlotParams.keys()):
                self.Cmd_Error("Error: wrong type!")
            if value is None:
                PrintParam(param)
            else:
                if isFloat(value) and (type(self.Prp_PlotParams[param])==type(0.0)):
                    value=float(value)
                if isInt(value) and (type(self.Prp_PlotParams[param])==type(0)):
                    value=int(value)
                if type(value)!=type(self.Prp_PlotParams[param]):
                    self.Cmd_Error("Error: wrong type!")
                else:
                    if type(self.Prp_PlotParams[param])==type(''):
                        value=value
                    self.Prp_PlotParams[param]=value
                    self.Cmd_UpdatePlot()
        return
    def Cmd_Quit(self):
        '''
Quit()
    Terminates OMCEanalyser.
'''
        sys.exit(0)
        return
    def Cmd_WritePdf(self,pdfn='',plots=None):
        '''
WritePdf(pdfn='',plots=None)
    pdfn: name of the pdf-file
    plots: list of plots to write (None: all plots) 
    Writes plots to a pdf file.
    If the pdf-file name is not given (pdfn='') then the filename of the 
    first read data file (DataFiles[0]) is used as a basis for the 
    pdf-file.
'''
        if pdfn=='':
            if self.opts['-fo']=='':
                if len(self.opts['FILENAMES']):
                    self.opts['-fo']=os.path.splitext(self.opts['FILENAMES'][0])[0]+'.pdf'
                else:
                    self.Cmd_Error("Error: Pdf-filename unknown!")
            pdfn=self.opts['-fo']
        if (re.match(r'.*\\|.*/',pdfn) is None) and len(self.opts['FILENAMES']):
            pdfn=os.path.join(os.path.dirname(self.opts['FILENAMES'][0]),pdfn)
        if pdfn!='':
            pdfn=MakeUniqueFile(pdfn)
            if plots is None:
                plots=plt.get_fignums()
            else:
                try:
                    plots[0]
                except:
                    plots=[plots]
            nps=[]
            PL=plt.get_fignums()
            for i in plots:
                if i in PL:
                    nps.append(i)
            plots=nps
            if len(plots)>0:
                PRINT(MSG(107,str(plots).replace(' ',''),pdfn),VL_Default)
                pp = pdf.PdfPages(pdfn)
                cf=plt.gcf().number
                for pn in PL:
                    if pn in plots:
                        figure = plt.figure(pn)
                        pp.savefig(figure)
                pp.close()
                plt.figure(cf)
            else:
                self.Cmd_Error("Error: Nothing to write!")
        return
    def Cmd_ReadCsv(self,fn):
        '''
ReadCsv(filename)
    Reads data from a csv-file to a ResultDataClass object and appends it
    to DataFiles (list). DataFiles[-1] is the last recently read data. 
'''
        CheckFile(DefConText,fn)
        R=ResultDataClass()
        PRINT('Reading data file: %s in DataFiles[%s]' % (fn,len(self.Prp_DataFiles)),VL_Default)
        R.readCSV(fn)
        self.Prp_DataFiles.append(R)
        return
    def Fct_BarDiagram(self,data,lower_limit=0,bar_width=None):
        '''
bar_limits,bar_heights = BarDiagram(data,lower_limit=0,bar_width=None)
    data: must be an array like type containing the bar heights
    lower_limit: is the lower limits of the bar diagram
    bar_width: is the width of each bar
    Returns the bar limits and the bar heights. The length of bar_limits
    and bar_heights is the length of data + 1. 
    The values of bar_heights are:
        bar_heights[0:-1]=data[:] 
        bar_heights[-1]=0.0 
'''
        data=np.array(data)        
        if len(np.shape(data))>1:
            data=data[0]
        if bar_width is None:
            bar_width=1.0/len(data)
        n, bins=getBinData(len(data),lower_limit,bar_width,data)
        left = np.array(bins[:-1])
        right = np.array(bins[1:])
        bottom = np.zeros(len(left))
        top = bottom + n
        n1=np.hstack((n,np.zeros(1)))
        # we need a (numrects x numsides x 2) numpy array for the path helper
        # function to build a compound path
        XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T
        # get the Path object
        barpath = MyPath.make_compound_path_from_polys(XY)
        # make a patch out of it
        color=self.Prp_PlotParams['Color']
        alpha=self.Prp_PlotParams['Alpha']
        patch = patches.PathPatch(barpath, facecolor=color, edgecolor=color, alpha=alpha)
        ax=plt.gca()
        ax.add_patch(patch)
        Y=top.max()*1.05
        ax.set_xlim(left[0], right[-1])
        ax.set_ylim(bottom.min(), Y)
        plt.draw_if_interactive()
        del barpath
        del patch
        return bins,n1
    def Cmd_Run(self,cmdfn,params='',noupdate=False):
        '''
Run(filename,params='',noupdate=False)
    Executes the python statements from the specified "filename" equivalent 
    to the -run option.
    The file must be in the special OMCEanalyser xml-format.
    Set noupdate=True if no screen update is needed during the execution.
'''
        if (re.match(r'.*\\|.*/',cmdfn) is None):
            cmdfn=os.path.join(os.path.dirname(sys.argv[0]),self.opts['-rundir'],cmdfn)
        cmds,xmlframe = ReadCmdFile(cmdfn)
        self.XR.Set_xml(xmlframe)
        PRINT('Run commands from: '+cmdfn,VL_Noise)
        #WriteLog(self.opts,'Run("'+cmdfn+'","'+params+'",'+str(noupdate)+')\n')
        if noupdate:
            plt.ioff()
        Psave={}
        for p in self.Prp_Params.keys():
            Psave[p]=self.Prp_Params[p]
        try:
            if params!='':
                self.XR.Set_params(params)
                self.SetParams(self.XR.ParamList)
            self.RunSource(cmds+[''],cmdfn)
            #WriteLog(self.opts,'\n'.join(cmds)+"\n")
            #WriteLog(self.opts,'# end Run\n')
        finally:
            self.Prp_Params={}
            for p in Psave.keys():
                self.Prp_Params[p]=Psave[p]
            self.IC.filename='<input>'
            if noupdate:
                plt.ion()
                n=plt.gcf().number
                for i in plt.get_fignums():
                    plt.figure(i)
                    plt.draw_if_interactive()
                plt.figure(n)
        return
    def Cmd_Help(self,item=None):
        D=dir(self)
        cmds=[]
        for pn in D:
            if pn.startswith('Cmd_') and (pn!='Cmd_help'):
                cmds.append(pn[4:])
        cmds.sort()
        if item is None:
            PRINT('Command list:')
            for i,cn in enumerate(cmds):
                WRITE('%-12s '%cn)
                if (i>0) and (i % 5==0):
                    PRINT('')
            PRINT('\nuse Help(<command>) for specific information.')
        else:
            if type(item)==type(''):
                if item in cmds:
                    item=getattr(self, 'Cmd_'+item)
                else:
                    PRINT('Error: %s is not a command!' % item)
            doc=item.__doc__
            if doc: 
                PRINT(doc)
        return
    def Cmd_help(self):
        PRINT('use: Help() for help.')
        return
    def Cmd_Plot(self,x,y,format=''):
        '''
Plot(x,y,format='')
    Plots y-values over x-value using the given format or the PlotParams
    specification for Lcolor, Lstyle and Lwidth if format=''.
'''
        if format=='':
            linecolor=self.Prp_PlotParams['Lcolor']
            linestyle=self.Prp_PlotParams['Lstyle']
        linewidth=self.Prp_PlotParams['Lwidth']
        alpha=self.Prp_PlotParams['Alpha']
        if format=='':
            plt.plot(x,y,format,color=linecolor, linewidth=linewidth,linestyle=linestyle,alpha=alpha)
        else:
            plt.plot(x,y,format,linewidth=linewidth,alpha=alpha)
        return
    def Cmd_Scatter(self,x,y):
        '''
Scatter(x,y)
    Plots a scatter (circles) diagram using the Plotparams Color and Alpha.
    The circles are empty.
'''
        color=self.Prp_PlotParams['Color']
        alpha=self.Prp_PlotParams['Alpha']
        plt.plot(x,y,'o',markerfacecolor='None',markeredgecolor=color,alpha=alpha)
        return
    def Fct_Range(self,x=None,y=None,f=1.0):
        '''
xrange,yrange=Range(x=None,y=None,f=1.0)
    If x or y are given then they are treated as a range with a min and
    max value. The limits of the active plot are set to these ranges multiplied
    by f. If f is a list of two values then f[0] is used for the lower limit and
    f[1] is used for the upper limit.
    The function returns the x- and y-range of the active plot.
'''
        ax=plt.gca()
        ch=False
        f1=f2=f
        if not isFloat(f):
            f1=f[0]
            f2=f[1]
        if not (x is None):
            xi=min(x)
            xa=max(x)
            xm=(xa+xi)/2
            xi=1.*f1*(xi-xm)+xm
            xa=1.*f2*(xa-xm)+xm
            ax.set_xlim(xi,xa)
            ch=True
        if not (y is None):
            yi=min(y)
            ya=max(y)
            ym=(ya+yi)/2
            yi=f1*(yi-ym)+ym
            ya=f2*(ya-ym)+ym
            ax.set_ylim(yi,ya)
            ch=True
        if ch: 
            plt.draw_if_interactive()
        return (ax.get_xlim(),ax.get_ylim())
    def Fct_RangeX(self,x=None,f=1.0):
        '''
xrange=RangeX(x=None,f=1.0)
    If x is given then it is treated as a range with a min and
    max value. The x-limits of the active plot are set to this range multiplied
    by f. If f is a list of two values then f[0] is used for the lower limit and
    f[1] is used for the upper limit.
    The function returns the x-range of the active plot.
'''
        ax=plt.gca()
        ch=False
        f1=f2=f
        if not isFloat(f):
            f1=f[0]
            f2=f[1]
        if not (x is None):
            xi=min(x)
            xa=max(x)
            xm=(xa+xi)/2
            xi=f1*(xi-xm)+xm
            xa=f2*(xa-xm)+xm
            ax.set_xlim(xi,xa)
            ch=True
        if ch: 
            plt.draw_if_interactive()
        return ax.get_xlim()
    def Fct_RangeY(self,y=None,f=1.0):
        '''
yrange=RangeY(y=None,f=1.0)
    If y is given then it is treated as a range with a min and
    max value. The y-limits of the active plot are set to this range multiplied
    by f. If f is a list of two values then f[0] is used for the lower limit and
    f[1] is used for the upper limit.
    The function returns the y-range of the active plot.
'''
        ax=plt.gca()
        ch=False
        f1=f2=f
        if not isFloat(f):
            f1=f[0]
            f2=f[1]
        if not (y is None):
            yi=min(y)
            ya=max(y)
            ym=(ya+yi)/2
            yi=f1*(yi-ym)+ym
            ya=f2*(ya-ym)+ym
            ax=plt.gca()
            ax.set_ylim(yi,ya)
            ch=True
        if ch: 
            plt.draw_if_interactive()
        return ax.get_ylim()
    def Fct_Mag(self,x):
        '''
mag=Mag(self,x)
    The function returns the magnitude of x.
'''
        return MAGNITUDE(x)
    def Cmd_Error(self,errmsg,*args):
        '''
Error(errmsg,*args)
    This procedure should be used to signal errors in scripts.
    It will produce errmsg combined with *args and terminates 
    the script execution. 
'''
        if len(args)>0:
            errmsg=errmsg % args
        PRINT(errmsg)
        raise Terminate(100)

def Analyser(filename,options,params):
    opts,specs=InitOptions()
    SetOptionsOf(opts,specs,options)
    opts['CONTEXT']=DefConText
    if opts['-info'] == 1:
        Info(opts,specs)
    if opts['-log']!='':
        logfn=VarConv(opts,None,opts['-log'])
        if (re.match(r'.*\\|.*/',logfn) is None):
            logfn=os.path.join(os.path.dirname(sys.argv[0]),opts['-logdir'],logfn)
        opts['-log']=MakeUniqueFile(logfn)
        PRINT('Commands are logged to: '+opts['-log'],VL_Noise)
    opts['RD']=[]
    if filename!='':
        params.insert(0,filename)
        fns=[]
        prms=[]
        for fn in params:
            if '=' in fn:
                prms.append(fn)
            else:
                fns.append(fn)
    else:
        fns=[]
        prms=[]
    opts['FILENAMES']=fns
    opts['PARAMS']=prms
    CI=CmdInterpreter(opts,specs)
    XR=XmlReader(opts)
    for fn in fns:
        CI.Cmd_ReadCsv(fn)
    if opts['-rm']!=0:
        matplotlib.rc('font', family = 'serif')
    xml_start='''<Script 
  Name=""
  Title=""
  Author=""
  Version=""
  Date=""
  Options="">
  <Description>
  </Description>
  <Parameters>
  </Parameters>
'''        
    sec_start='''<Python Section="%s" Enable="1">\n'''
    sec_end='''</Python>\n'''
    xml_end='''</Script>\n'''
    WriteLog(opts,xml_start,'w')
    try:
        if opts['-run']!='':
            if not (re.match(r'.*\\|.*/',opts['-run']) is None):
                cmdfn=opts['-run']
            else:
                cmdfn=os.path.join(os.path.dirname(sys.argv[0]),opts['-rundir'],opts['-run'])
            cmds,xmlframe = ReadCmdFile(cmdfn)
            XR.Set_xml(xmlframe)
            XR.Set_params(opts['PARAMS'])
            CI.SetParams(XR.ParamList)
            src='\n'.join(cmds)
            WriteLog(opts,sec_start % '0'+src+"\n"+sec_end)
            PRINT('Run commands from: '+cmdfn,VL_Noise)
            plt.ioff()
            CI.RunSource(cmds+[''],cmdfn)
            if opts['-iam']:
                WriteLog(opts,sec_start % '1')
                CI.RunInteractive()
                WriteLog(opts,sec_end)
        else:
            WriteLog(opts,sec_start % '1')
            CI.RunInteractive()
            WriteLog(opts,sec_end)
    except SystemExit: 
        pass
    finally:
        if (opts['-pdf']!=0) and (opts['-iam']==0):
            CI.Cmd_WritePdf()
        WriteLog(opts,xml_end)
    return

def MAIN(argv):
    filename,options,params=InitStdMainSingle(argv,__MODID__,__AUTHOR__)
    Analyser(filename,options,params)
    return

if __name__=="__main__":
    DefConText.StopQueue()
    ExitCode=run_main(MAIN,sys.argv)
    sys.exit(ExitCode)
#{EOF]

