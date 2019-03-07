import github
import xml.etree.ElementTree as ET

from os.path import join, basename, splitext

REPO_NAME = "github-webhook-handler-test"
ROOT_REPO_PATH = join("/tmp/", REPO_NAME)
ANALYTICS_ARTIFACTS_DIR = join(ROOT_REPO_PATH, "wix-bi-dev")
token = 'ac7c4b90dd28663f64fda583902294c849a26659'


def update_modules_list(xml_struct, modules_list):
    xml_str = ET.fromstring(xml_conf_raw_data.decode('utf-8'))
    ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")
    modules = xml_str.find('{http://maven.apache.org/POM/4.0.0}modules')
    for mod in modules_list:
        xml_el = ET.Element(mod)
        xml_el.tag = 'module'
        xml_el.text = mod
        modules.append(xml_el)
    return ET.tostring(xml_str)


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
        names.append(splitext(basename(m))[0])
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


def update_file_in_repo(content):
    repo = g.get_user().get_repo(REPO_NAME)
    contents = repo.get_contents("/wix-bi-dev/pom.xml")
    repo.update_file(contents.path, "Update modules", content, sha=contents.sha, branch='master')


if __name__ == "__main__":
    g = github.Github(token)

    repo = g.get_user().get_repo(REPO_NAME)
    file = repo.get_file_contents("/wix-bi-dev/pom.xml")
    xml_conf_raw_data = file.decoded_content
    defined_deps = set(find_xml_modules(xml_conf_raw_data))
    print('defined modules in xml conf:', defined_deps)
    modules_w_configs = set(get_all_content_recursively())
    print('modules_w_configs:', modules_w_configs)
    diff = modules_w_configs.difference(defined_deps)
    print('diff', diff)
    updated_xml = update_modules_list(xml_conf_raw_data, diff)
    update_file_in_repo(updated_xml)
