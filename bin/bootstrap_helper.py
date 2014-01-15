import os
from shutil import rmtree, copyfile
import subprocess

reset_ref = 'HEAD~4'

def symlink(name, target):
    if not os.path.islink(name):
        try:
            os.symlink(target, name)
        except AttributeError:
            from win32file import CreateSymbolicLink
            CreateSymbolicLink(name, target)
        except ImportError:
            exit('ERROR: platform does not contain support for symlinks. Windows users need to pywin32.')

def init_fabric(buildsystem, conf_file):
    fab_dir = 'fabfile'

    if os.path.islink(fab_dir):
        os.remove(fab_dir)
    elif os.path.isdir(fab_dir):
        rmtree(fab_dir)

    meta_link = os.path.join(buildsystem, 'bin', 'docs_meta.yaml')
    conf_dir_link = os.path.join(buildsystem, 'config')

    if os.path.exists(meta_link):
        os.remove(meta_link)

    if os.path.exists(conf_dir_link):
        os.remove(conf_dir_link)

    symlink('fabfile', os.path.join(buildsystem, 'fabsrc'))

    symlink('fabfile', os.path.join(buildsystem, 'fabsrc'))

    symlink(name=meta_link, target=os.path.join(os.getcwd(), conf_file))

    symlink(name=conf_dir_link, target=os.path.dirname(conf_file))

    symlink(name=os.path.join(buildsystem, 'fabsrc', 'utils'),
            target=os.path.join(os.path.abspath(buildsystem), 'utils'))

    symlink(name=os.path.join(buildsystem, 'bin', 'utils'),
            target=os.path.join(os.path.abspath(buildsystem), 'utils'))

    symlink(name=os.path.join(buildsystem, 'makecloth', 'utils'),
            target=os.path.join(os.path.abspath(buildsystem), 'utils'))

    symlink(name=os.path.join(buildsystem, 'fabsrc', 'docs_meta.py'),
            target=os.path.join(os.path.abspath(buildsystem), 'bin', 'docs_meta.py'))

    symlink(name=os.path.join(buildsystem, 'utils', 'docs_meta.py'),
            target=os.path.join(os.path.abspath(buildsystem), 'bin', 'docs_meta.py'))

def clean_buildsystem(buildsystem, output_dir):
    if os.path.islink('fabfile'):
        os.remove('fabfile')
        print('[bootstrap-clean]: removed fabfile symlink')
    import glob
    for i in glob.glob(os.path.join(output_dir, 'makefile.*')):
        os.remove(i)
        print('[bootstrap-clean]: cleaned %s' % i)

    if os.path.exists(buildsystem):
        rmtree(buildsystem)
        print('[bootstrap-clean]: purged %s' % buildsystem)

def bootstrap():
    """
    The bootstrap file calls this function. Use this as a site for future
    extension.
    """
    print('[bootstrap]: initialized fabfiles and dependencies. Regenerate buildsystem now.')

    # re/generate the makefile.meta
    makecloth_path = os.path.join(os.path.abspath(__file__).rsplit(os.path.sep, 2)[0], 'makecloth')
    cmd = 'python {0}/meta.py build/makefile.meta'.format(makecloth_path).split()
    subprocess.check_call(cmd)

    if 'primer' in os.path.split(os.getcwd()):
        bootstrap_primer()
        print('[bootstrap]: initialized "primer" project.')

def bootstrap_primer():
    os.remove(os.path.join(os.getcwd(), 'fabfile'))

    main_build = os.path.abspath(os.path.join(os.getcwd(), '..', 'build', 'primer'))
    tmp_build_dir = os.path.join(os.getcwd(), 'build-tmp')

    if not os.path.exists(main_build):
        os.makedirs(main_build)
    elif not os.path.isdir(main_build):
        raise Exception("[ERROR]: {0} is not a directory".format(main_build))

    os.rename(os.path.join(os.getcwd(), 'build'),
              tmp_build_dir)

    symlink(name='build', target=main_build)

    os.rename(os.path.join(tmp_build_dir, 'docs-tools'),
              os.path.join(os.getcwd(), 'build', 'docs-tools'))
    os.rename(os.path.join(tmp_build_dir, 'makefile.meta'),
              os.path.join(os.getcwd(), 'build', 'makefile.meta'))

    if os.path.islink(tmp_build_dir):
        os.remove(tmp_build_dir)
    elif os.path.isdir(tmp_build_dir):
        os.rmdir(tmp_build_dir)

    symlink(name='fabfile',
            target=os.path.abspath(os.path.join(main_build, '..', 'docs-tools', 'fabsrc')))

    symlink(name=os.path.join('build', 'docs-tools'),
            target=os.path.abspath(os.path.join(main_build, '..', 'docs-tools')))

def main():
    bootstrap()

if __name__ == '__main__':
    main()
