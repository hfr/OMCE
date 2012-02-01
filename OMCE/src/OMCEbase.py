#
# coding: latin-1
#-----------------------------------------------------
#
# Support functions for the Open Monte Carlo Engine
#
# Author: Rüdiger Kessel
#        National Institute of Standards and Technology (NIST)
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
__version__="1.0.5"
__MODID__="OMCE Base (V:"+__version__+")"
__AUTHOR__="Author: Rüdiger Kessel (ruediger.kessel@gmail.com)"
SERVICEVERSION="1.0.0"
SERVICE_VERSION="1.0.0"
#-----------------------------------------------------
# 1.0.0 2010-06-08 Rüdiger Kessel: created
# 1.0.1 2011-01-25 Rüdiger Kessel: unicode support
# 1.0.2 2011-02-11 Rüdiger Kessel: ConText support
# 1.0.3 2011-02-11 Rüdiger Kessel: security layer support
# 1.0.4 2011-02-11 Rüdiger Kessel: encode bugfix for Python 2.5
# 1.0.5 2011-02-11 Rüdiger Kessel: encode bugfix for missing VdbAuthenticator
#-----------------------------------------------------
from OMCEerrors import error
from OMCEmsgs import msg
import array
import sys
import math
import os
import imp
import csv
import StringIO
import time
import socket
from _csv import QUOTE_MINIMAL
from collections import deque
import traceback
import thread as TH
import threading as THG
import fnmatch
from rpyc.utils.server import ForkingServer
from rpyc.utils.server import ThreadedServer
import re
if False:
    import dbhash
    import dumbdbm
import amara

def cmpver(vA, vB):
    """
    Compares two version number strings
    @param vA: first version string to compare
    @param vB: second version string to compare
    @author <a href="http://sebthom.de/">Sebastian Thomschke</a>
    @return negative if vA < vB, zero if vA == vB, positive if vA > vB.

    Examples:
    >>> cmpver("0", "1")
    -1
    >>> cmpver("1", "0")
    1
    >>> cmpver("1", "1")
    0
    >>> cmpver("1.0", "1.0")
    0
    >>> cmpver("1.0", "1")
    0
    >>> cmpver("1", "1.0")
    0
    >>> cmpver("1.1.0", "1.0.1")
    1
    >>> cmpver("1.0.1", "1.1.1")
    -1
    >>> cmpver("0.3-SNAPSHOT", "0.3")
    -1
    >>> cmpver("0.3", "0.3-SNAPSHOT")
    1
    >>> cmpver("1.3b", "1.3c")
    -1
    >>> cmpver("1.14b", "1.3c")
    1
    """
    if vA == vB: return 0

    def num(s):
        if s.isdigit(): return int(s)
        return s

    seqA = map(num, re.findall('\d+|\w+', vA.replace('-SNAPSHOT', '')))
    seqB = map(num, re.findall('\d+|\w+', vB.replace('-SNAPSHOT', '')))

    # this is to ensure that 1.0 == 1.0.0 in cmp(..)
    lenA, lenB = len(seqA), len(seqB)
    for i in range(lenA, lenB): seqA += (0,)
    for i in range(lenB, lenA): seqB += (0,)

    rc = cmp(seqA, seqB)

    if rc == 0:
        if vA.endswith('-SNAPSHOT'): return -1
        if vB.endswith('-SNAPSHOT'): return 1
    return rc

if cmpver(amara.__version__,'2.0')>=0:
    amara_version=2
    from amara import bindery
else:
    amara_version=1
    bindery=None

#Default Server Port used for OMCE and OMCEclient
DefServerPort=4201

'''
Helper function to improve readability
'''
def DictMerge(*dicts):
    import operator
    return dict(reduce(operator.add, [x.items() for x in dicts]))

'''
  VerboseLevel:
     9 Error Messages
     8 Warnings
     7 Startup
     6 Finish
     5 Simulation progress
     4 Time info
     3 info
     2 default
     1 calculation details
     0 noise
'''
VL_Error=9
VL_Warn=8
VL_Startup=7
VL_Finish=6
VL_Progress=5
VL_Time=4
VL_Info=3
VL_Default=2
VL_Details=1
VL_Noise=0

class STDIO:
    def __init__(self,f_write,f_read):
        self.stdout=sys.stdout
        self.stdin=sys.stdin
        self.f_write=f_write
        self.f_read=f_read
    def write(self,s):
        self.f_write(s)
    def read(self,num):
        return self.f_read(num)
    def flush(self):
        return

def INIT_IO(iofs=None):
    if iofs is None:
        sys.stderr=sys.stdout
    else:
        io=STDIO(iofs[0],iofs[1])
        sys.stderr=io
        sys.stdout=io
        sys.stdin=io
    return

def _write(M):
    sys.stdout.write(M)
    sys.stdout.flush()
    return

def main_is_frozen():
    return (hasattr(sys, "frozen") or # new py2exe
           hasattr(sys, "importers") # old py2exe
           or imp.is_frozen("__main__")) # tools/freeze

def get_main_dir():
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)

class ConText:
    def __init__(self,FT):
        self._Write=FT['write']
        self._Read=FT['read']
        self.IsFile=FT['isfile']
        self.ReadFile=FT['readfile']
        self.WriteFile=FT['writefile']
        self.ReadBinFile=FT['readbinfile']
        self.PathJoin=FT['joinpath']
        self.SetDefExt=FT['setdeftext']
        self.DirPath=FT['dirpath']
        self.SplitExt=FT['splitext']
        self.EncodingOption = 'iso_8859_1'
        self.CodePage = 'cp850'
        self.VerboseLevel=2
        self.IsServer=False
        self.Imports=os.path.join(get_main_dir(),'imports')
        self.logfile=None
        self.QueueEvent=THG.Event()
        self.QueueEvent.clear()
        self.QueueLock=TH.allocate_lock()
        self.Queue=deque([])
        self.useQueue=True
        self.QueueThd=THG.Thread(target=self.DoQueue)
        self.QueueThd.setDaemon(True)
        self.QueueThd.start()
        return
    def Finish(self):
        self.StopQueue()
        if self.logfile: self.logfile.close()
        return
    def EmptyQueue(self):
        if self.useQueue:
            while True:
                self.QueueLock.acquire()
                loop=len(self.Queue)>0
                self.QueueLock.release()
                if not loop:
                    break;
                self.QueueEvent.set()
                time.sleep(0.01)
        return
    def StopQueue(self):
        self.useQueue=False
        self.QueueEvent.set()
        self.QueueThd.join()
        return
    def DoQueue(self):
        while self.useQueue:
            self.QueueEvent.wait()
            self.QueueEvent.clear()
            self.QueueLock.acquire()
            s=''
            while len(self.Queue):
                s+=self.Queue.popleft()
            self.QueueLock.release()
            self._Write(s)
        s=''
        while len(self.Queue):
            s+=self.Queue.popleft()
        self._Write(s)
        return
    def Write(self,s):
        if self.useQueue:
            self.QueueLock.acquire()
            self.Queue.append(s)
            self.QueueEvent.set()
            self.QueueLock.release()
        else:
            self._Write(s)
    def Read(self,n):
        self.EmptyQueue()
        s=self._Read(n)
        return s
    def _nodash(self,s):
        return s.replace('-','_')
    def UNICODE(self,s):
        if type(s)==type(''):
            s=unicode(s,encoding=self._nodash(self.EncodingOption), errors='replace')
        else:
            s=unicode(s)
        return s

    def FILENAME(self,s):
        return s.encode(sys.getfilesystemencoding(),'ignore')

    def STR(self,v):
        if type(v)==type(unicode('')):
            s=v.encode(self._nodash(self.EncodingOption),'replace')
        else:
            try:
                s=str(v)
            except:
                s='$$$ no string $$$'
        return s

    def STRCONV(self,v):
        if type(v)==type(''):
            v=unicode(v, encoding='latin-1',errors='replace')
            s=v.encode(self.CodePage,'replace')
        else:
            try:
                s=str(v)
            except:
                s='$$$ no string $$$'
        return s

    def PRINT(self,M,level=10):
        if type(M)!=type(' '):
            self.WRITE(self.MSG(3,self.STR(type(M)),VL_Warn))
        self.WRITE(self.STRCONV(M)+'\r\n',level)
        return

    def WRITE(self,M,level=10):
        if level>=self.VerboseLevel:
            self.Write(self.STRCONV(M))
            if self.logfile: self.logfile.write(self.STRCONV(M))
        return

    def READ(self,n):
        return self.Read(n)

    def SHOWTIME(self,opts,t, level=2, msg=''):
        if opts['-t']>=level:
            self.PRINT(msg + "%0.2f" % (t)+' sec',VL_Time)

    def FATALERROR(self,num,msg):
        self.PRINT(msg,VL_Error)
        Exit(num)
        return

    def ERROR(self,num,*args):
        raise Error(num,*args)

    def FormatError(self,f):
        self.ERROR(4,f)
        return

    def ERRORMSG(self,num,*args):
        EN="%03d" % num
        if num in error.keys():
            E=error[num]
            al=[]
            for i in range(len(E[1])):
                if i<len(args):
                    al.append(self.STR(args[i]))
                else:
                    al.append('')
            msg="\nError "+EN+": "+E[0] % tuple(al)
        else:
            al=[]
            for a in args:
                al.append(self.STR(a))
            msg="\nError "+EN+": ["+' '.join(al)+"]"
        return msg

    def MSG(self,num,*args):
        if num in msg.keys():
            E=msg[num]
            if E[0]:
                al=[]
                for i in range(len(E[1])):
                    if i<len(args):
                        al.append(self.STR(args[i]))
                    else:
                        al.append('')
                M=E[0] % tuple(al)
            else:
                M=''
        else:
            al=[]
            for a in args:
                al.append(self.STR(a))
            M="MSG(%04d" % num +", "+', '.join(al)+")"
        return M
    def NOISE(self,M):
        self.PRINT(M,VL_Noise)
        return
    def WARN(self,M):
        self.PRINT(M,VL_Warn)
        return

def CheckFile(context,filename):
    filename=MakeFilename(filename)
    if context.IsServer:
        errn1=252
        errn2=253
    else:
        errn1=2
        errn2=3
    if not os.path.exists(filename):
        context.ERROR(errn1,filename)
    if not os.path.isfile(filename):
        context.ERROR(errn2,filename)
    return

def insert(original, new, pos):
    '''Inserts new inside original at pos.'''
    return original[:pos] + new + original[pos:]

def GetErrors():
    L=[]
    ek=error.keys()
    ek.sort()
    for e in ek:
        E=error[e]
        EN="%03d" % e
        msg="Exit Code "+EN+" [Error: "+E[0] % tuple(E[1])+"]"
        msg=msg.replace('&amp;','&')
        msg=msg.replace('&lt;','<')
        msg=msg.replace('&gt;','>')
        L.append(msg)
    return '\n'.join(L)+'\n'

def GetErrorsTeX():
    L=[]
    ek=error.keys()
    ek.sort()
    header=r'''
\begin{center}
\begin{tabular}{|c|l|}
\hline
\multicolumn{2}{|c|}{\bf Program exit codes}  \\
 \hline
  Exit Code & Error message \\
 \hline'''
    footer=r''' \hline
\end{tabular}
\end{center}'''
    L.append(header)
    i=0
    max=100
    for e in ek:
        if ((i % 50)==0) and (i!=0):
            L.append(footer)
            L.append(header)
        E=error[e]
        EN="%03d" % e
        P=[EN]
        N=[]
        for e in E[1]:
            N.append(r'\verb.'+e+'.')
        M=E[0]
        M=M.replace('%%',r'\%%')
        j=M.find('<')
        while j>=0:
            M=insert(M,r'\verb.',j)
            l=M.find('>',j)
            if l<0:
                l=len(M)-1
            M=insert(M,'.',l+1)
            j=M.find('<',l)
        M=M.replace('&amp;','&')
        M=M.replace('&lt;','$<$')
        M=M.replace('&gt;','$>$')
        M=M.replace('|','$|$')
        M="Error: "+ (M % tuple(N))
        if len(M)>max:
            p=max
            while (M[p]!=' ') and (p>0):
                p-=1
            if p==0:
                p=M.find(' ')
            if p>=0:
                P.append(M[0:p])
                msg=r"  %s & %s \\" % tuple(P)
                L.append(msg)
                i+=1
                P=['   ']
                M=M[p:]
        P.append(M)
        msg=r"  %s & %s \\" % tuple(P)
        L.append(msg)
        i+=1
    L.append(footer)
    return '\n'.join(L)+'\n'

def MakeFilename(fn):
    if type(fn)==type([]):
        fn=os.path.join(*fn)
    return fn

def _IsFile(filename):
    filename=MakeFilename(filename)
    return os.path.isfile(filename)

def _ReadFile(filename,pos=0,count=-1):
    if (pos!=0) or (count!=-1):
        DefConText.WARN(MSG(9,'_ReadFile()'))
    filename=MakeFilename(filename)
    CheckFile(DefConText,filename)
    f=file(filename,'r')
    d=f.read()
    f.close()
    return d

def _WriteFile(file,data,mode="w"):
    file=MakeFilename(file)
    fdo=open(file,mode)
    fdo.write(data)
    fdo.close()

def LocReadBinFile(context,_file):
    import numpy as np
    def ReadDataBlock(fileobj,results,dimens,size):
        rdata = np.fromfile(fileobj, dtype='float64', count=dimens*size)
        rdata = np.reshape(rdata, (size, dimens))
        for j in range(0,dimens):
            results[j].append(rdata[:,j])
        return
    def ReadDataBlockFmt2(fileobj,results,dimens,size):
        for j in range(0,dimens):
            try:
                rdata = np.fromfile(fileobj, dtype='float64', count=size)
                results[j].append(rdata)
            except Exception,e:
                raise Error(8,fileobj.name,str(e))
        return
    _file=MakeFilename(_file)
    CheckFile(context,_file)
    results=[]
    fileobj = file(_file, mode='rb')
    longA =  array.array('l')
    longA.read(fileobj, 2)
    runs = longA[0]
    rcount = longA[1]
    blocksize=10000
    fmt=1
    RL=[]
    if runs==0:
        raise Error(9)
    if runs==-1:
        longA1 =  array.array('l')
        longA1.read(fileobj, 2)
        fmt=2
        runs=longA1[0]
        blocksize=longA1[1]
    elif runs==-1330463557:
        longA1 =  array.array('l')
        longA1.read(fileobj, 6)
        fmt=2
        runs=longA1[0]
        blocksize=longA1[1]
        skip=longA1[2] #symtable offset after header (usually 0)
        flags=longA1[3]
        if skip>0:
            skipA = array.array('B')
            skipA.read(fileobj, skip)
        if (flags & 1)>0:
            RL=Bytes2StringList(skipA)
    elif runs<-1:
        raise Error(7,runs)
    if runs<1:
        raise Error(8,_file,'runs=%s' % str(runs))
    if len(RL)>0:
        ws=', ['+', '.join(RL)+']'
    else:
        ws=''
    context.PRINT('reading '+context.STR(runs)+' * '+context.STR(rcount)+' values from '+_file+ws,VL_Info)
    fullblocks = runs // blocksize
    lbs = runs % blocksize
    for i in range(0,rcount):
        results.append([])
    if fmt==1:
        for i in range(0,fullblocks):
            ReadDataBlock(fileobj,results,rcount,blocksize)
        if lbs!=0:
            ReadDataBlock(fileobj,results,rcount,lbs)
    elif fmt==2:
        for i in range(0,fullblocks):
            ReadDataBlockFmt2(fileobj,results,rcount,blocksize)
        if lbs!=0:
            ReadDataBlockFmt2(fileobj,results,rcount,lbs)
    for i in range(0,rcount):
        results[i]=np.concatenate((results[i][:]))
        results[i]=results[i].dumps()
    fileobj.close()
    return results,RL

def _ReadBinFile(_file):
    return LocReadBinFile(DefConText,_file)

def _SetDefExt(fn,ext):
    if os.path.splitext(fn)[1]=='':
        fn=fn+ext
    return fn

def _DirPath(fn):
    return os.path.dirname(os.path.realpath(fn))

try:
    DefConText = ConText({
             'write':_write,
             'read':sys.stdin.read,
             'isfile':_IsFile,
             'readfile':_ReadFile,
             'writefile':_WriteFile,
             'readbinfile':_ReadBinFile,
             'joinpath':os.path.join,
             'setdeftext':_SetDefExt,
             'dirpath':_DirPath,
             'splitext':os.path.splitext})
except:
    DefConText = ConText({
             'write':_write,
             'read':sys.stdin.readline,
             'isfile':_IsFile,
             'readfile':_ReadFile,
             'writefile':_WriteFile,
             'readbinfile':_ReadBinFile,
             'joinpath':os.path.join,
             'setdeftext':_SetDefExt,
             'dirpath':_DirPath,
             'splitext':os.path.splitext})

WRITE=DefConText.WRITE
READ=DefConText.READ
STR=DefConText.STR
PRINT=DefConText.PRINT
ERROR=DefConText.ERROR
FATALERROR=DefConText.FATALERROR
MSG=DefConText.MSG
ERRORMSG=DefConText.ERRORMSG

def isFloat(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False

def isInt(s):
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False

def MAGNITUDE(v):
    if v==0.0:
        M=0
    else:
        M=math.floor(math.log10(abs(v)))
    return M

def GetDisclaimer():
    d=""" Disclaimer:

 This software was developed at the National Institute of Standards
 and Technology by employees of the Federal Government in the
 course of their official duties. Pursuant to title 17 Section 105
 of the United States Code this software is not subject to
 copyright protection and is in the public domain. This software is
 experimental. NIST assumes no responsibility whatsoever for its
 use by other parties, and makes no guarantees, expressed or
 implied, about its quality, reliability, or any other
 characteristic. We would appreciate acknowledgement if the
 software is used.
"""
    return d

def GetOptionInfo(opts,specs,LM=9):
    if 'context' in opts.keys():
        context=opts['CONTEXT']
    else:
        context=DefConText
    L=[]
    ol=specs.keys()
    ol.sort()
    F=" "*LM+'%-12s'
    for o in ol:
        L.append(F % (o+'='+context.STR(opts[o]))+" "+specs[o][4])
    return '\n'.join(L)+'\n'

def SetOptionsOf(opts,specs,argv):
    if 'context' in opts.keys():
        context=opts['CONTEXT']
    else:
        context=DefConText
    if len(argv)>0:
        for i in range(0,len(argv)):
            o=argv[i].split('=')
            if len(o)==2:
                opt=o[0]
                val=o[1]
                if opt in opts:
                    spec=specs[opt]
                    if spec[0] in ['f','i']:
                        if not isFloat(val):
                            context.ERROR(5,opt,val)
                        if (float(val)<spec[1]) or (float(val)>spec[2]):
                            context.ERROR(6,opt,spec[1],spec[2])
                    if spec[0]=='f':
                        opts[opt]=float(val)
                    if spec[0]=='i':
                        opts[opt]=int(val)
                    if spec[0]=='s':
                        opts[opt]=str(val)
                    if spec[0]=='is':
                        try:
                            opts[opt]=int(val)
                        except:
                            opts[opt]=str(val)
                    if spec[0]=='fs':
                        try:
                            opts[opt]=float(val)
                        except:
                            opts[opt]=str(val)
                else:
                    context.ERROR(1,opt)
    return

def StringList2Bytes(L):
    B=array.array('B')
    for s in L:
        for c in s:
            B.append(ord(c))
        B.append(0)
    B.append(0)
    return B

def Bytes2StringList(B):
    L=[]
    s=''
    for b in B:
        if b!=0:
            s+=chr(b)
        else:
            if s!='':
                L.append(s)
                s=''
            else:
                break
    return L

def PadZeros(B,BS):
    bc=len(B)/int(BS)
    br=len(B) % int(BS)
    if br>0:
        bc+=1
        for i in xrange(BS-br):
            B.append(0)
    return B

class excel:
    delimiter = ','
    quotechar = '\"'
    escapechar = None
    doublequote = True
    skipinitialspace = False
    lineterminator = '\n'
    quoting = QUOTE_MINIMAL

class ResultDataClass:
    def __init__(self):
        self.data=[]
        self.colnames=[]
        self.rowcount=0
        self._rowcount=0
        self.colcount=0
        self.mins=[]
        self.maxs=[]
        self.filename=''
        self.info={}
        self.sidspec=''
        self.filters={}
        self._data=[]
        return
    def __call__(self,coln,row=None):
        ca=self.colarrayf(coln)
        if (row is None) or (len(ca)==0):
            return ca
        else:
            return ca[row]
    def readCSV(self,filename):
        f=open(filename, 'r')
        csvlist=csv.reader(f,dialect=excel)
        data=[i for i in csvlist]
        keys=data[0][0:]
        keys=[k.strip() for k in keys]
        rdata=[]
        count=0
        for row in data[1:]:
            row1=[]
            for i in xrange(len(keys)):
                if row[i]=='':
                    v=0.0
                else:
                    v=row[i]
                row1.append(v)
            rdata.append(row1)
            count+=1
        self.colnames=keys
        self.rowcount=count
        self._rowcount=count
        self.data=rdata
        self._data=rdata
        self.colcount=len(keys)
        self.info['file']=filename
        if len(self.filters)>0:
            for ci in self.filters.keys():
                self.applyfilter(ci,self.filters[self.filters.keys()[ci]])
        return self
    def bincount(self,r):
        return self.entryi(r,'BinCount')
    def bin(self,r,i):
        return self.entryf(r,'Bin[%d]' % i)
    def bins(self,r):
        bs=[]
        for i in xrange(self.bincount(r)):
            bs.append(self.bin(r,i))
        return bs
    def colindices(self,colnames):
        '''
        colnames: list of column names (strings)
            example: ['BinCount','Bin[0]','Bin[1]']
            the following expansions will be applied:
                ['Bin[:]'] --> ['Bin[0]',...,'Bin[n]'], n=max(Bin)
                ['Bin[2:]'] --> ['Bin[2]',...,'Bin[n]'], n=max(Bin)
                ['Bin[:5]'] --> ['Bin[0]',...,'Bin[4]']
                ['Bin[1:5]'] --> ['Bin[0]',...,'Bin[4]']
        '''
        if type(colnames)==type(''):
            colnames=[colnames]
        ids=[]
        for coln in colnames:
            if '[' in coln:
                sids=[]
                sn=coln[0:coln.index('[')+1]
                for n in self.colnames:
                    if n.startswith(sn):
                        nn=''
                        for c in n[n.index('[')+1:]:
                            if c in '0123456789':
                                nn+=c
                        sids.append(int(nn))
                isp=''
                for c in coln[coln.index('[')+1:]:
                    if c in '0123456789:':
                        isp+=c
                isp=isp.split(':')
                if len(isp)==1:
                    if isp[0]=='':
                        isp[0]=0
                        isp.append(max(sids)+1)
                    else:
                        isp[0]=int(isp[0])
                        isp.append(isp[0]+1)
                else:
                    isp[0]=int('0'+isp[0])
                    if isp[1]=='':
                        isp[1]=max(sids)+1
                    else:
                        isp[1]=int(isp[1])
                for sid in sids:
                    if (sid>=isp[0]) and (sid<isp[1]):
                        cn=sn+str(sid)+']'
                        cid=self.colindex(cn)
                        if (cid>=0) and not (cid in ids):
                            ids.append(cid)
            else:
                cid=self.colindex(coln)
                if (cid>=0) and not (cid in ids):
                    ids.append(cid)
        ids.sort()
        return ids
    def arrayf(self,colnames):
        import numpy as np
        ids=self.colindices(colnames)
        if len(ids)==1:
            a=np.empty((self.rowcount), dtype='float64')
        else:
            a=np.empty((self.rowcount,len(ids)), dtype='float64')
        for i in xrange(self.rowcount):
            for j in xrange(len(ids)):
                f=self.data[i][ids[j]]
                if isFloat(f):
                    f=float(f)
                else:
                    f=np.nan
                if len(ids)==1:
                    a[i]=f
                else:
                    a[i,j]=f
        return a
    def rowarrayf(self,colnames,r):
        import numpy as np
        ids=self.colindices(colnames)
        a=np.empty(len(ids), dtype='float64')
        for i in xrange(len(ids)):
            f=self.data[r][ids[i]]
            if isFloat(f):
                f=float(f)
            else:
                f=np.nan
            a[i]=f
        return a
    def entry(self,r,coln):
        col=self.colindex(coln)
        return self.data[r][col]
    def entryi(self,r,coln):
        col=self.colindex(coln)
        i=self.data[r][col]
        if isInt(i):
            i=int(i)
        else:
            i=-1
        return i
    def entryf(self,r,coln):
        col=self.colindex(coln)
        f=self.data[r][col]
        if isFloat(f):
            f=float(f)
        else:
            f=0
        return f
    def colindex(self,coln):
        coln=coln.lower()
        id=-1
        for i in xrange(len(self.colnames)):
            if self.colnames[i].lower()==coln:
                id=i
                break
        return id
    def iscol(self,coln):
        return (self.colindex(coln) >= 0)
    def colarrayf(self,colns):
        return self.arrayf(colns)
    def clearfilter(self):
        self.filters={}
        self.data=self._data
        self.rowcount=self._rowcount
    def buildspecs(self,specs):
        '''
        specs: list of values specifications (strings)
            example: ['0','!0','0.5:1.0','!1.5:2.0']
            the following translations will be applied:
                ['0'] --> value==0
                ['!0'] --> value!=0
                ['0:'] == ['[0:'] --> value>=0

                [']0:'] --> value > 0
                ['[0:'] --> value >= 0
                ['0:']  --> value >= 0

                [':0]'] --> value <= 0
                [':0['] --> value < 0
                [':0']  --> value < 0

                ['!:0'] --> value >= 0
                [':0]'] --> value <= 0
                ['0.5:1.0'] == ['[0.5:1.0['] --> 0.5 <= value < 1.0
                ['!1.5:2.0'] == ['![1.5:2.0['] --> !(1.5 <= value < 2.0) == (value < 1.5) or (value >= 2.0)
            the return is a list of tuples
            return: [(<op>,<value>),...]
                <op>: '=','!=','>','<','>=','<='
                <value>: float
        '''
        def getfstr(s):
            sn=''
            for c in s:
                if c in '0123456789.Ee-+':
                    sn+=c
            return sn
        def gett(s,left=True):
            t=None
            if s!='':
                it='@'
                if left:
                    if s[0] in "[]":
                        it=s[0]
                        s=s[1:]
                else:
                    if s[-1] in "[]":
                        it=s[-1]
                        s=s[:-1]
                n=float(s)
                if (left and (it==']')): op='>'
                elif (left and (it in '[@')): op='>='
                elif (not left and (it==']')): op='<='
                elif (not left and (it in '[@')): op='<'
                t=(op,n)
            return t
        def invop(t):
            op=t[0]
            no=None
            if op=='==': no='!='
            elif op=='!=': no='=='
            elif op=='>=': no='<'
            elif op=='>': no='<='
            elif op=='<=': no='>'
            elif op=='<': no='>='
            tt=(no,t[1])
            return tt
        if type(specs)==type(''):
            specs=[specs]
        ids=[]
        for spec in specs:
            if (spec!=''):
                if spec[0]=='!':
                    inv=True
                    spec=spec[1:]
                else:
                    inv=False
                spa=spec.split(':')
                if len(spa)==1:
                    s=spa[0]
                    n=float(s)
                    if inv:
                        t=('!=',n)
                    else:
                        t=('==',n)
                    ids.append(t)
                else:
                    t=gett(spa[0],True)
                    if t and inv:
                        t=invop(t)
                    if t: ids.append(t)
                    t=gett(spa[1],False)
                    if t and inv:
                        t=invop(t)
                    if t: ids.append(t)
        return ids
    def setfilter(self,coln,specs):
        ci=self.colindex(coln)
        if ci>=0:
            ns=self.buildspecs(specs)
            self.applyfilter(ci,ns)
            self.filters[ci]=ns

    def applyfilter(self,ci,specl):
        def comp(op,v1,v2):
            if   op=='==': l= v1==v2
            elif op=='!=': l= v1!=v2
            elif op=='>=': l= v1>=v2
            elif op=='>' : l= v1>v2
            elif op=='<=': l= v1<=v2
            elif op=='<' : l= v1<v2
            return l
        if (ci>=0) and (ci<self.colcount):
            rdata=[]
            for i in xrange(self.rowcount):
                icl=True
                v=float(self.data[i][ci])
                if isFloat(v):
                    for spec in specl:
                        op,rv=spec
                        icl=comp(op,v,rv)
                        if not icl:
                            break
                if icl:
                    rdata.append(self.data[i])
            self.data=rdata
            self.rowcount=len(rdata)
        return
    def setsidfilter(self,sidspec):
        self.setfilter('SID',sidspec)
        return

def ReadOptionFile(context,fn,warn=True):
    '''
    Reads a list of options from a text file
      fn: file name
      return: list of well formed option strings
    '''
    L=[]
    if context.IsFile(fn):
        cfg=context.ReadFile(fn)
        f=StringIO.StringIO(cfg)
        for line in f:
            line=line.strip()
            if line=="":
                continue
            elif line=="\n":
                continue
            elif line.startswith("#"):
                continue
            elif line.startswith("-"):
                L.append(line)
                continue
            else:
                context.PRINT(context.MSG(4,line,fn),VL_Warn)
        f.close()
    else:
        if warn and (fn!=''):
            context.PRINT(context.MSG(2,fn),VL_Warn)
    return L

def ReadCmdFile(fn,warn=True,context=DefConText):
    '''
    Reads a list of commands from a text file
      fn: file name
      return: list of command strings, xml-text with stripped code sections
    '''
    xml=[]
    L=[]
    if context.IsFile(fn):
        cfg=context.ReadFile(fn)
        f=StringIO.StringIO(cfg)
        incode=False
        inpyth=False
        for line in f:
            line=line.strip('\n')
            if not incode:
                if line.strip().startswith('<Python'):
                    incode=True
                    enabled=True
                    inpyth=True
                    petext=''
                if inpyth:
                    clm=line.find('>')
                    if clm<0:
                        petext+=line+' '
                        continue
                    inpyth=False
                    line=petext+' '+line
                    line=line.strip()
                    ep=line.find('Enable')
                    if (ep>=0) and (ep<clm):
                        ss=line[ep+len('Enable'):clm].strip()
                        if ss.startswith('='):
                            ss=ss[1:].strip()
                            if ss.startswith('"'):
                                es=ss[1:ss.find('"',1)].strip()
                                if (es!='') and isInt(es):
                                    enabled=int(es)>0
                    xml.append(line)
                else:
                    xml.append(line)
                continue
            else:
                if line.startswith("</Python>"):
                    incode=False
                    xml.append(line)
                    continue
                elif not enabled:
                    continue
                elif line=="\n":
                    continue
                elif line.find("#")==0:
                    continue
                else:
                    L.append(line)
        f.close()
    else:
        if warn and (fn!=''):
            context.PRINT(context.MSG(7,fn),VL_Warn)
    xml='\n'.join(xml)
    return L,xml

class Terminate(Exception):
    def __init__(self,code=0):
        self.code=code
        return

class Abort(Exception):
    def __init__(self):
        return

class Error(Exception):
    def __init__(self,num,*p):
        self.number=num
        self.params=p
        return

def Exit(n=0):
    raise Terminate(n)

def TRACEINFO(excinfo = None):
    if not excinfo:
        excinfo = sys.exc_info()
    return "".join(traceback.format_exception(*excinfo))

class OMCElogger(object):
    def __init__(self, name, console = sys.stderr, file = None, show_name = True,
    show_pid = False, show_tid = False, show_date = False, show_time = True,
    show_label = True, quiet = False):
        self.name = name
        self.console = console
        self.file = file
        self.show_name = show_name
        self.show_pid = show_pid
        self.show_tid = show_tid
        self.show_date = show_date
        self.show_time = show_time
        self.show_label = show_label
        self.quiet = quiet
        self.filter = set()
        self.QueueEvent=THG.Event()
        self.QueueEvent.clear()
        self.QueueLock=TH.allocate_lock()
        self.Queue=deque([])
        self.useQueue=True
        self.QueueThd=THG.Thread(target=self.DoQueue)
        self.QueueThd.setDaemon(True)
        self.QueueThd.start()

    def StopQueue(self):
        self.useQueue=False
        self.QueueEvent.set()
        self.QueueThd.join()

    def DoQueue(self):
        while self.useQueue:
            self.QueueEvent.wait()
            self.QueueEvent.clear()
            self.QueueLock.acquire()
            s=''
            while len(self.Queue):
                s+=self.Queue.popleft()
            self.QueueLock.release()
            self._Write(s)

    def Write(self,s):
        if self.useQueue:
            self.QueueLock.acquire()
            self.Queue.append(s)
            self.QueueLock.release()
            self.QueueEvent.set()
        else:
            self._Write(s)

    def _Write(self,text):
        if self.console:
            self.console.write(text)
        if self.file:
            self.file.write(text)
            self.file.flush()

    def log(self, label, msg):
        if label in self.filter:
            return
        header = []
        if self.show_name:
            header.append("%-10s" % (self.name,))
        if self.show_label:
            header.append("%-10s" % (label,))
        if self.show_date:
            header.append(time.strftime("%Y-%m-%d"))
        if self.show_time:
            header.append(time.strftime("%H:%M:%S"))
        if self.show_pid:
            header.append("pid=%d" % (os.getpid(),))
        if self.show_tid:
            header.append("tid=%d" % (TH.get_ident(),))
        if header:
            header = "[" + " ".join(header) + "] "
        sep = "\n...." + " " * (len(header) - 4)
        text = header + sep.join(msg.splitlines()) + "\n"
        self.Write(text)

    def debug(self, msg, *args, **kwargs):
        if self.quiet: return
        if args: msg %= args
        self.log("DEBUG", msg)
    def info(self, msg, *args, **kwargs):
        if self.quiet: return
        if args: msg %= args
        self.log("INFO", msg)
    def warn(self, msg, *args, **kwargs):
        if self.quiet: return
        if args: msg %= args
        self.log("WARNING", msg)
    def error(self, msg, *args, **kwargs):
        if args: msg %= args
        self.log("ERROR", msg)
    def traceback(self, excinfo = None):
        self.log("TRACEBACK", TRACEINFO(excinfo))

class UnQuote(object):
    import pyparsing
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letters = lowercase + uppercase
    digits = '0123456789'
    punctuation = """!#$%&()*+,-./:;<=>?@[\]^_`{|}~"""
    nonsp = digits + letters + punctuation
    Nonsp=pyparsing.Word(nonsp)
    squote=pyparsing.QuotedString("'",escQuote="''")
    dquote=pyparsing.QuotedString('"',escQuote='""')
    atom=Nonsp|squote|dquote
    line=atom+pyparsing.ZeroOrMore(atom)
    def __init__(self,s):
        self.li=['']
        if s!='':
            self.li=list(self.line.parseString(s, parseAll=True))
    def __getitem__(self,i):
        return self.li[i]
    def __call__(self,i=None):
        if i is None:
            return self.li
        else:
            return self.li[i]
    def list(self,i=None):
        if i is None:
            return self.li
        else:
            return self.li[i]

def AddQuotes1(T):
    TO=[]
    for t in T:
        t=t.replace("'","\\'")
        TO.append("'"+t+"'")
    return TO

def AddQuotes2(T):
    TO=[]
    for t in T:
        t=t.replace('"','\\"')
        TO.append('"'+t+'"')
    return TO

class Str2ParamList(object):
    import pyparsing
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letters = lowercase + uppercase
    digits = '0123456789'
    punctuation = """!#$%&()*+,-./:;<=>?@[\]^_`{|}~"""
    nonsp = digits + letters + punctuation
    Nonsp=pyparsing.Word(nonsp)
    squote=pyparsing.QuotedString("'",escQuote="\\'").setParseAction(AddQuotes1)
    dquote=pyparsing.QuotedString('"',escQuote='\\"').setParseAction(AddQuotes2)
    equsign = pyparsing.Literal( "=" )
    ident = pyparsing.Word(pyparsing.alphas+"_", pyparsing.alphas+pyparsing.nums+"_")
    atom=ident+equsign+(Nonsp|squote|dquote)
    line=atom+pyparsing.ZeroOrMore(atom)
    def __init__(self,s):
        self.li=['']
        self.lp=[]
        if s!='':
            self.li=list(self.line.parseString(s, parseAll=True))
            for i in range(0,len(self.li),3):
                self.lp.append(''.join(self.li[i:i+3]))
    def __getitem__(self,i):
        return self.li[i]
    def __call__(self,i=None):
        if i is None:
            return self.lp
        else:
            return self.lp[i]
    def list(self,i=None):
        if i is None:
            return self.li
        else:
            return self.li[i]
    def plist(self,i=None):
        if i is None:
            return self.lp
        else:
            return self.lp[i]

try:
	from rpyc.utils.authenticators import VdbAuthenticator as VdbAuthenticator
except:
	from rpyc.utils.authenticators import TlsliteVdbAuthenticator as VdbAuthenticator
from rpyc.utils.authenticators import tlsapi, AuthenticationError

class OMCEAuthenticator(VdbAuthenticator):
    wait_time=60.0 # 1 min * number of non successful tries
    max_wait_time=600.0 # 10 min.
    valid_retries=3 # allow 3 valid retries
    bypass_known_ip=False
    def __init__(self,vdb):
        VdbAuthenticator.__init__(self,vdb)
        self.lastaccess={}
        self.users=[]
        self.update_accessdb()

    @classmethod
    def from_dict(cls, users):
        inst = cls(tlsapi.VerifierDB())
        for username, password in users.iteritems():
            inst.set_user(username, password)
        inst.update_accessdb()
        return inst

    def update_accessdb(self):
        self.users=self.list_users()
        self.lastaccess={}
        for u in self.users:
            self.lastaccess[u]={'last_try':None, 'no_success':0, 'success_ip':[]}
        return

    def set_user(self, username, password):
        VdbAuthenticator.set_user(self, username, password)
        self.update_accessdb()

    def del_user(self, username):
        VdbAuthenticator.del_user(self, username)
        self.update_accessdb()

    def __call__(self, sock):
        h, p = sock.getpeername()
        sock2 = tlsapi.TLSConnection(sock)
        sock2.fileno = lambda fd=sock.fileno(): fd    # tlslite omitted fileno
        try:
            sock2.handshakeServer(verifierDB = self.vdb)
        except Exception:
            if sock2.allegedSrpUsername!='':
                tries=''
                if sock2.allegedSrpUsername in self.users:
                    self.lastaccess[sock2.allegedSrpUsername]['last_try']=time.clock()
                    self.lastaccess[sock2.allegedSrpUsername]['no_success']+=1
                    tries="(%s tries)" % str(self.lastaccess[sock2.allegedSrpUsername]['no_success'])
            raise AuthenticationError("Bad try for user %s %s" % (sock2.allegedSrpUsername,tries))
        LA=self.lastaccess[sock2.allegedSrpUsername]
        if (self.bypass_known_ip and not (h in LA['success_ip'])) and (LA['no_success']>self.valid_retries) and (time.clock() - LA['last_try']<min(LA['no_success']*self.wait_time,self.max_wait_time)):
            LA['no_success']+=1
            LA['last_try']=time.clock()
            raise AuthenticationError("Repeated login failed for %s (%s tries)" % (sock2.allegedSrpUsername,LA['no_success']))
        else:
            LA['no_success']=0
            LA['last_try']=None
            if not (h in LA['success_ip']):
                LA['success_ip'].append(h)
        return sock2, sock2.allegedSrpUsername

def OMCE_authenticate_and_serve_client(inst, sock):
    try:
        if inst.authenticator:
            h, p = sock.getpeername()
            try:
                sock, credentials = inst.authenticator(sock)
            except AuthenticationError,e:
                inst.logger.warn("Authentication error: %s", str(e))
                inst.logger.warn("%s:%s failed to authenticate, rejecting connection", h, p)
                return
            else:
                inst.logger.info("%s:%s authenticated successfully", h, p)
        else:
            credentials = None
        try:
            inst._serve_client(sock, credentials)
        except Exception,e:
            etype = sys.exc_type
            excinfo = sys.exc_info()
            try:
                ename = etype.__name__
            except AttributeError:
                ename = etype
            inst.logger.warn("Exception: %s",ename)
            inst.logger.traceback(excinfo)
    finally:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        sock.close()
        inst.clients.discard(sock)
    return

    def start(self):
        """starts the server. use close() to stop"""
        self.listener.listen(self.backlog)
        h, p = self.listener.getsockname()
        self.logger.info("server started on %s:%s", h, p)
        self.active = True
        if self.auto_register:
            t = THG.Thread(target = self._bg_register)
            t.setDaemon(True)
            t.start()
        #if sys.platform == "win32":
        # hack so we can receive Ctrl+C on windows
        self.listener.settimeout(0.5)
        try:
            try:
                while True:
                    self.accept()
            except EOFError:
                pass # server closed by another thread
            except SystemExit:
                self.logger.warn("System exit")
            except KeyboardInterrupt:
                self.logger.warn("keyboard interrupt!")
        finally:
            self.logger.info("server has terminated")
            self.close()

class OMCEThreadedServer(ThreadedServer):
    def _authenticate_and_serve_client(self, sock):
        OMCE_authenticate_and_serve_client(self, sock)

class OMCEForkingServer(ForkingServer):
    def _authenticate_and_serve_client(self, sock):
        OMCE_authenticate_and_serve_client(self, sock)

def FilterSymbol(opts,sym):
    R=False
    for pat in opts['-sym']:
        if fnmatch.fnmatchcase(sym,pat):
            R=True
            break
    return R

def InitStdMainSingle(argv,modid,author):
    cfgfile=''
    for prm in argv[1:]:
        if prm[0:3]=="-v=":
            o=prm.split('=')
            if len(o)==2:
                DefConText.VerboseLevel=int(o[1])
        elif prm[0:5]=="-cfg=":
            o=prm.split('=')
            if len(o)==2:
                cfgfile=os.path.join(get_main_dir(),o[1])
    if cfgfile=='':
        cfgfile=os.path.splitext(argv[0])[0]+'.cfg'
    PRINT(modid,VL_Startup)
    PRINT(author,VL_Startup)
    PRINT('Config file: '+cfgfile,VL_Noise)
    options=ReadOptionFile(DefConText,cfgfile)
    filename=""
    params=[]
    for prm in argv[1:]:
        if prm[0:1]=="-":
            options.append(prm)
        else:
            if filename=="":
                filename=prm
            else:
                params.append(prm)
    return filename,options,params

def run_main(MAIN,argv,*args):
    try:
        ExitCode=0
        try:
            argv=list(argv)
            if '--qioq' in argv:
                DefConText.StopQueue()
                del argv[argv.index('--qioq')]
            INIT_IO()
            MAIN(argv,*args)
        except Error,er:
            if er.number==-1:
                DefConText.PRINT(er.params[0],VL_Error)
                ExitCode=255
            else:
                ExitCode=er.number
                DefConText.PRINT(DefConText.ERRORMSG(er.number,*er.params))
        except Terminate,te:
            ExitCode = te.code
        except Exception,e:
            DefConText.PRINT(TRACEINFO(),VL_Details)
            DefConText.PRINT(DefConText.ERRORMSG(255,'Fatal Error: '+DefConText.STR(e)+"!"),VL_Error)
            ExitCode=255
        except SystemExit:
            DefConText.PRINT('System exit')
    finally:
        if ExitCode!=0:
            DefConText.PRINT(DefConText.MSG(1,'Program'),VL_Error)
        DefConText.Finish()
    return ExitCode

def m_iff(con,T,F):
    if con:
        return T
    else:
        return F

def m_sqr(v):
    return v**2

def InitMathSymbols():
    glob={"__builtins__":None}
    glob['sqrt']=math.sqrt
    glob['sqr']=m_sqr
    glob['pow']=math.pow
    glob['abs']=math.fabs
    glob['exp']=math.exp
    glob['log']=math.log
    glob['log10']=math.log10
    glob['sin']=math.sin
    glob['cos']=math.cos
    glob['tan']=math.tan
    glob['asin']=math.asin
    glob['acos']=math.acos
    glob['atan']=math.atan
    glob['sinh']=math.sinh
    glob['cosh']=math.cosh
    glob['tanh']=math.tanh
    glob['minimum']=min
    glob['min']=min
    glob['maximum']=max
    glob['max']=max
    glob['iff']=m_iff
    glob['pi']=math.pi
    glob['e']=math.e
    return glob

def GetReservedWords(opts):
    '''
    returns a list of reserved words (case sensitive)
    '''
    wl=["and","del","from","not","while",
        "as","elif","global","or","with",
        "assert","else","if","pass","yield",
        "break","except","import","print",
        "class","exec","in","raise",
        "continue","finally","is","return",
        "def","for","lambda","try",
        "__builtins__","__block_size__","__print_error__"]
    return wl

from pyparsing import OneOrMore,Literal,Optional,ZeroOrMore,Forward,Or,alphas,nums,Word,CaselessLiteral,Combine,NoMatch,ParseException
class Grammar:
    def __init__(self,context,syms,funcs,usrfuncs,gtype):
        self.IdentList=[]
        self.UsrIdentList=[]
        self.ERROR=context.ERROR
        self.PRINT=context.PRINT
        self.G=self._grammar(syms,funcs,usrfuncs,gtype)
        return

    def markAsIdent(self,T):
        for t in T:
            self.IdentList.append(t)
        return T

    def markAsVIdent(self,T):
        self.markAsIdent(T)
        TO=[]
        for t in T:
            TO.append("'"+t+"'")
        return TO

    def markAsUsrIdent(self,T):
        for t in T:
            self.UsrIdentList.append(t)
        return T

    def markAsMant(self,T):
        found=False
        for t in T:
            if t == '.':
                found=True
                break
        if not found:
            T=list(T)
            T.append('.')
            T.append('0')
        return T

    def markAsNum(self,T):
        return T

    def replaceFunction(self,T):
        R=[]
        L={}
        for O in T:
            if O in L.keys():
                R.append(L[O])
            else:
                R.append(O)
        return R

    def replaceLogical(self,T):
        R=[]
        L={'.eq':'==','.lt':'<','.gt':'>','.le':'<=','.ge':'>=','.ne':'!=','not':'~','and':'&','or':'|'}
        for O in T:
            if O in L.keys():
                R.append(L[O])
            else:
                R.append(O)
        return R

    def replaceOperator(self,T):
        R=[]
        L={'^':'**'}
        for O in T:
            if O in L.keys():
                R.append(L[O])
            else:
                R.append(O)
        return R

    def _grammar(self,syms,funcs,usrfuncs,gtype):
        '''
        definition of the grammar used for expressions
        syms, funcs, usrfuncs are lists to symbols and functions which can be used
        gtype defines the grammar type: 1 = <Equ>, 2 = <Constraint>, 3 = Parameter
        '''
        point = Literal( "." )
        E     = CaselessLiteral( "E" )
        mant  = (Word( "+-"+nums, nums ) + Optional( point + Optional( Word( nums ) ) )).setParseAction(self.markAsMant)
        fnumber = Combine( mant + Optional( E + Word( "+-"+nums, nums ) ) ).setParseAction(self.markAsNum)
        ident = Word(alphas+"_", alphas+nums+"_").setParseAction(self.markAsIdent)
        vident = Word(alphas+"_", alphas+nums+"_").setParseAction(self.markAsVIdent)
        plus  = Literal( "+" )
        minus = Literal( "-" )
        mult  = Literal( "*" )
        div   = Literal( "/" )
        lpar  = Literal( "(" )
        rpar  = Literal( ")" )
        comma = Literal( "," )

        equal   = Literal( ".eq" ).setParseAction(self.replaceLogical) | Literal( "==" )
        less    = Literal( ".lt" ).setParseAction(self.replaceLogical) | Literal( "<" )
        greater = Literal( ".gt" ).setParseAction(self.replaceLogical) | Literal( ">" )
        lessequal = Literal( ".le" ).setParseAction(self.replaceLogical) | Literal( "<=" )
        greaterequal = Literal( ".ge" ).setParseAction(self.replaceLogical) | Literal( ">=" )
        notequal = Literal( ".ne" ).setParseAction(self.replaceLogical) | Literal( "!=" )
        _not = Literal( "not" ).setParseAction(self.replaceLogical)
        _and = Literal( "and" ).setParseAction(self.replaceLogical)
        _or = Literal( "or" ).setParseAction(self.replaceLogical)
        logicop = _not | _and | _or
        compop = equal | less | greater | lessequal | greaterequal | notequal
        truefalse = Literal('True') | Literal('False')

        addop  = plus | minus
        multop = mult | div
        expop = Literal( "**" ) | Literal( "^" ).setParseAction(self.replaceOperator)
        if len(syms)>0:
            symbol = None
            for s in syms:
                if symbol:
                    symbol = symbol ^ Literal(s)
                else:
                    symbol = Literal(s)
        else:
            symbol = NoMatch()

        if len(funcs)>0:
            funcname = None
            for f in funcs:
                if not (f in ['iff', 'val', 'u']):
                    if funcname:
                        funcname = funcname ^ Literal(f)
                    else:
                        funcname = Literal(f)
        else:
            funcname = NoMatch()

        if len(usrfuncs)>0:
            usrfuncname = None
            for f in usrfuncs:
                if usrfuncname:
                    usrfuncname = usrfuncname ^ Literal(f).setParseAction(self.markAsUsrIdent)
                else:
                    usrfuncname = Literal(f).setParseAction(self.markAsUsrIdent)
        else:
            usrfuncname = NoMatch()

        expr = Forward()
        logicterm = Forward()
        logiccomp = expr + compop + expr
        logicatom = Optional(_not)+((lpar+(logicterm|logiccomp)+rpar) | truefalse)
        logicterm << (logicatom + ZeroOrMore(logicop + logicatom))
        logicexpr = logicterm | logiccomp
        par2 = expr + comma + expr
        paramlist = (lpar+rpar) ^ (lpar + expr + ZeroOrMore(comma + expr)+ rpar)
        if gtype in [1]:
            iffunc = Literal( "iff" )+lpar+logicexpr+comma+par2+rpar
            valfunc = Literal( "val" )+lpar+vident+rpar
            ufunc = Literal( "u" )+lpar+vident+rpar
        else:
            iffunc = NoMatch()
            valfunc = NoMatch()
            ufunc = NoMatch()
        usrfunc = usrfuncname + paramlist
        functions = (funcname+paramlist)^iffunc^valfunc^ufunc^usrfunc
        atom = Optional(Word("+-"))+((fnumber^(symbol^functions^ident))|(lpar+expr+rpar))
        factor = Forward()
        factor << (atom + ZeroOrMore( ( expop + factor ) ))
        term = factor + ZeroOrMore( ( multop + factor ) )
        expr << (term + ZeroOrMore( ( addop + term ) ))
        if gtype==1:
            return expr
        elif gtype==2:
            return logicexpr
        elif gtype==3:
            return expr
        else:
            self.ERROR(29,gtype)
        return
    def CheckGrammar(self,equ,promt,name):
        '''
        check of the expression <equ> against the grammar
          <promt> and <name> are used for error handling
        '''
        self.G.setDebug(False)
        try:
            self.IdentList=[]
            self.UsrIdentList=[]
            ps=self.G.parseString(equ, parseAll=True)
        except ParseException,PE:
            self.PRINT(promt+': '+name)
            self.PRINT(PE.line)
            self.PRINT(" "*(PE.column-1) + "^")
            self.ERROR(13,PE)
        self.PRINT('CG out: '+''.join(ps),VL_Noise)
        return ps,self.IdentList,self.UsrIdentList

def GetPredefinedSymbols(opts):
    '''
    creates a dictionary with the predefined symbols
    the functions are mappings of the math symbols
    '''
    glob={}
    glob['pi']=math.pi
    glob['e']=math.e
    return glob

class TypeByName(object):
    typelist={'':str, 's':str, 'i':int, 'f':float}
    def __init__(self,name):
        self.name=name
        return
    def __call__(self):
        if self.name in self.typelist.keys():
            return self.typelist[self.name]
        else:
            return str


#{EOF]

