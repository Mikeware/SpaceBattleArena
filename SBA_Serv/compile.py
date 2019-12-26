# This will create a dist directory containing the executable file, all the data
# directories. All Libraries will be bundled in executable file.
#
# Run the build process by entering
# 'python compile.py build' in a console prompt.
#
# To build the exe, python, pygame, pymunk, and cx_Freeze have to be installed.
#
# https://cx-freeze.readthedocs.io/en/latest/distutils.html
#
 
try:
    import pymunk, pygame

    from distutils.core import setup    
    import cx_Freeze
    from modulefinder import Module
    import glob, fnmatch
    import sys, os, shutil
    import operator    
    from zipfile import ZipFile, ZIP_DEFLATED
    import zlib    
except ImportError as message:
    raise SystemExit("Unable to load module. %s" % message)

setup = cx_Freeze.setup

def update_and_get_build_number():
    #Update build num
    f = open("buildnum", "r+")
    bnum = int(f.read()) + 1

    f.seek(0)
    f.write(str(bnum))
    f.close()

    from SBA_Serv import __version__

    return __version__
 
class BuildExe:
    def __init__(self):
        self.dist_dir = 'dist'

        #pygamedir = os.path.split(pygame.base.__file__)[0]
        #pygame_default_font = os.path.join(pygamedir, pygame.font.get_default_font())

        #Extra files/dirs copied to game
        pymunk_dir = os.path.dirname(pymunk.__file__)

        self.extra_files = [
            ("GUI/", "GUI/"),
            (os.path.join(pymunk_dir, 'chipmunk.dll'), 'chipmunk.dll'),
            ("freesansbold.ttf", '.'),
            ("buildnum", '.'),
            ("../changelog.md", '.'),
            ("../README.md", '.'),
            ("../LICENSE", '.'),
            ("../COPYING", '.'),
        ]
        config = glob.glob("*.cfg")
        for f in config:
            self.extra_files.append((f, '.'))
        print(self.extra_files)
 
        #python scripts (strings) to be included, separated by a comma
        games = glob.glob('Game\\*.py')
        games.remove('Game\\__init__.py')
        games.remove('Game\\Game.py')
        games.remove('Game\\Players.py')
        games.remove('Game\\Utils.py')
        games.remove('Game\\Tournaments.py')
        self.extra_scripts = ",".join(games).replace("\\", ".").replace(".py", "")
        print(self.extra_scripts)
 
    ## Code from DistUtils tutorial at http://wiki.python.org/moin/Distutils/Tutorial
    ## Originally borrowed from wxPython's setup and config files
    def opj(self, *args):
        path = os.path.join(*args)
        return os.path.normpath(path)
 
    def find_data_files(self, srcdir, *wildcards, **kw):
        # get a list of all files under the srcdir matching wildcards,
        # returned in a format to be used for install_data
        def walk_helper(arg, dirname, files):
            if '.svn' in dirname:
                return
            names = []
            lst, wildcards = arg
            for wc in wildcards:
                wc_name = self.opj(dirname, wc)
                for f in files:
                    filename = self.opj(dirname, f)
 
                    if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                        names.append(filename)
            if names:
                lst.append( (dirname, names ) )
 
        file_list = []
        recursive = kw.get('recursive', True)
        if recursive:
            os.walk(srcdir, walk_helper, (file_list, wildcards))
        else:
            walk_helper((file_list, wildcards),
                        srcdir,
                        [os.path.basename(f) for f in glob.glob(self.opj(srcdir, '*'))])
        return file_list
 
    def run(self):
        if os.path.isdir(self.dist_dir): #Erase previous destination dir
            shutil.rmtree(self.dist_dir)
        
        # Dependencies are automatically detected, but it might need fine tuning.
        build_exe_options = {
            "build_exe": self.dist_dir,
            "packages": ["pygame", "pymunk", "ctypes"], 
            "includes": self.extra_scripts,
            "excludes": ['ssl', '_ssl', 'tcl', 'tkinter', 'numpy', 'distutils', 'email'],
            "bin_excludes": ['CRYPT32.dll'],
            "include_files": self.extra_files
        }

        executables = [cx_Freeze.Executable(
                script="SBA_Serv.py",
                #icon="GUI/Graphics/icon.png",
                copyright="Copyright (c) 2012-2020 Mikeware"
            )]

        cx_Freeze.setup(
            name = "Space Battle Arena",
            description = "Space Battle Arena Programming Game",
            version = update_and_get_build_number(),
            url = "http://battlearena.mikeware.com/",
            author = "Michael A. Hawker",
            author_email = "questions@mikeware.com",
            license = "GPLv2",

            requires = [
                "pygame (==1.9.6)",
                "pymunk (==5.6.0)"
            ],

            options = {
                "build_exe": build_exe_options
            },

            executables = executables
        )
        
        if os.path.isdir('build'): #Clean up build dir
            shutil.rmtree('build')
 
if __name__ == '__main__':
    if operator.lt(len(sys.argv), 2):
        sys.argv.append('build')

    BuildExe().run() #Run generation
    #raw_input("Press any key to continue") #Pause to let user see that things ends 

    # package up the result and drop in final output folder
    ziparchive = ZipFile('..\\bin\\SBAserver.zip', 'w')
    path = os.getcwd()
    os.chdir('dist')
    for root, dir, files in os.walk('.'):
        for file in files:
            ziparchive.write(os.path.join(root, file), compress_type=ZIP_DEFLATED)    
    ziparchive.close()
    os.chdir(path)
