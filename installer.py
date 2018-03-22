class Installer():
	def __init__(self, dependencies):
		self.dependencies = dependencies
		self.installedPackages = ''

	def load(self):
		import pip
		for package in self.dependencies:
			try:
				# check to see if packages already installed
				__import__(package)
			except:
				# install package if not already installed
				print('Could not import {}. Installing package.'.format(package))
				pip.main(['install', package])
				try:
					__import__(package)
					self.installedPackages += package + ', '
				except:
					print("Failed to import {}".format(package))

		if (len(self.installedPackages) > 0):
			print('\n====================================')
			print('Installed {} depenencies: {}'.format(len(self.dependencies), self.installedPackages))
			print('====================================\n')