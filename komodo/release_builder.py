import sys
from komodo import load_yaml
from komodo import write_to_file
from argparse import ArgumentParser
from komodo import release_cleanup
from queue import Queue
from collections import OrderedDict


def version_dependencies(soft_name, version, releases, repository):
    dependencies = {
        dependency: [] for dependency in repository[soft_name][version]["depends"]
    }
    for dependency in dependencies:
        for release in releases:
            if not (soft_name in release and release[soft_name] == version):
                continue

            if not dependency in release:
                continue

            if release[dependency] not in dependencies[dependency]:
                dependencies[dependency].append(release[dependency])

    return dependencies


def fix_all_dependencies(releases, repository):
    for soft_name in repository:
        for version in repository[soft_name]:
            if "depends" not in repository[soft_name][version]:
                continue
            deps = version_dependencies(soft_name, version, releases, repository)

            repository[soft_name][version]["depends"] = deps


def add_all_dependencies(requirements, repository):

    remaining = Queue()

    for soft_name, version in requirements.items():
        remaining.put((soft_name, version))
    result = {}
    while not remaining.empty():
        soft_name, version = remaining.get()

        # if soft_name in result and version not in result[soft_name]:
        #    raise ValueError("Incompatible versions", soft_name, version)

        result[soft_name] = version

        if "depends" not in repository[soft_name][version]:
            continue

        dependencies = repository[soft_name][version]["depends"]
        for dep, version in dependencies.items():
            if dep in requirements:
                remaining.put((dep, requirements[dep]))
            else:
                remaining.put((dep, version[0]))

    return result


if __name__ == "__main__":
    parser = ArgumentParser(description="Tidy up release and repository files.")

    parser.add_argument(
        "--repository",
        type=load_yaml,
        help="a yml file defining all libraries and their versions",
    )
    parser.add_argument(
        "--releases",
        type=release_cleanup._valid_path_or_files,
        help="list of release files or folders containing releases",
        nargs="+",
    )
    parser.add_argument(
        "--output", type=str, help="name of file to write new repository"
    )
    parser.add_argument(
        "--requirements", type=load_yaml, help="file describing required packages"
    )

    args = parser.parse_args()
    repository = args.repository
    releases = [
        load_yaml(filename) for sublist in args.releases for filename in sublist
    ]

    fix_all_dependencies(releases, repository)

    if args.output:
        write_to_file(repository, args.output)

    if args.requirements:
        result = add_all_dependencies(args.requirements, repository)
        write_to_file(result, "new_release")
