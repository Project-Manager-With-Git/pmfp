# build

suncommand `build` can build your project.

if your project is a application which is init as a web application or a gui application.

pmfp will build your project to a `.pyz` file.

if if your project is a model. pmfp will build it to a wheel. if you want to build a egg, you can use the flag `-e`.


if your project is a commandline application. pmfp will build it to a `pyz` file as default.
but if there is `-w` or `-e`, pmfp will build it to wheel or egg
