# -*- coding: utf-8 -*-

from tkinter import *
import tkinter
import server_multi


def buttonclick1():
    """当点击add的时候触发，获取链接，执行线程"""
    text = var.get()
    t1 = server_multi.Task(text)
    t1.start()
    var.set('')


def on_entry_click(event):
    """输入框被点击时触发，输入框清空等待输入链接"""
    if var.get() == '请输入种子详情链接：':
        var.set('')  # delete all the text in the entry
        entry_1.config(fg='black')


def on_focus_out(event):
    """当点击别的控件的时候恢复输入框默认内容，这里没有别的控件，所以……为后续准备吧"""
    if var.get() == '':
        var.set('请输入种子详情链接：')
        entry_1.config(fg='grey')


if __name__ == "__main__":  # tkinter最基本的使用
    root = tkinter.Tk()
    root.geometry('600x100+600+300')
    root.title('蝴蝶做种客户端')
    root.iconbitmap('', './icon/bitbug_favicon.ico')
    root.resizable(False, False)

    # TOP
    label1 = Label(root, text="HUDBT",  font=('Helvetica', '14'), width=5, height=2)
    label1.pack(side=TOP)   # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM

    var = StringVar()
    # LEFT
    frm = Frame(root)
    frm_L = Frame(frm)
    entry_1 = Entry(frm_L, textvariable=var, width=45, borderwidth=3, font=('Helvetica', '14'))
    entry_1.pack(side=TOP)
    var.set('请输入种子详情链接：')
    entry_1.bind('<FocusIn>', on_entry_click)
    entry_1.bind('<FocusOut>', on_focus_out)
    entry_1.config(fg='grey')
    frm_L.pack(side=LEFT)

    # RIGHT
    frm_R = Frame(frm)
    button1 = tkinter.Button(frm_R, text='Add', font=('Helvetica', '11'), command=buttonclick1).pack(side=TOP, padx=5)
    frm_R.pack(side=RIGHT)

    frm.pack()
    root.mainloop()
