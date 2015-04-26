# py2exe setup program
from distutils.core import setup
import py2exe, pygame
import pymunk
import sys
import os
import glob, shutil
#sys.argv.append("py2exe")

VERSION = '0.1'
AUTHOR_NAME = 'Michael A. Hawker'
AUTHOR_EMAIL = 'support@mikeware.com'
AUTHOR_URL = "http://www.mikeware.com/"
PRODUCT_NAME = "Space Battle Arena"
SCRIPT_MAIN = 'SBA_Serv.py'
VERSIONSTRING = PRODUCT_NAME + " v" + VERSION
ICONFILE = 'icon.ico'

# Remove the build tree on exit automatically
REMOVE_BUILD_ON_EXIT = True

origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ["sdl_ttf.dll"]:
                return 0
        return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

if os.path.exists('dist/'): shutil.rmtree('dist/', ignore_errors=True)

pymunk_dir = os.path.dirname(pymunk.__file__)

graphics = glob.glob(os.path.join('GUI\Graphics\*','*.png'))
extra_files = [os.path.join(pymunk_dir, 'chipmunk.dll')]

d = {}
for f in graphics:
     p = os.path.dirname(f)
     if not d.has_key(p):
          d[p] = []
     d[p].append(f)
print d
for k in d:
     extra_files.append((k, d[k]))
print extra_files
extra_files.append(("", ["freesansbold.ttf",
                         "SDL.dll",
                         "SDK_tff.dll"
                         "libfreetype-6.dll",
                         "zlib1.dll"]))
#extra_files = [ #("",[ICONFILE,'icon.png','readme.txt']),
                   #("", ["freesansbold.ttf"]),
                   #(os.path.dirname(graphics), ),
                   #("graphics",glob.glob(os.path.join('graphics','*.png'))),
                   #("fonts",glob.glob(os.path.join('fonts','*.ttf'))),
                   #("music",glob.glob(os.path.join('music','*.ogg'))),
                   #("sounds",glob.glob(os.path.join('sounds','*.wav')))
     #]

# List of all modules to automatically exclude from distribution  build
# This gets rid of extra modules that aren't necessary for proper functioning of app
# You should only put things in this list if you know exactly what you DON'T need
# This has the benefit of drastically reducing the size of your dist

MODULE_EXCLUDES =[
'email',
'AppKit',
'Foundation',
'bdb',
'difflib',
'tcl',
'Tkinter',
'Tkconstants',
'curses',
'distutils',
'setuptools',
'BaseHTTPServer',
'_LWPCookieJar',
'_MozillaCookieJar',
'ftplib',
'gopherlib',
'_ssl',
'htmllib',
'httplib',
'mimetools',
'mimetypes',
'rfc822',
'tty',
'webbrowser',
'compiler',
'pydoc']

INCLUDE_STUFF = ['encodings',"encodings.latin_1","encodings.cp1252","encodings.zlib_codec","encodings.hex_codec","encodings.ascii"]

setup(console=[
             {'script': SCRIPT_MAIN,
               'other_resources': [(u"VERSIONTAG",1,VERSIONSTRING)],
               #'icon_resources': [(1,ICONFILE)]
               }],
         options = {"py2exe": {
                             "optimize": 2,
                             "includes": INCLUDE_STUFF,
                             "compressed": 1,
                             "ascii": 1,
                             "bundle_files": 2,
                             "ignores": ['tcl','AppKit','Foundation'],
                             "excludes": MODULE_EXCLUDES} },
          name = PRODUCT_NAME,
          version = VERSION,
          data_files = extra_files,
          zipfile = 'pylib.zip',
          author = AUTHOR_NAME,
          author_email = AUTHOR_EMAIL,
          url = AUTHOR_URL)

# Create the /save folder for inclusion with the installer
#shutil.copytree('save','dist/save')

if os.path.exists('dist/tcl'): shutil.rmtree('dist/tcl')

# Remove the build tree
if REMOVE_BUILD_ON_EXIT:
     shutil.rmtree('build/')

if os.path.exists('dist/tcl84.dll'): os.unlink('dist/tcl84.dll')
if os.path.exists('dist/tk84.dll'): os.unlink('dist/tk84.dll')
