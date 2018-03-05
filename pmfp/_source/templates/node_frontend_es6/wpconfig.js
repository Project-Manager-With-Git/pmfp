/**
* @Author: HSZ <huangsizhe>
* @Date:   2016-04-05T22:46:53+08:00
* @Email:  hsz1273327@gmail.com
* @Last modified by:   huangsizhe
* @Last modified time: 2016-04-06T13:03:08+08:00
* @License: MIT
*/


import path from "path"

export default {
  entry: "./js/src/main.js",
  output: {
    path: path.join(__dirname, 'js/bin'),
    filename: "bundle.js"
  },
  module: {
    loaders: [
      {
        test: path.join(__dirname, 'js/src'),
        loader: 'babel-loader',
        query: {
          presets: ['es2015']
        }
      }
    ]
  }
}
