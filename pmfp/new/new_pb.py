import shutil
from pmfp.const import  PMFP_PB_TEMP,PROJECT_HOME


def new_pb(c_name, rename,to="pbschema"):
    t_path = PROJECT_HOME.joinpath(to)
    if not t_path.exists():
        print(f"找不到目标目录{str(t_path)},新建")
        t_path.mkdir(parents=True, exist_ok=False)
    if c_name == "pb":
        c_path = PMFP_PB_TEMP.joinpath("pbschema/data.proto")
    elif c_name == "grpc":
        c_path = PMFP_PB_TEMP.joinpath("rpc-pbschema/data.proto")
    to_path = t_path.joinpath(rename+".proto")
    if to_path.exists():
        print(f"存在同名文件{rename}.proto")
        return
    else:
        shutil.copy(
            str(c_path),
            str(to_path)
        )