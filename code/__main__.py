from attr.setters import convert
import wx
import asyncio
from wx.core import Size
from epub import Epub
from text2speech import Text2Speech

class Epub2AudioApp(wx.Frame):       
   def __init__(self, parent, title): 
      super().__init__(parent = None, title = title)
      
      self.panel = wx.Panel(self)

      vbox = wx.BoxSizer(wx.VERTICAL)

      boxVoice = wx.BoxSizer(wx.HORIZONTAL)
      
      boxVoice = wx.BoxSizer(wx.HORIZONTAL) 
      lblVoice = wx.StaticText(self.panel, -1, "Voice: ") 
		
      boxVoice.Add(lblVoice, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
      
      lstVoices = ["pt-PT-FernandaNeural", "pt-PT-RaquelNeural", "pt-PT-DuarteNeural"]

      cbVoices = wx.ComboBox(self.panel, value = lstVoices[0], choices = lstVoices, size=(200,20))
      #cbVoices.Bind(wx.EVT_COMBOBOX, self.ComboBoxEvent)
      boxVoice.Add(cbVoices, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

      vbox.Add(boxVoice)

      boxFile = wx.BoxSizer(wx.HORIZONTAL)
      
      btnFile = wx.Button(self.panel, label="Choose ebook file...")
      btnFile.Bind(wx.EVT_BUTTON, self.onBtFile)


      boxFile.Add(btnFile, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
 
      self.txtFile = wx.TextCtrl(self.panel, value = "",style = wx.TE_READONLY, size=(300,10))
      boxFile.Add(self.txtFile,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

      vbox.Add(boxFile)

      boxConvRecord = wx.BoxSizer(wx.HORIZONTAL)
      
      btnConv = wx.Button(self.panel, label="Convert to text")
      btnConv.Bind(wx.EVT_BUTTON, self.onBtConvert)
      boxConvRecord.Add(btnConv, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

      btnRec = wx.Button(self.panel, label="Record")
      btnRec.Bind(wx.EVT_BUTTON, self.onBtRecord)
      boxConvRecord.Add(btnRec, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

      vbox.Add(boxConvRecord)

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
      Epub(self.txtFile.Value)

   def onBtRecord(self, event):
      asyncio.run(Text2Speech.convert())
 
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