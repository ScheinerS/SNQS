#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Channel
"""
import netsquid as ns
from netsquid.components import Channel, QuantumChannel
channel = Channel(name="MyChannel")


channel.send("hello world!")
ns.sim_run()

items, delay = channel.receive()
items
