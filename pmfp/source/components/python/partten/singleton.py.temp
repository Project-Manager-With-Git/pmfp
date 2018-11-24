class SingletonMeta(type):
    """单例元类.

    通过元类来构造单例模式,以其为元类的类的唯一对象都会被保存在本元类的_instances字典下.

    使用方法:

    >>> class A(metaclass = SingletonMeta):
    >>>     pass

    protected:
        _instances (Dict[str,Any]): 用于保存[类名,唯一对象]的字典结构

    """

    _instances={}
    
    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args,**kwargs)
        return cls._instances[cls]



class SingletonAbc(metaclass = SingletonMeta):
    """单例模式抽象基类.
    
    使用方法:
    
    >>> class A(SingletonAbc):
    >>>    pass
    
    """
    pass

__all__ = ["SingletonMeta","SingletonAbc"]