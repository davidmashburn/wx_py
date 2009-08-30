"""PySlices combines the slices and filling into one control."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com> / "
__author__ += "David N. Mashburn <david.n.mashburn@gmail.com>"
__cvsid__ = "$Id: crust.py 44235 2007-01-17 23:05:14Z RD $"
__revision__ = "$Revision: 44235 $"[11:-2]

import wx

import os
import pprint
import re
import sys

import dispatcher
import document
import editwindow
import editor
from filling import Filling
import frame
from slices import Shell as Slice_Shell
from version import VERSION


class CrustSlices(wx.SplitterWindow):
    """Slices based on SplitterWindow."""

    name = 'Slices'
    revision = __revision__
    sashoffset = 300

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.SP_3D|wx.SP_LIVE_UPDATE,
                 name='Slices Window', rootObject=None, rootLabel=None,
                 rootIsNamespace=True, intro='', locals=None,
                 InterpClass=None,
                 startupScript=None, execStartupScript=True,
                 showPySlicesTutorial=True,
                 enableShellMode=False, hideFoldingMargin=False,
                 *args, **kwds):
        """Create CrustSlices instance."""
        wx.SplitterWindow.__init__(self, parent, id, pos, size, style, name)

        # Turn off the tab-traversal style that is automatically
        # turned on by wx.SplitterWindow.  We do this because on
        # Windows the event for Ctrl-Enter is stolen and used as a
        # navigation key, but the Shell window uses it to insert lines.
        style = self.GetWindowStyle()
        self.SetWindowStyle(style & ~wx.TAB_TRAVERSAL)
        
        self.shell = Slice_Shell(parent=self, introText=intro,
                                 locals=locals, InterpClass=InterpClass,
                                 startupScript=startupScript,
                                 execStartupScript=execStartupScript,
                                 showPySlicesTutorial=showPySlicesTutorial,
                                 enableShellMode=enableShellMode,
                                 hideFoldingMargin=hideFoldingMargin,
                                 *args, **kwds)
        
        self.editor = self.shell
        if rootObject is None:
            rootObject = self.shell.interp.locals
        self.notebook = wx.Notebook(parent=self, id=-1)
        self.shell.interp.locals['notebook'] = self.notebook
        self.filling = Filling(parent=self.notebook,
                               rootObject=rootObject,
                               rootLabel=rootLabel,
                               rootIsNamespace=rootIsNamespace)
        # Add 'filling' to the interpreter's locals.
        self.shell.interp.locals['filling'] = self.filling
        self.notebook.AddPage(page=self.filling, text='Namespace', select=True)
        
        self.display = Display(parent=self.notebook)
        self.notebook.AddPage(page=self.display, text='Display')
        # Add 'pp' (pretty print) to the interpreter's locals.
        self.shell.interp.locals['pp'] = self.display.setItem
        self.display.nbTab = self.notebook.GetPageCount()-1
        
        self.calltip = Calltip(parent=self.notebook)
        self.notebook.AddPage(page=self.calltip, text='Calltip')
        
        self.sessionlisting = SessionListing(parent=self.notebook)
        self.notebook.AddPage(page=self.sessionlisting, text='History')
        
        self.dispatcherlisting = DispatcherListing(parent=self.notebook)
        self.notebook.AddPage(page=self.dispatcherlisting, text='Dispatcher')

        
        # Initialize in an unsplit mode, and check later after loading
        # settings if we should split or not.
        self.shell.Hide()
        self.notebook.Hide()
        self.Initialize(self.shell)
        self._shouldsplit = True
        wx.CallAfter(self._CheckShouldSplit)
        self.SetMinimumPaneSize(100)

        self.Bind(wx.EVT_SIZE, self.SplitterOnSize)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnChanged)
        self.Bind(wx.EVT_SPLITTER_DCLICK, self.OnSashDClick)

    def _CheckShouldSplit(self):
        if self._shouldsplit:
            self.SplitHorizontally(self.shell, self.notebook, -self.sashoffset)
            self.lastsashpos = self.GetSashPosition()
        else:
            self.lastsashpos = -1
        self.issplit = self.IsSplit()       

    def ToggleTools(self):
        """Toggle the display of the filling and other tools"""
        if self.issplit:
            self.Unsplit()
        else:
            self.SplitHorizontally(self.shell, self.notebook, -self.sashoffset)
            self.lastsashpos = self.GetSashPosition()
        self.issplit = self.IsSplit()

    def ToolsShown(self):
        return self.issplit

    def OnChanged(self, event):
        """update sash offset from the bottom of the window"""
        self.sashoffset = self.GetSize().height - event.GetSashPosition()
        self.lastsashpos = event.GetSashPosition()
        event.Skip()

    def OnSashDClick(self, event):
        self.Unsplit()
        self.issplit = False

    # Make the splitter expand the top window when resized
    def SplitterOnSize(self, event):
        splitter = event.GetEventObject()
        sz = splitter.GetSize()
        splitter.SetSashPosition(sz.height - self.sashoffset, True)
        event.Skip()


    def LoadSettings(self, config):
        self.shell.LoadSettings(config)
        self.filling.LoadSettings(config)

        pos = config.ReadInt('Sash/CrustPos', 400)
        wx.CallAfter(self.SetSashPosition, pos)
        def _updateSashPosValue():
            sz = self.GetSize()
            self.sashoffset = sz.height - self.GetSashPosition()
        wx.CallAfter(_updateSashPosValue)
        zoom = config.ReadInt('View/Zoom/Display', -99)
        if zoom != -99:
            self.display.SetZoom(zoom)
        self.issplit = config.ReadInt('Sash/IsSplit', True)
        if not self.issplit:
            self._shouldsplit = False

    def SaveSettings(self, config):
        self.shell.SaveSettings(config)
        self.filling.SaveSettings(config)

        if self.lastsashpos != -1:
            config.WriteInt('Sash/CrustPos', self.lastsashpos)
        config.WriteInt('Sash/IsSplit', self.issplit)
        config.WriteInt('View/Zoom/Display', self.display.GetZoom())
        

           


class Display(editwindow.EditWindow):
    """STC used to display an object using Pretty Print."""

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.CLIP_CHILDREN | wx.SUNKEN_BORDER,
                 static=False):
        """Create Display instance."""
        editwindow.EditWindow.__init__(self, parent, id, pos, size, style)
        # Configure various defaults and user preferences.
        self.SetReadOnly(True)
        self.SetWrapMode(False)
        if not static:
            dispatcher.connect(receiver=self.push, signal='Interpreter.push')

    def push(self, command, more):
        """Receiver for Interpreter.push signal."""
        self.Refresh()

    def Refresh(self):
        if not hasattr(self, "item"):
            return
        self.SetReadOnly(False)
        text = pprint.pformat(self.item)
        self.SetText(text)
        self.SetReadOnly(True)

    def setItem(self, item):
        """Set item to pretty print in the notebook Display tab."""
        self.item = item
        self.Refresh()
        if self.GetParent().GetSelection() != self.nbTab:
            focus = wx.Window.FindFocus()
            self.GetParent().SetSelection(self.nbTab)
            wx.CallAfter(focus.SetFocus)
            

# TODO: Switch this to a editwindow.EditWindow
class Calltip(wx.TextCtrl):
    """Text control containing the most recent shell calltip."""

    def __init__(self, parent=None, id=-1):
        style = (wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        wx.TextCtrl.__init__(self, parent, id, style=style)
        self.SetBackgroundColour(wx.Colour(255, 255, 208))
        dispatcher.connect(receiver=self.display, signal='Shell.calltip')

        df = self.GetFont()
        font = wx.Font(df.GetPointSize(), wx.TELETYPE, wx.NORMAL, wx.NORMAL)
        self.SetFont(font)

    def display(self, calltip):
        """Receiver for Shell.calltip signal."""
        ## self.SetValue(calltip)  # Caused refresh problem on Windows.
        self.Clear()
        self.AppendText(calltip)


# TODO: Switch this to a editwindow.EditWindow
class SessionListing(wx.TextCtrl):
    """Text control containing all commands for session."""

    def __init__(self, parent=None, id=-1):
        style = (wx.TE_MULTILINE | wx.TE_READONLY |
                 wx.TE_RICH2 | wx.TE_DONTWRAP)
        wx.TextCtrl.__init__(self, parent, id, style=style)
        dispatcher.connect(receiver=self.addHistory,
                           signal="Shell.addHistory")
        dispatcher.connect(receiver=self.clearHistory,
                           signal="Shell.clearHistory")
        dispatcher.connect(receiver=self.loadHistory,
                           signal="Shell.loadHistory")

        df = self.GetFont()
        font = wx.Font(df.GetPointSize(), wx.TELETYPE, wx.NORMAL, wx.NORMAL)
        self.SetFont(font)

    def loadHistory(self, history):
        # preload the existing history, if any
        hist = history[:]
        hist.reverse()
        self.SetValue('\n'.join(hist) + '\n')
        self.SetInsertionPointEnd()

    def addHistory(self, command):
        if command:
            self.SetInsertionPointEnd()
            self.AppendText(command + '\n')

    def clearHistory(self):
        self.SetValue("")


class DispatcherListing(wx.TextCtrl):
    """Text control containing all dispatches for session."""

    def __init__(self, parent=None, id=-1):
        style = (wx.TE_MULTILINE | wx.TE_READONLY |
                 wx.TE_RICH2 | wx.TE_DONTWRAP)
        wx.TextCtrl.__init__(self, parent, id, style=style)
        dispatcher.connect(receiver=self.spy)

        df = self.GetFont()
        font = wx.Font(df.GetPointSize(), wx.TELETYPE, wx.NORMAL, wx.NORMAL)
        self.SetFont(font)

    def spy(self, signal, sender):
        """Receiver for Any signal from Any sender."""
        text = '%r from %s' % (signal, sender)
        self.SetInsertionPointEnd()
        start, end = self.GetSelection()
        if start != end:
            self.SetSelection(0, 0)
        self.AppendText(text + '\n')



class CrustSlicesFrame(frame.Frame, frame.ShellFrameMixin):
    """Frame containing all the PySlices components."""

    name = 'SliceFrame'
    revision = __revision__


    def __init__(self, parent=None, id=-1, title='PySlices',
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE,
                 rootObject=None, rootLabel=None, rootIsNamespace=True,
                 locals=None, InterpClass=None,
                 config=None, dataDir=None,
                 *args, **kwds):
        """Create CrustFrame instance."""
        frame.Frame.__init__(self, parent, id, title, pos, size, style,
                             shellName='PySlices')
        frame.ShellFrameMixin.__init__(self, config, dataDir)
        
        if size == wx.DefaultSize:
            self.SetSize((800, 600))
        
        intro = 'PySlices %s - The Flakiest Python Shell... Cut up!' % VERSION
        
        self.SetStatusText(intro.replace('\n', ', '))
        self.crust = CrustSlices(parent=self, intro=intro,
                                 rootObject=rootObject,
                                 rootLabel=rootLabel,
                                 rootIsNamespace=rootIsNamespace,
                                 locals=locals,
                                 InterpClass=InterpClass,
                                 startupScript=self.startupScript,
                                 execStartupScript=self.execStartupScript,
                                 showPySlicesTutorial=self.showPySlicesTutorial,
                                 enableShellMode=self.enableShellMode,
                                 hideFoldingMargin=self.hideFoldingMargin,
                                 *args, **kwds)
        self.shell = self.crust.shell
        self.buffer = self.shell.buffer
        # Override the filling so that status messages go to the status bar.
        self.crust.filling.tree.setStatusText = self.SetStatusText
        
        # Override the shell so that status messages go to the status bar.
        self.shell.setStatusText = self.SetStatusText
        
        self.shell.SetFocus()
        self.LoadSettings()
        
        self.Bind(wx.EVT_IDLE, self.OnIdle)

    def OnClose(self, event):
        """Event handler for closing."""
        self.bufferClose()
    
    def OnAbout(self, event):
        """Display an About window."""
        title = 'About PyCrust'
        text = 'PyCrust %s\n\n' % VERSION + \
               'Yet another Python shell, only flakier.\n\n' + \
               'Half-baked by Patrick K. O\'Brien,\n' + \
               'the other half is still in the oven.\n\n' + \
               'Shell Revision: %s\n' % self.shell.revision + \
               'Interpreter Revision: %s\n\n' % self.shell.interp.revision + \
               'Platform: %s\n' % sys.platform + \
               'Python Version: %s\n' % sys.version.split()[0] + \
               'wxPython Version: %s\n' % wx.VERSION_STRING + \
               ('\t(%s)\n' % ", ".join(wx.PlatformInfo[1:]))
        dialog = wx.MessageDialog(self, text, title,
                                  wx.OK | wx.ICON_INFORMATION)
        dialog.ShowModal()
        dialog.Destroy()

    def ToggleTools(self):
        """Toggle the display of the filling and other tools"""
        return self.crust.ToggleTools()

    def ToolsShown(self):
        return self.crust.ToolsShown()

    def OnHelp(self, event):
        """Show a help dialog."""
        frame.ShellFrameMixin.OnHelp(self, event)
    
    def OnEnableShellMode(self,event):
        """Change between Slices Mode and Shell Mode"""
        frame.Frame.OnEnableShellMode(self,event)
        self.shell.ToggleShellMode(self.enableShellMode)
    
    def OnHideFoldingMargin(self,event):
        """Change between Slices Mode and Shell Mode"""
        frame.Frame.OnHideFoldingMargin(self,event)
        self.shell.ToggleFoldingMargin(self.hideFoldingMargin)

    def LoadSettings(self):
        if self.config is not None:
            frame.ShellFrameMixin.LoadSettings(self)
            frame.Frame.LoadSettings(self, self.config)
            self.crust.LoadSettings(self.config)


    def SaveSettings(self, force=False):
        if self.config is not None:
            frame.ShellFrameMixin.SaveSettings(self,force)
            if self.autoSaveSettings or force:
                frame.Frame.SaveSettings(self, self.config)
                self.crust.SaveSettings(self.config)


    def DoSaveSettings(self):
        if self.config is not None:
            self.SaveSettings(force=True)
            self.config.Flush()
    # Stolen Straight from editor.EditorFrame
    # Modified a little... :)
    # ||
    # \/
    def OnIdle(self, event):
        """Event handler for idle time."""
        self._updateTitle()
        event.Skip()
    
    def _updateTitle(self):
        """Show current title information."""
        title = self.GetTitle()
        if self.bufferHasChanged():
            if title.startswith('* '):
                pass
            else:
                self.SetTitle('* ' + title)
        else:
            if title.startswith('* '):
                self.SetTitle(title[2:])
    
    def hasBuffer(self):
        """Return True if there is a current buffer."""
        if self.buffer:
            return True
        else:
            return False

    def bufferClose(self):
        """Close buffer."""
        if self.buffer.hasChanged():
            cancel = self.bufferSuggestSave()
            if cancel and event.CanVeto():
                event.Veto()
                return cancel
        self.SaveSettings()
        self.crust.shell.destroy()
        self.bufferDestroy()
        self.Destroy()
        
        return False

    def bufferCreate(self, filename=None):
        """Create new buffer."""
        self.bufferDestroy()
        buffer = Buffer()
        self.panel = panel = wx.Panel(parent=self, id=-1)
        panel.Bind (wx.EVT_ERASE_BACKGROUND, lambda x: x)        
        editor = Editor(parent=panel)
        panel.editor = editor
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(editor.window, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)
        sizer.Layout()
        buffer.addEditor(editor)
        buffer.open(filename)
        self.setEditor(editor)
        self.editor.setFocus()
        self.SendSizeEvent()
        

    def bufferDestroy(self):
        """Destroy the current buffer."""
        if self.buffer:
            self.editor = None
            self.buffer = None


    def bufferHasChanged(self):
        """Return True if buffer has changed since last save."""
        if self.buffer:
            return self.buffer.hasChanged()
        else:
            return False

    def bufferNew(self):
        """Create new buffer."""
        if self.bufferHasChanged():
            cancel = self.bufferSuggestSave()
            if cancel:
                return cancel
        self.bufferCreate()
        cancel = False
        return cancel

    def bufferOpen(self):
        """Open file in buffer."""
        if self.bufferHasChanged():
            cancel = self.bufferSuggestSave()
            if cancel:
                return cancel
        
        file=wx.FileSelector("Load File As New Slice")
        if file!=u'':
            fid=open(file,'r')
            self.shell.LoadPySlicesFile(fid)
            fid.close()
            self.SetTitle( os.path.split(file)[1] + ' - PySlices')
            self.shell.NeedsCheckForSave=False
            self.shell.SetSavePoint()
            self.buffer.doc = document.Document(file)
            self.buffer.name = self.buffer.doc.filename
            self.buffer.modulename = self.buffer.doc.filebase
        return
    
##     def bufferPrint(self):
##         """Print buffer."""
##         pass

##     def bufferRevert(self):
##         """Revert buffer to version of file on disk."""
##         pass
    
    # was self.buffer.save(self): # """Save buffer."""
    def simpleSave(self,confirmed=False):
        filepath = self.buffer.doc.filepath
        self.buffer.confirmed = confirmed
        if not filepath:
            return  # XXX Get filename
        if not os.path.exists(filepath):
            self.buffer.confirmed = True
        if not self.buffer.confirmed:
            self.buffer.confirmed = self.buffer.overwriteConfirm(filepath)
        if self.buffer.confirmed:
            try:
                fid = open(filepath, 'wb')
                self.shell.SavePySlicesFile(fid)
            finally:
                if fid:
                    fid.close()
            self.shell.SetSavePoint()
            self.SetTitle( os.path.split(filepath)[1] + ' - PySlices')
            self.shell.NeedsCheckForSave=False
    
    def bufferSave(self):
        """Save buffer to its file."""
        if self.buffer.doc.filepath:
            # self.buffer.save()
            self.simpleSave(confirmed=True)
            cancel = False
        else:
            cancel = self.bufferSaveAs()
        return cancel

    def bufferSaveAs(self):
        """Save buffer to a new filename."""
        if self.bufferHasChanged() and self.buffer.doc.filepath:
            cancel = self.bufferSuggestSave()
            if cancel:
                return cancel
        filedir = ''
        if self.buffer and self.buffer.doc.filedir:
            filedir = self.buffer.doc.filedir
        result = editor.saveSingle(title='Save PySlices File',directory=filedir,
                                   wildcard='PySlices Files (*.pyslices)|*.pyslices')
        if result.path!='':
            if result.path[-9:]!=".pyslices":
                result.path+=".pyslices"
        if result.path:
            self.buffer.doc = document.Document(result.path)
            self.buffer.name = self.buffer.doc.filename
            self.buffer.modulename = self.buffer.doc.filebase
            self.simpleSave()
            cancel = False
        else:
            cancel = True
        return cancel
    
    def bufferSuggestSave(self):
        """Suggest saving changes.  Return True if user selected Cancel."""
        result = editor.messageDialog(parent=None,
                               message='%s has changed.\n'
                                       'Would you like to save it first'
                                       '?' % self.buffer.name,
                               title='Save current file?',
                               style=wx.YES_NO | wx.CANCEL | wx.NO_DEFAULT |
                                     wx.CENTRE | wx.ICON_QUESTION )
        if result.positive:
            cancel = self.bufferSave()
        else:
            cancel = result.text == 'Cancel'
        return cancel

    def updateNamespace(self):
        """Update the buffer namespace for autocompletion and calltips."""
        if self.buffer.updateNamespace():
            self.SetStatusText('Namespace updated')
        else:
            self.SetStatusText('Error executing, unable to update namespace')
