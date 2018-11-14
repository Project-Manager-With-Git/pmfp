import json
from itertools import groupby
from functools import partial
from collections.abc import Mapping
from pmfp.const import PMFP_COMPONENTS_HOME
from .find_path import find_path

EXCEPT = ["doc","env","protobuf","readme","setup","test"]

def show(name=None, language=None, category=None):
    if name is None:
        if language is None:
            def _find(path, depth):
                if depth == 2:
                    result = True
                else:
                    result = False
                for i in EXCEPT:
                    if "/"+i+"/" in str(path):
                        result = False
                return result
            print("展示所有组件列表")
            result = find_path(PMFP_COMPONENTS_HOME, _find, max_depth=3)
        else:
            if category is None:
                print(f"展示{language}的组件列表")

                def _find(path, depth): return depth == 1
                p = PMFP_COMPONENTS_HOME.joinpath(language.lower())
                if p.is_dir():
                    result = find_path(p, _find, max_depth=3)
                else:
                    print(f"找不到{language}语言对应的组件")
                    return
            else:
                print(f"展示{language}中的{category}分类的组件列表")

                def _find(path, depth): return depth == 0
                p = PMFP_COMPONENTS_HOME.joinpath(language.lower()).joinpath(category.lower())
                if p.is_dir():
                    result = find_path(p, _find, max_depth=3)
                else:
                    print(f"找不到{language}语言下{category}分类对应的组件")
                    return
        if len(result) == 0:
            print("空的组件分类")
            return
        else:
            to_show = []
            for path in result:
                result = path.parts[-3:]
                to_show.append(result)
            gp_language = groupby(sorted(to_show, key=lambda x: x[0]), key=lambda x: x[0])
            for i, ite in gp_language:
                print(f"=====语言:{i}========")
                gp_c = groupby(sorted(ite, key=lambda x: x[1]), key=lambda x: x[1])
                for j, jte in gp_c:
                    print(f"-----分类:{j}------")
                    for k in jte:
                        #print(k[-2] + "-" + k[-1].split(".")[0])
                        print(k[-2] + "-" + k[-1])
            return True

    else:
        if language is None:
            print(f"从全局查找组件{name}")

            def _find(path, depth): return path.name == name and depth == 2
            result = find_path(PMFP_COMPONENTS_HOME, _find, 3)
        else:
            if category is None:
                print(f"从{language}的组件中查找模板{name}")

                def _find(path, depth): return path.name == name and depth == 1
                p = PMFP_COMPONENTS_HOME.joinpath(language.lower())
                if p.is_dir():
                    result = find_path(p, _find, 3)
                else:
                    print(f"{language}语言不存在")
                    return
            else:
                print(f"从{language}的{category}模板中查找模板{name}")

                def _find(path, depth): return path.name == name and depth == 0
                p = PMFP_COMPONENTS_HOME.joinpath(language.lower()).joinpath(category.lower())
                if p.is_dir():
                    result = find_path(p, _find, 3)
                else:
                    print(f"{language}语言的{category}分类不存在")
                    return
        if len(result) == 0:
            print(f"找不到对应的组件{name}")
            return
        else:
            print(f"符合条件的组件有")
            to_show = []
            for path in result:
                result = path.parts[-3:]
                to_show.append(result)
            gp_language = groupby(sorted(to_show, key=lambda x: x[0]), key=lambda x: x[0])
            for i, ite in gp_language:
                print(f"=====语言:{i}========")
                gp_c = groupby(sorted(ite, key=lambda x: x[1]), key=lambda x: x[1])
                for j, jte in gp_c:
                    print(f"-----分类:{j}------")
                    for k in jte:
                        #print(k[-2] + "-" + k[-1].split(".")[0])
                        print(k[-2] + "-" + k[-1])
            return True
