from setuptools import setup, find_packages

setup(
    name='OneMake_Project',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'chinese_calendar',
        'cx_Oracle',
        'os',
        'locale',
        'datetime',
        'configparser',
        'pyhive',
        'pyarrow'
    ],
    author='fmg',
    author_email='dushi233@qq.com',
    description='hive时间维度表创建',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/EchoAlice1/Dim_Time_generate.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
