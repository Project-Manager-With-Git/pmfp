"""用于将对象的属性转为字典输出的mixin."""


class ToDictMixin:
    """用于将对象的属性转为字典输出的mixin."""

    def to_dict(self):
        """递归的将对象转化为字典形式."""
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        """递归的将对象转化为字典形式的核心代码."""
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value
