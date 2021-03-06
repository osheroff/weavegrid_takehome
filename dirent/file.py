from dirent.base import Base

class File(Base):
    def json(self, include_contents, recurse):
        j = super().json(include_contents)
        j['type'] = 'file'
        j['size'] = self.stat_result.st_size
        if include_contents:
            with open(self.full_path, "r") as file:
                j['contents'] = file.read()

        return j




