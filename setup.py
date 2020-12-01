import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysurges-matyilona", # Replace with your own username
    version="0.0.0.dev2",
    author="Matyas Kocsis",
    author_email="matyilona@gmail.com",
    description="Package for the parametric design on superconducting resonator systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matyilona/pysurges",
    packages=setuptools.find_packages(),
    install_requires=['shapely','gdstk','ezdxf','lxml','jupyter','ipyparams'],
    license="GPLv3",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
