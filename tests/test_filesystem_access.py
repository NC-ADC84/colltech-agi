import os
import tempfile
from pathlib import Path

from colltech_agi_enhanced_backend import FileSystemAccess


def test_list_directory_success_and_error(tmp_path):
    fs = FileSystemAccess(allowed_directories=[str(tmp_path)])
    # create files
    (tmp_path / 'a.txt').write_text('hello')

    res = fs.list_directory(str(tmp_path))
    assert isinstance(res.get('success'), bool)
    assert res['success'] is True
    assert 'items' in res

    # non-existent directory
    res2 = fs.list_directory(str(tmp_path / 'nope'))
    assert res2.get('success') is False


def test_read_write_delete_file(tmp_path):
    fs = FileSystemAccess(allowed_directories=[str(tmp_path)])
    filep = tmp_path / 'file.txt'

    # write
    w = fs.write_file(str(filep), 'content')
    assert w.get('success') is True
    assert filep.exists()

    # read
    r = fs.read_file(str(filep))
    assert r.get('success') is True
    assert 'content' in r

    # delete
    d = fs.delete_file(str(filep))
    assert d.get('success') is True
    assert not filep.exists()


def test_access_denied(tmp_path):
    # allowed folder is different
    other = tempfile.TemporaryDirectory()
    try:
        fs = FileSystemAccess(allowed_directories=[str(tmp_path)])
        res = fs.read_file(os.path.join(str(other.name), 'nope.txt'))
        assert res.get('success') is False
    finally:
        other.cleanup()
