#! /usr/bin/env python3
from .cli import CLI
import os

def main():

    # Change to the directory of execution
    # TODO: This is a temporary fix, need to find a better way to handle this
    os.chdir(os.getcwd())

    cli = CLI()
    cli.run()
