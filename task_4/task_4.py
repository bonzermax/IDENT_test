import inspect
from pydantic import BaseModel

class Task(BaseModel):
    id: int
    name: str




if __name__ == '__main__':
    inspect_result = inspect.get_annotations(Task)
    print(inspect.get_annotations(Task))
    for key, value in inspect_result.items():
        print(key, value)
