from setuptools import setup


setup(
    name="aiobestproxiesapi",
    version="0.0.2",
    packages=[
        "aiobestproxiesapi"
    ],
    url="https://github.com/Abstract-X/aiobestproxiesapi",
    license="MIT",
    author="Abstract-X",
    author_email="turinwhites@gmail.com",
    description="Asynchronous API wrapper for best-proxies.ru.",
    install_requires=[
        "aiohttp>=3.6.2,<4.0.0"
    ],
    include_package_data=False
)
