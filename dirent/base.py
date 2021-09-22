import os
import stat
import pdb

from pwd import getpwuid
from grp import getgrgid

class Base:
    """
    base class representing a directory entry and how to transform it into a JSON-able dictionary.
    """

    def __init__(self, base_path, relative_path, stat_result):
        self.base_path = base_path
        self.relative_path = relative_path
        self.stat_result = stat_result
        self.full_path = os.path.join(base_path, relative_path)

    def from_path(base_path, relative_path):
        """
        given a base (webserver root) path and a relative path, return a concrete instance of [Directory, File, Link].
        Returns None if the path doesn't exist or we can't handle the file type.
        """
        # late import to avoid circular imports.  is there a more python-esque way to structure this?

        from dirent.directory import Directory
        from dirent.file import File
        from dirent.link import Link

        full_path = os.path.join(base_path, relative_path)
        try:
            s = os.stat(full_path, follow_symlinks=False)
        except FileNotFoundError:
            return None

        if stat.S_ISDIR(s.st_mode):
            return Directory(base_path, relative_path, s)
        elif stat.S_ISLNK(s.st_mode):
            return Link(base_path, relative_path, s)
        elif stat.S_ISREG(s.st_mode):
            return File(base_path, relative_path, s)
        else:
            # something else, socket, etc.  skip
            return None

    def permissions(self):
        octal = oct(self.stat_result.st_mode)
        return int(octal[4:])

    # TODO, for a productized app -- investigate cost of getpwuid() call, possible cache locally
    def user(self):
        uid = self.stat_result.st_uid
        return getpwuid(uid).pw_name

    def group(self):
        gid = self.stat_result.st_gid
        return getgrgid(gid).gr_name

    def json(self, include_contents, recurse = False):
        """
        transform the directory entry into a JSON-able map.
        """
        return {
                "path": "/" + self.relative_path,
                "permissions": self.permissions(),
                "user": self.user(),
                "group": self.group()
                }






