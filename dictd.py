#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-10-29 22:55:22
from __future__ import unicode_literals, division, absolute_import, print_function

"""
DICT协议的字典服务器
"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import json
import datetime

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
from twisted.application import service, internet
#from twisted.internet.protocol import DatagramProtocol
#from twisted.internet.threads import deferToThread
from twisted.internet import defer
# import txredisapi as redis
from twisted.application import service, internet
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.threads import deferToThread
from twisted.protocols.basic import LineReceiver
from twisted.internet.endpoints import TCP4ServerEndpoint


# 实例化时间服务容器
time_service_container = service.MultiService()

class Dict(LineReceiver):
    '''字典协议'''
    commands = {"CLIENT": '', "DEFINE": '', "MATCH": '', "SHOW": '', "STATUS": '', "HELP": '', "QUIT": '', "OPTION": '', "AUTH": '', "SASLAUTH": ''}

    def __init__(self):
        self.users = set()

    def connectionMade(self):
        print("connectionMade")
        self.sendLine(b"220 pan.alephnull.com dictd 1.12.1/rf on Linux 4.4.0-1-amd64 <auth.mime> <68206816.12719.1509287985@pan.alephnull.com>")

    def connectionLost(self, reason):
        print("connectionLost")

    def lineReceived(self, line):
        print('[%s]' % line)
        # client "dict 1.12.1/rf on Linux 4.4.0-97-generic"
        # define * "hello"
        line = line.decode('utf8')
        # UnicodeDecodeError
        cmd_word, *cmd_param = line.split(maxsplit=1)
        cmd_word = cmd_word.upper()
        if cmd_word not in self.commands:
            self.sendLine(b"502 Command not implemented")
            print('未知命令')
        command = eval(f"self.handle_{cmd_word}")
        if not cmd_param:
            command()
        else:
            command(*cmd_param)

    def handle_CLIENT(self, cmd_param):
        print('客户端信息:%s' % cmd_param)
        print(dir(self.transport))
        print(self.transport.getPeer().host)
        # self.sendLine(b"250 ok (optional timing information here)")
        self.sendLine(b"250 ok ")

    def handle_DEFINE(self, cmd_param):
        database, word = cmd_param.split()
        print(cmd_param)
        self.sendLine(b"250 text capabilities msg-id")
        # if self.users.has_key(name):
        #     self.sendLine("Name taken, please choose another.")
        #     return
        # self.sendLine("Welcome, %s!" % (name,))
        # self.name = name
        # self.users[name] = self
        # self.state = "CHAT"

    def handle_MATCH(self, name):
        pass

    def handle_SHOW(self, name):
        pass

    def handle_STATUS(self, name):
        pass

    def handle_HELP(self, name):
        pass

    def handle_QUIT(self):
        print('客户端退出')
        self.transport.loseConnection()

    def handle_OPTION(self, name):
        pass

    def handle_AUTH(self, name):
        pass

    def handle_SASLAUTH(self, name):
        pass


class DICTFactory(Factory):
    def buildProtocol(self, addr):
        return Dict()

application = service.Application('Manager_Service')    # 给应用起个名字

# ts.setServiceParent(time_service_container)
#port = 9999
#udp_server = internet.UDPServer(port, Helloer())        # 定义udp服务
#udp_server.setServiceParent(application)                # 将管理服务挂到应用下面

endpoint = TCP4ServerEndpoint(reactor, 2628)
endpoint.listen(DICTFactory())
reactor.run()

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

