import os
from komodo import release_builder
from komodo import write_to_file
from tests import _get_test_root, _load_yaml


def test_version_dependencies():
    files = [
        os.path.join(_get_test_root(), "data/test_releases/2020.01.a1-py27.yml"),
        os.path.join(_get_test_root(), "data/test_releases/2020.01.a1-py36.yml"),
    ]
    releases = [_load_yaml(f) for f in files]
    repository = _load_yaml(os.path.join(_get_test_root(), "data/test_repository.yml"))
    deps = release_builder.version_dependencies('lib2', '2.3.4', releases, repository)
    assert deps == {'lib1' : ['1.2.3']}
    

def test_version_all():
    files = [
        os.path.join(_get_test_root(), "data/test_releases/2020.01.a1-py27.yml"),
        os.path.join(_get_test_root(), "data/test_releases/2020.01.a1-py36.yml"),
    ]
    releases = [_load_yaml(f) for f in files]
    repository = _load_yaml(os.path.join(_get_test_root(), "data/test_repository.yml"))

    release_builder.fix_all_dependencies(releases, repository)
    write_to_file(repository, "test.yml")
