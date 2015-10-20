#!/usr/bin/env python

import sys
import argparse
import subprocess
import pyinotify


def canBuildLess(f):
    try:
        subprocess.Popen(['lessc', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print('Il semblerait qu\'il soit impossible de compiler le style, \
               demande à ce cher Paulloz de le faire pour toi.', file=sys.stderr)
        return lambda: None
    return f


@canBuildLess
def buildLessFiles():
    p = subprocess.Popen(['lessc', 'less/main.less', '--include-path=less/'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode > 0:
        print(stderr.decode('utf-8'), file=sys.stderr)
    else:
        print("Built style.css")
        with open('style.css', mode='w') as f:
            f.write(stdout.decode('utf-8'))


def watchFiles():
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY

    class EventHandler(pyinotify.ProcessEvent):
        def __process_change(self, event):
            print("{0} has been modified".format(event.pathname))
            buildLessFiles()

        def process_IN_DELETE(self, event):
            self.__process_change(event)

        def process_IN_CREATE(self, event):
            self.__process_change(event)

        def process_IN_MODIFY(self, event):
            self.__process_change(event)

    notifier = pyinotify.Notifier(wm, EventHandler())
    wm.add_watch('less/', mask, rec=True)

    notifier.loop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['watch', 'build'], default='build', nargs='?')
    args = parser.parse_args()

    if args.action == 'watch':
        buildLessFiles()
        watchFiles()
    elif args.action == 'build':
        buildLessFiles()
