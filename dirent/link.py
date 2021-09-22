from dirent.base import Base
from os import readlink
import os.path

import pdb


class Link(Base):
    def json(self, include_contents, recurse):
        j = super().json(include_contents, recurse)
        j['type'] = 'link'

        # resolve link
        l = readlink(self.full_path)
        if l[0] != '/':
            l = os.path.join(os.path.dirname(self.full_path), l)

        l = os.path.abspath(l)

        if l.startswith(self.base_path):
            j['link'] = l[len(self.base_path):]
            return j
        else:
            # outside our immediate file system.  if it's in a directory,
            # we will simply remove it from the listing.  if we're being asked to show contents,
            # we want to return 403.
            if include_contents:
                raise PermissionError("Asked to follow symlink outside root")
            else:
                return None




