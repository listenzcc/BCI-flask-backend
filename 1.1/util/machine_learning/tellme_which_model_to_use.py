import yaml


def tellme(label, project_name):
    with open('util/machine_learning/model_label_map.yaml', 'r', encoding='utf-8') as f:
        model_label_map = yaml.safe_load(f)
    try:

        if project_name not in model_label_map.keys():
            raise ValueError(f"未知项目名称: {project_name}")
        else:
            if label not in model_label_map.get(project_name).keys():
                raise ValueError(f"输入label:{label}与模型:"+project_name+"不匹配!" +
                                 project_name+f"对应label为{model_label_map.get(project_name).keys()}")
            return model_label_map.get(project_name).get(label)

    except Exception as e:
        print("获取模型名称失败:", str(e))


if __name__ == '__main__':

    print(tellme(1, '星驰脑力'))
    print(tellme(1, '专注训练'))
