from dirent.base import Base
import os
import pytest

@pytest.fixture(autouse=True)

def remove_file():
    try:
        os.unlink('/tmp/test_file')
    except FileNotFoundError:
        pass

def test_build_file():
    with open('/tmp/test_file', "w+") as file:
        file.write("HIHIHI")

    link = Base.from_path('/tmp', 'test_file')

    assert type(link).__name__ == 'File'

    json = link.json(include_contents = True, recurse = False)
    assert json
    assert json['contents'] == 'HIHIHI'
    assert json['size'] == 6
