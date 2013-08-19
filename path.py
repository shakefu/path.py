"""
Path
====

An object representing a path to a file or directory.

Copyright Notice
----------------

This file modified and maintained by Jacob Alheid ``jacob.alheid@gmail.com``.

Based on the `path.py` project.

Original copyright 2010 Mikhail Gusarov ``dottedmag@dottedmag.net``.

.. rubric:: Original author
    * Jason Orendorff ``jason.orendorff@gmail.com``

.. rubric:: Contributors
    * Mikhail Gusarov ``dottedmag@dottedmag.net``
    * Marc Abramowitz ``marc@marc-abramowitz.com``
    * Jason R. Coombs ``jaraco@jaraco.com``
    * Jason Chu ``jchu@xentac.net``
    * Vojislav Stojkovic ``vstojkovic@syntertainment.com``

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
from __future__ import generators

import os
import glob
import fnmatch

try:
    import win32security
except ImportError:
    pass

try:
    import pwd
except ImportError:
    pass

__version__ = '2.4.1'
__all__ = ['path']


class path(unicode):
    """ Represents a filesystem path.

    For documentation on individual methods, consult their
    counterparts in os.path.
    """
    def __init__(self, other):
        super(path, self).__init__(self, other)
        if not isinstance(other, basestring):
            raise TypeError("path must be a string")

    module = os.path
    "The path module to use for path operations."

    def open(self, *args, **kwargs):
        """ Return an :py:func:`open` file object. All arguments are passed to
        the open function. """
        return open(self, *args, **kwargs)

    # Magic Methods
    ###############
    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, super(path, self).__repr__())

    def __add__(self, more):
        """
        Adding a path and a string returns a new path object.

        >>> path('/tmp/') + 'spam'
        path(u'tmp/spam')
        >>> path('/tmp/spam') + 'alot'
        path(u'/tmp/spamalot')

        """
        try:
            return self.__class__(super(path, self).__add__(more))
        except TypeError:  # Python bug
            return NotImplemented

    def __radd__(self, other):
        if not isinstance(other, basestring):
            return NotImplemented
        return self.__class__(other.__add__(self))

    def __div__(self, other):
        """
        The division, "/", operator joins two paths or a path to a string and
        adds a separator if necessary. This is the same as using
        :func:`os.path.join`.

        >>> path('/tmp') / 'spam'
        path(u'/tmp/spam')
        >>> path('/tmp/') / 'spamalot'
        path(u'/tmp/spamalot')
        >>> path('/tmp/') / '/spamalot'
        path(u'/spamalot')
        >>> path('/tmp/') / 'spam' / 'alot'
        path(u'/tmp/spam/alot')

        """
        return self.__class__(self.module.join(self, other))

    __truediv__ = __div__  # Make the / operator work with true division

    # Context manager methods
    #########################
    def __enter__(self):
        self._old_dir = self.getcwd()
        os.chdir(self)

    def __exit__(self, *_):
        os.chdir(self._old_dir)

    def getcwd(cls):
        """ Return the current working directory as a path object. """
        return cls(os.getcwdu())
    getcwd = classmethod(getcwd)

    # Path string methods
    #####################
    def abspath(self):
        """ Return this path as an absolute path. """
        return self.__class__(self.module.abspath(self))

    def normcase(self):
        """ Return this path with normalized case. Has no effect under Posix.
        """
        return self.__class__(self.module.normcase(self))

    def normpath(self):
        """ Return this path normalized, eliminating double slashes, etc. """
        return self.__class__(self.module.normpath(self))

    def realpath(self):
        """ Return the canonical path of this path, eliminating any symbolic
        links encountered in the path. """
        return self.__class__(self.module.realpath(self))

    def expanduser(self):
        """ Return this path with expanded ~ and ~user constructions. If user
        or $HOME is unknown, do nothing.  """
        return self.__class__(self.module.expanduser(self))

    def expandvars(self):
        """ Return this path with expanded shell variables of the form $var and
        ${var}. Unknown variables are left unchanged. """
        return self.__class__(self.module.expandvars(self))

    def dirname(self):
        """ Return the directory component of this path. """
        return self.__class__(self.module.dirname(self))

    def basename(self):
        """ Return the final component of this path. """
        return self.__class__(self.module.basename(self))

    def expand(self):
        """ Return this path with expanded ~user and $var, and normalized
        slashes, dots, etc. """
        return self.expandvars().expanduser().normpath()

    def splitpath(self):
        """
        Return a 2-tuple containing the parent path and name of this file or
        directory.

        >>> path('/tmp/spam/path.py').splitpath()
        path('/tmp/spam/path.py').splitpath()
        >>> path('path.py').splitpath()
        (path(u''), u'path.py')

        """
        parent, child = self.module.split(self)
        return self.__class__(parent), child

    def relpath(self):
        """
        Return this path as a relative path to the current working directory.

        """
        cwd = self.__class__(os.getcwd())
        return cwd.relpathto(self)

    # Methods for getting information about this path
    #################################################
    def isabs(self):
        """ Return ``True`` if this is an absolute path. """
        return self.module.isabs(self)

    def exists(self):
        """ Return ``True`` if this path exists. """
        return self.module.exists(self)

    def isdir(self):
        """ Return ``True`` if this path is a directory. """
        return self.module.isdir(self)

    def isfile(self):
        """ Return ``True`` if this path is a file. """
        return self.module.isfile(self)

    def islink(self):
        """ Return ``True`` if this path is a link. """
        return self.module.islink(self)

    def ismount(self):
        """ Return ``True`` if this path is a mount. """
        return self.module.ismount(self)

    def getatime(self):
        """ Return this path's access time. """
        return self.module.getatime(self)

    def getmtime(self):
        """ Return this path's last modified time. """
        return self.module.getmtime(self)

    def getctime(self):
        """ Return this path's creation time. """
        return self.module.getctime(self)

    def getsize(self):
        """ Return the size of this file in bytes. """
        return self.module.getsize(self)

    def stat(self):
        """ Perform a stat() system call on this path. """
        return os.stat(self)

    def lstat(self):
        """ Like path.stat(), but do not follow symbolic links. """
        return os.lstat(self)

    def __get_owner_windows(self):
        """
        Return the name of the owner of this file or directory. Follow
        symbolic links.

        Return a name of the form u'DOMAIN\\User Name'; may be a group.

        """
        desc = win32security.GetFileSecurity(
            self, win32security.OWNER_SECURITY_INFORMATION)
        sid = desc.GetSecurityDescriptorOwner()
        account, domain, typecode = win32security.LookupAccountSid(None, sid)
        return domain + u'\\' + account

    def __get_owner_unix(self):
        """
        Return the name of the owner of this file or directory. Follow
        symbolic links.

        """
        st = self.stat()
        return pwd.getpwuid(st.st_uid).pw_name

    def __get_owner_not_implemented(self):
        raise NotImplementedError("Ownership not available on this platform.")

    if 'win32security' in globals():
        get_owner = __get_owner_windows
    elif 'pwd' in globals():
        get_owner = __get_owner_unix
    else:
        get_owner = __get_owner_not_implemented

    # Methods for listing and searching paths
    #########################################
    def listdir(self, pattern=None):
        """
        Return a list of items in this directory.

        :param pattern: A file pattern to match
        :type pattern: str

        Use :meth:`files` or :meth:`dirs` instead if you want a listing of just
        files or just subdirectories.

        The elements of the list are path objects.

        With the optional `pattern` argument, this only lists items whose names
        match the given pattern.

        """
        names = os.listdir(self)
        if pattern is not None:
            names = fnmatch.filter(names, pattern)
        return [self / child for child in names]

    ls = property(listdir, None, None,
        """ Same as :meth:`listdir`. """)

    def dirs(self, pattern=None):
        """
        Return a list of this directory's subdirectories.

        :param pattern: A file pattern to match
        :type pattern: str

        The elements of the list are path objects. This does not walk
        recursively into subdirectories.

        With the optional `pattern` argument, this only lists directories whose
        names match the given pattern.  For example, ``d.dirs('build-*')``.

        """
        return [p for p in self.listdir(pattern) if p.isdir()]

    def files(self, pattern=None):
        """
        Return a list of the files in this directory.

        :param pattern: A file pattern to match
        :type pattern: str

        The elements of the list are path objects. This does not walk into
        subdirectories.

        With the optional `pattern` argument, this only lists files whose names
        match the given pattern.  For example, ``d.files('*.pyc')``.

        """
        return [p for p in self.listdir(pattern) if p.isfile()]

    def glob(self, pattern):
        """
        Return a list of path objects that match the pattern.

        :param pattern: a path relative to this directory, with wildcards.
        :type pattern: str

        For example, ``path('/users').glob('*/bin/*')`` returns a list of all
        the files users have in their bin directories.

        """
        cls = self.__class__
        return [cls(s) for s in glob.glob(self / pattern)]

    # Convenience properties
    ########################
    owner = property(
        get_owner, None, None,
        """ Name of the owner of this file or directory. """)

    parent = property(dirname, None, None,
        """ This path's parent directory, as a new path object.

        >>> path('/usr/local/lib/libpython.so').parent
        path('/usr/local/lib')

        """)

    name = property(basename, None, None,
        """ The name of this file or directory without the full path.

        >>> path('/usr/local/lib/libpython.so').name
        u'libpython.so'

        """)

    ext = property(lambda self: self.module.splitext(self)[1], None, None,
        """ This path's file extension.

        >>> path('path.py').ext
        u'.py'

        """)

    atime = property(
        getatime, None, None,
        """ Last access time of the file. """)

    mtime = property(
        getmtime, None, None,
        """ Last-modified time of the file. """)

    ctime = property(
        getctime, None, None,
        """ Creation time of the file. """)

    size = property(
        getsize, None, None,
        """ Size of the file, in bytes. """)

    # Methods which modify either files or directories
    ##################################################
    def utime(self, times):
        """
        Set the access and modified times of this file.

        `times` should be a 2-tuple of unix timestamps, which set the access
        and modified times for this file.

        :param times: A 2-tuple containing (atime, mtime)
        :type times: tuple

        """
        os.utime(self, times)
        return self

    def chmod(self, mode):
        """
        Change the permissions of this path.

        The `mode` argument should be composed from the constants in the
        :py:mod:`stat` module.

        :param mode: Mode for the file
        :type mode: int

        """
        os.chmod(self, mode)
        return self

    def chown(self, uid=-1, gid=-1):
        """
        Change ownership of this path.

        Does nothing if the OS does not support `chown`.

        :param uid: Numeric user id
        :param gid: Numeric group id
        :type uid: int
        :type gid: int

        """
        if hasattr(os, 'chown'):
            os.chown(self, uid, gid)
        return self

    def rename(self, new):
        """
        Rename this path and return the new path name.

        :param new: New path name
        :type new: str

        """
        os.rename(self, new)
        return self.__class__(new)

    # Methods which modify files
    ############################
    def touch(self):
        """ Set the access/modified times of this file to the current time.
        Create the file if it does not exist.  """
        fd = os.open(self, os.O_WRONLY | os.O_CREAT, 0666)
        os.close(fd)
        os.utime(self, None)
        return self

    def remove(self):
        """ Remove this file. """
        os.remove(self)
        return self

    def unlink(self):
        """ Unlink this file. """
        os.unlink(self)
        return self

    # Methods which modify directories
    ##################################
    def rmdir(self):
        """ Remove this directory. """
        os.rmdir(self)
        return self

