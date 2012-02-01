
import sys
# ModuleFinder can't handle runtime changes to __path__, but win32com uses them
try:
    # py2exe 0.6.4 introduced a replacement modulefinder.
    # This means we have to add package paths there, not to the built-in
    # one.  If this new modulefinder gets integrated into Python, then
    # we might be able to revert this some day.
    # if this doesn't work, try import modulefinder
    try:
        import py2exe.mf as modulefinder
    except ImportError:
        import modulefinder
    import win32com
    for p in win32com.__path__[1:]:
        modulefinder.AddPackagePath("win32com", p)
    for extra in ["win32com.shell"]: #,"win32com.mapi"
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, p)
except ImportError:
    # no build path setup, no worries.
    pass

from distutils.core import setup
from Ft.Lib.DistExt import Py2Exe
from py2exe.build_exe import py2exe

import py2exe
import os
import shutil
import zipfile
import OMCE

infolevel=2

def info(l,text):
    if l>=infolevel:
        print text
    return

shutil.rmtree("build", ignore_errors=True)

shutil.rmtree("dist", ignore_errors=True)

excludes = ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
                "pywin.dialogs", "pywin.dialogs.list",
                "Tkconstants","Tkinter","tcl"
           ]

if len(sys.argv)<2:
    sys.argv.append('py2exe')

setup(console=['../OMCE.py','../OMCEserver.py','../OMCEclient.py','../OMCEcomp.py','../double_bs.py'],
      zipfile = r'library.zip',
      options={
                "py2exe":{
                        "unbuffered": True,
                        "compressed": 2,
                        "optimize": 2,
                        "excludes": excludes,
                        "packages": ["encodings","amara","tlslite","tlslite.api","tlslite.errors"],
                        "bundle_files": 2
                        }
                }
      )

SRCPATH = os.path.dirname(sys.argv[0])
DESTPATH = SRCPATH+"\\OMCE"

BINSRCPATH = SRCPATH+"\\GenOMCE\\dist"

BINDESTPATH = DESTPATH+"\\bin"

DOCDESTPATH = DESTPATH+"\\doc"

SRCDESTPATH = DESTPATH+"\\src"

def DeleteAllFilesIn(dir):
    if dir[-1] == os.sep: dir = dir[:-1]
    files = os.listdir(dir)
    for file in files:
        if (file == '.') or (file == '..'): continue
        path = dir + os.sep + file
        if os.path.isdir(path):
            info(2,"Warning: ["+path+"] is a directory!")
        else:
            info(0,"Delete '"+path+"'")
            os.remove(path)
    return

def CopyAll(files,src,dest):
    if src[-1] == os.sep: src = src[:-1]
    if dest[-1] == os.sep: dest = dest[:-1]
    for f in files:
        info(0,"copy '"+src + os.sep + f+"' to '"+dest + os.sep + f+"'")
        shutil.copy (src + os.sep + f,dest + os.sep + f)
    return

def CopyAllInTo(src,dest,dirs=False):
    if src[-1] == os.sep: src = src[:-1]
    if dest[-1] == os.sep: dest = dest[:-1]
    files = os.listdir(src)
    for file in files:
        if (file == '.') or (file == '..'): continue
        spath = src + os.sep + file
        dpath = dest + os.sep + file
        if os.path.isdir(spath):
            if dirs:
                CopyAllInTo(spath,dpath,dirs)
        else:
            info(0,"copy '"+spath+"' to '"+dpath+"'")
            shutil.copy(spath,dpath)
    return

def ZipAll(zip,src,dest,dirs=False):
    if src[-1] == os.sep: src = src[:-1]
    if dest[-1] == os.sep: dest = dest[:-1]
    files = os.listdir(src)
    for file in files:
        if (file == '.') or (file == '..'): continue
        spath = src + os.sep + file
        if dest=='':
            dpath = file
        else:
            dpath = dest + os.sep + file
        if os.path.isdir(spath):
            if dirs:
                ZipAll(zip,spath,dpath,dirs)
        else:
            info(0,"zip '"+spath+"' as '"+dpath+"'")
            zip.write(spath,dpath)
    return


DeleteAllFilesIn(BINDESTPATH)

DeleteAllFilesIn(DOCDESTPATH)

DeleteAllFilesIn(SRCDESTPATH)

binfiles = ['OMCE.cfg','OMCEclient.cfg','OMCE.ofd','OMCE.vfd','OMCE.xsd','ALT.ofd','ALT.vfd',
            'OMCE_V1_0.ofd','OMCE_V1_1.ofd','!RunServer.bat','OMCEserver.cfg','!RunView.bat',
            '!Register_OMCE_tools.bat']

CopyAllInTo(BINSRCPATH,BINDESTPATH)

CopyAll(binfiles,SRCPATH,BINDESTPATH)

docfiles = ['OMCE_Schema.html','OMCE.pdf']

CopyAll(docfiles,SRCPATH,DOCDESTPATH)

srcfiles = ['OMCE.ofd','OMCE.py','OMCEd.py','OMCEd_config','OMCE.cfg','OMCEclient.py','OMCEclient.cfg',
            'OMCEbase.py','OMCE.vfd','OMCE.xsd','ALT.ofd','ALT.vfd','MakeExe_OMCE.py','OMCEview.py',
            'OMCEview.cfg','MakeExe_OMCEview.py','OMCE_V1_0.ofd','OMCE_V1_1.ofd','OMCEcomp.py',
            'OMCEserver.py','OMCEserver.cfg','OMCEerrors.py','OMCEmsgs.py','OMCEanalyser.py',
            'OMCEanalyser.cfg','OMCEanalyser.xsd','double_bs.py']

CopyAll(srcfiles,SRCPATH,SRCDESTPATH)

vf=file(BINDESTPATH+'\\version.txt','w')
vf.write(OMCE.__version__+'\r\n')
vf.close()

zipfilename=SRCPATH+'\\OMCE-'+OMCE.__version__+'.zip'

if os.path.exists(zipfilename):
    os.remove(zipfilename)

info(0,"Create zip file: "+zipfilename)
zip=zipfile.ZipFile(zipfilename,'w',zipfile.ZIP_DEFLATED)
ZipAll(zip,DESTPATH,'OMCE',True)
info(2,zipfilename+" created.")

info(2,'done.')
