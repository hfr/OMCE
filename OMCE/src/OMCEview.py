#!/usr/bin/env python
# coding: latin-1
#-----------------------------------------------------
#
# Open Monte Carlo Histogram Viewer
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
# 1.0.0 2010-02-26 Rüdiger Kessel: Module created
# 1.1.0 2011-01-14 Rüdiger Kessel: Integration with OMCEbase
# 1.1.1 2011-01-21 Rüdiger Kessel: font size support
# 1.1.2 2011-01-23 Rüdiger Kessel: use run_main()
# 1.1.3 2011-01-23 Rüdiger Kessel: added option -its
#-----------------------------------------------------
__version__="1.1.3"
__MODID__="OMCE Histogram Viewer (Viewer V:"+__version__+")"
__AUTHOR__="Author: Ruediger Kessel (ruediger.kessel@gmail.com)"
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
        MSG, STR, PRINT, WRITE, FATALERROR, DefConText, GetOptionInfo, GetErrors, \
        GetDisclaimer, CheckFile, isFloat, isInt, VL_Error, VL_Warn, VL_Startup, \
        VL_Finish, VL_Progress, VL_Time, VL_Info, VL_Default, VL_Details, VL_Noise, \
        FilterSymbol, run_main, InitStdMainSingle, Exit

def histOutline(bincount,lowbin,binwidth,abins):
    bins = np.zeros(bincount*2 + 2, dtype=np.float)
    data = np.zeros(bincount*2 + 2, dtype=np.float)
    for bb in range(bincount):
        bins[2*bb + 1] = lowbin+binwidth*bb
        bins[2*bb + 2] = lowbin+binwidth*bb + binwidth
        if bb < bincount:
            data[2*bb + 1] = abins[bb]
            data[2*bb + 2] = abins[bb]
    bins[0] = bins[1]
    bins[-1] = bins[-2]
    data[0] = 0
    data[-1] = 0
    return (bins, data)

def getBinData(bincount,lowbin,binwidth,abins):
    bins=[lowbin]
    for i in xrange(bincount):
        bins.append(lowbin+(i+1)*binwidth)
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
    specs['-mark']=['s',0,1024,'[(Mean,b,dashed,1),(Low95,b,dashed,1),(High95,b,dashed,1)]', 'marker list -mark=[(<name>,<color>,<style>,<width>),...]']
    specs['-sid']=['s',0,255,':', 'range of simulation ID values which should be plotted']
    specs['-sym']=['s',0,255,'*', 'filter of symbols which should be plotted']
    specs['-max']=['i',1,maxi,20,  'maximum number of plots']
    specs['-v']=['i',0,10,2,       'verbose level 0..10: all..nothing']
    specs['-fo']=['s',0,255,'',    'name of the output file for plots']
    specs['-pdf']=['i',0,1,0,      'save plots as pdf, if set']
    specs['-mm']=['i',0,1,1,       'use fancy symbols']
    specs['-it']=['i',0,1,1,       'use italic for symbols']
    specs['-its']=['i',0,1,1,      'use italic for subscripts in symbols']
    specs['-rm']=['i',0,1,1,       'use serif font']
    specs['-sht']=['i',0,1,1,      'show x-label']
    specs['-shx']=['i',0,1,1,      'show y-label']
    specs['-shy']=['i',0,1,1,      'show title']
    specs['-ttl']=['s',0,255,'',   'diagram title']
    specs['-xl']=['s',0,255,'',    'x-label']
    specs['-yl']=['s',0,255,'',    'y-label']
    specs['-h']=['f',0.0,maxf,150.0,    'diagram height in mm']
    specs['-w']=['f',0.0,maxf,200.0,    'diagram width in mm']
    specs['-cfg']=['s',0,255,'OMCEview.cfg','name of the configuration file']
    specs['-xls']=['fs',1,100,16.0,    'x-label font size']
    specs['-yls']=['fs',1,100,16.0,    'y-label font size']
    specs['-tls']=['fs',1,100,16.0,    'title font size']
    specs['-xts']=['fs',1,100,12.0,    'x-axis ticks font size']
    specs['-yts']=['fs',1,100,12.0,    'y-axis ticks font size']
    for skey in specs.keys():
        opts[skey]=specs[skey][3]
    return opts,specs

def TexSymbol(opts,s,its=True):
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
                else:
                    if not its:
                        t=r'\mathregular{'+t+r'}'
                    if K[i]>0:
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

def Info(opts,specs):
    PRINT("Error: missing input file name!\n")
    PRINT("Usage: OMCEview <ohd-filename> [Options]")
    PRINT("Options:")
    PRINT(GetOptionInfo(opts,specs))
    PRINT("")
    PRINT("Exit Codes:")
    PRINT(GetErrors())
    PRINT("")
    PRINT(GetDisclaimer())
    PRINT("\nPress Enter...")
    sys.stdin.read(1)
    Exit()
    return

def VarConv(opts,D,ttl):
    if ttl.find('%def%')>=0:
        ttl=ttl.replace(r'%def%',MakeTeX(opts,TexSymbol(opts,D['def'])))
    if ttl.find('%fp%')>=0:
        ttl=ttl.replace(r'%fp%',os.path.splitext(opts['FILENAME'])[0])
    if ttl.find('%fn%')>=0:
        ttl=ttl.replace(r'%fn%',os.path.splitext(os.path.basename(opts['FILENAME']))[0])
    if ttl.find('%sym%')>=0:
        ttl=ttl.replace(r'%sym%',MakeTeXSym(opts,TexSymbol(opts,D['sym'],opts['-its'])))
    if ttl.find('%unit%')>=0:
        ttl=ttl.replace(r'%unit%',MakeTeX(opts,TexSymbol(opts,D['unit'])))
    if ttl.find('%unit-1%')>=0:
        if D['unit']!='':
            ttl=ttl.replace(r'%unit-1%',MakeTeX(opts,'('+TexSymbol(opts,D['unit'])+')^{-1}'))
        else:
            ttl=ttl.replace(r'%unit-1%','')
    if ttl.find('%phi%')>=0:
        ttl=ttl.replace(r'%phi%',MakeTeXSym(opts,r'\phi('+TexSymbol(opts,D['sym'],opts['-its'])+r')'))
    return ttl

def Viewer(filename,options):
    opts,specs=InitOptions()
    SetOptionsOf(opts,specs,options)
    if len(filename) == 0:
        Info(opts,specs)
    CheckFile(DefConText,filename)
    opts['FILENAME']=filename
    rs=ResultDataClass()
    PRINT('Reading data file: '+filename,VL_Default)
    rs.readCSV(filename)
    rs.setsidfilter(opts['-sid'].split(','))
    opts['-sym']=opts['-sym'].split(',')
    if rs.rowcount>opts['-max']:
        PRINT(MSG(108,STR(opts['-max'])),VL_Warn)
        rs.rowcount=opts['-max']
    if opts['-pdf']!=0:
        if opts['-fo']=='':
            opts['-fo']=os.path.splitext(opts['FILENAME'])[0]+'.pdf'
        pp = pdf.PdfPages(opts['-fo'])
    else:
        pp=None
    if opts['-mm']!=0:
        pass
    if opts['-rm']!=0:
        pass
        matplotlib.rc('font', family = 'serif')
    plotcount=0
    for r in xrange(rs.rowcount):
        D={}
        D['sym']=rs.entry(r,'Symbol')
        if rs.iscol('Unit'):
            D['unit']=rs.entry(r,'Unit')
            if type(D['unit'])==type(0.0):
                D['unit']=''
        else:
            D['unit']=''
        if rs.iscol('Definition'):
            D['def']=rs.entry(r,'Definition')
            if type(D['def'])==type(0.0):
                D['def']=''
        else:
            D['def']=''
        if not FilterSymbol(opts,D['sym']):
            continue
        plotcount+=1
        fig = plt.figure(figsize=(opts['-w']/25.4,opts['-h']/25.4))
        ax = fig.add_subplot(1,1,1)
        n, bins=getBinData(rs.bincount(r),rs.entryf(r,'LowBinLimit'),rs.entryf(r,'BinWidth'),rs.bins(r))
        left = np.array(bins[:-1])
        right = np.array(bins[1:])
        bottom = np.zeros(len(left))
        top = bottom + n


        # we need a (numrects x numsides x 2) numpy array for the path helper
        # function to build a compound path
        XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T

        # get the Path object
        barpath = MyPath.make_compound_path_from_polys(XY)

        # make a patch out of it
        patch = patches.PathPatch(barpath, facecolor='gray', edgecolor='gray', alpha=1)
        ax.add_patch(patch)

        PRINT(MSG(106,D['sym']),VL_Default)
        if opts['-sht']!=0:
            ttl=opts['-ttl']
            if ttl=='':
                if rs.iscol('Definition') and (D['def']!=''):
                    ttl='%def%'
                else:
                    ttl='%fn%'
            plt.title(VarConv(opts,D,ttl),fontsize=opts['-tls'],x=0.5,y=1.01)
        Y=top.max()*1.05
        if len(opts['-mark'])>0:
            Ms=opts['-mark'].replace(" ","").split("),(")
            for M in Ms:
                M=M.replace("[(","")
                M=M.replace(")]","")
                M=M.split(",")
                if rs.colindex(M[0])<0:
                    FATALERROR(86,M[0])
                if len(M)==1:
                    M.append('b')
                if len(M)==2:
                    M.append('dashed')
                if len(M)==3:
                    M.append('1')
                X=rs.entryf(r,M[0])
                plt.plot([X,X],[0, Y],color=M[1], linewidth=float(M[3]),linestyle=M[2])
        ax.set_xlim(left[0], right[-1])
        ax.set_ylim(bottom.min(), Y)
        if opts['-shx']!=0:
            xl=opts['-xl']
            if xl=='':
                if D['unit']!='':
                    xl=r'%sym% in %unit%'
                else:
                    xl=r'%sym%'
            ax.set_xlabel(VarConv(opts,D,xl),size=opts['-xls'])
        if opts['-shy']!=0:
            yl=opts['-yl']
            if yl=='':
                if D['unit']!='':
                    if opts['-mm']!=0:
                        yl=r'%phi% in %unit-1%'
                    else:
                        yl=r'phi(%sym%) in (%unit%)^-1'
                else:
                    yl='%phi%'
            ax.set_ylabel(VarConv(opts,D,yl),size=opts['-yls'])
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(opts['-xts'])
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(opts['-yts'])
        if not (pp is None):
            pp.savefig(fig)
    if (rs.rowcount>0) and (opts['-pdf']==0):
        plt.show()
    if not (pp is None):
        pp.close()
        m='[1-%d]' % plotcount
        PRINT(MSG(107,m,opts['-fo']),VL_Default)
    return

def MAIN(argv):
    filename,options,params=InitStdMainSingle(argv,__MODID__,__AUTHOR__)
    Viewer(filename,options)
    return

if __name__=="__main__":
    DefConText.StopQueue()
    ExitCode=run_main(MAIN,sys.argv)
    sys.exit(ExitCode)
#{EOF]
