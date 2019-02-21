""" dummy place holder modular input to enable Embedded Dashboards for Splunk config """
__author__ = 'Michael Uschmann / MuS'
__date__ = 'Copyright $Oct 25, 2018 11:00:00 AM$'
__version__ = '0.1.1'

import sys
import os
import splunk.Intersplunk
import logging
import logging.handlers
import xml.dom.minidom
import xml.sax.saxutils
import subprocess

""" get SPLUNK_HOME form OS """
SPLUNK_HOME = os.environ['SPLUNK_HOME']

""" get myScript name and path """
myScript = os.path.basename(__file__)
myPath = os.path.dirname(os.path.realpath(__file__))

SCHEME = """<scheme>
    <title>EDFS</title>
    <description>Configure Embedded Dashboards For Splunk.</description>
    <endpoint>
        <args>
            <arg name="username">
                <title>Splunk Username</title>
                <description>This is the local Splunk user name to be used to login
                </description>
            </arg>
            <arg name="connect_from">
                <title>The IP that is allowed to connect</title>
                <description>This is the IP of the client that will connect and display the dashboard.</description>
            </arg>
            <arg name="port">
                <title>The port we are using to connect to</title>
                <description>This is the port the edfs proxy will listen on.</description>
            </arg>
        </args>
    </endpoint>
</scheme>
"""

def do_scheme():
    """ show a different setup screen """
    print SCHEME

def validate_arguments():
    """ we don't do any validation - yet """
    pass

# read XML configuration passed from splunkd
def get_config():
    try:
        config = {}
        # read everything from stdin
        config_str = sys.stdin.read()
        # parse the config XML
        doc = xml.dom.minidom.parseString(config_str)
        root = doc.documentElement
        conf_node = root.getElementsByTagName("configuration")[0]
        if conf_node:
            logging.debug("XML: found configuration")
            stanza = conf_node.getElementsByTagName("stanza")[0]
            if stanza:
                stanza_name = stanza.getAttribute("name")
                if stanza_name:
                    logging.debug("XML: found stanza " + stanza_name)
                    config["name"] = stanza_name
                    params = stanza.getElementsByTagName("param")
                    for param in params:
                        param_name = param.getAttribute("name")
                        logging.debug("XML: found param '%s'" % param_name)
                        if param_name and param.firstChild and param.firstChild.nodeType == param.firstChild.TEXT_NODE:
                            data = param.firstChild.data
                            config[param_name] = data
                            logging.debug("XML: '%s' -> '%s'" % (param_name, data))

        checkpnt_node = root.getElementsByTagName("checkpoint_dir")[0]
        if checkpnt_node and checkpnt_node.firstChild and checkpnt_node.firstChild.nodeType == checkpnt_node.firstChild.TEXT_NODE:
            config["checkpoint_dir"] = checkpnt_node.firstChild.data
        if not config:
            raise Exception, "Invalid configuration received from Splunk."
    except Exception, e:
        raise Exception, "Error getting Splunk configuration via STDIN: %s" % str(e)

    return config

def run_main():
    """ get the config """
    config = get_config()
    #process_string = '%s/bin/splunk cmd %s/00_start.sh %s %s %s' % (SPLUNK_HOME, myPath, config['username'], config['port'], config['connect_from'])
    process_string = 'export NODE_PATH="$NODE_PATH:%s"; %s/bin/splunk cmd node %s/dash-proxy.js %s %s %s' % (myPath, SPLUNK_HOME, myPath, config['username'], config['port'], config['connect_from'])
    subprocess.Popen(process_string, shell=True)

if __name__ == '__main__':
    """ Script must implement these args: scheme, validate-arguments """
    if len(sys.argv) > 1:
        if sys.argv[1] == '--scheme':
            do_scheme()
        elif sys.argv[1] == '--validate-arguments':
            validate_arguments()
        else:
            pass
    else:
        run_main()
