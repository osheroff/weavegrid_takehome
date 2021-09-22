from dirent.base import Base
from os import listdir
import os

class Directory(Base):
    def json(self, include_contents):
        j = super().json(include_contents)
        j['type'] = 'directory'

        if include_contents:
            entries = []
            for entry in listdir(self.full_path):
                entries.append(entry)
            entries.sort()

            j['entries'] = []
            for entry in entries:
                de = Base.from_path(self.base_path, os.path.join(self.relative_path, entry))
                if de is not None:
                    json = de.json(include_contents = False)
                    if json is not None:
                        j['entries'].append(json)
        return j



