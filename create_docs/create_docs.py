import os
import sys
import re
import shutil


LOCATION = os.path.dirname(os.path.realpath(__file__))


def convert_dir_filename(dir_, tldir):
    """Returns a human readable .rst filename for the DIR doc.

    Naming convention: 
        Start doc name based on the top level dir name of the `root_dir_`
        Dir paths in filename are separated by '__'
    """
    dir_path = os.path.realpath(dir_).split('\\')
    doc_file = '__'.join(dir_path[dir_path.index(tldir):])
    return doc_file+'.rst'


def get_sql_files(dir_):
    return [f for f in os.listdir(dir_) if os.path.splitext(f)[1] == '.sql']


def process_dir(dir_, doc_dir, tldir):
    """Write all files' contents to a .rst for the DIR."""

    doc_file = convert_dir_filename(dir_, tldir)
    with open(os.path.join(doc_dir, doc_file), 'w') as w:
        files = get_sql_files(dir_)
        for f in files:
            # add title to file
            w.write(f+'\n' + ('='*len(f)) + '\n')
            # read file using regex and add only => /* <some_comments> */
            with open(os.path.join(dir_, f), 'r') as f:
                f = f.read()
                match = re.findall(r"/\*.*?\s*((?<=\n)?.*?)\s*(?:\n)?\*/", f, re.DOTALL)
                for ea in match:
                    w.write(ea)
                    w.write('\n\n')
                w.write('\n\n')


def get_doc_dir(root_dir_):
    """Remove the old "docs directory and return an empty one.

    Returns:
        A "doc directory" by it's absolute path.
    """
    doc_dir = os.path.join(root_dir_, 'docs')
    if not os.path.isdir(doc_dir):
        os.mkdir(os.path.join(root_dir_, 'docs'))
    return doc_dir


def remove_old_docs(root_dir_):
    """Remove all old documentation files from the "doc_dir"."""
    doc_dir = os.path.join(root_dir_, 'docs')
    if os.path.isdir(doc_dir):
        # Erase all files in doc_dir
        docfiles = [ f for f in os.listdir(doc_dir) if os.path.isfile(os.path.join(doc_dir,f)) ]
        for f in docfiles:
            try:
                os.remove(os.path.join(doc_dir, f))
            except WindowsError as e:
                print e, "can't find file."


def get_dirs(root_dir_):
    """Return a set() of all dirs to create documentation for.
    Ignore system dirs."""
    return {dp for dp, dn, filenames in os.walk(root_dir_)
            for f in filenames
            if os.path.split(dp)[1][0] not in ('.', '_')}


def main(root_dir_=os.path.dirname(os.path.realpath(__file__))):
    """Starts Doc output in current DIR if a DIR arg is not supplied.

    1. root_dir_: Root Directory to start retrieving documentation from.
    2. doc_dir: Documentation Directory
    3. tldir: Top level directory to start with for documentation file names
    """
    remove_old_docs(root_dir_)
    doc_dir = get_doc_dir(root_dir_)

    tldir = os.path.split(root_dir_)[1]

    dirs = get_dirs(root_dir_)

    for dir_ in dirs:
        process_dir(dir_=dir_, doc_dir=doc_dir, tldir=tldir)


if __name__ == '__main__':
    try:
        main(root_dir_=sys.argv[1])
    except IndexError:
        main()


##########
# PYTEST #
##########
"""
PYTEST
------
When running py.test current `docs Dir` will be deleted and updated 
with the test results.
    
**This is fine, as long as you remember to re-run the "Create
Documentation proceess once done running py.test.

"""
def f():
    return 3

def test_fail():
    """This test is suppose to fail!!"""
    assert f() == 4

def test_ok():
    assert f() == 3

def test_get_doc_dir(dir_=LOCATION):
    """
    Test with & without the presence of a "doc directory". 

    Remove "doc directory" when finished.
    """
    doc_dir = get_doc_dir(dir_)
    assert os.path.exists(doc_dir)
    assert doc_dir == os.path.join(LOCATION, 'docs')

    # remove file and test
    shutil.rmtree(doc_dir)
    doc_dir = get_doc_dir(dir_)
    assert os.path.exists(doc_dir)
    assert doc_dir == os.path.join(LOCATION, 'docs')

    # cleanup
    shutil.rmtree(doc_dir)
    assert os.path.exists(doc_dir) == False

def test_convert_dir_filename(dir_=LOCATION):
    tldir = os.path.split(LOCATION)[1]
    assert convert_dir_filename(dir_, tldir) == 'sql_docs.rst'

def test_get_dirs(root_dir_=LOCATION):
    dirs = get_dirs(root_dir_)
    for ea in dirs:
        assert os.path.split(ea)[1][0] not in ('.', '_')
    assert isinstance(dirs, set)

def test_get_sql_files(dir_=LOCATION):
    sql_files = get_sql_files(dir_)
    assert isinstance(sql_files, list)
    for f in sql_files:
        assert f.split('.')[-1] == 'sql'

def test_process_dir(dir_=LOCATION, doc_dir=get_doc_dir(LOCATION)):
    '''Make sure the "documentation directory" exists b/f process_dir.'''
    assert dir_
    assert doc_dir

    doc_dir = get_doc_dir(dir_)
    tldir = os.path.split(LOCATION)[1]
    process_dir(dir_, doc_dir, tldir)

    doc_dir_contents = os.listdir(doc_dir)
    assert doc_dir_contents
    assert isinstance(doc_dir_contents, list)

def test_remove_old_docs(root_dir_=LOCATION):
    doc_dir = os.path.join(root_dir_, 'docs')
    for i in range(5):
        new_file = os.path.join(doc_dir, "myfile_"+str(i)+".txt")
        with open(new_file, 'w') as w:
            w.write("some random content")
        w.close()

    remove_old_docs(root_dir_=LOCATION)
    assert [f for f in os.listdir(doc_dir)] == []