"""入口类的定义和一级入口对象."""
from schema_entry import EntryPoint


class PPM(EntryPoint):
    """ppm <subcmd> [<args>]
    ppm工具的子命令有:

        工具自身相关:
        help              展示ppm的帮助说明
        version           展示ppm的版本
        reset             将ppm工具的设置初始化
        cache             管理ppm的缓存             

        项目管理类:
        template          管理模板项目
        project           管理项目
        stack             管理项目组

        常用工具类:
        run               执行一条bash/ps1命令
        proto             管理protobuffer文件
        schema            管理json schema文件
        http              http服务相关的工具  
        test              执行测试
        env               环境初始化
        apidoc            维护api文档
        build             编译静态语言
    """
    epilog = ""
    description = '项目脚手架'


ppm = PPM()
