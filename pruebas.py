class MyClass:
  def __init__(self):
    self._protected_data = "protegido"

  @property
  def protected_data(self):
    return self._protected_data

my_object = MyClass()
print(my_object.protected_data)