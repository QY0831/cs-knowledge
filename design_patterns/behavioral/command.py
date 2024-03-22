"""
解耦调用job的对象和真正执行job的对象，引入中间对象来执行命令。

例子：
有一个包含两个项目的菜单。
其中一项隐藏文件，另一个将其删除。 
每个项目都是一个 MenuItem 类，它接受相应的命令作为输入并执行。

"""

from typing import List, Union


class HideFileCommand:
    """
    A command to hide a file given its name
    """

    def __init__(self) -> None:
        # an array of files hidden, to undo them as needed
        self._hidden_files: List[str] = []

    def execute(self, filename: str) -> None:
        print(f"hiding {filename}")
        self._hidden_files.append(filename)

    def undo(self) -> None:
        filename = self._hidden_files.pop()
        print(f"un-hiding {filename}")


class DeleteFileCommand:
    """
    A command to delete a file given its name
    """

    def __init__(self) -> None:
        # an array of deleted files, to undo them as needed
        self._deleted_files: List[str] = []

    def execute(self, filename: str) -> None:
        print(f"deleting {filename}")
        self._deleted_files.append(filename)

    def undo(self) -> None:
        filename = self._deleted_files.pop()
        print(f"restoring {filename}")


class MenuItem:
    """
    The invoker class. Here it is items in a menu.
    """

    def __init__(self, command: Union[HideFileCommand, DeleteFileCommand]) -> None:
        self._command = command

    def on_do_press(self, filename: str) -> None:
        self._command.execute(filename)

    def on_undo_press(self) -> None:
        self._command.undo()


def main():
    """
    >>> item1 = MenuItem(DeleteFileCommand())

    >>> item2 = MenuItem(HideFileCommand())

    # create a file named `test-file` to work with
    >>> test_file_name = 'test-file'

    # deleting `test-file`
    >>> item1.on_do_press(test_file_name)
    deleting test-file

    # restoring `test-file`
    >>> item1.on_undo_press()
    restoring test-file

    # hiding `test-file`
    >>> item2.on_do_press(test_file_name)
    hiding test-file

    # un-hiding `test-file`
    >>> item2.on_undo_press()
    un-hiding test-file
    """
