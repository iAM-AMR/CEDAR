

# Generating Entity Relationship Diagrams

A Entity Relationship Diagram (ERD) is a high-level graphical representation of tables and relationships. We can generate a ERD for CEDAR using [PyGraphviz](https://pygraphviz.github.io/), an interface to the open-source [Graphviz](https://graphviz.org/).

These instructions are for installation and use of PyGraphviz on Windows. See the [official instructions](https://pygraphviz.github.io/documentation/stable/install.html) for other systems.


## Install a C++ compiler

To install PyGraphviz, you'll need a C++ compiler. If you have Visual Studio installed, or do C++ development, you probably already have a compiler available. If not, or if you're not sure, download the latest version of [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

- Use the latest version of the Microsoft C++ Build Tools.
- Only install the Build tools roll, or the installation size is dramatically increased.


## Get Graphviz

We're going to extract the Graphviz files to the /Graphviz directory (this directory) instead of performing a complete installation.

- Download [Graphviz 2.46.0](https://gitlab.com/graphviz/graphviz/-/packages/1000451)
  - Newer versions do not work with PyGraphviz.
  - An alternate link is available in the [official instructions](https://pygraphviz.github.io/documentation/stable/install.html).
- Open the .exe using 7-zip (or another archive tool).
  - Copy the contents into the /Graphviz directory.

The structure of the /Graphviz directory should be:

```
├───bin
├───include
│   └───graphviz
├───lib
│   └───pkgconfig
└───share
    └───man
        └───man3
```


## Install PyGraphviz

Ensure you've installed the pre-requisites: pyparsing and pydot. These are listed in the [dev-packages] section of CEDAR's Pipfile; they can be installed using `pipenv install --dev`. Note, PyGraphviz is not listed here due to this complex installation process.

Add this line to your local settings:

```
os.environ["PATH"] += os.pathsep + 'C:/Path/to/Graphviz/bin'
```

In your virtual environment, run:

```
python -m pip install --global-option=build_ext --global-option="-IC:\Path\from\filesystem\root\to\include" --global-option="-LC:\Path\from\filesystem\root\to\lib" pygraphviz
```


## Run PyGraphviz

To generate an ERD with all models:

```
python .\cedar_root\manage.py graph_models -a -g -o my_project_visualized.png
```

To generate an ERD with only some models:
```
python .\cedar_root\manage.py graph_models -a -I reference,factor,res_outcome -o my_project_subsystem.png
```


## Links 

- https://github.com/pygraphviz/pygraphviz/issues/74
- 