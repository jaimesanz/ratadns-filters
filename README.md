# RaTA-DNS Preliminar Reducers

## Description

This framework tranforms a stream of DNS Packets into multiple streams of processed data.
To do this, the software takes a stream with the format of the [Packet Analyzer](https://github.com/niclabs/ratadns-packet-analyzer), and pass it through several preliminar reducers. Each preliminar reducer send it output to different channels. For example, a pub-sub redis channel, the standard output or a file.
The input stream may be the standard input, or a previously defined file.
