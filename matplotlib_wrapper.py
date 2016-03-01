#!/usr/bin/env python2.7

"""Work around for matplotlib + App Engine dev server problems.

See:
    https://github.com/matplotlib/matplotlib/issues/1823#issuecomment-16481823
"""

__author__ = 'github.com/linuxluser'


import os
import subprocess


# Determine if we are running in the dev server
IN_APP_ENGINE_DEV_SERVER = False
if os.environ.has_key('APPENGINE_RUNTIME'):
  if 'Development' in os.environ.get('SERVER_SOFTWARE', ''):
    IN_APP_ENGINE_DEV_SERVER = True


if IN_APP_ENGINE_DEV_SERVER:

  # Check for mpl-data directory
  matplotlib_data_dir = os.path.join(os.getcwdu(), 'mpl-data')
  if os.path.exists(matplotlib_data_dir):
    raise SystemExit('mpl-data directory required')

  # Required environment variables to make matplotlib happy
  os.environ['MATPLOTLIBDATA'] = matplotlib_data_dir
  os.environ['MPLCONFIGDIR'] = os.path.join(os.getcwdu())
  os.environ['HOME'] = os.path.join(os.getcwdu())

  # Add Popen stubs to prevent errors from matplotlib's usage of it
  def no_popen(*args, **kwargs):
    raise OSError('Popen not supported')
  subprocess.Popen = no_popen
  subprocess.PIPE = None
  subprocess.STDOUT = None


# Should be safe to import matplotlib now
import matplotlib
matplotlib.use('Agg')


# Prevent matplotlib from trying to update the font cache (an I/O error)
if IN_APP_ENGINE_DEV_SERVER:
  from matplotlib import font_manager
  def no_pickle_dump(*args, **kwargs):
    pass
  font_manager.pickle_dump = no_pickle_dump
