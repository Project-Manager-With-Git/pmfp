import Person from '../js/src/Person.js'
import chai from 'chai'

let expect = chai.expect
/**
 * add的测试函数
 */
describe('Person测试',() => {
    it('小明 23岁 说我是小明,我今年23岁了。',
    () => {
        let p = new Person('小明', 23);
        expect(p.say()).to.be.equal("我是小明,我今年23岁了。")
    })
})
