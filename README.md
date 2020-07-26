<!-- MarkdownTOC -->

- sublime 同步
    - windows

<!-- /MarkdownTOC -->

# sublime 同步

## windows

1.  安装 package control

2.  clone git
    ```
    cd /d/apps/Sublime Text Build 3211 x64/Data
    rm -fr Packages

    git init
    git remote add origin git@github.com:linkhanfeng/sublime-text3.git
    git pull origin master
    ```