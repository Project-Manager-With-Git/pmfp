# init

## init a new project

init subcommand can build a project Automatically.

### choose virtual env

The project will build a virtual environment. And use the virtual environment as default python environment if there is a folder named `env`.

`pmfp` will build the environment by `venv`. you can choose `conda` to build the env by use the flag `-C`



### templates

init subcommand can build a basic template for different kinds of situations.

There are several choices:

+ script `-s`
+ model  `-m`
+ command line tools `-c`
+ gui `-g` gui with `tk`
+ web `-w` you can choose a parameter from `sanic`, `flask`, `zerorpc`

### with scientific calculation tools

you can use the flag `-M` to install `numpy`,`scipy`,`sklearn` Automatically.



## init a exist project

If you want to init a exist project with some code ,requirements and `.ppmrc`.
you can just run `ppm init`, and then follow the questions.
