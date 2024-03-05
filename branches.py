import os
import json
import shutil

def get_tries():
    return [i.replace('.json', '') for i in os.listdir('inventory') if i != '.DS_Store']

class Tree:
    def __init__(self, tree_name):
        self.tree_name = tree_name
        if os.path.exists(f'inventory/{tree_name}.json'):
            self.file = open(f'inventory/{tree_name}.json', 'r', encoding='utf-8')
        else:
            self.file = open(f'inventory/{tree_name}.json', 'w', encoding='utf-8')
            json.dump({}, self.file)
            self.file = open(f'inventory/{tree_name}.json', 'r', encoding='utf-8')

    def informator(self, branch):
        #branch = ['Филлиалы', 'Корпусы', 'Кабинеты'] / []
        data = json.load(self.file)
        if branch == []:
            return [i for i in data]
        else:
            result = data
            for i in branch:
                # print(f'{branch}: {i} -> {result}')
                result = result[i]
            return [i for i in result]

    def create_branch(self, branch, branch_name):
        def add_branch(json_obj, keys, new_branch):
            if len(keys) == 1:
                if keys[0] not in json_obj:
                    json_obj[keys[0]] = new_branch
                else:
                    if isinstance(json_obj[keys[0]], dict):
                        json_obj[keys[0]].update(new_branch)
                    else:
                        json_obj[keys[0]] = {keys[0]: json_obj[keys[0]], **new_branch}
            else:
                key = keys.pop(0)
                if key not in json_obj:
                    json_obj[key] = {}
                add_branch(json_obj[key], keys, new_branch)
        data = json.load(self.file)
        if branch == []:
            with open(f'inventory/{self.tree_name}.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            data[branch_name] = {}
        else:
            keys = branch
            pred_data = data
            for i in keys:
                pred_data = pred_data[i]
            pred_data[branch_name] = {}
            new_branch = pred_data

            add_branch(data, keys, new_branch)

        self.file.close()
        with open(f'inventory/{self.tree_name}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)
        self.file = open(f'inventory/{self.tree_name}.json', 'r', encoding='utf-8')
    def del_tree(self):
        self.file.close()
        if not os.path.exists(f'Temp'):
            os.mkdir('Temp')
        shutil.move(f'inventory/{self.tree_name}.json', 'Temp')
        shutil.rmtree('Temp')


