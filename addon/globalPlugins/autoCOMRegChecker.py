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

import wx
import os
import subprocess
import schedule
import time
import winVersion

import globalPluginHandler
from gui.message import isModalMessageBoxActive, messageBox
from utils.schedule import (
	scheduleThread,
	ThreadTarget
)
from logHandler import log
from addonHandler import (
	initTranslation,
	AddonError
)
from core import postNvdaStartup
from COMRegistrationFixes import (
	SYSTEM_ROOT,
	SYSTEM32,
	SYSNATIVE,
)

CHECK_REGISTRATIONS_AFTER_MINUTES = 5
"""
Perform the COM registration check every VALUE minutes.
"""

try:
	initTranslation()
except AddonError:  # Probably running in scratchpad
	pass

# Constants
OLEACC_PROXY_BASE: str = r"HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{618736E0-3C3D-11CF-810C-00AA00389B71}"
REG32EXE = os.path.join(SYSTEM32, "reg.exe")
REG64EXE = os.path.join(SYSNATIVE, "reg.exe")

# Keys and values to check
goodRegEntries: tuple = (  # Key, Expected value
	(OLEACC_PROXY_BASE, "IAccessible"),
	(rf"{OLEACC_PROXY_BASE}\ProxyStubClsid32", "{03022430-ABC4-11D0-BDE2-00AA001A1953}"),
)
badRegEntries: tuple = (  # These shouldn't exist
	rf"{OLEACC_PROXY_BASE}\TypeLib"
)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self) -> None:
		super().__init__()
		winVer = winVersion.getWinVer()
		OSMajorMinor = (winVer.major, winVer.minor)
		self.is64bit = winVer.processorArchitecture.endswith("64")
		# Wait until NVDA is fully operational to setup the run schedule
		postNvdaStartup.register(self._scheduleJob)

	def _scheduleJob(self) -> None:
		scheduleThread.scheduleJob(
			self.checkCOMRegistrationsUsingTools,
			schedule.every(CHECK_REGISTRATIONS_AFTER_MINUTES).minutes,
			queueToThread=ThreadTarget.DAEMON
		)

	def checkCOMRegistrationsUsingTools(self):
		log.info("Running scheduled check for COM registrations.")

	def checkForBadRegistrations(self) -> bool:

	def checkReg(self, key: str, val: str | None = None) -> bool:
		# Make sure a console window doesn't show when running reg.exe
		startupInfo = subprocess.STARTUPINFO()
		startupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		startupInfo.wShowWindow = subprocess.SW_HIDE
		try:
			subprocess.check32call([REG_EXE, "/s", fileName], startupinfo=startupInfo)
		except subprocess.CalledProcessError as e:
			log.error(rf"Error getting registration of key \"{key}\" in a 32-bit context: {e}")
