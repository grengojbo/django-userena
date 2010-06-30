from distutils.core import setup

setup(name='django-userenity',
      version='0.1.0',
      description='Complete user management application for Django',
      author='Petar Radosevic',
      author_email='petar@wunki.org',
      url='http://github.com/wunki/django-userenity',
      download_url='http://github.com/wunki/django-userenity/downloads',
      packages=['accounts'],
      requires=[
        'django (>1.1.0)',
        'python-dateutil (>1.5)',
      ],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )