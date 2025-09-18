# Copyright 2025 Adam Samec <adam.samec@gmail.com>
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2). see <https://www.gnu.org/licenses/gpl-2.0.html>.

import globalPluginHandler
import scriptHandler

from .brailleTeacher import BrailleTeacher

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()

		self.app = BrailleTeacher()

	def terminate(self):
		self.app.terminate()

	def __terminate__(self):
		self.terminate()
		super(GlobalPlugin, self).__terminate__()

	@scriptHandler.script(
		gesture="kb:NVDA+Alt+B",
		# Translators: Gesture description for the Input gestures settings dialog
		description="Shows Braille teacher.",
	)
	def script_show(self, gesture):
		self.app.show()
