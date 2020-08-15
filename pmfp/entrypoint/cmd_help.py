import argparse
"""help命令的处理."""
PPM_HELP = f"""ppm <command> [<args>]
ppm {STATUS}-{VERSION}
ppm工具的子命令有:

  ppm自身信息:
   help              展示ppm的说明
   version           展示ppm的版本
  
  管理模板:
   show              展示官方的模板
   init_template     创建一个模板项目
   init_components   创建一个组件项目

  管理项目:
   init              初始化一个项目
   status            查看项目状态
   update            更新项目版本
   clean             清空一个项目
   add               新增一个组件
   rm                删除一个组件
  
  依赖管理:
   install           安装依赖
   freeze            将依赖及其版本持久化

  测试管理:
   test              执行测试

  项目分发:
   upload            将项目上传至git仓库
   release           将项目发表出去,application型的发表到docker的镜像仓库,module,package,tools型的发表到包管理仓库

  项目执行
   run               执行项目,需要在配置文件中指定入口文件
   build             将项目打包,go项目可以以`$GOARCHS,$GOOSS,`的个形式指定交叉编译的平台

  项目维护:
   doc               编译文档
  
  其他功能:
   build_pb          将pb编译为对应项目语言的文件
   md2rst            将markdown文档转成rst格式文档
   init_env          初始化执行环境
"""

PPM_HELP_HELP = f"""ppm help <subcommand>

ppm工具的子命令有:

  ppm自身信息:
   help              展示ppm的说明
   version           展示ppm的版本
  
  管理模板:
   show              展示官方的模板
   init_template     创建一个模板项目
   init_components   创建一个组件项目

  管理项目:
   init              初始化一个项目
   status            查看项目状态
   update            更新项目版本
   clean             清空一个项目
   add               新增一个组件
   rm                删除一个组件
  
  依赖管理:
   install           安装依赖
   freeze            将依赖及其版本持久化

  测试管理:
   test              执行测试

  项目分发:
   upload            将项目上传至git仓库
   release           将项目发表出去,application型的发表到docker的镜像仓库,module,package,tools型的发表到包管理仓库

  项目执行
   run               执行项目,需要在配置文件中指定入口文件
   build             将项目打包,go项目可以以`$GOARCHS,$GOOSS,`的个形式指定交叉编译的平台

  项目维护:
   doc               编译文档
  
  其他功能:
   build_pb          将pb编译为对应项目语言的文件
   md2rst            将markdown文档转成rst格式文档
   init_env          初始化执行环境


"""
def help(argv):
    parser = argparse.ArgumentParser(
        prog='ppm help',
        description='查看子命令的帮助说明',
        usage= PPM_HELP_HELP
    )
    parser.add_argument('subcmd', type=str,
                        default="DEFAULT", help="要安装的依赖名")
    parser.set_defaults(func=install_cmd)
    args = parser.parse_args(argv)
    args.func(args)