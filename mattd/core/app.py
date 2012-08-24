# TODO - LICENSE
#
# Based on an example from the CMUSphinx project.
# Copyright (c) 2008 Carnegie Mellon University.
#
# You may modify and redistribute this file under the same terms as
# the CMU Sphinx system.  See
# http://cmusphinx.sourceforge.net/html/LICENSE for more information.

import pkg_resources

import gtk
import pygst
pygst.require('0.10')
import gst

import logging
log = logging.getLogger("mattd")

# TODO - remove this
logging.basicConfig(level=logging.DEBUG)


class MattDaemon(object):

    def __init__(self):
        """Initialize the speech components"""
        self.active_plugin = None
        self.plugins = []
        for plugin_cls in pkg_resources.iter_entry_points("mattd.plugins"):
            log.info("Loading plugin %r" % plugin_cls.name)
            try:
                plugin = plugin_cls(self)
                self.plugins.append(plugin)
            except Exception as e:
                log.warn("%r failed.  %r" % (plugin_cls.name, e))

        log.info("Loaded %i plugins." % len(self.plugins))

        one_second_in_nanoseconds = 1000000000

        def dict2properties(d):
            return " ".join([
                "%s=%s" % (k, str(v)) for k, v in d.items()
            ])

        vader_properties = {
            'name': 'vader',
            'auto-threshold': 'true',
            'run-length': one_second_in_nanoseconds,
            'pre-length': one_second_in_nanoseconds,
        }
        self.pipeline = gst.parse_launch(
            'gconfaudiosrc ! audioconvert ! audioresample '
            + '! vader %s ' % dict2properties(vader_properties)
            + '! pocketsphinx name=asr ! fakesink')
        asr = self.pipeline.get_by_name('asr')
        asr.connect('partial_result', self.asr_partial_result)
        asr.connect('result', self.asr_result)
        asr.set_property('configured', True)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::application', self.application_message)

        self.pipeline.set_state(gst.STATE_PLAYING)

    def asr_partial_result(self, asr, text, uttid):
        """Forward partial result signals on the bus to the main thread."""
        struct = gst.Structure('partial_result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        asr.post_message(gst.message_new_application(asr, struct))

    def asr_result(self, asr, text, uttid):
        """Forward result signals on the bus to the main thread."""
        struct = gst.Structure('result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        asr.post_message(gst.message_new_application(asr, struct))

    def application_message(self, bus, msg):
        """Receive application messages from the bus."""
        msgtype = msg.structure.get_name()
        content = msg.structure['hyp']
        if msgtype == 'partial_result':
            log.debug(content)
        elif msgtype == 'result':
            self.pipeline.set_state(gst.STATE_PAUSED)

            if not self.active_plugin:
                for plugin in self.plugins:
                    if plugin.matches_keyphrase(content):
                        self.active_plugin = plugin
                        break

            if self.active_plugin:
                self.active_plugin.handle(content)

            self.pipeline.set_state(gst.STATE_PLAYING)


def _daemonize(func):
    from daemon import DaemonContext
    try:
        from daemon.pidfile import TimeoutPIDLockFile as PIDLockFile
    except:
        from daemon.pidlockfile import PIDLockFile

    pidlock = PIDLockFile('/var/run/mattd/mattd.pid')
    output = file('/var/log/mattd/mattd.log', 'a')
    daemon = DaemonContext(pidfile=pidlock, stdout=output, stderr=output)
    #daemon.terminate = _handle_signal

    with daemon:
        return func()


def main(daemonize=True):
    def payload():
        app = MattDaemon()
        gtk.main()

    if daemonize:
        _daemonize(payload)
    else:
        payload()

if __name__ == '__main__':
    main(False)
