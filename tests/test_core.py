# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from mediaproxy.core import Core


class TestCore(unittest.TestCase):

    def setUp(self):
        self.core = Core(datapath='/home/merlink/.mediaproxy', level=1)

        if not self.core.setup_check():
            self.core.setup('portable')
            self.core.channel_add(u'test', 'Channels.Youtube', None, u'PLJpMp7EPOGSAk60elkLYz0wBLKJMQXzEv', None)

        assert self.core.setup_check()


    def tearDown(self):
        pass

    def test_listdir(self):
        p = self.core.filesystem.listdir(u'/test')
        print(p)

    def test_channels(self):
        print (self.core.channels())

    def test_plugins(self):
        print (self.core.plugins_list(only_active=True))

