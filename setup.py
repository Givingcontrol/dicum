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
	package_data={
		'Dicum': ['resources/game.csv', 'resources/templates/*', 'resources/js/*.js', 'resources/icons/*',
		          'resources/fonts/*']},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Affero General Public License v3",
		"Operating System :: OS Independent",
		'Intended Audience :: End Users/Desktop',
		"Topic :: Games/Entertainment :: Role-Playing",
		"Development Status :: 3 - Alpha",
		"Natural Language :: English"
	],
	python_requires='>=3.6',
)
