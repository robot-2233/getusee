from selenium.webdriver.common.by import By


def traverse(element, sniff_word):
    for child in element.find_elements(by=By.XPATH, value="./*"):
        if sniff_word in child.get_attribute('outerHTML'):
            print(len(str(child.get_attribute('outerHTML'))))
            if str(child.get_attribute('outerHTML')).count('<') - child.text.count('<') < 3:
                return child
            else:
                return traverse(child, sniff_word)


def traverse_all(element, sniff_word):
    for child in element.find_elements(by=By.XPATH, value="./*"):
        if sniff_word in child.get_attribute('outerHTML'):
            if str(child.get_attribute('outerHTML')).count('<') - child.text.count('<') < 3:
                yield child
            yield from traverse_all(child, sniff_word)


def class_server(element, sniff_classname):
    elements_list = []
    for matched_element in traverse_all(element, sniff_classname):
        source_html = matched_element.get_attribute('outerHTML')
        if f'class="{sniff_classname}"' in source_html:
            if '<input' in source_html or '<textarea' in source_html:
                elements_list.append(matched_element)
    return elements_list


def id_server(element, sniff_id):
    elements_list = []
    for matched_element in traverse_all(element, sniff_id):
        source_html = matched_element.get_attribute('outerHTML')
        if f'id="{sniff_id}"' in source_html:
            if '<input' in source_html or '<textarea' in source_html:
                elements_list.append(matched_element)
    return elements_list


def sniffer(element, something_weird):
    for child in element.find_elements(by=By.XPATH, value="./*"):
        if something_weird in child.get_attribute('outerHTML'):
            if str(child.get_attribute('outerHTML')).count('<') - child.text.count('<') < 3:
                yield child
            yield from sniffer(child, something_weird)