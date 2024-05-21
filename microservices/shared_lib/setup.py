from setuptools import setup, find_packages

setup(
    name="shared_lib",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        "SQLAlchemy>=1.3.23",
        "alembic>=1.5.8",
    ],
)
