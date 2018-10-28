**`TA-EDFS`**

Based on my blogs post
https://www.splunk.com/blog/2016/02/04/sso-without-an-active-directory-or-ldap-provider.html
I came up with the idea to create this app, which enables/provides embedded
dashboards for Splunk (EDFS).

Please note this app is provided as is, and you need to make sure that your
environment is secured.

**What this app does?**

The app will provide new TCP port[s] that one can connect to, and automagically
gets authenticated as the configured user in Splunk.

Please be aware this app sets 'trustedIP=127.0.0.1' in 'server.conf'. Please
read http://docs.splunk.com/Documentation/Splunk/latest/Admin/Serverconf#General_Server_Configuration
to understand this option. The configured options in 'web.conf' are explained
in detail in the blog post linked at the top.

The configured EDFS dashboards are only accessible from the configured IP.
The app blocks any HTTP POST requests other then searches, so the EDFS port
cannot be used to change settings.

**Install:**

Install as usual in the Splunk web or copy into $SPLUNK_HOME/etc/apps and
restart Splunk.

**Configure:**

Copy 'default/inputs.conf' to 'local/' and use the provided stanza as template.
Configure the Splunk user with the least possible permissions (Make everything
read-only ), make a separate app, add the dashboard you want to show as the
default dashboard for the app.

Configure the EDFS inputs using the Splunk web in the inputs section. You need
to configure the Splunk user that will be authenticated, the port Splunk will
listen on, and the IP that is allowed to connect to the port.

**Debug**

Currently there is no debug option in the app, but the app logs all connections
into 'index=_internal sourcetype=splunkd_edfs_access'

**Support**

This is an open source project, no support provided, but you can ask questions
on answers.splunk.com and I will most likely answer it.
Github repository: https://github.com/M-u-S/TA-EDFS

**Things to-do / Future ideas**

- Add SSL Support
- Allow multiple IP's to connect
- anything else ? `¯\_(ツ)_/¯`  

**Version**

`29. October 2018 : 0.1.0 / Initial`
