# -*- coding: utf-8 -*-
# Copyright 2010-2021, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""A library to operate version definition file.

This script has two functionarity which relate to version definition file.

1. Generate version definition file from template and given parameters.
  To generate version definition file, use GenerateVersionFileFromTemplate
  method.

2. Parse (generated) version definition file.
  To parse, use MozcVersion class.

Typically version definition file is ${PROJECT_ROOT}/mozc_version.txt
(Not in the repository because it is generated by this script)
Typically version template file is
${PROJECT_ROOT}/data/version/mozc_version_template.bzl,
which is in the repository.
The syntax of template is written in the template file.
"""
# TODO(matsuzaki): MozcVersion class should have factory method which takes
#   file path and we should remove all the module methods instead to
#   simplify the design. Currently I'd keep this design to reduce
#   client side's change.
import datetime
import logging
import optparse
import os
import re
import sys


TARGET_PLATFORM_TO_DIGIT = {
    'Windows': '0',
    'Mac': '1',
    'Linux': '2',
    'Android': '3',
    'ChromeOS': '4',
    'iOS': '6',
    'iOS_sim': '6',
    'Wasm': '7',
}

VERSION_PROPERTIES = [
    'MAJOR',
    'MINOR',
    'BUILD',
    'REVISION',
    'TARGET_PLATFORM',
    'BUILD_OSS',
    'QT_VERSION',
    'ENGINE_VERSION',
    'DATA_VERSION',
    ]

MOZC_EPOCH = datetime.date(2009, 5, 24)


def _GetRevisionForPlatform(revision, target_platform):
  """Returns the revision for the current platform."""
  if revision is None:
    logging.critical('REVISION property is not found in the template file')
    sys.exit(1)
  last_digit = TARGET_PLATFORM_TO_DIGIT.get(target_platform, None)
  if last_digit is None:
    logging.critical('target_platform %s is invalid. Accetable ones are %s',
                     target_platform, list(TARGET_PLATFORM_TO_DIGIT.keys()))
    sys.exit(1)

  if not revision:
    return revision

  if last_digit:
    return revision[0:-1] + last_digit

  # If not supported, just use the specified version.
  return revision


def _ParseVersionTemplateFile(template_path, target_platform, version_override):
  """Parses a version definition file.

  Args:
    template_path: A filename which has the version definition.
    target_platform: The target platform on which the programs run.
    version_override: An optional string to override version number.
      If it is a single number, it means a build number (e.g. "4500").
      If it is a four numbers, it means a full version (e.g. "2.28.4500.0").
  Returns:
    A dictionary generated from the template file.
  """
  template_dict = {}
  with open(template_path) as template_file:
    for line in template_file:
      matchobj = re.match(r'(\w+) *= *(\w*)', line.strip())
      if matchobj:
        var = matchobj.group(1)
        val = matchobj.group(2)
        if var in template_dict:
          logging.warning(('Dupulicate key: "%s". Later definition "%s"'
                           'overrides earlier one "%s".'),
                          var, val, template_dict[var])
        # If `val` is a variable (e.g. BUILD_OSS), replace it with the value.
        if val in template_dict:
          val = template_dict[val]
        template_dict[var] = val

  # Some properties need to be tweaked.
  template_dict['REVISION'] = _GetRevisionForPlatform(
      template_dict.get('REVISION', None), target_platform)

  template_dict['TARGET_PLATFORM'] = target_platform
  if version_override:
    nums = version_override.split('.')
    if len(nums) == 1:
      # On Windows, BUILD number must be within 16-bit range.
      if target_platform != 'Windows' or int(nums[0]) <= 0xffff:
        template_dict['BUILD'] = nums[0]
    if len(nums) == 4:
      template_dict['MAJOR'] = nums[0]
      template_dict['MINOR'] = nums[1]
      template_dict['BUILD'] = nums[2]
      template_dict['REVISION'] = nums[3]
  return template_dict


def _GetVersionInFormat(properties, version_format):
  """Returns the version string based on the specified format.

  format can contains @MAJOR@, @MINOR@, @BUILD@ and @REVISION@ which are
  replaced by self._major, self._minor, self._build, and self._revision
  respectively.

  Args:
    properties: a property dicitonary. Typically gotten from
      _ParseVersionTemplateFile method.
    version_format: a string which contains version patterns.

  Returns:
    Return the version string in the format of format.
  """

  result = version_format
  for keyword in VERSION_PROPERTIES:
    result = result.replace('@%s@' % keyword, properties.get(keyword, ''))
  return result


def _GetChangelistNumber(build_override, build_changelist_file):
  """Returns the changelist number from the value or the file path."""
  if build_override:
    return build_override

  if not build_changelist_file:
    return None

  with open(build_changelist_file, 'r') as cl_file:
    for line in cl_file:
      if line.startswith('BUILD_CHANGELIST'):
        return line.rstrip().split(' ')[1]

  return None


def GenerateVersionFileFromTemplate(template_path,
                                    output_path,
                                    version_format,
                                    target_platform,
                                    version_override=None):
  """Generates version file from template file and given parameters.

  Args:
    template_path: A path to template file.
    output_path: A path to generated version file.
      If already exists and the content will not be updated, nothing is done
      (the timestamp is not updated).
    version_format: A string which contains version patterns.
    target_platform: The target platform on which the programs run.
    version_override: An optional string to override BUILD number
      in the template.
      If it is a single number, it means a build number (e.g. "4500").
      If it is a four numbers, it means a full version (e.g. "2.28.4500.0").
  """

  properties = _ParseVersionTemplateFile(template_path, target_platform,
                                         version_override)
  version_definition = _GetVersionInFormat(properties, version_format)
  old_content = ''
  if os.path.exists(output_path):
    # If the target file already exists, need to check the necessity of update
    # to reduce file-creation frequency.
    # Currently generated version file is not seen from Make (and Make like
    # tools) so recreation will not cause serious issue but just in case.
    with open(output_path) as output_file:
      old_content = output_file.read()

  if version_definition != old_content:
    with open(output_path, 'w') as output_file:
      output_file.write(version_definition)


def GenerateVersionFile(version_template_path, version_path, target_platform,
                        version_override=None):
  """Reads the version template file and stores it into version_path.

  This doesn't update the "version_path" if nothing will be changed to
  reduce unnecessary build caused by file timestamp.

  Args:
    version_template_path: a file name which contains the template of version.
    version_path: a file name to be stored the official version.
    target_platform: target platform name. c.f. --target_platform option
    version_override: an optional string to override version number.
      If it is a single number, it means a build number (e.g. "4500").
      If it is a four numbers, it means a full version (e.g. "2.28.4500.0").
  """
  version_format = '\n'.join([
      'MAJOR=@MAJOR@',
      'MINOR=@MINOR@',
      'BUILD=@BUILD@',
      'REVISION=@REVISION@',
      'TARGET_PLATFORM=@TARGET_PLATFORM@',
      'BUILD_OSS=@BUILD_OSS@',
      'QT_VERSION=@QT_VERSION@',
      'ENGINE_VERSION=@ENGINE_VERSION@',
      'DATA_VERSION=@DATA_VERSION@',
  ]) + '\n'
  GenerateVersionFileFromTemplate(
      version_template_path,
      version_path,
      version_format,
      target_platform=target_platform,
      version_override=version_override)


class MozcVersion(object):
  """A class to parse and maintain the version definition data.

  Note that this class is not intended to parse "template" file but to
  "generated" file.
  Typical usage is;
    GenerateVersionFileFromTemplate(template_path, version_path, format)
    version = MozcVersion(version_path)
  """

  def __init__(self, path):
    """Parses a version definition file.

    Args:
      path: A filename which has the version definition.
            If the file is not existent, empty properties are prepared instead.
    """

    self._properties = {}
    if not os.path.isfile(path):
      return
    for line in open(path):
      matchobj = re.match(r'(\w+)=(.*)', line.strip())
      if matchobj:
        var = matchobj.group(1)
        val = matchobj.group(2)
        if var not in self._properties:
          self._properties[var] = val

    # Check mandatory properties.
    for key in VERSION_PROPERTIES:
      if key not in self._properties:
        # Don't raise error nor exit.
        # Error handling is the client's responsibility.
        logging.warning('Mandatory key "%s" does not exist in %s', key, path)

  def IsDevChannel(self):
    """Returns true if the parsed version is dev-channel."""
    revision = self._properties['REVISION']
    return revision is not None and len(revision) >= 3 and revision[-3] == '1'

  def GetTargetPlatform(self):
    """Returns the target platform.

    Returns:
      A string for target platform.
      If the version file is not existent, None is returned.
    """
    return self._properties.get('TARGET_PLATFORM', None)

  def GetVersionString(self):
    """Returns the normal version info string.

    Returns:
      a string in format of "MAJOR.MINOR.BUILD.REVISION"
    """
    return self.GetVersionInFormat('@MAJOR@.@MINOR@.@BUILD@.@REVISION@')

  def GetShortVersionString(self, use_build_oss=False):
    """Returns the short version info string.

    Args:
      use_build_oss: use BUILD_OSS if true.

    Returns:
      a string in format of "MAJOR.MINOR.BUILD"
    """
    if use_build_oss:
      return self.GetVersionInFormat('@MAJOR@.@MINOR@.@BUILD_OSS@')
    return self.GetVersionInFormat('@MAJOR@.@MINOR@.@BUILD@')

  def GetVersionInFormat(self, version_format):
    """Returns the version string based on the specified format."""
    return _GetVersionInFormat(self._properties, version_format)


def main():
  """Generates version file based on the default format.

  Generated file is mozc_version.txt compatible.
  """
  parser = optparse.OptionParser(usage='Usage: %prog ')
  parser.add_option('--template_path', dest='template_path',
                    help='Path to a template version file.')
  parser.add_option('--output', dest='output',
                    help='Path to the output version file.')
  parser.add_option('--target_platform', dest='target_platform',
                    help='Target platform of the version info.')
  parser.add_option('--build_override', dest='build_override',
                    help='Overrides BUILD number in the template.')
  parser.add_option('--build_changelist_file', dest='build_changelist_file',
                    help='Filepath containing the BUILD number.')
  (options, args) = parser.parse_args()
  assert not args, 'Unexpected arguments.'
  assert options.template_path, 'No --template_path was specified.'
  assert options.output, 'No --output was specified.'
  assert options.target_platform, 'No --target_platform was specified.'

  cl_number = _GetChangelistNumber(options.build_override,
                                   options.build_changelist_file)
  GenerateVersionFile(
      version_template_path=options.template_path,
      version_path=options.output,
      target_platform=options.target_platform,
      version_override=cl_number)

if __name__ == '__main__':
  main()
