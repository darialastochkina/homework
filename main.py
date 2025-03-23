import json


def file_name(file_path, city_name):
    with open(file_path) as f:
        data = json.load(f)
    v = dict(data).get(city_name)
    temp = 0
    for t in list(v.values()):
        temp += t
    result = temp / len(list(v.values()))
    with open('output.json', 'w') as f:
        json.dump({
            city_name: {
                "Average temperature": result
            }
        }
            , f)


res = file_name("temperature.json", "St. Petersburg")
print(res)
