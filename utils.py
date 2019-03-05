import git
import os
from glob import glob


REPO_NAME = "github-webhook-handler"
ROOT_REPO_PATH = os.path.join("/tmp/dir/github-webhook-handler", REPO_NAME)
ANALYTICS_ARTIFACTS_DIR = os.path.join(ROOT_REPO_PATH, "wix-bi-dev")


def clone_repo():
    repo_dir = "/tmp/dir/github-webhook-handler"
    print('clonning repo')
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
    git.Git(repo_dir).clone(f"git@github.com:remm/{REPO_NAME}.git")


def find_main_pom_xml():
    if os.path.exists(os.path.join(ANALYTICS_ARTIFACTS_DIR, 'pom.xml')):
        return os.path.join(ANALYTICS_ARTIFACTS_DIR, 'pom.xml')


def find_all_dependencies():
    all_deps = []
    deps = [d for d in os.listdir(ANALYTICS_ARTIFACTS_DIR)]

    for dep in deps:
        if glob(os.path.join(ANALYTICS_ARTIFACTS_DIR, dep, '*.params')):
            all_deps.append(dep)
    print('find_all_dependencies: deps', all_deps)
    return all_deps


def check_deps_from_main_pom():
    import xml.etree.ElementTree as ET

    project_deps = find_all_dependencies()
    xml = '/tmp/dir/github-webhook-handler/github-webhook-handler/wix-bi-dev/pom.xml'
    tree = ET.parse(xml)
    root = tree.getroot()
    pom_dependencies = root[5]
    print(root[5].attrib)
    if len(project_deps) != len(pom_dependencies):
        print(type(root[5]))
    else:
        print('deps are correct')
    # for pd in pom_dependencies:
    #     print(pd)


def update_main_pom_with_dep():
    pass

