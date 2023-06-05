import cx_Freeze

executables = [cx_Freeze.Executable('main.py')]

cx_Freeze.setup(
    name="banco",
    options={'build_exe': {'packages': ['PyQt6', 'mysql', 'xml'],
                           'include_files':['controller', 'data', 'img', 'model', 'view']}},
    executables = executables

)
