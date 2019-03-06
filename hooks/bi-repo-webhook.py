import github
import xml.etree.ElementTree as ET

from os.path import join

REPO_NAME = "github-webhook-handler-test"
ROOT_REPO_PATH = join("/tmp/", REPO_NAME)
ANALYTICS_ARTIFACTS_DIR = join(ROOT_REPO_PATH, "wix-bi-dev")
token = '049140259575365d2299e467c4fd1be81d3696c2'


def update_modules_list(file_name, dep):
    tree = ET.parse(file_name)
    ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")
    root = tree.getroot()
    modules = root.find('{http://maven.apache.org/POM/4.0.0}modules')
    child = ET.Element(dep)
    child.tag = 'module'
    child.text = dep
    modules.append(child)
    tree.write(file_name, xml_declaration=True, encoding="utf-8")


def find_xml_modules(file_name):
    modules = []
    parsed_xml = ET.fromstring(file_name)
    for elem in parsed_xml:
        for subelem in elem.findall('./'):
            if 'module' in subelem.tag:
                modules.append(subelem.text)
    return modules


def _get_modules_names(lm):
    names = []
    for m in lm:
        names.append(m.split('/')[2].replace('.params', ''))
    return names


def get_all_content_recursively():
    option_files = []
    repo = g.get_user().get_repo("github-webhook-handler-test")
    contents = repo.get_contents("/wix-bi-dev")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            if file_content.path.endswith('.params'):
                option_files.append(file_content.path)

    return _get_modules_names(option_files)


def update_pom_xml(raw_file, modules):
    ml = list(modules)
    while ml:
        update_modules_list(raw_file, ml[0])
        ml.pop(0)


def save_content_to_file(content):
    with open("/tmp/pom.xml", "wb") as f:
        f.write(content)


def update_file_in_repo():
    with open("/tmp/pom.xml", "r") as f:
        content = f.read()

    repo = g.get_user().get_repo(REPO_NAME)
    contents = repo.get_contents("/wix-bi-dev/pom.xml")
    repo.update_file(contents.path, "Update modules", content, sha=contents.sha, branch='master')


if __name__ == "__main__":
    g = github.Github(token)

    repo = g.get_user().get_repo(REPO_NAME)
    file = repo.get_file_contents("/wix-bi-dev/pom.xml")
    xml_conf_raw_data = file.decoded_content
    save_content_to_file(xml_conf_raw_data)
    defined_deps = set(find_xml_modules(xml_conf_raw_data))
    print('defined modules in xml conf:', defined_deps)
    modules_w_configs = set(get_all_content_recursively())
    print('modules_w_configs:', modules_w_configs)
    diff = modules_w_configs.difference(defined_deps)
    print('diff', diff)
    update_pom_xml('/tmp/pom.xml', diff)
    update_file_in_repo()
