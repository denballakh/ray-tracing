import setuptools

setuptools.setup(
    name="ray-tracing",
    version="0.1",
    author="Denis Ballakh",
    description="2D ray tracing",
    url="https://github.com/denballakh/ray-tracing",
    packages=setuptools.find_packages(
        include=('ray_tracing',),
    ),
    python_requires='>=3.10',
    install_requires=[
        'pillow',
        'types-pillow',
        'mypy',
        'mypy-extensions',
        'typing-extensions',
    ],
)

# also requires 'https://github.com/denballakh/ranger-tools' be installed
