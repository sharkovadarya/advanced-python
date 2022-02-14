import setuptools

setuptools.setup(
    name="fib_ast",
    version="0.0.3",
    description="Generates AST for a function that finds the first n Fibonacci numbers",
    url="https://github.com/sharkovadarya/advanced-python",
    author="Darya Sharkova",
    author_email="sharkovadarya@gmail.com",
    packages=setuptools.find_packages(),
    py_modules=["print_ast"],
    install_requires=[
        'matplotlib',
        'networkx'
    ]
)
