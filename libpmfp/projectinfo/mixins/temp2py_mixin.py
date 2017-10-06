class Temp2pyMixin:

    def temp2py(self, path):
        if path.is_dir():
            for child in path.iterdir():
                self.temp2py(child)
        if path.is_file():
            if path.suffix == ".temp":
                path.rename(str(path)[:-5])


__all__ = ["Temp2pyMixin"]
