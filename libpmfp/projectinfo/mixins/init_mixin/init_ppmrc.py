

def init_ppmrc(rc: Dict[str, str], ky: str, conda: bool=False, cython=False)->int:
    if local_path.joinpath(".ppmrc").exists():
        print("already inited")
    else:
        rccontent = copy.copy(rc)
        rccontent.update(form={'form': ky})
        if conda:
            env = {'env': "conda"}
        else:
            env = {'env': "venv"}
        if cython:
            env.update(**{'compiler': "cython"})
        else:
            env.update(**{'compiler': "python"})
        rccontent.update(env=env)
        write_ppmrc(rccontent)

    return 1