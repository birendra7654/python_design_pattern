#!/usr/bin/env python

# Standard imports
from abc import ABCMeta, abstractmethod
import logging
import os
import sys
import json
import shlex
import subprocess
from typing import Callable

# Third party imports
import paramiko

# Application imports

logger = logging.getLogger(__name__)


class ExecutorFactory:
    def __init__(self):
        print("constructor")
    """ The factory class for creating executors"""

    registry = {}
    """ Internal registry for available executors """

    @classmethod
    def register(cls, name: str) -> Callable:
        """ Class method to register Executor class to the internal registry.
        Args:
            name (str): The name of the executor.
        Returns:
            The Executor class itself.
        """
        print("11111")
        print(name)
        print("11111")
        def inner_wrapper(wrapped_class: ExecutorBase) -> Callable:
            print("222222")
            if name in cls.registry:
                logger.warning('Executor %s already exists. Will replace it', name)
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    # end register()

    @classmethod
    def create_executor(cls, name: str, **kwargs) -> 'ExecutorBase':
        """ Factory command to create the executor.
        This method gets the appropriate Executor class from the registry
        and creates an instance of it, while passing in the parameters
        given in ``kwargs``.
        Args:
            name (str): The name of the executor to create.
        Returns:
            An instance of the executor that is created.
        """

        if name not in cls.registry:
            logger.warning('Executor %s does not exist in the registry', name)
            return None

        exec_class = cls.registry[name]
        executor = exec_class(**kwargs)
        return executor

    # end create_executor()

# end class ExecutorFactory


class ExecutorBase(metaclass=ABCMeta):
    """ Base class for an executor """

    def __init__(self, **kwargs):
        """ Constructor """
        pass

    @abstractmethod
    def run(self, command: str) -> (str, str):
        """ Abstract method to run a command """
        pass

# end class ExecutorBase


@ExecutorFactory.register('local')
class LocalExecutor(ExecutorBase):

    def run(self, command: str) -> (str, str):
        """ Runs the given command using subprocess """

        args = shlex.split(command)
        stdout, stderr = subprocess.Popen(args,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE).communicate()

        out = stdout.decode('utf-8')
        err = stderr.decode('utf-8')
        return out, err
    # end run()

# end class LocalExecutor


@ExecutorFactory.register('remote')
class RemoteExecutor(ExecutorBase):

    def __init__(self, **kwargs):
        """ Constructor """
        self._hostname = kwargs.get('hostname', 'localhost')
        self._username = kwargs.get('username', None)
        self._password = kwargs.get('password', None)
        self._pem = kwargs.get('pem', None)

    # end __init__()

    def run(self, command: str) -> (str, str):
        """ Runs the command using paramiko """

        # Creates the client, connects and issues the command
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self._hostname,
                       username=self._username,
                       password=self._password,
                       pkey=paramiko.RSAKey.from_private_key_file(self._pem) if self._pem else None)

        _, stdout, stderr = client.exec_command(command)
        out = ''.join(stdout.readlines())
        err = ''.join(stderr.readlines())
        client.close()
        return out, err

    # end run()

# end class RemoteExecutor


if __name__ == '__main__':
    print("Main Execution start")
    # Creates a local executor
    local = ExecutorFactory.create_executor('local')
    local_out = local.run('ls -ltra')
    print(local_out)

    # remote = ExecutorFactory.create_executor('remote',
    #                                          hostname=vcIp,
    #                                          username='root',
    #                                          password="vmware")
    # remote_out = remote.run('')
