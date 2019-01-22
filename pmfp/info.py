"""info.

存放pmfp的元信息.
"""
VERSION = "3.0.10"

PPM_HELP = f'''ppm <command> [<args>]
ppm {VERSION}
ppm工具的子命令有:
   show        展示已有的模板和组件

   install     安装依赖
   freeze      (python专用)将依赖保存到requirements.txt

   new         新增一个组件
   init        初始化一个项目
   clean       清空一个项目

   status      查看项目状态
   update      更新项目版本
   upload      将项目上传至git仓库

   run         执行项目,需要在配置文件中指定入口文件
   build       将项目打包
   release     将项目发表出去,app型的发表到docker的镜像仓库,module型的发表到包管理仓库
               
   test        执行测试
   doc         编译文档

   build_pb    将pb编译为对应项目语言的文件
'''