Running Tests
====

The following dependencies are required for running the testing suite:

- docker
- git
- make

To run the testing suite, perform the following:

```
git clone https://github.com/CyberReboot/vcontrol.git
cd vcontrol
make test
```

The build time will take a little while the first time, but subsequent runs will be much fast as it makes use of caching.  The output at the end will give a detailed report of the tests that ran, which ones passed or failed, and the line number coverage for each python file in the project.

The tests use `py.test` and are located under the tests folder.  The tests are broken into the three areas of the project, the main `vcontrol.py` file that controls everything, and then the `cli` (actions run from the command line) functions and the `rest` (actions run from the browser) functions.

To run the tests more quickly in development:

Attach your current checkout's tests folder to the container's volume using the "-v" command in you docker "run" statement. For example ```-v ~/repos/vcontrol/tests/:/vcontrol/tests/```, where your local checkout is ```~/repos/vcontrol/```:

```#>docker run --link vcontrol-daemon:localhost -it -v ~/repos/vcontrol/tests/:/vcontrol/tests/  --entrypoint py.test vcontrol /vcontrol -v --cov=/vcontrol/vcontrol --cov-report term-missing```

Then attach to the currently running container:

```#> docker exec -it vcontrol-daemon /bin/bash ```

Now you can edit your local checkout's tests in your IDE and run the tests quickly in the container using:

```#> py.test /vcontrol```


Writing Tests
====

Simple create a new function in one of the test file under the tests directory with the prefix `test_` and py.test will automatically pick them up the next time that `make test` is run.
