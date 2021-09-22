import pytest
import os

from dirlist import create_app

def index_path():
    return os.path.join(os.path.dirname(__file__), "test_index")

@pytest.fixture
def client():
    app = create_app(index_path(), {'TESTING': True})
    with app.test_client() as client:
        yield client


def test_list_root(client):
    r = client.get('/')
    json = r.get_json()
    assert json
    assert json['path'] == '/'
    assert json['type'] == 'directory'
    assert json['permissions'] == 755

    assert json['user']
    assert json['group']

def test_get_file(client):
    r = client.get('/plainfile')

    json = r.get_json()
    assert json
    assert json['path'] == '/plainfile'
    assert json['type'] == 'file'
    assert json['contents'] == 'hi imma file.\n'

def test_list_subdir(client):
    r = client.get('/subdir')
    json = r.get_json()
    assert json
    assert json['type'] == 'directory'
    assert json['entries']

    entry_map = {}
    for entry in json['entries']:
        entry_map[entry['path']] = entry

    assert '/subdir/linky' in entry_map
    assert entry_map['/subdir/linky']['link'] == '/subdir/plain'

    assert '/subdir/badlink' not in entry_map

    assert '/subdir/relative_link' in entry_map
    assert entry_map['/subdir/relative_link']['link'] == '/plainfile'

def test_not_exists(client):
    r = client.get("/notthere")
    assert r.status_code == 404
    assert r.get_json() == { "error": "not found" }

def test_permission_denied(client):
    path = os.path.join(index_path(), "nopermissions")

    try:
        with open(path, 'w') as file:
            pass

        os.chmod(path, 0)
        r = client.get("/nopermissions")
        assert r.status_code == 403
        assert r.get_json() == { "error": "permission denied" }
    finally:
        os.unlink(path)

def test_follow_breakout_link(client):
    r = client.get("/passwdlink")
    assert r.status_code == 403
    assert r.get_json() == { "error": "permission denied" }



### tests:
# not-exists 404s
# permission-denied 421s????
# attempt to follow symlink also perm-denies



