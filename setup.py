from setuptools import setup, find_packages

setup(
    name="flet_object_inspector",
    version="0.1.0", 
    author="Sergey Vasilyev",
    author_email="sergey.vasilyev.dev@google.com",
    description="The flet_object_inspector module is used to visualize the structure of Flet framework objects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)