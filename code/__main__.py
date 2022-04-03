from attr.setters import convert
import wx
import asyncio
import os
import shutil
from wx.core import Size
from epub import Epub
from text2speech import Text2Speech

class Epub2AudioApp(wx.Frame):       
   def __init__(self, parent, title): 
      super().__init__(parent = None, title = title, size=(400,300))
      
      self.panel = wx.Panel(self)

      vbox = wx.BoxSizer(wx.VERTICAL)
      
      

      #step 1) choose e-book fle
      lblStep1 = wx.StaticText(self.panel, -1, "Step 1) Choose e-book file") 
      vbox.Add(lblStep1)

      boxFile = wx.BoxSizer(wx.HORIZONTAL)
      
      btnFile = wx.Button(self.panel, label="Choose ebook file...")
      btnFile.Bind(wx.EVT_BUTTON, self.onBtFile)


      boxFile.Add(btnFile, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
 
      self.txtFile = wx.TextCtrl(self.panel, value = "",style = wx.TE_READONLY, size=(300,10))
      boxFile.Add(self.txtFile,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

      vbox.Add(boxFile)

      #step 2) Convert file to text
      lblStep2 = wx.StaticText(self.panel, -1, "Step 2) Convert file to text") 
      vbox.Add(lblStep2)

      boxConvRecordText = wx.BoxSizer(wx.HORIZONTAL)
      
      btnConv = wx.Button(self.panel, label="Convert to text")
      btnConv.Bind(wx.EVT_BUTTON, self.onBtConvert)
      boxConvRecordText.Add(btnConv, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

      vbox.Add(boxConvRecordText)


      #step 3) Choose voice
      lblStep3 = wx.StaticText(self.panel, -1, "Step 3) Choose voice") 
      vbox.Add(lblStep3)

      boxVoice = wx.BoxSizer(wx.HORIZONTAL) 
      lblVoice = wx.StaticText(self.panel, -1, "Voice: ") 
		
      boxVoice.Add(lblVoice, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
      
      lstVoices = ["pt-PT-DuarteNeural", "pt-PT-FernandaNeural", "pt-PT-RaquelNeural", "en-US-AmberNeural", "en-US-ChristopherNeural"]

      self.cbVoices = wx.ComboBox(self.panel, value = lstVoices[0], choices = lstVoices, size=(200,20))
      #cbVoices.Bind(wx.EVT_COMBOBOX, self.ComboBoxEvent)
      boxVoice.Add(self.cbVoices, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

      vbox.Add(boxVoice)

      #step 4) Record audio
      lblStep4 = wx.StaticText(self.panel, -1, "Step 4) Record audio") 
      vbox.Add(lblStep4)

      boxConvRecordAudio = wx.BoxSizer(wx.HORIZONTAL)

      btnOut = wx.Button(self.panel, label="Record")
      btnOut.Bind(wx.EVT_BUTTON, self.onBtRecord)
      boxConvRecordAudio.Add(btnOut, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

      vbox.Add(boxConvRecordAudio)
      
      self.panel.SetSizer(vbox) 
      

      

      self.Centre()
      self.Show()

   def onButton(self, event):
      self.openFileDialog.ShowModal()

   def onBtFile(self, event):
        openFileDialog = wx.FileDialog(self.panel, "Choose book file...", "", "", 
         "EPUB files (*.epub)|*.epub", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_OK:
            self.txtFile.Value = openFileDialog.GetPath()
        openFileDialog.Destroy()

   def onBtConvert(self, event):
      shutil.rmtree('output')
      Epub(self.txtFile.Value)
      path = os.path.realpath('output')
      os.startfile(path)

   def onBtRecord(self, event):
      asyncio.run(Text2Speech.convert(self.cbVoices.GetValue()))
 
   def ComboBoxEvent(self, event):
      cb = event.GetEventObject()
      print(cb.GetStringSelection())
		
   def on_browse(self, event):
        """
        Browse for an image file
        @param event: The event object
        """
        wildcard = "EPUB files (*.epub)|*.epub"
        with wx.FileDialog(None, "Choose a file",
                           wildcard=wildcard,
                           style=wx.ID_OPEN) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.photo_txt.SetValue(dialog.GetPath())
                self.load_image()


if __name__ == '__main__':
    app = wx.App(redirect=False)
    Epub2AudioApp(None,'ePub2audio') 
    app.MainLoop()