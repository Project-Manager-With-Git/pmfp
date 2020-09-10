"""ppm apidoc命令的处理."""
from ..core import ppm, EntryPoint


ppm_apidoc = EntryPoint("apidoc")
ppm_apidoc.__doc__ = """ppm apidoc <subcmd>

    ppm apidoc 的子命令有:

    new             为项目创建一个api文档
    update          更新api文档
    newlocale       新增小语种支持
    build           编译文档源文件为html静态页面
    """
ppm_apidoc.prog = "ppm apidoc"
ppm_apidoc.epilog = ''
ppm_apidoc.description = 'apidoc相关的子命令'
ppm.regist_subcmd(ppm_apidoc)
