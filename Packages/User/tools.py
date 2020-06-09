# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import os
from os import path
import datetime
import re
import webbrowser
import json
# import platform
# import urllib
import yaml
# 公用方法


def fileInfoObj(filepath):
    path_name, ext_dot = os.path.splitext(filepath)
    path, name = path_name.rsplit('/', 1)
    ext = ext_dot.replace('.', '', 1)
    return {
        'path': path,               # /user
        'name': name,               # a
        'ext_dot': ext_dot,         # .txt
        'ext': ext,                 # txt
        'name_ext': name + ext_dot,  # a.txt
    }

# 插入 当前日期


class GetDateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        t = datetime.datetime.now()
        curIsoTime = t.isoformat(' ').split('.', maxsplit=1)[0]
        selList = self.view.sel()
        for selRegion in selList:
            self.view.insert(edit, selRegion.a, curIsoTime)

# 打开浏览器 - 当前文档


class OpenInBrowerCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        path = kwargs.get('url', None) if kwargs.get(
            'url', None) else self.view.file_name()
        path = 'file://' + path
        webbrowser.open_new_tab(path)

# 打开浏览器 - js 文档


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

# 打开目录 Sublime User


class OpenUserDirCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        path = sublime.packages_path() + '/User'
        sublime.active_window().run_command("open_dir", {"dir": path})

# 打开文件 js补全 js.sublime-completions


# 打开文件 - 补全文件js.sublime-completions
class OpenCompletionsFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        # view = self.window.active_view()
        path = sublime.packages_path() + '/User/MySubl/js.sublime-completions'
        self.window.open_file(path)

# 打开文件 - tools.py


class OpenToolsFileCommand(sublime_plugin.WindowCommand):

    def run(self):
        # view = self.window.active_view()
        toolPath = sublime.packages_path() + '/User/tools.py'
        commandPath = sublime.packages_path() + '/User/Default.sublime-commands'
        self.window.open_file(commandPath)
        self.window.open_file(toolPath)

# 打开文件 - tips.md


class OpenTipsCommand(sublime_plugin.WindowCommand):

    def run(self):
        # view = self.window.active_view()
        path = '/Users/hf/it/note/dev/developer/tips.md'
        self.window.open_file(path)

# 打开文件 - test.js


class OpenTipsCommand(sublime_plugin.WindowCommand):

    def run(self):
        # view = self.window.active_view()
        path = '/Users/hf/it/note/dev/developer/tips.md'
        self.window.open_file(path)


# 转换选择文本 - 将选择的文本转换为 completions
class VuexAttrCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        selList = self.view.sel()
        for selRegion in selList:
            selTxt = self.view.substr(selRegion)
            getterStr = "\tweightModifyInterFace (state) {\n\t\treturn state.weightModifyInterFace\n\t},\n"
            setterStr = "\tSET_weightModifyInterFace (state, param) {\n\t\tstate.weightModifyInterFace = param\n\t},\n"
            actionStr = "\tasync SET_weightModifyInterFace_ASYNC ({ commit }, param) {\n\t\tcommit('SET_weightModifyInterFace', param)\n\t},"
            allStr = getterStr + setterStr + actionStr
            formatedStr = allStr.replace('weightModifyInterFace', selTxt)
            self.view.replace(edit,  sublime.Region(selRegion.a, selRegion.b), formatedStr)

# 转换选择文本 - 将选择的文本转为 js 补全文件


class SelToCompletionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        letters = {'aa': '1', 'bb': '2', 'cc': '3', 'dd': '4', 'ee': '5', 'ff': '6', 'gg': '7', 'hh': '8', 'ii': '9'}
        view = self.view
        sel = view.sel()
        selTxt = []
        for region in sel:
            txt = view.substr(region)
            selTxt.append(txt)
        selStr = selTxt[0]

        def dashrepl(matchobj):
            mm = matchobj.group(0)
            if mm:
                ll = mm[0:2]
                llc = mm[2:len(mm)-1]
                llEnd = mm[len(mm)-1:len(mm)]
                return "${" + letters[ll] + ":" + llc + "}" + llEnd

        regStr = ""
        for x in letters:
            regStr = regStr + x + '\S*\s|'
        selStrb = re.sub(regStr, dashrepl, selStr)
        comStr = json.dumps(selStrb, ensure_ascii=False)
        comStr = comStr.replace('  ', '\\t').strip('"')
        # triStr = '{"trigger": "TTT   | jj UUU", "contents": '+comStr+'}'
        sublime.set_clipboard(comStr)

# 添加markdown文件的元信息和 TOC
class InsertMarkdownMetaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # 格式化时间
        t = datetime.datetime.now()
        curIsoTime = t.isoformat(' ').split('.', maxsplit=1)[0]
        # 检测是否已经存在信息, 不存在插入信息, 存在更新时间和检测标题是否修改
        isMetaStr = self.view.substr(sublime.Region(0, 3))
        # print('InsertMarkdownMetaCommand::', isMetaStr)
        if isMetaStr == '---':
            # 从文件提取 yaml 并解析为对象
            endYamlRg = self.view.find('---', 3, sublime.LITERAL)
            yamlStr = self.view.substr(sublime.Region(3, endYamlRg.a))
            # print(endYamlRg, yamlStr)
            yamlObj = yaml.load(yamlStr)
            # print(yamlObj)
            # 更新时间
            yamlObj['updated'] = curIsoTime
            # 更新标题
            titleRg = self.view.find('# ', 0, sublime.LITERAL)
            if not titleRg:
                return
            titleLineStr = self.view.substr(self.view.line(titleRg)).replace('# ', '')
            if yamlObj['title'] != titleLineStr:
                yamlObj['title'] = titleLineStr
                yamlObj['titleen'] = translater(titleLineStr)

            # yaml_d_str = yaml.dump(yamlObj)
            yaml_d_str = yaml.dump(yamlObj, allow_unicode=True, explicit_start=True, explicit_end=True)
            self.view.replace(edit, sublime.Region(0, endYamlRg.a), yaml_d_str)
            # 更新 toc
            self.view.run_command('markdowntoc_update')
            # 更新参考链接 如果参考链接变更的话
            isRefLink = self.view.find('\n## 参考\n', 0, sublime.LITERAL)
            if isRefLink.a > 10:
                view_size = self.view.size()
                ref_str = self.view.substr(sublime.Region(isRefLink.a + 1, view_size))
                ref_arr = ref_str.strip().split("\n")
                while '' in ref_arr:
                    ref_arr.remove('')

                if ref_arr[1] != '' and '[]' in ref_arr[1]:
                    ref_arr[1] = ''
                    ref_arr.insert(2, '')
                else:
                    ref_arr.insert(1, '')
                    ref_arr.insert(2, '')

                url_str = ''
                for i in ref_arr:
                    index = ref_arr.index(i)
                    if index > 2:
                        if '](' in i:
                            url_arr = re.findall("\\[(.*)\\]\\((.*)\\)",i)[0]
                            ref_arr[index] = "[{}]:{}".format(url_arr[0], url_arr[1])
                        else:
                            url_arr = re.findall("\\[(.*)\\]:(.*)",i)[0]
                        url_str = url_str + '[{}][] | '.format(url_arr[0])
                ref_arr[1] = url_str.rstrip(' | ')
                ref_arr.append('')
                ref_new_str = "\n".join(ref_arr)
                self.view.replace(edit, sublime.Region(isRefLink.a + 1, view_size), ref_new_str)
        else:
            # 获取 tag, 根据目录结构在插入时
            tagsList = []
            fileInfo = fileInfoObj(self.view.file_name())
            filename = fileInfo['name']
            filePathList = fileInfo['path'].strip('/').split('/')
            if 'note' in filePathList:
                noteIndex = filePathList.index('note')
            else:
                noteIndex = -1
            if noteIndex > -1:
                if 'mysql-doc' in filePathList:
                    # mysql_doc_Index 仅仅是mysql文档的设置不让章节目录添加到标签 (可以删除)
                    mysql_doc_Index = filePathList.index('mysql-doc')
                    for value in filePathList:
                        if filePathList.index(value) > noteIndex and filePathList.index(value) <= mysql_doc_Index:
                            tagsList.append(value)
                else:
                    for value in filePathList:
                        if filePathList.index(value) > noteIndex:
                            tagsList.append(value)

            metaObj = {
                'title': filename,
                'titleen': '',
                'date': curIsoTime,
                'updated': curIsoTime,
                'tags': tagsList,
                'categories': tagsList,
            }
            class NoAliasDumper(yaml.Dumper):
                def ignore_aliases(self, data):
                    return True

            yamlStr = yaml.dump(metaObj, Dumper=NoAliasDumper, allow_unicode=True, explicit_start=True, explicit_end=True)
            # yamlStr = yaml.dump(metaObj).encode('utf-8').decode('unicode_escape')
            # print(yamlStr)
            self.view.insert(edit, 0, yamlStr + '---\n')
            self.view.run_command('markdowntoc_insert')
            # 添加回到主目录链接 如果有主目录的话
            def isFileExit(startpath, filename):
                parents_arr = startpath.split('/')
                parents_arr_copy = parents_arr[:]
                level = 0
                for path in parents_arr:
                    parents_arr_copy.pop()
                    indexpath = "/".join(parents_arr_copy) + '/' + filename
                    if os.path.exists(indexpath):
                        if level == 0:
                            return './' + filename
                        else:
                            return '../' * level + filename
                    level = level + 1

            indexpath = isFileExit(fileInfo['path'] + '/', 'index.md')
            if indexpath:
                self.view.insert(edit, self.view.size(), '[回到系列教程主目录]({})\n\n'.format(indexpath))
