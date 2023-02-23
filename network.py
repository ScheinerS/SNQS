#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 17:17:25 2023

@author: santiago

https://docs.netsquid.org/latest-release/tutorial.components.html
"""

# To send a message from Alice to Bob, we can schedule an event when Bob could pick up the message sent by Alice. This functionality of sending a message with a delay can be modelled by a channel (Channel), which is a subclass of the component (Component).

import netsquid as ns
from netsquid.components import Channel, QuantumChannel
channel = Channel(name="MyChannel")
#%%
# A channel is capable of sending a message in one direction i.e. from its input port at one end to its output port at the other end. To send any Python object as a message we can put it on the channel’s input port using send().

channel.send("hello world!")
ns.sim_run()

#%% 
# Channels are a subclass of Entity and schedule events to transmit the message. Therefore we will have to run the simulator for the message to arrive. To receive the messages, we can call receive(). It returns the messages on the output, as well as the time the messages have been travelling through the channel. As we did not specify a transmission delay model for the channel it has defaulted to no delay, which means we can retrieve the message at the same time instance it was sent.

items, delay = channel.receive()
items
delay

#%%

# There are multiple ways to add a delay to the channel. One approach is to initialize the channel with a fixed delay.

Channel(name="DelayChannel", delay=10)

#%%