import datetime
import os
import json
import xml.etree.ElementTree as ET

def a_decorator_passing_arguments(file_path):
    def decor(function_to_decorate):
        def a_wrapper_accepting_arguments(*args, **kwargs):
            ret_val = function_to_decorate(*args, **kwargs)
            with open(file_path, 'r', encoding = 'utf-8') as f:
                data = json.load(f)

            data.append({'Description': function_to_decorate.__doc__,
                         'Args': args, 'Kwargs': kwargs,
                         'Function name': function_to_decorate.__name__,
                         'result': ret_val,
                         'Current time': str(datetime.datetime.now())})
            with open(file_path, 'w', encoding = 'utf-8') as f:
                json.dump(data, f, ensure_ascii = False, indent = 2)
                f.write('\n')
            return ret_val
        return a_wrapper_accepting_arguments
    return decor


file_path = os.path.join(os.getcwd(), 'log.json')
@a_decorator_passing_arguments(file_path)
def print_sorted_data(data_dict, count):
    """Функция получает список слов и частоту их повторения и выводет первые N слов"""
    ret_val = []
    data_list = list(data_dict.items())
    data_list.sort(key=lambda i: i[1], reverse=True)
    for i in range(count):
        ret_val.append({'Место': i+1, 'Слово': data_list[i][0], 'Количество повторений': data_list[i][1]})
    return ret_val

with open('log.json', 'w', encoding = 'utf-8') as f:
    json.dump([], f)

# открытие json
with open('newsafr.json', encoding = 'utf-8') as f:
    data = json.load(f)
    word_dict_json= {}
    for news in data["rss"]["channel"]["items"]:
        for word in news["description"].split():
            if len(word) > 6:
                if word in word_dict_json:
                    word_dict_json[word] += 1
                else:
                    word_dict_json.setdefault(word, 1)

# открытие xml
parser = ET.XMLParser(encoding = 'utf-8')
tree = ET.parse('newsafr.xml', parser)
root = tree.getroot()
news_list = root.findall('channel/item/description')
word_dict_xml = {}
for news in news_list:
    for word in news.text.split():
        if len(word) > 6:
            if word in word_dict_xml:
                word_dict_xml[word] += 1
            else:
                word_dict_xml.setdefault(word, 1)

print_sorted_data(word_dict_json, 10)
print_sorted_data(word_dict_xml, 10)
