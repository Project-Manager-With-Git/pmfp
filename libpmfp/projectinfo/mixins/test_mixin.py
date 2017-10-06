class RunMixin:

    def test(self, cmd=""):
        if self.form.compiler in ["cython", "python"]:
            
        elif self.form.compiler == "cpp":
            command = "conan create demo/testing"
            subprocess.call(command, shell=True)
        elif self.form.compiler == "js:
            command = "npm run test".formmat(cmd=cmd)
            subprocess.call(command, shell=True)
        else:
            print("unknown compiler!")
            return False