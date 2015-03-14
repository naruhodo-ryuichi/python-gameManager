# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import wx
from ObjectListView import GroupListView, ColumnDefn
import GameContr
import GameGui


class GamesFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Games", size=(1024, 768))
        self.games = GameContr.search("all")
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        searchsizer = wx.BoxSizer(wx.HORIZONTAL)
        ssearch = wx.StaticText(self, label="Search:")
        searchsizer.Add(ssearch, 0, wx.EXPAND)
        self.tsearch = wx.TextCtrl(self)
        self.tsearch.Bind(wx.EVT_TEXT, self.onsearch)
        searchsizer.Add(self.tsearch, 0, wx.EXPAND)
        genres = sorted(list(set([x.genre for x in self.games])))
        self.bgenres = wx.ComboBox(self, size=wx.DefaultSize, choices=genres)
        self.bgenres.Bind(wx.EVT_COMBOBOX, self.onsearch)
        searchsizer.Add(self.bgenres, 0, wx.ALL | wx.EXPAND, 0)
        sistemas = sorted(list(set([x.platform for x in self.games if "," not in x.platform])))
        self.bsistemas = wx.ComboBox(self, size=wx.DefaultSize, choices=sistemas)
        self.bsistemas.Bind(wx.EVT_COMBOBOX, self.onsearch)
        searchsizer.Add(self.bsistemas, 0, wx.ALL | wx.EXPAND, 0)
        sdownloadeds = wx.StaticText(self, wx.ID_ANY, "Downloadeds")
        searchsizer.Add(sdownloadeds, 0, wx.ALL, 0)
        self.cdownloadeds = wx.CheckBox(self, style=wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        self.cdownloadeds.Set3StateValue(2)
        self.cdownloadeds.Bind(wx.EVT_CHECKBOX, self.onsearch)
        searchsizer.Add(self.cdownloadeds, 0, wx.ALL, 0)
        splayeds = wx.StaticText(self, wx.ID_ANY, "Playeds")
        searchsizer.Add(splayeds, 0, wx.ALL, 0)
        self.cplayeds = wx.CheckBox(self, style=wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        self.cplayeds.Set3StateValue(2)
        self.cplayeds.Bind(wx.EVT_CHECKBOX, self.onsearch)
        searchsizer.Add(self.cplayeds, 0, wx.ALL, 0)
        sroute = wx.StaticText(self, wx.ID_ANY, "Route")
        searchsizer.Add(sroute, 0, wx.ALL, 0)
        self.croute = wx.CheckBox(self, style=wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        self.croute.Set3StateValue(2)
        self.croute.Bind(wx.EVT_CHECKBOX, self.onsearch)
        searchsizer.Add(self.croute, 0, wx.ALL, 0)
        mainsizer.Add(searchsizer, 0, wx.CENTER)
        searchbtn = wx.Button(self, label="Search")
        searchbtn.Bind(wx.EVT_BUTTON, self.onsearch)
        searchsizer.Add(searchbtn, 0, wx.ALL, 0)

        self.olvgames = GroupListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.olvgames.SetEmptyListMsg("No se encontraron games")
        self.olvgames.SetColumns([
            ColumnDefn("Genre", "left", 50, "genre", groupKeyGetter="genre"),
            ColumnDefn("Name", "left", 150, "name", isSpaceFilling=True),
            ColumnDefn("Year", "left", 40, "year"),
            ColumnDefn("Score", "left", 50, "score"),
            ColumnDefn("Downloaded", "left", 40, checkStateGetter="downloaded"),
            ColumnDefn("Played", "left", 40, checkStateGetter="played"),
            ColumnDefn("Platform", "left", 150, "platform"),
            ColumnDefn("Style", "left", 150, "style"),
            ])
        self.olvgames.SetObjects(self.games)
        self.olvgames.Bind(wx.EVT_COMMAND_LEFT_DCLICK, self.onedit)
        mainsizer.Add(self.olvgames, 1, wx.ALL | wx.EXPAND, 0)

        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        bnew = wx.Button(self, label="New")
        bnew.Bind(wx.EVT_BUTTON, self.onadd)
        btnsizer.Add(bnew, 0, wx.ALL, 0)
        bedit = wx.Button(self, label="Edit")
        bedit.Bind(wx.EVT_BUTTON, self.onedit)
        btnsizer.Add(bedit, 0, wx.ALL, 0)
        bdelete = wx.Button(self, label="Delete")
        bdelete.Bind(wx.EVT_BUTTON, self.ondelete)
        btnsizer.Add(bdelete, 0, wx.ALL, 0)
        ball = wx.Button(self, label="All")
        ball.Bind(wx.EVT_BUTTON, self.onsearch)
        btnsizer.Add(ball, 0, wx.ALL, 0)
        bbnews = wx.Button(self, label="Search New")
        bbnews.Bind(wx.EVT_BUTTON, self.onsearchnews)
        btnsizer.Add(bbnews, 0, wx.ALL, 0)
        mainsizer.Add(btnsizer, 0, wx.CENTER)

        self.SetSizer(mainsizer)
        self.Show()

    def onsearchnew(self, ev):
        news = GameContr.searchnew()
        for j in news:
            j.downloaded = True
            j.played = False
            dlg = GameGui.GameDialog(game=j)
            dlg.ShowModal()
            dlg.Destroy()
        self.onsearch(None)

    def onsearch(self, ev):
        games = GameContr.search("name", self.tsearch.GetValue())
        games = [j for j in games if self.bsistemas.GetValue() in j.platform]
        games = [j for j in games if self.bgenres.GetValue() in j.genre]
        cdownloadeds = self.tristate(self.cdownloadeds.Get3StateValue())
        if cdownloadeds is not None:
            games = [j for j in games if j.downloaded == cdownloadeds]
        cplayeds = self.tristate(self.cplayeds.Get3StateValue())
        if cplayeds is not None:
            games = [j for j in games if j.played == cplayeds]
        croute = self.tristate(self.croute.Get3StateValue())
        if croute is not None:
            games = [j for j in games if (j.route == "") != croute]
        self.games = games
        self.olvgames.SetObjects(self.games)

    def onadd(self, event):
        dlg = GameGui.GameDialog()
        dlg.ShowModal()
        dlg.Destroy()
        self.onsearch(None)

    def onedit(self, event):
        selectedrow = self.olvgames.GetSelectedObject()
        game = GameContr.search("id", selectedrow.id)
        dlg = GameGui.GameDialog(game)
        dlg.ShowModal()
        dlg.Destroy()
        self.onsearch(None)

    def ondelete(self, event):
        selectedrow = self.olvgames.GetSelectedObject()
        GameContr.delete(selectedrow.id)
        self.onsearch(None)

    @staticmethod
    def tristate(box):
        ret = None
        if box == 1:
            ret = True
        elif box == 0:
            ret = False
        return ret

    @staticmethod
    def rowbuilder(widgets):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl, txt = widgets
        sizer.Add(lbl, 0, wx.ALL, 5)
        sizer.Add(txt, 1, wx.EXPAND | wx.ALL, 5)
        return sizer

if __name__ == "__main__":
    app = wx.App(False)
    frame = GamesFrame()
    app.MainLoop()