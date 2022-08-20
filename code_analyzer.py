import re
import sys
import os
import ast

blank_line_count = 0


def main():
    """Obtain a path as a command_line argument.
    Search for all .py files in the directory and call all_test() func on their paths.
    """
    base_path = sys.argv[1]
    if os.path.isfile(base_path):
        all_tests(base_path)
    elif os.path.isdir(base_path):
        for dirpath, dirnames, filenames in os.walk(base_path):
            for filename in filenames:
                if filename.endswith(".py"):
                    path_to_file = os.path.join(dirpath, filename)
                    all_tests(path_to_file)


def all_tests(path_to_file):
    """Check the lines of code in given file.
    Print the Issue Messages in case they are found.
    """
    file = open(path_to_file)
    code = file.read()
    tree = ast.parse(code)
    file.seek(0)
    lines = file.readlines()

    argnames_errors = ast_argnames_check(tree)
    var_name_errors = ast_var_name_check(tree)
    defaults_in_args = ast_check_defaults(tree)

    for line_number, line in enumerate(lines, 1):
        long_line(path_to_file, line_number, line)
        indentation(path_to_file, line_number, line)
        unnecessary_semicolon(path_to_file, line_number, line)
        less_two_space(path_to_file, line_number, line)
        todo_found(path_to_file, line_number, line)
        blank_line_check(path_to_file, line_number, line)
        many_spaces_after_constr_name(path_to_file, line_number, line)
        check_class_name(path_to_file, line_number, line)
        check_func_name(path_to_file, line_number, line)
        check_argnames_errors(path_to_file, line_number, argnames_errors)
        check_var_names_errors(path_to_file, line_number, var_name_errors)
        check_mutable_defaults(path_to_file, line_number, defaults_in_args)
    file.close()


def ast_argnames_check(tree) -> dict:
    """Find argument names and check them for snake_case writing.

    Return argname_errors dictionary ->  {line_number: arg_name} where "arg_name"
    is not written in snake_case
    """
    args_names_with_line = dict()
    tree_walk = ast.walk(tree)

    # creating dict with line_n: args_names
    for node in tree_walk:
        if isinstance(node, ast.FunctionDef):
            line_num = node.lineno
            args_names_with_line[line_num] = []
            for a in node.args.args:
                args_names_with_line[line_num].append(a.arg)

    # checking whether arg_names written in snake_case
    argname_errors = dict()
    for line_n, arg_name in args_names_with_line.items():
        for name in arg_name:
            match_010 = re.match(r"\b(_{0,2}[a-z0-9]+_{0,2})+\b", name)
            if match_010 is None and line_n not in argname_errors:
                argname_errors[line_n] = name
    return argname_errors


def ast_check_defaults(tree) -> dict:
    """Check whether default argument value is mutable
    Return defaults_in_args dictionary -> {line_number: default_type}
    """
    defaults_in_args = dict()
    tree_walk = ast.walk(tree)

    for node in tree_walk:
        if isinstance(node, ast.FunctionDef):
            line_num = node.lineno
            for a in node.args.defaults:
                if (isinstance(a, ast.List) or isinstance(a, ast.Dict) or isinstance(a, ast.Call)
                        and line_num not in defaults_in_args):
                    defaults_in_args[line_num] = type(a)
    return defaults_in_args


def ast_var_name_check(tree) -> dict:
    """Find variable names and check them for snake_case writing.

    Return var_name_errors dictionary ->  {line_number: var_name} where "var_name"
    is not written in snake_case.
    """
    var_names_with_line = dict()
    tree_walk = ast.walk(tree)

    for node in tree_walk:
        if isinstance(node, ast.Name):
            line_num = node.lineno
            if isinstance(node.ctx, ast.Store):
                var_names_with_line[line_num] = node.id

    var_name_errors = dict()
    for line_n, var_name in var_names_with_line.items():
        match_010 = re.match(r"\b(_{0,2}[a-z0-9]+_{0,2})+\b", var_name)
        if match_010 is None and line_n not in var_name_errors:
            var_name_errors[line_n] = var_name

    return var_name_errors


def print_output(path: str, line_num: int, message: str):
    """Print given message in special format"""
    print(f"{path}: Line {line_num}: {message}")


# CHECKS
def long_line(path_to_file, line_number, line):
    if len(line) > 79:
        print_output(path_to_file, line_number, "S001 Too long")


def indentation(path_to_file, line_number, line):
    if line != '\n' and (len(line) - len(line.lstrip())) % 4 != 0:
        print_output(path_to_file, line_number, "S002 Indentation is not a multiple of four")


def unnecessary_semicolon(path_to_file, line_number, line):
    match = re.findall(r"\);", line)
    match_1 = re.findall(r"; #", line)
    if len(match) > 0 or len(match_1) > 0:
        print_output(path_to_file, line_number, "S003 Unnecessary semicolon after a statement")


def less_two_space(path_to_file, line_number, line):
    if not line.startswith("#") and "#" in line:
        if "  #" not in line.lower():
            print_output(path_to_file, line_number, "S004 Less than two spaces before inline comments")


def todo_found(path_to_file, line_number, line):
    if "# todo" in line.lower():
        print_output(path_to_file, line_number, "S005 TODO found")


def blank_line_check(path, line_num, line):
    global blank_line_count
    if line == "\n":
        blank_line_count += 1
    elif line != "\n":
        if blank_line_count > 2:
            print_output(path, line_num, "S006 More than two blank lines preceding a code line")
            blank_line_count = 0
        else:
            blank_line_count = 0


def many_spaces_after_constr_name(path_to_file, line_number, line):
    match_s007 = re.findall(r"(def|class) {2,}\w+", line)
    if len(match_s007) > 0:
        print_output(path_to_file, line_number, "S007 Too many spaces after construction_name")


def check_class_name(path_to_file, line_number, line):
    if "class" in line:
        match_s008 = re.match(r"class +([A-Z][a-z]+)+\b", line)
        if match_s008 is None:
            print_output(path_to_file, line_number, "S008 Class name should be written in CamelCase")


def check_func_name(path_to_file, line_number, line):
    if "def" in line:
        line_strip = line.lstrip()
        match_009 = re.match(r"def *(_{0,2}[a-z0-9]+_{0,2})+\b", line_strip)
        if match_009 is None:
            print_output(path_to_file, line_number,
                         "S009 Function name should be written in snake_case")


def check_argnames_errors(path_to_file, line_number, argname_errors):
    if line_number in argname_errors:
        arg_name = argname_errors[line_number]
        print_output(path_to_file, line_number,
                     f"S010 Argument name '{arg_name}' should be written in snake_case")


def check_var_names_errors(path_to_file, line_number, var_name_errors):
    if line_number in var_name_errors:
        var_name = var_name_errors[line_number]
        print_output(path_to_file, line_number, f"S011 Variable '{var_name}' should be written in snake_case")


def check_mutable_defaults(path_to_file, line_number, defaults_in_args):
    if line_number in defaults_in_args:
        print_output(path_to_file, line_number,
                     f"S012 The default argument value is mutable.")


if __name__ == '__main__':
    main()
