# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ObjectListView.ObjectListView import ObjectListView, ColumnDefn
import wx
from DB import Game
import GameContr
from plugins import metacritic, gamerankings


class GameDialog(wx.Dialog):

    def __init__(self, game=None):
        wx.Dialog.__init__(self, None, title="Edit Game", size=(800, 650))
        self.games = GameContr.search("all")
        if game:
            self.id = game.id
            route = game.route
            saga = game.saga
            played = game.played
            downloaded = game.downloaded
            notes = game.notes
            name = game.name
            platform = game.platform
            year = str(game.year)
            genre = game.genre
            style = game.style
            score = str(game.score)
        else:
            played = downloaded = False
            year = score = 0
            route = saga = notes = name = platform = genre = style = ""

        size = (80, -1)
        mainsizer = wx.BoxSizer(wx.VERTICAL)

        # search engines
        searchsizer = wx.BoxSizer(wx.VERTICAL)
        ssearch = wx.StaticText(self, label="Search:", size=size)
        self.tsearch = wx.TextCtrl(self, value=name)
        mihsizer = self.rowbuilder([ssearch, self.tsearch])
        bmeta = wx.Button(self, label="Meta")
        bmeta.Bind(wx.EVT_BUTTON, self.onsearchmeta)
        mihsizer.Add(bmeta, 0, wx.EXPAND)
        brank = wx.Button(self, label="Rank")
        brank.Bind(wx.EVT_BUTTON, self.onsearchrank)
        mihsizer.Add(brank, 0, wx.EXPAND)
        searchsizer.Add(mihsizer, 0, wx.EXPAND)
        self.olvresult = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.olvresult.Bind(wx.EVT_COMMAND_LEFT_DCLICK, self.setdata)
        self.olvresult.SetColumns([
            ColumnDefn("name", "left", 150, "name", isSpaceFilling=True),
            ColumnDefn("year", "left", 40, "year"),
            ColumnDefn("platform", "left", 150, "platform"),
            ColumnDefn("score", "left", 150, "score"),
            ColumnDefn("genre", "left", 150, "genre"),
            ColumnDefn("style", "left", 150, "style"),
            ])
        searchsizer.Add(self.olvresult, 0, wx.EXPAND)
        mainsizer.Add(searchsizer, 0, wx.EXPAND)

        #game fields
        gamesizer = wx.BoxSizer(wx.VERTICAL)
        sname = wx.StaticText(self, label="name:", size=size)
        self.tname = wx.TextCtrl(self, value=name)
        gamesizer.Add(self.rowbuilder([sname, self.tname]), 0, wx.EXPAND)
        syear = wx.StaticText(self, label="Año:", size=size)
        self.tyear = wx.TextCtrl(self, value=str(year))
        gamesizer.Add(self.rowbuilder([syear, self.tyear]), 0, wx.EXPAND)
        sscore = wx.StaticText(self, label="Score:", size=size)
        self.tscore = wx.TextCtrl(self, value=str(score))
        gamesizer.Add(self.rowbuilder([sscore, self.tscore]), 0, wx.EXPAND)
        sdownloaded = wx.StaticText(self, label="Downloaded:", size=size)
        self.tdownloaded = wx.CheckBox(self)
        self.tdownloaded.SetValue(downloaded)
        gamesizer.Add(self.rowbuilder([sdownloaded, self.tdownloaded]), 0, wx.EXPAND)
        splayed = wx.StaticText(self, label="Played:", size=size)
        self.tplayed = wx.CheckBox(self)
        self.tplayed.SetValue(played)
        gamesizer.Add(self.rowbuilder([splayed, self.tplayed]), 0, wx.EXPAND)
        sgenre = wx.StaticText(self, label="Genre:", size=size)
        genres = sorted(list(set([x.genre for x in self.games])))
        self.tgenre = wx.ComboBox(self, size=wx.DefaultSize, choices=genres)
        gamesizer.Add(self.rowbuilder([sgenre, self.tgenre]), 0, wx.EXPAND)
        sstyle = wx.StaticText(self, label="Style:", size=size)
        styles = sorted(list(set([x.style for x in self.games])))
        self.tstyle = wx.ComboBox(self, size=wx.DefaultSize, choices=styles)
        gamesizer.Add(self.rowbuilder([sstyle, self.tstyle]), 0, wx.EXPAND)
        ssaga = wx.StaticText(self, label="Saga:", size=size)
        self.tsaga = wx.TextCtrl(self, value=saga)
        gamesizer.Add(self.rowbuilder([ssaga, self.tsaga]), 0, wx.EXPAND)
        splatform = wx.StaticText(self, label="Platform:", size=size)
        platforms = sorted(list(set([x.platform for x in self.games])))
        self.tplatform = wx.ComboBox(self, size=wx.DefaultSize, choices=platforms)
        gamesizer.Add(self.rowbuilder([splatform, self.tplatform]), 0, wx.EXPAND)
        if game:
            self.tgenre.SetValue(genre)
            self.tstyle.SetValue(style)
            self.tplatform.SetValue(platform)
        sroute = wx.StaticText(self, label="Route:", size=size)
        self.troute = wx.TextCtrl(self, value=route)
        gamesizer.Add(self.rowbuilder([sroute, self.troute]), 0, wx.EXPAND)
        snotes = wx.StaticText(self, label="Notes:", size=size)
        self.tnotes = wx.TextCtrl(self, value=notes)
        gamesizer.Add(self.rowbuilder([snotes, self.tnotes]), 0, wx.EXPAND)
        mainsizer.Add(gamesizer, 1, wx.EXPAND)

        #Actions
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        bok = wx.Button(self, label="Save")
        bok.Bind(wx.EVT_BUTTON, self.onsave)
        btnsizer.Add(bok, 0, wx.ALL, 0)
        broute = wx.Button(self, label="Route")
        broute.Bind(wx.EVT_BUTTON, self.onroute)
        btnsizer.Add(broute, 0, wx.ALL, 0)
        bclose = wx.Button(self, label="Cancel")
        bclose.Bind(wx.EVT_BUTTON, self.onclose)
        btnsizer.Add(bclose, 0, wx.ALL, 0)
        mainsizer.Add(btnsizer, 0, wx.CENTER)

        self.SetSizer(mainsizer)

    def getdata(self):
        """"""
        j = Game()
        j.route = self.troute.GetValue()
        j.year = self.tyear.GetValue()
        j.saga = self.tsaga.GetValue()
        j.played = self.tplayed.GetValue()
        j.downloaded = self.tdownloaded.GetValue()
        j.notes = self.tnotes.GetValue()
        j.name = self.tname.GetValue()
        j.platform = self.tplatform.GetValue()
        j.genre = self.tgenre.GetValue()
        j.style = self.tstyle.GetValue()
        j.score = self.tscore.GetValue()
        return j

    def setdata(self, ev):
        j = self.olvresult.GetSelectedObject()
        self.tname.SetValue(j.name)
        self.tyear.SetValue(str(j.year))
        self.tscore.SetValue(str(j.score))
        self.tplatform.SetValue(j.platform)
        self.tgenre.SetValue(j.genre)
        self.tstyle.SetValue(j.style)
        self.Refresh()

    def onroute(self, ev):
        dialog = wx.DirDialog(None, "Choose path for %s:" % self.tname.GetValue(), defaultPath=r"f:\games", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.troute.SetValue(dialog.GetPath())
        dialog.Destroy()

    def onsearchmeta(self, ev):
        res = metacritic.search(self.tsearch.GetValue(), type="game")
        for r in res:
            b = metacritic.get_info(r.id)
            r.genre = b.genres
            r.style = b.type
            self.olvresult.AddObject(r)

    def onsearchrank(self, ev):
        res = gamerankings.search(self.tsearch.GetValue())
        for r in res:
            b = gamerankings.searchgenre(r)
            self.olvresult.AddObject(b)

    def onadd(self):
        game = self.getdata()
        if not GameContr.add(game):
            midlg = wx.MessageDialog(self, "Game ya existe %s" % game.name, "Error", wx.OK | wx.ICON_WARNING)
            midlg.ShowModal()
            midlg.Destroy()
        self.onclose(None)

    def onclose(self, event):
        """"""
        self.Destroy()

    def onedit(self):
        """"""
        game = self.getdata()
        GameContr.modify(self.id, game)
        self.onclose(None)

    def onsave(self, event):
        """"""
        if self.id:
            self.onedit()
        else:
            self.onadd()

    @staticmethod
    def rowbuilder(widgets):
        """"""
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl, txt = widgets
        sizer.Add(lbl, 0, wx.ALL, 5)
        sizer.Add(txt, 1, wx.EXPAND | wx.ALL, 5)
        return sizer

if __name__ == "__main__":
    app = wx.App(False)
    dlg = GameDialog()
    dlg.ShowModal()
    app.MainLoop()