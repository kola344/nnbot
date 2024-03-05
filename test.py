import json

# Рекурсивная функция для добавления новой ветви в JSON
def add_branch(json_obj, keys, new_branch):
    if len(keys) == 1:
        if keys[0] not in json_obj:
            json_obj[keys[0]] = new_branch
        else:
            if isinstance(json_obj[keys[0]], dict):
                json_obj[keys[0]].update(new_branch)
            else:
                # Если элемент не является словарем, преобразуем его в словарь и добавляем новую ветвь
                json_obj[keys[0]] = {keys[0]: json_obj[keys[0]], **new_branch}
    else:
        key = keys.pop(0)
        if key not in json_obj:
            json_obj[key] = {}
        add_branch(json_obj[key], keys, new_branch)

# Ваш JSON-файл
json_data = '{"item": {"bread": {"item": "desired_value"}}, "barashik": {"bobik": {"hlebushek": {"item": "value"}}}, "barash": {"tupoy": {"item": "da"}}}'

# Преобразование JSON-строки в объект Python
data = json.loads(json_data)

# Ваш список ключей
keys = ['barashik', 'bobik', 'hlebushek']

# Новая ветвь
pred_data = data
for i in keys:
    print(pred_data)
    print(i)
    pred_data = pred_data[i]
pred_data['new_key'] = {}
new_branch = pred_data

# Добавление новой ветви через рекурсивную функцию
add_branch(data, keys, new_branch)
new_branch = {"new_key2": {}}
add_branch(data, keys, new_branch)

# Вывод обновленного JSON
print(json.dumps(data, indent=2))