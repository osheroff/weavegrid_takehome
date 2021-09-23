from dirent.base import Base
import os
import pytest

@pytest.fixture(autouse=True)

def remove_link():
    try:
        os.unlink('/tmp/test_link')
    except FileNotFoundError:
        pass


def test_build_link():
    os.symlink('/tmp/foo', '/tmp/test_link')
    link = Base.from_path('/tmp', 'test_link')

    assert type(link).__name__ == 'Link'

    json = link.json(include_contents = False, recurse = False)
    assert json

    assert json['link'] == '/foo'

def test_link_outside_root():
    os.symlink('/usr/foo', '/tmp/test_link')
    link = Base.from_path('/tmp', 'test_link')

    json = link.json(include_contents = False, recurse = False)
    assert json is None

    with pytest.raises(PermissionError):
        # if asked to include include_contents on this, we raise a permission-denied instead
        json = link.json(include_contents = True, recurse = False)



