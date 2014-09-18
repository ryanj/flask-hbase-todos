## Todo Application##

A simple todo list application built on Python 2.7, [Flask](http://flask.pocoo.org/), and [Twitter Bootstrap](http://getbootstrap.com/).  [HappyBase](http://happybase.readthedocs.org/en/latest/index.html) is used to provide easy hbase access to a remote [Hortonworks](http://hortonworks.com/) cluster.

In order to follow along, you'll need:
* The [HortonWorks Sanbox](http://hortonworks.com/products/hortonworks-sandbox/), or an Amazon account for hosting a HortonWorks Hadoop AMI.
* VirtualBox
* git
* ssh
* RubyGems
* Python (with easy_install or pip)
* a Free [OpenShift Online](http://openshift.com/) account
* and, the [RHC](https://www.openshift.com/get-started#cli) command-line tool

The [rhc command-line tool](https://www.openshift.com/get-started#cli) can be installed via RubyGems with:

```bash
gem install rhc
```

After signing up for an OpenShift account, and installing `rhc`, you'll be able to configure your local machine to work with your new cloud applications:

```bash
rhc setup
```

Now that your development environment is ready, spin up a fresh copy of this app in a single command:
```bash
$ rhc app create todo python-2.7 --from-code=https://github.com/ryanj/flask-hbase-todos HBASE_HOST=MY_REMOTE_HBASE_HOST HBASE_PORT=9090
```

If you already have a Hadoop cluster available, enter it's host URL or IP address as the value to your application's `HBASE_HOST` key.

For this application, we'll use the `HBASE_HOST` environment variable to help keep our source clean, and to help enhance the project's portability and reusablility.

If you choose to create your application using [OpenShift's web workflow](https://www.openshift.com/blogs/launching-applications-with-openshifts-web-based-workflow), or if you would like to make changes to your app's current "HBASE_HOST" setting, run the following (assuming "todo" is your app name):
```bash
$ rhc env set HBASE_HOST=MY_REMOTE_HBASE_HOST -a todo
$ rhc env set HBASE_PORT=MY_REMOTE_HBASE_PORT -a todo
```

OpenShift operators can also make `hbase` service connection strings available to developers as a cartridge, by installing a modified copy of this [hbase-external cart](https://github.com/ryanj/openshift-cartridge-hbase-external) into their [OpenShift Enterprise](https://www.openshift.com/products/enterprise) or [Origin](https://www.openshift.com/products/origin) environments.

### AMIs from HortonWorks
Hosting your own Hadoop in the cloud is a breeze with the `HDP2_REDSHIFT_DEMO_AMI` image, available in Amazon's US East Region.

Just click 'Launch', then open up port `9090` for outside access, allowing your OpenShift environment to connect directly to your new datastore.

Then, make sure to pass your `HBASE_HOST`, and `HBASE_PORT` to your application through the system environment, as documented in the previous section.

### HortonWorks Sandbox
The [HortonWorks Sandbox](http://hortonworks.com/products/hortonworks-sandbox/) is an excellent choice for local development scenarios.

After firing up the Sandbox virtual environement, you'll be presented with instructions on how to connect to the Hortonworks Hadoop web dashboard.

Support for Hbase can be enabled in just a click or two.

### Local Developmet

Flask, happybase, and a [HoronWorks Sandbox](http://hortonworks.com/products/hortonworks-sandbox/) are all required for setting up your local development environment.

When you create an application using the `rhc` command-line tool, a local copy of your project source code will automatically be created for you to work with.

If you created your application using a web-based workflow, you can always retrieve your project source with:

```bash
rhc git-clone todo
```

Then, run the following to start your local server:
```bash
python app.py
```

***Enjoy!***

## License
This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to CC0 (http://creativecommons.org/publicdomain/zero/1.0/)
