#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from pytube import YouTube
from pprint import pprint
import threading
import os,time,re
from time import sleep


root = os.path.split(os.path.realpath(__file__))[0]
def view_bar(num, total):  #显示进度条
    rate = num/total
    rate_num = int(rate * 100)
    number=int(50*rate)
    r = '\r[%s%s]%d%%' % ("#"*number, " "*(50-number), rate_num, )
    print("\r {}".format(r),end=" ")   #\r回到行的开头


class VideoDownload():
    def __init__(self,url):
        self.url = url
        self.yt = None
        self.count = 0
        self.title = None
        self.videoformat = None
        self.file_size = 0
        self.stream = None
        # self.down_time = 0
        # self.down_rate = 0
    def getStreams(self):
        print("开始解析视频...........")
        self.yt = YouTube(self.url)
        print("======解析格式如下=========")
        pprint(self.yt.streams.all())

    def downloadVideo(self, res, videoformat):
        self.videoformat = videoformat
        self.title = re.sub("[\s+\.\!\/,$%^*:(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "",self.yt.title)
        print("=====视频标题为："+self.yt.title)
        titlepath = self.title+'.'+videoformat
        self.filename = self.createFile(titlepath)
        # [:-len(videoformat)]
        self.stream = self.yt.streams.filter(res=res, file_extension=videoformat).first()
        self.file_total = self.stream.filesize
        size = round(self.file_total/1024/1024, 2)
        print("=====视频大小为："+ str(size)+"M")
        th1 = threading.Thread(target=self.down)
        th1.start()
        self.progress()
        print(self.filename+"视频下载完成！")


    def down(self):
        self.stream.download(filename=self.title)

    def createFile(self, filename):
        if os.path.exists(filename):
            self.count += 1
            self.title += '(' + str(self.count) + ')'
            fname = self.title+'.'+self.videoformat
            filename = self.createFile(fname)
            return filename
        else:
            return filename

    def progress(self):
        while self.file_size < self.file_total:  # 获取当前下载进度
            # time.sleep(1)
            if os.path.exists(self.filename):
                # self.down_rate = (os.path.getsize(self.filename) - self.file_size) / 1024 / 1024
                # self.down_time = (self.file_total - self.file_size) / 1024 / 1024 / self.down_rate
                # print(" " + str('%.2f' % self.down_rate + "MB/s"), end="")
                self.file_size = os.path.getsize(self.filename)
            # print(" " + str(int(self.down_time)) + "s", end="")
            # print(" " + str('%.2f' % (self.file_size / 1024 / 1024)) + "MB", end="")
            view_bar(self.file_size, self.file_total)


if __name__ == '__main__':
    print("=============程序制作者：@Buukie=============\n")
    url = input("=====请输入视频地址：")
    down = VideoDownload(url)
    down.getStreams()
    res, videoformat = input("=====请输入想要下载的帧率和格式：").split()
    print(res+'   '+videoformat)
    down.downloadVideo(res, videoformat)
    os.system("pause")

# yt = YouTube('https://www.youtube.com/watch?v=_eQmGhvr5U4')
# pprint(yt.streams.all())
# pprint(yt.streams.filter(res='1080p',file_extension='mp4').all())
# s = yt.streams.filter(res='1080p',file_extension='mp4')
# pprint(s)
# s.first().download(filename='dance')
# vedio.download(root)
# pprint(yt.fmt_streams)

