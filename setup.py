from distutils.core import setup
import setup_translate


setup(name='enigma2-plugin-systemplugins-satipserver',
		version='1.0',
		author='Dimitrij openPLi',
		author_email='dima-73@inbox.lv',
		package_dir={'SystemPlugins.SATIPserver': 'src'},
		packages=['SystemPlugins.SATIPserver'],
		package_data={'SystemPlugins.SATIPserver': ['*.png']},
		description='SAT>IP servers for enigma2',
		cmdclass=setup_translate.cmdclass,
	)
