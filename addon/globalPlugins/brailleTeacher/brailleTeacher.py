# Copyright 2025 Adam Samec <adam.samec@gmail.com>
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2). see <https://www.gnu.org/licenses/gpl-2.0.html>.

import braille
import gui
import speech
import ui
import wx

class BrailleTeacher:
	def __init__(self):
		self.prevSpeechMode = None

	def show(self):
		window = MainWindow(gui.mainFrame, self, title="Braille Teacher")
		window.Raise()
		window.Show()

	def muteSpeech(self):
		self.prevSpeechMode = speech.getState().speechMode
		speech.setSpeechMode(speech.SpeechMode.off)

	def restoreSpeech(self):
		if self.prevSpeechMode is not None:
			speech.setSpeechMode(self.prevSpeechMode)
			self.prevSpeechMode = None

	def displayBraille(self):
		braille.handler.message("Hello world")

class MainWindow(wx.Frame):
	def __init__(self, parent, app, title):
		super(MainWindow, self).__init__(parent, title=title)

		self.app = app
		self.Bind(wx.EVT_CLOSE, self.handleWindowClose)

		self.addWidgets()
		self.SetSize((600, 400))

	def addWidgets(self):
		self.panel = wx.Panel(self)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = gui.guiHelper.BoxSizerHelper(self.panel, wx.VERTICAL)

		self.showBrailleButton = sHelper.addItem(wx.Button(self.panel, label="Show test in braille"))
		self.showBrailleButton.Bind(wx.EVT_BUTTON, self.handleShowBrailleButtonClick)

		self.brailleTextbox = sHelper.addLabeledControl("Read this braille", wx.TextCtrl, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP)
		self.brailleTextbox.Bind(wx.EVT_SET_FOCUS, self.handleBrailleTextboxFocus)
		self.brailleTextbox.Bind(wx.EVT_KILL_FOCUS, self.handleBrailleTextboxFocusOut)
		self.brailleTextbox.SetValue("Read this using your braille display. This may span several lines.")

		self.transcriptTextbox = sHelper.addLabeledControl("Transcribe characters from braille", wx.TextCtrl, style=wx.TE_MULTILINE)

		self.verifyButton = sHelper.addItem(wx.Button(self.panel, label="Verify transcript"))
		self.verifyButton.Bind(wx.EVT_BUTTON, self.handleVerifyButtonClick)

		mainSizer.Add(sHelper.sizer, border=10, flag=wx.ALL)
		mainSizer.Fit(self)
		self.panel.SetSizer(mainSizer)

	def handleWindowClose(self, event):
		self.app.restoreSpeech()
		self.Destroy()

	def handleShowBrailleButtonClick(self, event):
		self.app.displayBraille()

	def handleBrailleTextboxFocus(self, event):
		speech.speakMessage("Read braille")
		self.app.muteSpeech()

	def handleBrailleTextboxFocusOut(self, event):
		self.app.restoreSpeech()

	def handleVerifyButtonClick(self, event):
		dialog = CorrectTranscriptDialog(self, title="Correct transcript")
		dialog.ShowModal()

class CorrectTranscriptDialog(wx.Dialog):
	def __init__(self, parent, title):
		super().__init__(parent, title=title)

		self.addWidgets()
		self.SetSize((300, 200))

	def addWidgets(self):
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = gui.guiHelper.BoxSizerHelper(self, wx.VERTICAL)

		self.transcriptCorrectText = sHelper.addItem(wx.StaticText(self, -1, "The transcript is correct"))

		self.okButton = sHelper.addItem(wx.Button(self, label="Ok"))
		self.okButton.Bind(wx.EVT_BUTTON, self.handleOkButtonClick)

		mainSizer.Add(sHelper.sizer, border=10, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)

	def handleOkButtonClick(self, event):
		self.Close()
