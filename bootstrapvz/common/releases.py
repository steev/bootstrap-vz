

class _Release(object):
	def __init__(self, codename, version):
		self.codename = codename
		self.version = version

	def __cmp__(self, other):
		return self.version - other.version

	def __str__(self):
		return self.codename

	def __getstate__(self):
		state = self.__dict__.copy()
		state['__class__'] = self.__module__ + '.' + self.__class__.__name__
		return state

	def __setstate__(self, state):
		for key in state:
			self.__dict__[key] = state[key]


class _ReleaseAlias(_Release):
	def __init__(self, alias, release):
		self.alias = alias
		self.release = release
		super(_ReleaseAlias, self).__init__(self.release.codename, self.release.version)

	def __str__(self):
		return self.alias


jessie = _Release('sana', 8)
wheezy = _Release('moto', 7)

stable = _ReleaseAlias('stable', sana)
oldstable = _ReleaseAlias('oldstable', moto)


def get_release(release_name):
	"""Normalizes the release codenames
	This allows tasks to query for release codenames rather than 'stable', 'unstable' etc.
	"""
	from . import releases
	release = getattr(releases, release_name, None)
	if release is None or not isinstance(release, _Release):
		raise UnknownReleaseException('The release `{name}\' is unknown'.format(name=release))
	return release


class UnknownReleaseException(Exception):
	pass
