from setuptools import setup

setup(
    name='gym_diamond',
    version='0.0.1',
    install_requires=[
        'gym>=0.2.3',
        'ray==0.6.5',
        'opencv-python',
        'pandas',
        'matplotlib',
        'requests',
        'psutil'
    ]
)
