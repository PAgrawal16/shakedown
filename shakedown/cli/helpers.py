import click
import contextlib
import os
import re

import shakedown as shakedown


def banner():
    """Display a product banner
    """

    banner_dict = {
        'a0': click.style(chr(9601), fg='magenta'),
        'a1': click.style(chr(9601), fg='magenta', bold=True),
        'b0': click.style(chr(9616), fg='magenta'),
        'c0': click.style(chr(9626), fg='magenta'),
        'c1': click.style(chr(9626), fg='magenta', bold=True),
        'd0': click.style(chr(9622), fg='magenta'),
        'd1': click.style(chr(9622), fg='magenta', bold=True),
        'e0': click.style(chr(9623), fg='magenta'),
        'e1': click.style(chr(9623), fg='magenta', bold=True),
        'f0': click.style(chr(9630), fg='magenta'),
        'f1': click.style(chr(9630), fg='magenta', bold=True),
        'g1': click.style(chr(9612), fg='magenta', bold=True),
        'h0': click.style(chr(9624), fg='magenta'),
        'h1': click.style(chr(9624), fg='magenta', bold=True),
        'i0': click.style(chr(9629), fg='magenta'),
        'i1': click.style(chr(9629), fg='magenta', bold=True),
        'j0': click.style(_fchr('>>'), fg='magenta'),
        'k0': click.style(chr(9473), fg='magenta'),
        'v0': click.style('mesosphere', fg='magenta',),
        'x1': click.style('shakedown', fg='magenta', bold=True),
        'y0': click.style('v' + shakedown.VERSION, fg='magenta'),
        'z0': chr(32)
    }

    banner_map = [
        "%(z0)s%(z0)s%(z0)s%(a0)s%(a0)s%(a1)s%(a0)s%(a1)s%(a1)s%(a1)s%(a1)s%(a1)s%(a1)s%(a1)s",
        "%(z0)s%(z0)s%(b0)s%(z0)s%(c0)s%(z0)s%(d0)s%(z0)s%(z0)s%(z0)s%(z0)s%(e1)s%(z0)s%(f1)s%(z0)s%(g1)s",
        "%(z0)s%(z0)s%(b0)s%(z0)s%(z0)s%(c0)s%(z0)s%(h0)s%(e0)s%(d1)s%(i1)s%(z0)s%(f1)s%(z0)s%(z0)s%(g1)s%(z0)s%(j0)s%(v0)s %(x1)s %(y0)s",
        "%(k0)s%(z0)s%(b0)s%(z0)s%(z0)s%(f0)s%(c0)s%(i0)s%(z0)s%(z0)s%(h1)s%(f1)s%(c1)s%(z0)s%(z0)s%(g1)s%(z0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(k0)s%(z0)s%(k0)s%(k0)s%(z0)s%(z0)s%(k0)s",
        "%(z0)s%(z0)s%(i0)s%(f0)s%(h0)s%(z0)s%(z0)s%(c0)s%(z0)s%(z0)s%(f0)s%(z0)s%(z0)s%(i1)s%(c1)s%(h1)s",
        "%(z0)s%(z0)s%(z0)s%(z0)s%(z0)s%(z0)s%(z0)s%(z0)s%(c0)s%(f0)s",
    ]

    if os.environ['TERM'] in ('xterm', 'xterm-256color', 'xterm-color'):
        return echo("\n".join(banner_map) % banner_dict)
    else:
        return echo('>> mesosphere shakedown v' + shakedown.VERSION, b=True)


def decorate(text, style):
    """ Console decoration style definitions
    """

    return {
        'step-maj': click.style("\n" + '> ' + text, fg='yellow', bold=True),
        'step-min': click.style('  - ' + text + ' ', bold=True),
        'item-maj': click.style('    - ' + text + ' '),
        'item-min': click.style('      - ' + text + ' '),
        'quote-head-fail': click.style("\n" + chr(9485) + chr(9480) + ' ' + text, fg='red'),
        'quote-head-pass': click.style("\n" + chr(9485) + chr(9480) + ' ' + text, fg='green'),
        'quote-head-skip': click.style("\n" + chr(9485) + chr(9480) + ' ' + text, fg='yellow'),
        'quote-fail': re.sub('^', click.style(chr(9482) + ' ', fg='red'), text, flags=re.M),
        'quote-pass': re.sub('^', click.style(chr(9482) + ' ', fg='green'), text, flags=re.M),
        'quote-skip': re.sub('^', click.style(chr(9482) + ' ', fg='yellow'), text, flags=re.M),
        'fail': click.style(text + ' ', fg='red'),
        'pass': click.style(text + ' ', fg='green'),
        'skip': click.style(text + ' ', fg='yellow')
    }.get(style, '')


def _fchr(char):
    return {
        '>>': chr(12299)
    }.get(char, '')

def echo(text, **kwargs):
    """ Print results to the console
    """

    if shakedown.cli.quiet:
        return

    if not 'n' in kwargs:
        kwargs['n'] = True

    if 'd' in kwargs:
        text = decorate(text, kwargs['d'])

    click.echo(text, nl=kwargs.get('n'))


@contextlib.contextmanager
def stdchannel_redirected(stdchannel, dest_filename):
    """ A context manager to temporarily redirect stdout or stderr
    """

    try:
        oldstdchannel = os.dup(stdchannel.fileno())
        dest_file = open(dest_filename, 'w')
        os.dup2(dest_file.fileno(), stdchannel.fileno())

        yield
    finally:
        if oldstdchannel is not None:
            os.dup2(oldstdchannel, stdchannel.fileno())
        if dest_file is not None:
            dest_file.close()