# Static_Code_Analyzer
Python Core project on JetBrains Academy.

A small static code analyzer provided to understand 
how static source code analyzers work, what is AST and regular expressions. 
This project could be implemented with OOP, UnitTesting or with 
try: -- except: block, but here you can see it in a functional programming way.

Script obtains a path to file or directory as a command line argument.
Searches for all '.py' files in the directory or analyze a single '.py' file. 
Finds common stylistic issues in Python code and provides 
certain output in a format:

"Path to file: Line number: Code(S001 - S012) of Issue and Issue message".

How to run:

cmd: python static_analyzer.py {path_to_file/path_to_directory}


Modules used: re, sys, ast, os.

Checks implemented:
  1) long_line
  2) indentation
  3) unnecessary_semicolon
  4) less_two_space
  5) todo_found
  6) blank_line_check
  7) many_spaces_after_constr_name
  8) check_class_name
  9) check_func_name
  10) check_argnames_errors
  11) check_var_names_errors
  12) check_mutable_defaults

You can find all the functions descriptions within DocStrings inside code_analyzer.py file.
