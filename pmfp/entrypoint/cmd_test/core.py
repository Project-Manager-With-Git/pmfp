"""ppm test命令的处理."""
from ..core import ppm, EntryPoint


ppm_test = EntryPoint("test")
ppm_test.__doc__ = """ppm test <subcmd>

    ppm test 的子命令有:

    unittest            执行代码单元测试
    benchmark           执行代码性能测试
    static              执行代码静态类型检验
    """
ppm_test.prog = "ppm test"
ppm_test.epilog = ''
ppm_test.description = 'test相关的子命令'
ppm.regist_subcmd(ppm_test)
