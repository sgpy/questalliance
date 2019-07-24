from setuptools import setup

setup(
    name='questalliance',
    version='0.1b',
    py_modules=['questalliance'],
    install_requires=[
        "Click",
        "flask",
        "six",
        "dialogflow",
        "python-dotenv",
    ],
    entry_points='''
        [console_scripts]
        deploy_relay_server=commands.server:deploy_relay_server
        deploy_backend_server=commands.server:deploy_backend_server
        generate_db=commands.server:generate_db
    ''',
)