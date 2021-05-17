import warnings
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
from pmfp.utils.run_command_utils import run


def upx_process(target: str, cwd: Path) -> None:
    command = f"upx --best --lzma -o {target}_upx {target}"
    run(command, cwd=cwd, visible=True, fail_exit=True)


def addToZip(zf: ZipFile, cwd: Path, path: Path, output_dir: Path) -> None:
    zippath = path.relative_to(cwd).as_posix()
    if path.is_file() and not path.name.startswith("."):
        zf.write(path, zippath, ZIP_DEFLATED)
    elif path.is_dir() and not path.name.startswith("."):
        if zippath:
            zf.write(path, zippath)
        for p in path.iterdir():
            if p.resolve().as_posix() != output_dir.resolve().as_posix():
                addToZip(zf, cwd, p, output_dir)


def zip_pack(code: str, output_dir: Path, cwd: Path, project_name: str) -> None:
    codep = cwd.joinpath(code)
    if not codep.exists():
        warnings.warn(f"源码目录{codep}不存在")
    with ZipFile(output_dir.joinpath(f"{project_name}.zip"), 'w') as myzip:
        addToZip(myzip, cwd, codep, output_dir)
