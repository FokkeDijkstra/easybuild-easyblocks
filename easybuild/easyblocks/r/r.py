##
# Copyright 2012-2013 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of the University of Ghent (http://ugent.be/hpc).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild. If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for building and installing R, implemented as an easyblock

@author: Jens Timmerman (Ghent University)
"""
from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.tools import environment

def exts_filter_for_R_packages():
    """Return extension filter details for R packages."""
    return ["R -q --no-save", "library(%(name)s)"]

class EB_R(ConfigureMake):
    """
    Build and install R, including list of libraries specified as extensions.
    Install specified version of libraries, install hard-coded library version
    or latest library version (in that order of preference)
    """

    def prepare_for_extensions(self):
        """
        We set some default configs here for R packages
        """
        # insert new packages by building them with RPackage
        self.cfg['exts_defaultclass'] = "RPackage"
        self.cfg['exts_filter'] = exts_filter_for_R_packages()

    def configure_step(self):
        """Configuration step, we set FC, F77 is already set by EasyBuild to the right compiler,
        FC is used for Fortan90"""
        environment.setvar("FC", self.toolchain.get_variable('F90'))
        ConfigureMake.configure_step(self)

    def extra_packages_pre(self):
        """
        We set some default configs here for extentions for R.
        """
        self.setcfg('pkgdefaultclass', ['easybuild.easyblocks.rextension', "EB_RExtension"])
        self.setcfg('pkgfilter', ["R -q --no-save", "library(%(name)s)"])
        self.setcfg('pkgtemplate', '%(name)s/%(name)s_%(version)s.tar.gz')
        self.setcfg('pkginstalldeps', True)
