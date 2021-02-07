#!/usr/bin/env python
import subprocess
import click


def execute(cmd):
    print(cmd)
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
    return popen


@click.group()
def cli():
    pass


@cli.command()
@click.option('--model', '-m', default='lpr:4')
@click.option('--inferconfig', '--ic', default='inferconfig.json')
# @click.option('--deployconfig', '--dc', default='localdeploy.json')
@click.option('deployconfig', '--local', flag_value='localdeploy.json', default=True)
@click.option('deployconfig', '--aks',  flag_value='aksdeploy.json')
@click.option('deployconfig', '--deployconfig', '--dc', default='localdeploy.json')
@click.option('--name', '-n', default='lprtest')
def deploy(model, inferconfig, deployconfig, name):
    run = execute(['az', 'ml', 'model', 'deploy', '-m', model, '--ic',
                   inferconfig, '--dc', deployconfig, '--name', name, '--overwrite'])
    for line in run:
        print(line, end="")
    pass


@cli.command()
@click.option('--workspace', '-w', default='LPR')
@click.option('--group', '-g', default='fyp-smartcarpark')
def workspace(workspace, group):
    run = execute(['az', 'ml', 'folder', 'attach',
                   '-w', workspace, '-g', group])
    for line in run:
        print(line, end="")


if '__main__' == __name__:
    cli()
