/**
* @Author: HSZ <huangsizhe>
* @Date:   2016-04-06T13:40:04+08:00
* @Email:  hsz1273327@gmail.com
* @Last modified by:   huangsizhe
* @Last modified time: 2016-04-06T13:40:38+08:00
* @License: MIT
*/



let path = require("path")
let webpack = require('webpack')
module.exports = {
    entry: "./js/src/main",
    output: {
        path: path.join(__dirname, 'js/bin'),
        filename: "bundle.js"
    },
    resolve: {
        // Add '.ts' and '.tsx' as a resolvable extension.
        extensions: [".ts", ".js"]
    },
    module: {
        loaders: [
            // all files with a '.ts' or '.tsx' extension will be handled by 'ts-loader'
            {
                test: /\.ts/,
                loader: 'ts-loader',
                exclude: /node_modules/
            }
        ]
    }
}
