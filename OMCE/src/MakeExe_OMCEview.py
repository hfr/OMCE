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
import matplotlib

import py2exe
import os
import shutil
import zipfile
import OMCEview
import sys
import glob

import shutil
shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("dist", ignore_errors=True)

excludes = ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
                "pywin.dialogs", "pywin.dialogs.list"
           ]

if len(sys.argv)<2:
    sys.argv.append('py2exe')

setup(console=['../OMCEview.py','../OMCEanalyser.py'],
    zipfile = r'library.zip',
    data_files=[(r'mpl-data', glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\*.*')),
                    # Because matplotlibrc does not have an extension, glob does not find it (at least I think that's why)
                    # So add it manually here:
                  (r'mpl-data', [r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\matplotlibrc']),
                  (r'mpl-data\images',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\images\*.*')),
                  (r'mpl-data\fonts',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\fonts\*.*'))]
,
    options={
                "py2exe":{
                        'includes': ["matplotlib.backends",
                                    "matplotlib.figure","pylab", "numpy","matplotlib.pyplot","matplotlib.numerix.fft",
                                    "matplotlib.numerix.linear_algebra", "matplotlib.numerix.random_array",
                                    "matplotlib.backends.backend_tkagg", "matplotlib.backends.backend_pdf",
                                    "matplotlib.axes","matplotlib.rcsetup"],  
                        #"optimize": 2,
                        "bundle_files": 3,
                        "excludes": excludes,
                        "packages": ["encodings",'matplotlib', 'pytz',"tlslite","tlslite.api","tlslite.errors","amara",
                                     "Ft.Xml.XInclude"],
                        'dll_excludes': ['libgdk-win32-2.0-0.dll','libgobject-2.0-0.dll','libgdk_pixbuf-2.0-0.dll',
                                          'MSVCP90.dll']
                        }
                }
      )

infolevel=2

def info(l,text):
    if l>=infolevel:
        print text
    return


def DeleteAllFilesIn(dir,subdirs=False):
    if dir[-1] == os.sep: dir = dir[:-1]
    files = os.listdir(dir)
    for file in files:
        if (file == '.') or (file == '..'): continue
        path = dir + os.sep + file
        if os.path.isdir(path):
            if subdirs:
                info(0,"Delete dir '"+path+"'")
                shutil.rmtree(path)
            else:
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

SRCPATH = os.path.dirname(sys.argv[0])
DESTPATH = SRCPATH+"\\OMCE"

BINSRCPATH = SRCPATH+"\\GenOMCEview\\dist"

BINDESTPATH = DESTPATH+"\\viewer"

shutil.rmtree(BINDESTPATH)

binfiles = ['OMCEview.cfg','OMCEanalyser.cfg','OMCEanalyser.xsd']
            
shutil.copytree(BINSRCPATH,BINDESTPATH)

CopyAll(binfiles,SRCPATH,BINDESTPATH)

os.mkdir(BINDESTPATH+"\\logs")

os.mkdir(BINDESTPATH+"\\cmds")

print 'done.'
