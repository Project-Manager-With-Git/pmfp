"""使用npm初始化node的执行环境."""
import json
import warnings
from pathlib import Path
from typing import Optional, List
from pmfp.utils.run_command_utils import run

WEBPACK_BASE_CONFIG = """const path = require('path')
const webpack = require('webpack')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const CleanWebpackPlugin = require("clean-webpack-plugin")
module.exports = {
    entry: path.resolve(__dirname, '../src/index.js'),
    output: {
        path: path.resolve(__dirname, '../build'),
        filename: 'bundle-[hash].js'
    },
    devServer: {
        contentBase: path.resolve(__dirname, '../build'), //本地服务器所加载的页面所在的目录
        historyApiFallback: true, //不跳转
        inline: true,
        hot: true
    },
    module: {
        rules: [{
                test: /\.js$/,
                use: {
                    loader: 'babel-loader'
                },
                exclude: path.resolve(__dirname, '../node_modules'),
                include: path.resolve(__dirname, '../src')
            },
            {
                test: /\.(png|jpg|jpeg|gif|eot|ttf|woff|woff2|svg|svgz)$/i,
                use: [{
                        loader: 'url-loader',
                        options: {
                            limit: 10000,
                            name: '[path][name].[ext]?[hash:6]!./dir/file.png'
                        }
                    },
                    {
                        loader: 'image-webpack-loader',
                        query: {
                            progressive: true,
                            optimizationLevel: 7,
                            interlaced: false,
                            pngquant: {
                                quality: '65-90',
                                speed: 4
                            }
                        }
                    }
                ]
            }
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: path.resolve(__dirname, '../src/index.tmpl.html') //new 一个这个插件的实例，并传入相关的参数
        }),
        new webpack.HotModuleReplacementPlugin(), //热加载插件
        new CleanWebpackPlugin('build/*.*', {
            root: path.resolve(__dirname, ".."),
            verbose: true,
            dry: false
        })
    ]
}
"""

WEBPACK_PROD_CONFIG = """const webpack = require('webpack')
const UglifyJSPlugin = require('uglifyjs-webpack-plugin')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const merge = require('webpack-merge')
const base = require('./webpack.config.base.js')
const env = require("./conf/prod.json")
module.exports = merge(base,{
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: "style-loader",
                    use: ["css-loader"]
                })
            },
            {
                test: /\.styl$/,
                use: ExtractTextPlugin.extract({
                    fallback: "style-loader",
                    use: ["css-loader", "stylus-loader"]
                })
            }
        ]
    },
    plugins: [
        new webpack.optimize.OccurrenceOrderPlugin(),
        new ExtractTextPlugin("style.css"),
        new webpack.DefinePlugin({
            'process.env': {
                'NODE_ENV': JSON.stringify(env)
            }
        })
    ],
    optimization: {
        minimizer: [
            new UglifyJSPlugin(),
        ]
    }
})
"""

WEBPACK_TEST_CONFIG = """
const webpack = require('webpack')
const UglifyJSPlugin = require('uglifyjs-webpack-plugin')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const merge = require('webpack-merge')
const base = require('./webpack.config.base.js')
const env = require("./conf/test.json")
module.exports = merge(base,{
    devtool: 'eval-source-map',
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: "style-loader",
                    use: ["css-loader"]
                })
            },
            {
                test: /\.styl$/,
                use: ExtractTextPlugin.extract({
                    fallback: "style-loader",
                    use: ["css-loader", "stylus-loader"]
                })
            }
        ]
    },
    plugins: [
        new webpack.optimize.OccurrenceOrderPlugin(),
        new ExtractTextPlugin("style.css"),
        new webpack.DefinePlugin({
            'process.env': {
                'NODE_ENV': JSON.stringify(env)
            }
        })
    ],
    optimization: {
        minimizer: [
            new UglifyJSPlugin(),
        ]
    }
})
"""

WEBPACK_DEV_CONFIG = """const webpack = require('webpack')
const merge = require('webpack-merge')
const base = require('./webpack.config.base.js')
const env = require("./conf/dev.json")
module.exports = merge(base,{
    devtool: 'eval-source-map',
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [{
                    loader: "style-loader"
                }, {
                    loader: "css-loader"
                }]
            },
            {
                test: /\.styl$/,
                use: [{
                    loader: "style-loader"
                }, {
                    loader: "css-loader"
                }, {
                    loader: "stylus-loader"
                }]
            }
        ]
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env': {
                'NODE_ENV': JSON.stringify(env)
            }
        })
    ]
})
"""

PROD_CONFIG = """{
    "env":"prod"
}
"""

TEST_CONFIG = """{
    "env":"test"
}
"""

DEV_CONFIG = """{
    "env":"dev"
}
"""


def new_env_webpack(cwd: Path, project_name: str, version: str, description: str, author: str,
                    author_email: Optional[str] = None,
                    keywords: Optional[List[str]] = None,
                    requires: Optional[List[str]] = None,
                    test_requires: Optional[List[str]] = None) -> None:
    """初始化golang默认的虚拟环境.

    Args:
        cwd (Path): 虚拟环境所在的根目录
        project_name (str): 项目名

    """

    js_env_path = cwd.joinpath("package.json")
    if js_env_path.exists():
        warnings.warn("package.json已存在!")
    else:
        jsenv = {
            "name": project_name,
            "version": version,
            "description": description,
            "main": "index.js",
            "license": "MIT",
            "scripts": {
                "start": "./node_modules/.bin/webpack-dev-server --open --config env/webpack.config.dev.js",
                "serv:dev": "./node_modules/.bin/webpack-dev-server --open --config env/webpack.config.dev.js",
                "serv:test": "./node_modules/.bin/webpack-dev-server --open --config env/webpack.config.test.js",
                "serv:prod": "./node_modules/.bin/webpack-dev-server --open --config env/webpack.config.prod.js",
                "build": "./node_modules/.bin/webpack --config env/webpack.config.prod.js",
                "build:dev": "./node_modules/.bin/webpack --config env/webpack.config.dev.js",
                "build:test": "./node_modules/.bin/webpack --config env/webpack.config.test.js",
                "build:prod": "./node_modules/.bin/webpack --config env/webpack.config.prod.js",
            },

            "babel": {
                "presets": [
                    ["@babel/preset-env"]
                ]
            }
        }
        if author_email:
            jsenv.update({
                "author": {"name": author, "email": author_email}
            })
        else:
            jsenv.update({
                "author": author
            })

        if keywords:
            jsenv.update({
                "keywords": keywords
            })
        with open(js_env_path, "w", encoding="utf-8") as fw:
            json.dump(jsenv, fw, indent=4)

        if not cwd.joinpath("env").is_dir():
            cwd.joinpath("env").mkdir()
        with open(str(cwd.joinpath("env/webpack.config.base.js")), "w", encoding="utf-8") as f:
            f.write(WEBPACK_BASE_CONFIG)
        with open(str(cwd.joinpath("env/webpack.config.dev.js")), "w", encoding="utf-8") as f:
            f.write(WEBPACK_DEV_CONFIG)
        with open(str(cwd.joinpath("env/webpack.config.prod.js")), "w", encoding="utf-8") as f:
            f.write(WEBPACK_PROD_CONFIG)
        with open(str(cwd.joinpath("env/webpack.config.test.js")), "w", encoding="utf-8") as f:
            f.write(WEBPACK_TEST_CONFIG)

        if not cwd.joinpath("env/conf").is_dir():
            cwd.joinpath("env/conf").mkdir()

        with open(str(cwd.joinpath("env/conf/dev.json")), "w", encoding="utf-8") as f:
            f.write(DEV_CONFIG)
        with open(str(cwd.joinpath("env/conf/prod.json")), "w", encoding="utf-8") as f:
            f.write(PROD_CONFIG)
        with open(str(cwd.joinpath("env/conf/test.json")), "w", encoding="utf-8") as f:
            f.write(TEST_CONFIG)
        run("npm install --save-dev babel-loader @babel/core @babel/cli @babel/preset-env @babel/register webpack webpack-cli style-loader css-loader stylus stylus-loader url-loader file-loader image-webpack-loader html-webpack-plugin webpack-dev-server clean-webpack-plugin extract-text-webpack-plugin@next uglifyjs-webpack-plugin webpack-merge", cwd=cwd, visible=True, fail_exit=True)
        if requires:
            for i in requires:
                run(f"npm install {i}", cwd=cwd, visible=True, fail_exit=True)
        if test_requires:
            for i in test_requires:
                run(f"npm install --save-dev {i}", cwd=cwd, visible=True, fail_exit=True)
