from setuptools import setup

setup(
    name='grep_click',
    version='0.1',
    py_modules=['grep_click'],
    include_package_data=True,
    install_requires=[
        'click',
        'os',
        're',
        #'shlex',
        #'subprocess',
        'pathlib',

    ],
    entry_points='''
        [console_scripts]
        grep_click=grep_click:cli
    ''',
)
