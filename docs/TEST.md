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

Writing Tests
====

Simple create a new function in one of the test file under the tests directory with the prefix `test_` and py.test will automatically pick them up the next time that `make test` is run.
