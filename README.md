# flask_api_sample
simple example of using flask to generate an api

## Setup

This project is used as a demonstration for Vagrant and Chef, and so there are several Git tags in the repository at particular checkpoints of the demonstration. 

* v0.1.0 - the original state of the project 
* v0.2.0 - Added Vagrant configuration with provisioning by chef_zero for a "development" environment 
* v0.3.0 - Added a second environment "test"
* v0.4.0 - Split out environment-specific application conifguration values into configuration files and deploying application services with Upstart scripts
* v0.5.0 - Added a third environment "production"
 
Feel free to play with this code and extract what you may find useful for your projects. Note, however that the "test" and "production" environments that are included here reference servers in Microsoft's Azure cloud environment, and so without credentials, you will not be able to run deployments to "test" and "production" environments. 

## Dependencies

This configuration has been tested successfully with Vagrant 1.8.1 and VirtualBox 4.3.30. Vagrant 1.7.3 will _not_ work with the specified `chef_zero` provisioner, however it can be reconfigured to use `chef_solo` with Vagrant 1.7.3.

The package dependencies for the project are documented as part of the IaC scripts (see `/cookbooks`). For reference, the following Python modules meet the application's requirements:

[Flask](http://flask.pocoo.org/)
:   `pip install Flask`

[Requests](http://docs.python-requests.org/en/latest/)
:   `pip install requests`

[flask-httpauth](https://flask-httpauth.readthedocs.org/en/latest/)
:   `pip install flask-httpauth`

[passlib](https://pythonhosted.org/passlib/)
:   `pip install passlib`

## How to Use This Application

Code after the v0.4.0 tag will deploy the services using Upstart configuration and will start after boot. Code prior to this tag requires that the services are started manually.

From a command line at the root of the project, run

	python flask_api.py

A list of `curl` commands to test the REST API is included in `curl_commands.txt`.

To test the api service using the Front End flask app, open another terminal window and run 

	python front_end.py

This sample uses a simple list of objects as our data store. The principles can be easily transferred to using a backend of your choice.

Code after the v0.2.0 tag can be executed within the development VM, and can be reached through `http://localhost:8000`, where port `8000` is forwarded to port `5001` within the VM. Code prior to this will simply run on your local machine and can be reached at `http://localhost:5001`. 

You can run tests from the command line by running 

	python api_tests.py

## Future Work

This demo/example would work great with a simple mongo backend and ORM implementation in the code.

## Acknowledgements

In preparing this demo, I consulted and pulled from a few tutorials online:

* [Designing a RESTful API with Python and Flask](http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)
* [RESTful Authentication with Flask](http://blog.miguelgrinberg.com/post/restful-authentication-with-flask)
* [How to Build an API with Python and Flask](http://tech.pro/tutorial/1213/how-to-build-an-api-with-python-and-flask)
* [PassLib Tutorials](https://pythonhosted.org/passlib/)
