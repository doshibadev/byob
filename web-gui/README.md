![Banner](https://github.com/malwaredllc/byob/blob/master/byob/static/byob_logo_black.svg)

[![license](https://img.shields.io/badge/license-GPL-brightgreen.svg)](https://github.com/malwaredllc/byob/blob/master/LICENSE)
[![version](https://img.shields.io/badge/version-1.0-lightgrey.svg)](https://github.com/malwaredllc/byob)
![build](https://github.com/malwaredllc/byob/workflows/build/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/malwaredllc/byob/badge.svg)](https://coveralls.io/github/malwaredllc/byob)
[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=BYOB%20(Build%20Your%20Own%20Botnet)&url=https://github.com/malwaredllc/byob&via=malwaredllc&hashtags=botnet,python,infosec,github)

Questions? [Join the Discord support server](https://discord.gg/8FsSrw7)

__Disclaimer__: This project should be used for authorized testing or educational purposes only.

## Fork Information

This is a fork of the original BYOB project, updated for 2025 with modern Python compatibility and package updates. The following changes have been made to ensure compatibility with current Python versions and maintain functionality:

### Updates & Changes

1. **Cryptocurrency Mining Module**
   - Replaced deprecated `pyrx` and `pycryptonight` libraries with direct execution of XMRig binaries
   - Implemented a more reliable mining solution that works across Python versions
   - Added proper process management for mining operations

2. **Keylogger Module**
   - Replaced unmaintained `pyHook`/`PyWinHook` with modern `pynput` library
   - Improved cross-platform compatibility for keylogging functionality
   - Enhanced key event handling with better special key support

3. **Dependencies**
   - Updated package requirements to support Python 3.x
   - Removed dependencies on abandoned libraries
   - Added compatibility with modern security libraries

4. **Code Modernization**
   - Updated string formatting to use f-strings
   - Improved error handling and logging
   - Enhanced cross-platform compatibility

These updates ensure that BYOB remains functional with modern Python environments while maintaining all the original functionality of the framework.

BYOB is an open-source post-exploitation framework for students, researchers and developers. It includes features such as:
- Command & control server with intuitive user-interface
- Custom payload generator for multiple platforms
- 12 post-exploitation modules

It is designed to allow students and developers to easily implement their own code and add cool new
features *without* having to write a C2 server or Remote Administration Tool from scratch.

This project has 2 main parts: the **original console-based application** (`/byob`) and the **web GUI** (`/web-gui`).

# Web GUI

## Dashboard
A control panel for your C2 server with a point-and-click interface for executing post-exploitation modules. The control panel includes an interactive map of client machines and a dashboard which allows efficient, intuitive administration of client machines.

![dashboard_preview](https://github.com/malwaredllc/byob/blob/master/web-gui/buildyourownbotnet/assets/images/previews/preview-dashboard.png)

## Payload Generator
The payload generator uses black magic involving Docker containers & Wine servers to compile executable payloads for any platform/architecture you select. These payloads spawn reverse TCP shells with communication over the network encrypted via AES-256 after generating a secure symmetric key using the [Diffie-Hellman IKE](https://tools.ietf.org/html/rfc2409).

![payloads_preview](https://github.com/malwaredllc/byob/blob/master/web-gui/buildyourownbotnet/assets/images/previews/preview-payloads2.png)

## Terminal Emulator
The web app includes an in-browser terminal emulator so you can still have direct shell access even when using the web GUI.

![terminal_preview](https://github.com/malwaredllc/byob/blob/master/web-gui/buildyourownbotnet/assets/images/previews/preview-shell.png)
