# AwAws
Dilex AWS Botocore/Boto3 Wrapper SDK

![Python application](https://github.com/DilexNetworks/AwAws/workflows/Python%20application/badge.svg)

## Why?

Yeah, boto3 is awsome but it's also pretty dense.  Using a service like SQS
is a real pain when you have to deal with stuff on the JSON level, especially
when a lot of options in there is not really are that useful.  That said, the
main idea behind this module is to provide a simple interface to make life a 
lot easier when using boto3 or botocore.  If you need the full power of boto3,
then maybe this is not the module for you, if you are doing some simple things 
in boto3 then you might find these wrappers fairly useful.

This package is used as a foundation for using AWS Lambda. This
package will typically be installed on Lamabda Service as a Layer.  

Ultimately, this project is about creating a nice interface bewteen your code
and Aws - so when boto4 comes out, all of the code that needs to be refactored
all lives in one place.


## Install
Steps to get up and running with AwAws:
1) Install python virtualenvwrappers (if you don't already have it)
   More info at: https://virtualenvwrapper.readthedocs.io/en/latest/
   or this awesome blog post: https://www.dilex.net/data-blog/python-virtual-environments-on-osx

2) Create a new virtual environment:
```
mkvirtualenv -p python3 thaws (or thynk)
```

3) Install all of the required modules:
```
pip install -r requirements.txt
```
Now, `pytest` to make sure everything is setup correctly
+ `pytest -v` will give a list of all of the tests being run with statuses
+ `pytest --flake8` to run syntax checking
+ `pytest --bandit` to run security checks

## Creating a Release
No automatic way to do this right now.  Update the `setup.py` file
with the latest version (use semantic version numbers i.e., v1.2.1)

Tag the branch and push it up:
```
git tag -a v0.1.0 -m 'this is a note about this version'
git push --tags
```

## Testing AWS Events
There is a lot of data in each AWS event.  We don't necessarily need
all of the data AWS passes around but it is useful to have the entire
even syntax available for testing.  Fortunately, the `sam` cli tool now
has some helper functions to getnerate the event syntax for a number of
common events.  This allows us to create dufferent events an ensure that
our code is handling the event correctly.

To get a list of available event type, use the cli command:
```
sam local generate-event --help
```
An example that gets a specifc event:
```
sam local generate-event apigateway aws-proxy
```
The output of that command can be redirected to a file, typically put
in a directory called `support` in the directory containing the tests that
will use the event.  Then use the `datadir` fixture with the test that will
use the event.

```
def test_some_stuff(datadir):
    with open(datadir.join('event_file.json'), 'r') as event:
        # now use `event` to passing into the function being tested
```


## Using AwAws in your modules
Include the AwAws module in the `requirements.txt` file for this project,
referring to the correct version tag.  An example requirements.txt file
may look like the following:

```
git+ssh://git@github.com/DilexNetworks/AwAws.git@branch-name#tag-name
```
where:
+ __branch-name__ is the name of the branch to load from (typically *master*)
+ __tag-name__ is the release tag on the branch to load from

When building the `requirements.txt` for a project, keep in mind that
the dependencies for this module (i.e., the dependencies in this module's
requirements.txt file) are not automatically loaded by pip when using the
git checkout syntax above.  In a sense, this is desired as is allows you
to chose the dependencies that you will be using without grabbing a lot
of unnecessary modules. This is of particular importance to AWS lambda
code which should be kept as small as possible.

**NOTE 1:** AwAws can be loaded into a lambda layer and then included in
lambda code. This simplifies the configuration and setup of new lambdas.

**NOTE:** It is highly recommended that a branch and/or tag name
are used as changes to the repo by other developers may cause
unexpected issues (and nobody like unexpected issues).

## Details

This project is using botocore directly to interface to AWS

### I know it's a stupid name

One of the hardest things in computer programming is naming things. So when your
initials are AW and you are writing a wrapper for AWS boto it seems reasonable
to just smush those things together to get AwAws.  In my head it's A W Aws, but
I suspect people will just call is awaws (ah-whas) which is fine by me.

