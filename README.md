# AI as a Service - Showcase Application

The main purpose of this app is to showcase all the posibilities that the 
existing cloud services can offer in terms of AI services accessible to anyone.

## Requirements

- Python 3.7+
- Poetry: for instructions see https://python-poetry.org/docs/

## Installation

1. Verify Python and Poetry installation

    ```bash
    $ cd aiaas-showcase-app
    $ poetry env info
    # you should get a similar output
    Virtualenv
    Python:         3.7.11
    Implementation: CPython
    Path:           NA

    System
    Platform: darwin
    OS:       posix
    Python:   /path/to/python/3.7.11
    ```

2. Create virtual environment and install dependencies:

    ```bash
    $ cd aiaas-showcase-app
    $ poetry install
    ```

3. Configure environment:

    You will create a your service account key and download it as a JSON key file from 
    Google Cloud. This file is required by the app to be able to access google services. 
    To create and download this file follow the instructions [here](https://cloud.google.com/vision/docs/quickstart-client-libraries).

    Once downloaded, you need to set the environment variable GOOGLE_APPLICATION_CREDENTIALS to 
    the path of this file. This variable only applies to your current shell session, 
    so if you open a new session, set the variable again.

    To setup the environment variable you have 2 options:

    ### Option 1:

    You can create a `.env` file on the repository root folder with this content:

    ```
    GRPC_DNS_RESOLVER=native
    GOOGLE_APPLICATION_CREDENTIALS="/path/to/json/key/file/downloaded/from/google-cloud"
    ```

    ### Option 2:

    Set it directly from the CLI:

    ```bash
    export GRPC_DNS_RESOLVER=native
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/json/key/file/downloaded/from/google-cloud"
    ```

4. Run the application:

    ```bash
    $ cd aiaas-showcase-app
    $ poetry run flask run
    ```