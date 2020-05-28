# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import datetime
import os
import urllib
import yaml
import re
import platform
import webbrowser
import json
# 公用方法


def fileInfoObj(filepath):
    path_name, ext_dot = os.path.splitext(filepath)
    path, name = path_name.rsplit('\\', 1)
    ext = ext_dot.replace('.', '', 1)
    return {
        'path': path,               # /user
        'name': name,               # a
        'ext_dot': ext_dot,         # .txt
        'ext': ext,                 # txt
        'name_ext': name + ext_dot,  # a.txt
    }

# 获取当前日期


class GetDateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        t = datetime.datetime.now()
        curIsoTime = t.isoformat(' ').split('.', maxsplit=1)[0]
        selList = self.view.sel()
        for selRegion in selList:
            self.view.insert(edit, selRegion.a, curIsoTime)

# 在浏览器中打开


class OpenInBrowerCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        path = kwargs.get('url', None) if kwargs.get(
            'url', None) else self.view.file_name()
        path = 'file://' + path
        webbrowser.open_new_tab(path)

# 打开 js 文档


class OpenJsDocCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # jsDocPath = 'file://' + sublime.packages_path() + '/User/MySubl/wangdoc-js/index.html'
        pPath = 'file://' + sublime.packages_path()
        jsDocPath = pPath + '/User/MySubl/wangdoc-js/index.html'
        webbrowser.open_new_tab(jsDocPath)

# 打开 Finder


class OpenFinderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        path = os.path.expanduser('~/it/')
        sublime.active_window().run_command("open_dir", {"dir": path})

# 打开 Sublime User 目录


class OpenUserDirCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        path = sublime.packages_path() + '/User'
        sublime.active_window().run_command("open_dir", {"dir": path})

# 打开补全文件


class OpenCompletionsFileCommand(sublime_plugin.WindowCommand):

    def run(self):
        # view = self.window.active_view()
        path = sublime.packages_path() + '/User/MySubl/js.sublime-completions'
        self.window.open_file(path)

# 打开 tools.py 文件
class OpenToolsFileCommand(sublime_plugin.WindowCommand):

    def run(self):
        # view = self.window.active_view()
        toolPath = sublime.packages_path() + '/User/tools.py'
        commandPath = sublime.packages_path() + '/User/Default.sublime-commands'
        self.window.open_file(commandPath)
        self.window.open_file(toolPath)

# 打开tips文件


class OpenTipsCommand(sublime_plugin.WindowCommand):

    def run(self):
        # view = self.window.active_view()
        path = '/Users/hf/it/note/dev/developer/tips.md'
        self.window.open_file(path)


# 将选择的文本转换为 completions
class VuexAttrCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        selList = self.view.sel()
        for selRegion in selList:
            selTxt = self.view.substr(selRegion)
            print(11111, selTxt)
            getterStr = "\tweightModifyInterFace (state) {\n\t\treturn state.weightModifyInterFace\n\t},\n"
            setterStr = "\tSET_weightModifyInterFace (state, param) {\n\t\tstate.weightModifyInterFace = param\n\t},\n"
            actionStr = "\tasync SET_weightModifyInterFace_ASYNC ({ commit }, param) {\n\t\tcommit('SET_weightModifyInterFace', param)\n\t},"
            allStr = getterStr + setterStr + actionStr
            formatedStr = allStr.replace('weightModifyInterFace', selTxt)
            self.view.replace(edit,  sublime.Region(selRegion.a, selRegion.b), formatedStr)

class SelToCompletionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        letters = {'aa': '1', 'bb': '2', 'cc': '3', 'dd': '4',
                   'ee': '5', 'ff': '6', 'gg': '7', 'hh': '8', 'ii': '9'}
        view = self.view
        sel = view.sel()
        selTxt = []
        for region in sel:
            txt = view.substr(region)
            selTxt.append(txt)
            # print(111, txt)
        selStr = json.dumps(selTxt[0], ensure_ascii=False)
        selStr = selStr.replace('  ', '\\t')

        # print(333, selStr)
        def dashrepl(matchobj):
            mm = matchobj.group(0)
            # print(3, mm)
            if mm:
                return '${' + letters[mm] + ':}'
        selStrb = re.sub(
            'a{2}|b{2}|c{2}|d{2}|e{2}|f{2}|g{2}|h{2}|i{2}', dashrepl, selStr)
        # print(444, selStrb)
        comObj = {
            'trigger': 'TTT',
            'contents': selStrb.strip('"')
        }
        # print(555, comObj)
        comStr = json.dumps(comObj, ensure_ascii=False)
        comStr = comStr.replace('\\t', 't')
        comStr = comStr.replace('\\n', 'n')
        comStr = comStr + ','
        sublime.set_clipboard(comStr)
