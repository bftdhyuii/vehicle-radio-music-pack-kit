from pathlib import Path
import contextlib
import json
import os
import queue
import runpy
import subprocess
import sys
import threading
import traceback
import uuid

ROOT=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]/'build/simple-kit'
BUNDLE=Path(getattr(sys,'_MEIPASS',Path(__file__).parent))

def build_worker(arguments):
    arguments=list(arguments)
    pos=arguments.index('--worker-log')
    log=Path(arguments[pos+1]);del arguments[pos:pos+2]
    log.parent.mkdir(parents=True,exist_ok=True)
    with log.open('w',encoding='utf8') as output,contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):
        try:
            sys.argv=['build_music_pack.py']+arguments
            runpy.run_path(str(BUNDLE/'build_music_pack.py'),run_name='__main__')
        except BaseException:
            traceback.print_exc()
            return 1
    return 0

def generate(name,folder):
    if not name.strip() or not name.isascii() or any(c in name for c in '\\/:*?"<>|') or name.strip() in {'.','..'}:
        raise ValueError('音乐包名称请使用英文或数字, 不要使用文件名特殊符号.')
    name=name.strip()
    folder=Path(folder)
    if not folder.is_dir():raise ValueError('请选择存放歌曲的文件夹.')
    if not any(p.is_file() and p.suffix.lower() in {'.mp3','.wav','.ogg','.flac','.m4a'} for p in folder.iterdir()):
        raise ValueError('文件夹里没有歌曲. 支持 MP3, WAV, OGG, FLAC, M4A.')
    ffmpeg=ROOT/'Tools/ffmpeg.exe'
    if not ffmpeg.is_file():raise ValueError('缺少转换工具. 请完整解压工具包后运行, 不要单独移动 EXE.')
    database=ROOT/'Tools/pack_ids.json'
    ids=json.loads(database.read_text(encoding='utf8')) if database.exists() else {}
    if name not in ids:
        ids[name]='music_'+uuid.uuid4().hex
        database.write_text(json.dumps(ids,indent=2),encoding='utf8')
    output=ROOT/'Output'/f'{name}.zip'
    log=ROOT/'Tools/last_build.log'
    command=[sys.executable]
    if not getattr(sys,'frozen',False):command.append(str(Path(__file__).resolve()))
    command+=['--build','--worker-log',str(log),'--id',ids[name],'--name',name,'--input',str(folder),'--output',str(output),'--ffmpeg',str(ffmpeg)]
    result=subprocess.run(command,creationflags=subprocess.CREATE_NO_WINDOW)
    if result.returncode:
        raise RuntimeError('生成失败. 请查看 Tools/last_build.log. 音频文件可能无法读取或转换.')
    return output

def show_gui():
    import tkinter as tk
    from tkinter import ttk,filedialog,messagebox
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'Music').mkdir(exist_ok=True)
    (ROOT/'Output').mkdir(exist_ok=True)
    root=tk.Tk();root.title('Vehicle Radio - 音乐包制作工具');root.geometry('600x360');root.minsize(600,360)
    frame=ttk.Frame(root,padding=22);frame.pack(fill='both',expand=True)
    frame.columnconfigure(0,weight=1)
    ttk.Label(frame,text='制作你的车载音乐包',font=('Microsoft YaHei UI',16)).grid(row=0,column=0,columnspan=2,sticky='w',pady=(0,14))
    ttk.Label(frame,text='1. 把歌曲放进 Music 文件夹, 或选择已有的歌曲文件夹.').grid(row=1,column=0,columnspan=2,sticky='w')
    folder=tk.StringVar(value=str(ROOT/'Music'))
    ttk.Entry(frame,textvariable=folder).grid(row=2,column=0,sticky='ew',pady=(7,12))
    browse=ttk.Button(frame,text='选择文件夹',command=lambda:choose_folder())
    browse.grid(row=2,column=1,padx=(8,0))
    ttk.Label(frame,text='2. 填写音乐包名称 (英文或数字, 会显示在游戏轮盘里).').grid(row=3,column=0,columnspan=2,sticky='w')
    name=tk.StringVar(value='My Music')
    ttk.Entry(frame,textvariable=name).grid(row=4,column=0,columnspan=2,sticky='ew',pady=(7,14))
    events=queue.Queue();busy=False
    status=tk.StringVar(value='生成的 ZIP 会保存在 Output 文件夹, 可以直接导入 mod 管理器.')
    progress=ttk.Progressbar(frame,mode='indeterminate')
    progress.grid(row=6,column=0,columnspan=2,sticky='ew',pady=(12,8))
    ttk.Label(frame,textvariable=status,wraplength=550).grid(row=7,column=0,columnspan=2,sticky='w')
    def choose_folder():
        selected=filedialog.askdirectory(initialdir=folder.get(),title='选择歌曲文件夹')
        if selected:folder.set(selected)
    def worker(pack_name,music_folder):
        try:events.put((True,generate(pack_name,music_folder)))
        except Exception as error:events.put((False,str(error)))
    def start():
        nonlocal busy
        if busy:return
        busy=True;button.state(['disabled']);browse.state(['disabled']);progress.start(15)
        status.set('正在转换并打包歌曲, 请稍候...')
        threading.Thread(target=worker,args=(name.get(),folder.get()),daemon=True).start()
    button=ttk.Button(frame,text='3. 生成音乐包 ZIP',command=start)
    button.grid(row=5,column=0,columnspan=2,sticky='ew')
    def poll():
        nonlocal busy
        try:
            success,value=events.get_nowait()
            busy=False;button.state(['!disabled']);browse.state(['!disabled']);progress.stop()
            if success:
                status.set('完成! ZIP 已保存到 Output 文件夹.');os.startfile(str(value.parent))
            else:status.set('生成失败.');messagebox.showerror('生成失败',value,parent=root)
        except queue.Empty:pass
        root.after(100,poll)
    def close():
        if busy:messagebox.showinfo('正在生成','请等音乐包生成完成后再关闭工具.',parent=root)
        else:root.destroy()
    root.protocol('WM_DELETE_WINDOW',close);poll();root.mainloop()

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--build':sys.exit(build_worker(sys.argv[2:]))
    show_gui()
