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

PROD_CONFIG="""{
    "env":"prod"
}
"""

TEST_CONFIG="""{
    "env":"test"
}
"""

DEV_CONFIG="""{
    "env":"dev"
}
"""