#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import yaml
import click

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0]
DEFAULT_CONFIG_PATH = os.path.join(SCRIPT_PATH, "../static/CONFIG_TEMPLATE.yml")
OUT_FILE_PATH = os.path.join(os.path.expanduser('~'), ".git_ext.yml")

def main():
    with open(DEFAULT_CONFIG_PATH) as default_config:
        config = yaml.load(default_config)
        click.echo("Init git-ext config... The config file saved in ~/.git_ext.yml, you can change it later")
        email = raw_input("Your bitbucket email: ")
        password = raw_input("Your bitbucket password: ")
        config['bitbucket']['email'] = email
        config['bitbucket']['password'] = password
        output_file = yaml.dump(config)
        with open(OUT_FILE_PATH, 'w') as final_config:
            final_config.write(output_file)
        click.echo("All done! Config file saved to ~/.git_ext.yml")


if __name__ == '__main__':
    main()
