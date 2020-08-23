import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="dicum",
	version="0.1",
	author="Jas Nombre",
	author_email="jas.nombre@web.com",
	description="A keyholding game for chastity fetishists",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/joka-beep/dicum",
	packages=setuptools.find_packages(),
	package_dir={'Dicum': 'Dicum'},
	package_data={'Dicum': ['resources/*.dat']},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: GPLv3 License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
