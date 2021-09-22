from dirent.base import Base
from os import listdir
import os

class Directory(Base):
    def json(self, include_contents, recurse = False):
        """
        transform the directory into a JSON-able map.
        If include_contents or recurse is true, add the "entries" key enumerating the directory's children
        """
        j = super().json(include_contents, recurse)
        j['type'] = 'directory'

        if include_contents or recurse:
            entries = []
            for entry in listdir(self.full_path):
                entries.append(entry)
            entries.sort()

            j['entries'] = []
            for entry in entries:
                de = Base.from_path(self.base_path, os.path.join(self.relative_path, entry))
                if de is None: # file types we don't handle can return None here
                    continue

                json = de.json(include_contents = False, recurse = recurse)
                if json is not None: # some symlinks can choose to remove themselves
                    j['entries'].append(json)
        return j



