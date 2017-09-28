import shutil
class InitTestMixin:

    def _init_test(self):
        print("copy test template")
        if local_path.joinpath("test").exists():
            print(str(local_path.joinpath("test")) + " exists")
        else:
            shutil.copytree(str(dir_path.joinpath("test")),
                            str(local_path.joinpath("test")))
        print("copy test template done!")
        return 1