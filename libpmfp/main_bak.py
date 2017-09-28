parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command',
        help="ppm(pmfp) is a tool to manage your python,cpython,cpp,node codes")
    # init command
    init_parsers = subparsers.add_parser("init", help="init a project")
    # init python command

    init_python_parsers = init_parsers.add_parser(
        "python", aliases=["py"], help="init a python project")
    # init python web command
    init_python_web_parsers = init_python_parsers.add_parser(
        "web", aliases=["W"], help="init a python web project")
    init_python_web_parsers.add_argument(
        '-e', '--env', type=str, choices=["env", "conda"], default="env")
    init_python_web_parsers.add_argument('-t', '--template', type=str, choices=[
        "sanic", "flask",
        "sanic_api", "flask_api",
        "sanic_mvc", "flask_mvc",
        "sanic_blueprints",
        "flask_blueprints"],
        default="flask")
    init_python_web_parsers.add_argument('--without_test', action='store_false')
    init_python_web_parsers.add_argument('--without_docs', action='store_false')
    init_python_web_parsers.add_argument(
        '--without_dockerfile', action='store_false')
    init_python_web_parsers.set_defaults(func=init_python_web)

    # init python gui command
    init_python_gui_parsers = init_python_parsers.add_parser(
        "gui", aliases=["G"], help="init a python gui project")
    init_python_gui_parsers.add_argument(
        '-e', '--env', type=str, choices=["env", "conda"], default="env")
    init_python_gui_parsers.add_argument('-t', '--template', type=str, choices=[
        "tk", "tk_mvc"],
        default="tk")
    init_python_gui_parsers.add_argument('--without_test', action='store_false')
    init_python_gui_parsers.add_argument('--without_docs', action='store_false')
    init_python_gui_parsers.add_argument(
        '--without_dockerfile', action='store_false')
    init_python_gui_parsers.set_defaults(func=init_python_gui)

    # init python command-line command
    init_python_command_parsers = init_python_parsers.add_parser(
        "command-line", aliases=["command", "C"], help="init a python command-line project")
    init_python_command_parsers.add_argument(
        '-e', '--env', type=str, choices=["env", "conda"], default="env")
    init_python_command_parsers.add_argument('-t', '--template', type=str, choices=[
        "simple"],
        default="simple")
    init_python_command_parsers.add_argument(
        '--without_test', action='store_false')
    init_python_command_parsers.add_argument(
        '--without_docs', action='store_false')
    init_python_command_parsers.add_argument(
        '--without_dockerfile', action='store_false')
    init_python_command_parsers.set_defaults(func=init_python_command)

    # init python model command
    init_python_model_parsers = init_python_parsers.add_parser(
        "model", aliases=["M"], help="init a python model project")
    init_python_model_parsers.add_argument(
        '-e', '--env', type=str, choices=["env", "conda"], default="env")
    init_python_model_parsers.add_argument('-t', '--template', type=str, choices=[
        "simple"],
        default="simple")
    init_python_model_parsers.add_argument(
        '--without_test', action='store_false')
    init_python_model_parsers.add_argument(
        '--without_docs', action='store_false')
    init_python_model_parsers.add_argument(
        '--without_dockerfile', action='store_false')
    init_python_model_parsers.set_defaults(func=init_python_model)

    # init python script command
    init_python_script_parsers = init_python_parsers.add_parser(
        "script", aliases=["S"], help="init a python script")
    init_python_script_parsers.add_argument(
        '-e', '--env', type=str, choices=["env", "conda"], default="env")
    init_python_script_parsers.add_argument('-t', '--template', type=str, choices=[
        "simple"],
        default="simple")
    init_python_script_parsers.add_argument(
        '--without_test', action='store_false')
    init_python_script_parsers.add_argument(
        '--without_docs', action='store_false')
    init_python_script_parsers.add_argument(
        '--without_dockerfile', action='store_false')
    init_python_script_parsers.set_defaults(func=init_python_script)

    # init python celery command
    init_python_celery_parsers = init_python_parsers.add_parser(
        "celery", aliases=["C"], help="init a celery project")
    init_python_celery_parsers.add_argument(
        '-e', '--env', type=str, choices=["env", "conda"], default="env")
    init_python_celery_parsers.add_argument('-t', '--template', type=str, choices=[
        "simple"],
        default="simple")
    init_python_celery_parsers.add_argument(
        '--without_test', action='store_false')
    init_python_celery_parsers.add_argument(
        '--without_docs', action='store_false')
    init_python_celery_parsers.add_argument(
        '--without_dockerfile', action='store_false')
    init_python_celery_parsers.set_defaults(func=init_python_celery)


    # init cython command
    init_cython_parsers = init_parsers.add_parser(
        "cython", aliases=["cy"], help="init a cython project")

    # init cython command-line command
    init_cython_command_parsers = init_cython_parsers.add_parser(
        "command-line", aliases=["command", "C"], help="init a cython command-line project")
    init_cython_command_parsers.add_argument(
        '-e', '--env', type=str, choices=["env", "conda"], default="env")
    init_cython_command_parsers.add_argument('-t', '--template', type=str, choices=[
        "simple","wrap","pure"],
        default="simple")
    init_cython_command_parsers.add_argument(
        '--without_test', action='store_false')
    init_cython_command_parsers.add_argument(
        '--without_docs', action='store_false')
    init_cython_command_parsers.add_argument(
        '--without_dockerfile', action='store_false')
    init_cython_command_parsers.set_defaults(func=init_cython_command)

    # init cython model command
    init_cython_model_parsers = init_cython_parsers.add_parser(
        "model", aliases=["M"], help="init a python model project")
    init_cython_model_parsers.add_argument(
        '-e', '--env', type=str, choices=["env", "conda"], default="env")
    init_cython_model_parsers.add_argument('-t', '--template', type=str, choices=[
        "simple","wrap","pure"],
        default="simple")
    init_cython_model_parsers.add_argument(
        '--without_test', action='store_false')
    init_cython_model_parsers.add_argument(
        '--without_docs', action='store_false')
    init_cython_model_parsers.add_argument(
        '--without_dockerfile', action='store_false')
    init_cython_model_parsers.set_defaults(func=init_cython_model)

    # init cython script command
    init_cython_script_parsers = init_cython_parsers.add_parser(
        "script", aliases=["S"], help="init a python script")
    init_cython_script_parsers.add_argument(
        '-e', '--env', type=str, choices=["env", "conda"], default="env")
    init_cython_script_parsers.add_argument('-t', '--template', type=str, choices=[
        "simple"],
        default="simple")
    init_cython_script_parsers.add_argument(
        '--without_test', action='store_false')
    init_cython_script_parsers.add_argument(
        '--without_docs', action='store_false')
    init_cython_script_parsers.add_argument(
        '--without_dockerfile', action='store_false')
    init_cython_script_parsers.set_defaults(func=init_cython_script)

    # init cpp model


    # status command
    status_parsers = subparsers.add_parser("status")
    status_parsers.set_defaults(func=status)

    # update command
    update_parsers = subparsers.add_parser("update")
    update_parsers.add_argument('vers', type=str)
    update_parsers.set_defaults(func=update)

    # # clean command
    # clean_parsers = subparsers.add_parser("clean",help="clean the project")
    # clean_parsers.add_argument('-s', '--leave_source', action="store_true")
    # clean_parsers.set_defaults(func=clean)

    # # install command
    # install_parsers = subparsers.add_parser("install")
    # install_group = install_parsers.add_mutually_exclusive_group(required=True)
    # install_group.add_argument('-d', '--dev', nargs='*', required=False)
    # install_group.add_argument('-t', '--test', nargs='*', required=False)
    # install_group.add_argument(
    #     '-r', '--requirements', nargs='*', required=False)
    # install_group.add_argument('--self', action="store_true")
    # install_parsers.set_defaults(func=install)

    

    

    # # build command
    # build_parsers = subparsers.add_parser("build")
    # build_parsers.add_argument(
    #     '-e', '--egg', action="store_true")
    # build_parsers.add_argument(
    #     '-w', '--wheel', action="store_true")

    # build_parsers.add_argument(
    #     '-d', '--docker', action="store_true")
    # build_parsers.set_defaults(func=build)
    # # run command
    # run_parsers = subparsers.add_parser("run")
    # run_parsers.add_argument('args', type=str, nargs='+')
    # run_parsers.set_defaults(func=run)

    
    # test_parsers = subparsers.add_parser("test")
    # test_parsers.add_argument('-t', '--typecheck', action="store_true")
    # test_parsers.add_argument(
    #     '-c', '--coverage', type=str, choices=["report", "html"])
    # test_parsers.set_defaults(func=test)

    # # upload command
    # upload_parsers = subparsers.add_parser("upload")
    # upload_group = upload_parsers.add_mutually_exclusive_group(required=False)
    # upload_group.add_argument('-r', '--regist', type=str,
    #                           choices=["pypi", "local"])
    # upload_group.add_argument('-p', '--pypi', action="store_true")
    # upload_group.add_argument('-l', '--localpypi', type=str)
    # upload_group.add_argument('-g', '--git', type=str,
    #                           nargs='*', required=False)
    # upload_parsers.set_defaults(func=upload)

    # # docs command
    # doc_parsers = subparsers.add_parser("doc")
    # doc_group = doc_parsers.add_mutually_exclusive_group(required=False)
    # doc_group.add_argument('-s', '--serve', action="store_true")
    # doc_group.add_argument('-b', '--build', action="store_true")
    # doc_parsers.set_defaults(func=doc)

    # # test commmand
    # test_parsers = subparsers.add_parser("status")
    # test_parsers.set_defaults(func=status)

    args = parser.parse_args()
    args.func(args)
