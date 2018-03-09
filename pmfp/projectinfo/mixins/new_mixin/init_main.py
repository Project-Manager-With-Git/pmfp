"""创建入口文件."""
from string import Template
from pathlib import Path

PYTHON_MAIN = Template("""# !/usr/bin/env python3
import sys


if __name__ == '__main__':
    from $project_name.main import main
    sys.exit(main(sys.argv[1:]))
""")

PYTHON_PROJECT_MAIN = Template("""import sys
import argparse
from .command.echo import echo_command
from typing import Sequence


class Command:

    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            description='Project Manager for Pythoner',
            usage='''$project_name.py <command> [<args>]

The most commonly used ppm commands are:
   echo        echo a string
''')
        parser.add_argument('command', help='Subcommand to run')
        
        self.argv = argv
        args = parser.parse_args(argv[0:1])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def echo(self):
        parser = argparse.ArgumentParser(
            description='echo string')
        parser.add_argument("command", type=str)
        parser.set_defaults(func=echo_command)
        args = parser.parse_args(self.argv[1:])
        args.func(args) 


def main(argv: Sequence[str]=sys.argv[1:]):
    Command(argv)
""")

CPP_MAIN = Template("""/*
name:$project_name
author:$author
description:$description
*/
#include <unistd.h>
#include <iostream>
#include <string>

using std::string;
using std::cout;
using std::endl;

namespace $project_name {
    int helloworld(void){
        string words = "hello world!";
        cout << words << endl;
        return 0;
    }
}


int main(int argc, char **argv){

    int ch;
    opterr = 0;
    while ((ch = getopt(argc,argv,"s:v\n")) != -1){
        switch(ch){
            case "e":
                cout << ("option echo: %s\n",optarg)<<endl;
                break;
            default:
                $project_name::helloworld();
        }
    }  
}
""")

NODE_MAIN = """#!/usr/bin/env node  
let program = require('commander')
const appInfo = require('./package.json')


program
    .version(appInfo.version)
    .usage('$project_name [options] <package>')

program
    .command('echo <cmd>')
    .alias("ec")
    .description('回音')
    .option("-n, --name <mode>", "with name")
    .action((cmd, options)=>{
        let nm = typeof options.name=='string'?options.name:""
        console.log('echo "%s" with name %s ', cmd, nm)
    }).on('--help', function() {
        //这里输出子命令的帮助
        console.log('Examples:')
        console.log('  run：')
        console.log('    $ ./main.js echo ss -n aaaaa')
        console.log('    $ ./main.js echo ss')
        console.log()
    })

program.parse(process.argv)
"""


class InitMainMixin:
    """创建入口文件."""

    def _init_main(self):
        if self.form.compiler == "python":
            if Path("main.py").exists():
                print("already have a main.py file")
                return
            if Path(self.meta.project_name).is_dir:
                with open("main.py", "w") as f:
                    f.write(PYTHON_MAIN.substitute(
                        project_name=self.meta.project_name))
                with open("{self.meta.project_name}/main.py".format(self=self), "w") as f:
                    f.write(PYTHON_PROJECT_MAIN.substitute(
                        project_name=self.meta.project_name))
            else:
                with open("main.py", "w") as f:
                    f.write(PYTHON_PROJECT_MAIN.substitute(
                        project_name=self.meta.project_name))

        elif self.form.compiler == "cpp":
            if Path("src").is_dir:
                with open("src/main.cpp", "w") as f:
                    f.write(CPP_MAIN.substitute(
                        author=self.author.author,
                        description=self.desc.description,
                        project_name=self.meta.project_name))

        elif self.form.compiler == "node":
            if not Path("main.js").exists():
                self.install('commander', record="dev")
                with open("main.js", "w") as f:
                    f.write(
                        NODE_MAIN.substitute(
                            project_name=self.meta.project_name)
                    )
            else:
                print("already have a main.js")
        else:
            print("unknown compiler!")


__all__ = ["InitMainMixin"]
