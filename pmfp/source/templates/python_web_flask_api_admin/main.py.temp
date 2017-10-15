import argparse
import sys
from server import choose_server
from app_creater import create_app

ENV = ("development", "testing", "production","test","dev","default")


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--environment", type=str, default="default", help="默认为debug模式,可选的环境:\n" + ",".join(ENV))
    parser.add_argument("-p", "--port", type=int, default=5000, help="使用的端口")
    parser.add_argument("-H", "--host", type=str, default="localhost", help="使用的主机名")
    args = parser.parse_args()

    if args.environment and args.environment not in ENV:
        print("未知的运行环境")
        parser.print_help()
        sys.exit(0)
    else:
        return args


def run(app, args):
    server = choose_server(args.environment)
    server(app, args.host, args.port)


def main():
    args = parser()
    app = create_app(args.environment)
    run(app, args)


if __name__ == '__main__':
    main()
