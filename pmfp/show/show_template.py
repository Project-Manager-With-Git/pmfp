import json
from itertools import groupby
from functools import partial
from collections.abc import Mapping
from pmfp.const import PMFP_TEMPLATES_HOME
from .find_path import find_path


def find_template_detail(name, path, depth):
    if path.suffix == ".json":
        with open(str(path)) as f:
            content = json.load(f)
        if content["name"] == name:
            return True
        else:
            return False
    else:
        return False


def show(name=None, language=None, category=None):
    if name is None:
        def _find(path, _): return path.suffix == ".json" and path.is_file()
        if language is None:
            print("展示所有模板列表")
            result = find_path(PMFP_TEMPLATES_HOME, _find)
        else:
            if category is None:
                print(f"展示{language}的模板列表")
                p = PMFP_TEMPLATES_HOME.joinpath(language.lower())
                if p.is_dir():
                    result = find_path(p, _find)
                else:
                    print(f"找不到{language}语言对应的模板")
                    return
            else:
                print(f"展示{language}中的{category}分类的模板列表")
                p = PMFP_TEMPLATES_HOME.joinpath(language.lower()).joinpath(category.lower())
                if p.is_dir():
                    result = find_path(p, _find)
                else:
                    print(f"找不到{language}语言下{category}分类对应的模板")
                    return
        if len(result) == 0:
            print("空的模板分类")
            return
        else:
            to_show = []
            for path in result:
                result = path.parts[-3:]
                to_show.append(result)
            gp_language = groupby(sorted(to_show, key=lambda x: x[0]), key=lambda x: x[0])
            ret = []
            for i, ite in gp_language:
                print(f"=====语言:{i}========")
                gp_c = groupby(sorted(ite, key=lambda x: x[1]), key=lambda x: x[1])
                for j, jte in gp_c:
                    print(f"-----分类:{j}------")
                    for k in jte:
                        temp_name = k[-2] + "-" + k[-1].split(".")[0]
                        print(temp_name)
                        ret.append(temp_name)
            return ret

    else:
        _find = partial(find_template_detail, name)
        if language is None:
            print(f"从全局查找模板{name}")
            result = find_path(PMFP_TEMPLATES_HOME, _find)
        else:
            if category is None:
                p = PMFP_TEMPLATES_HOME.joinpath(language.lower())
                if p.is_dir():
                    result = find_path(p, _find)
                else:
                    print(f"{language}语言不存在")
                    return
            else:
                print(f"从{language}的{category}模板中查找模板{name}")
                p = PMFP_TEMPLATES_HOME.joinpath(language.lower()).joinpath(category.lower())
                if p.is_dir():
                    result = find_path(p, _find)
                else:
                    print(f"{language}语言的{category}分类不存在")
                    return
        if len(result) == 0:
            print(f"找不到对应的模板{name}")
            return
        else:
            for path in result:
                parts = "/".join(path.parts[-3:])
                with open(str(path)) as f:
                    content = json.load(f)
                print(f"-----{parts}---------------------")
                for k, v in content.items():
                    print(f"{k}:")
                    if isinstance(v, Mapping):
                        for i, j in v.items():
                            print(f'- {i}: {j}')
                    else:
                        print(f'- {v}')
            return True
