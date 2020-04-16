# SAQWS

Session Aware Queue over WebSocket (in Python)

## Introduction

When publishing events, clients can connect to receive these events in real-time. But
additionally these clients might be interested in all events that were published in the
past too, but only up to some point in the past.

For instance, in an online mult-player game the client might be interested in all the 
events related to the ongoing game (points scored by each player, medals achieved, ...)
while all events of the previous game have become irrelevant.

The session-aware-queue provides subscribes with real-time updates from the publisher
and on connection provides the history of all events of the _current_ session.
