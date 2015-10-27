#!/usr/bin/python2

from optparse import OptionParser
import ConfigParser
import sys
import importlib

from core import RedisFile, mainloop


class Options:

    def __init__(self):
        self.__default_config_file = "rata.cfg"

        # Get the configuration file name from command line arguments.
        parser = OptionParser()
        parser.add_option("-c", "--configuration",
                          dest="config_file",
                          help="Set the configuration file to FILE",
                          metavar="FILE")
        opts, args = parser.parse_args()

        # Parse the configuration file
        config_file = opts.config_file \
            if opts.config_file is not None else self.__default_config_file

        config = ConfigParser.ConfigParser()
        config.read(config_file)

        self.server_id = config.get("core", "ServerId")

        # Get the window size (self.window_size)
        self.window_size = config.getint("core", "WindowSize")

        # Create the input method (self.input)
        input_method = config.get("core", "InputMethod")
        if input_method == 'stdin':
            self.input = sys.stdin
        elif input_method == 'file':
            input_file = config.get("core", "FileName")
            self.input = open(input_file, "r", 1)
        else:  # Default input method
            self.input = sys.stdin

        # Create the PreR's with each's input methods (self.prers)
        prers_path = config.get("core", "PreliminarReducersPackage")
        prers_names = config.get("core", "PreliminarReducers").split(",")
        self.prers = []
        for prer_name in prers_names:
            module_name, class_name = prer_name.rsplit(".", 1)
            prer_class = getattr(importlib.import_module(
                prers_path + "." + module_name), class_name)
            prer_args = dict(config.items(class_name))

            output_method = prer_args.pop('outputmethod')

            if output_method == 'stdout':
                f = sys.stdout
            elif output_method == 'file':
                f = open(prer_args.pop('filename'), 'a', 1)
            elif output_method == 'redis':
                host = prer_args.pop('redishost')
                channel = prer_args.pop('redischannel')
                f = RedisFile(host, channel)
            else:  # Default Output Method
                f = sys.stdout

            prer_instance = prer_class(f, **prer_args)
            # if not prer_args:
            #     prer = PreR(f)
            # else:
            #     prer = PreR(f, **prer_args)

            self.prers.append(prer_instance)


if __name__ == '__main__':
    options = Options()
    mainloop(options)
