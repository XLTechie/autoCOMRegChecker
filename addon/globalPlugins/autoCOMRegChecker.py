# Automatic COM Registration Checker: an NVDA add-on
# Copyright (c) 2024, Luke Davis and Open Source Systems, Ltd., all rights reserved.
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by    the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import wx
import schedule
import time

import gui
import globalPluginHandler
from logHandler import log
from addonHandler import initTranslation
from utils.schedule import scheduleThread, ThreadTarget
from core import postNvdaStartup

CHECK_REGISTRATIONS_AFTER_MINUTES = 5
"""
Perform the COM registration check every VALUE minutes.
"""

try:
	initTranslation()
except:  # Probably running in scratchpad
	pass

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self) -> None:
		# Wait until NVDA is fully operational to setup the run schedule
		postNvdaStartup.register(self._scheduleJob)

	def _scheduleJob(self) -> None:
		scheduleThread.scheduleJob(
			self.checkCOMRegistrationsUsingTools,
			schedule.every(CHECK_REGISTRATIONS_AFTER_MINUTES).minutes,
			queueToThread=ThreadTarget.GUI
		)

	def checkCOMRegistrationsUsingTools(self):
		log.info("Running scheduled check for good COM registrations.")
