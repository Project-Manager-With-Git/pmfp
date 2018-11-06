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
class Person{
    /**
     * 初始化函数,用于构造一个对象.
     * @param {string} name 名字.
     * @param {number} age 年龄.
     */
  constructor(name, age){
    this.name = name;
    this.age = age;
  }
  /**
   * Person对象的说方法.
   * @return {string} 返回说的字符串.
   */
  say(){
    return `我是${this.name},我今年${this.age}岁了。`;
  }
}

export default Person;
