WEBPACK_CONFIG = """const htmlWebpackPlugin = require('html-webpack-plugin')
const path = require('path')

module.exports = {
    entry: './src/index.js',
    output: {
        path: __dirname + './dist',
        filename: 'js/[name].bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                use:{
                    loader: 'babel-loader'
                },
                exclude: path.resolve(__dirname, 'node_modules'),
                include: path.resolve(__dirname, 'src')
            }, 
            {
                test: /\.styl/,
                use:{
                    loader: 'style-loader!css-loader!stylus-loader'
                },
                exclude: /(node_modules|bower_components)/
            }
        ]
    },
    plugins: [
        new htmlWebpackPlugin({
            filename: 'index.html',
            template: __dirname + '/src/index.tmpl.html',
            inject: 'body',
            title: 'this is a complete webpack demo'
        })
    ]
}
"""