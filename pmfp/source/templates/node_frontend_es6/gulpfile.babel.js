/**
* @Author: HSZ <huangsizhe>
* @Date:   2016-04-06T11:23:13+08:00
* @Email:  hsz1273327@gmail.com
* @Last modified by:   huangsizhe
* @Last modified time: 2016-04-06T13:30:42+08:00
* @License: MIT
*/


'use strict'
import gulp from 'gulp'
import uglify from 'gulp-uglify'
import clean from 'gulp-clean'
import eslint from "gulp-eslint"
import minifyHtml from "gulp-minify-html"
import notify from 'gulp-notify'
//重命名插件
import rename from "gulp-rename"
import path from "path"
//定义task,参数为task名字,执行的步骤
//html压缩
import wpconfig from './wpconfig'
import webpack from 'webpack'
import gutil from 'gulp-util'
gulp.task('htmlmini', () => {
    return gulp.src('index.html')
    .pipe(rename('index.mini.html'))
    .pipe(minifyHtml()) //压缩
    .pipe(gulp.dest('./html'))
    .pipe(notify({ message: 'htmlmini task complete' }))
})

//webpack整理
gulp.task("webpack", (callback) => {

    var myconfig = Object.create(wpconfig)
    // run webpack
    webpack(
        myconfig
        , (err, stats) => {
        if(err) throw new gutil.PluginError("webpack", err);
        gutil.log("[webpack]", stats.toString({
            // output options
        }))
        callback()
    })
})

//js代码检查
gulp.task('lint', () => {
    return gulp.src('js/src/*.js')
    .pipe(eslint({
        "parser": "babel-eslint",
        "rules": {
          "strict": 0
        }
    }))
    .pipe(eslint.format())
    .pipe(eslint.failAfterError())
})

//js压缩
gulp.task('jsmini', () => {
    return gulp.src('./js/bin/bundle.js')
    .pipe(rename('bundle.mini.js'))
    .pipe(uglify())
    .pipe(gulp.dest('./js/bin'))
    .pipe(notify({ message: 'jsmini task complete' }))
})

//处理js文件
gulp.task('jsdeal', () => {
    console.log('start dealing with js Script!')
    gulp.start('jsmini', "webpack")
})

//预设任务
gulp.task('default', () => {
    gulp.start('jsdeal','htmlmini')
})

// 清理
gulp.task('clean', function() {
  return gulp.src('./js/bin', {read: false})
    .pipe(clean())
})
