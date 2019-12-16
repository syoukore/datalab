def create(module_name):
  import sys
  PKG_PATH = "packages/"
  if PKG_PATH not in sys.path:
    sys.path.append(PKG_PATH)

  import importlib.util
  spec = importlib.util.spec_from_file_location(module_name, f"packages/{module_name}/__init__.py")
  foo = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(foo)
  mod = getattr(foo, 'Module')()
  return mod

def fetch(path):
  mod = create(path.split('.')[0])
  return mod.fetch(path)

class Module:
  def fetch(self, path):
    args = tuple(path.split('.')[1:])
    return self.run(args)

  def run(self, args):
    assert False, 'not implemented'
