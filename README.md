# IRC Bot + Client  [![Build Status](https://travis-ci.org/tommai78101/IRCBot.svg?branch=master)](https://travis-ci.org/tommai78101/IRCBot)

![](http://i.imgur.com/xmM2oTC.gif)

### Description:

This is an internet relay chat (IRC) bot written in Python 3.5.1, using Visual Studio 2015 Community as the primary IDE for Python. This bot can also act as an IRC client that the user can interact with others with. This bot's nickname is "WedrBot", and uses a public channel, #wedrbot, as a test bed for plugin development and debugging purposes.

The main purpose of this project is for me to learn about Python 3, how to create a feature complete IRC bot, add support for an IRC client, and touch up on using scripting languages as well.

Please create new issues to request for new features, report bugs, and other things in general for any IRC Bot improvements.

### Features:

* **Quotes** - Allowing users to add/remove quotes in the quotes list.   
* **Saving/Loading** - Allowing the bot host to store and load the quotes list.   
* **Updates Lookup** - For Nintendo 3DS, this bot parses the data gather from [this site](https://yls8.mtheall.com/ninupdates/reports.php), and tells the users what the minimum firmware update is required for their respective games. The updates repository can be located [here](https://github.com/yellows8/ninupdates).   
* **Custom Plugins Support** - Creating new plugins to run in this bot is now more centralized and streamlined.    
* **Streamlined Commands** - Typing a command into the IRC bot is now very straightforward, and it acts just like any other IRC clients.   
* **And many more plugins!!**

### How to Use:

0. REQUIRES Python 3. If you don't have Python 3, grab the latest Python 3 from [here](https://www.python.org/downloads/).
1. Download the [ZIP file here](https://github.com/tommai78101/IRCBot/archive/master.zip) and extract the contents to a new folder/directory.
2. Run "start.py".

### How to Create Plugins:

1. Download the [ZIP file here](https://github.com/tommai78101/IRCBot/archive/master.zip) and extract the contents to a new folder/directory.
2. In the `/plugins` folder, duplicate the `template.py`, and rename.
3. Edit your renamed copy, and follow the instructions written in the comments.
4. Save your plugin in `/plugins` folder/directory.
5. Run "start.py"
6. To reload your plugins, type `"/reload"` in the command prompt/terminal to reload all plugins.

### Credits:

**asperatology (wedr) / tom_mai78101** - For the creation of the IRC Bot Client.    
**yellows8** - Many contributions on finding required firmware update versions.

### License:

The MIT License (MIT)
Copyright (c) 2016 Thompson Lee