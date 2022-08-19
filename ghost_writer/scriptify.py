from pathlib import Path
from typing import List

from .ghost_writer import ScriptGenerator


class PythonMetaGenerator(ScriptGenerator):
    def __init__(
        self, file_name: str, lines: List[str], indents: List[int]
    ) -> None:

        self._lines: List[str] = lines
        self._indents: List[int] = indents

        super().__init__(file_name)

    def _build_script(self) -> None:

        self._add_line("from ghost_writer import ScriptGenerator")
        self._end_line()
        self._end_line()

        self._add_line("class NewGenerator(ScriptGenerator):")
        self._add_line(
            "def __init__(self, file_name: str) -> None:", indent_level=1
        )
        self._add_line("super().__init__(file_name)", indent_level=2)
        self._end_line()

        self._add_line("def _build_script(self) -> None:", indent_level=1)

        for line, indent in zip(self._lines, self._indents):

            self._add_line(line, indent_level=indent + 2)


def scriptify_python(file_name: str) -> None:

    gen_lines: List[str] = []
    indents: List[int] = []
    with Path(file_name).open("r") as f:

        script_lines: List[str] = f.readlines()

    for line in script_lines:

        tmp = []

        if line.startswith(" "):

            for char in line:

                if char == " ":

                    tmp.append(char)

                else:

                    break

        elif line.startswith("\t"):

            for char in line:

                if char == "\t":

                    tmp.append(char)

                else:

                    break

        num_indents = len(tmp)

        gen_lines.append(line[num_indents:])

        indents.append(num_indents)

    script_gen = PythonMetaGenerator(f"generated_{file_name}", gen_lines, indents)

    script_gen.write()
