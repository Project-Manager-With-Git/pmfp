/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _Person = __webpack_require__(1);

	var _Person2 = _interopRequireDefault(_Person);

	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

	var p = new _Person2.default('张三', 20); /**
	                                        * @Author: HSZ <huangsizhe>
	                                        * @Date:   2016-04-05T23:08:35+08:00
	                                        * @Email:  hsz1273327@gmail.com
	                                        * @Last modified by:   huangsizhe
	                                        * @Last modified time: 2016-04-05T23:08:38+08:00
	                                        * @License: MIT
	                                        */

	document.write(p.say());

/***/ },
/* 1 */
/***/ function(module, exports) {

	"use strict";

	Object.defineProperty(exports, "__esModule", {
	  value: true
	});

	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

	/*
	* @Author: HSZ <huangsizhe>
	* @Date:   2016-04-05T23:08:53+08:00
	* @Email:  hsz1273327@gmail.com
	* @Last modified by:   huangsizhe
	* @Last modified time: 2016-04-05T23:09:16+08:00
	* @License: MIT

	/**
	 * Person类
	 */

	var Person = function () {
	  /**
	   * 初始化函数,用于构造一个对象.
	   * @param {string} name 名字.
	   * @param {number} age 年龄.
	   */

	  function Person(name, age) {
	    _classCallCheck(this, Person);

	    this.name = name;
	    this.age = age;
	  }
	  /**
	   * Person对象的说方法.
	   * @return {string} 返回说的字符串.
	   */


	  _createClass(Person, [{
	    key: "say",
	    value: function say() {
	      return "我是" + this.name + ",我今年" + this.age + "岁了。";
	    }
	  }]);

	  return Person;
	}();

	exports.default = Person;

/***/ }
/******/ ]);