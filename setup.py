from setuptools import setup

setup(
    name='nico2finder',
    version='0.1.1',
    description='The toolkit for search video contents which is on niconico.',
    author='aqmr-kino',
    url='https://github.com/aqmr-kino/nico2finder',
    license='MIT',
    setup_requires=[
        'wheel',
    ],
    tests_require=[
        'pytest',
    ],
    py_modules=[
        'nico2finder/__init__',
        'nico2finder/finder',
    ],
    python_requires='>=3.4',
)
