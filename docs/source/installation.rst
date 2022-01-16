Installation
============ 

To run ImageDatabase, there are two options.
1. Run as Docker container (Recommended).
2. Setup server manually ().

Docker Setup
------------

.. code-block:: shell

       docker build -t "image-database:Dockerfile" .
       docker run --name ImageDatabase -d -p 5000:5000 image-database:Dockerfile

Manual/Dev Setup
------------
To get started, you will need `Python3 <https://www.python.org/downloads/>`_.

1. Install pip and virtualenv

.. code-block:: shell

       python -m ensurepip --upgrade
       python -m pip install virtualenv

2. Create and activate virtualenv

.. code-block:: shell
    :caption: Linux and MacOS
       
       virtualenv venv
       Linux/MacOS: source venv/bin/activate

.. code-block:: shell
    :caption: Windows

       virtualenv venv
       Windows: venv/Scripts/activate

3. Install required packages

.. code-block:: shell

       python -m pip install -r requirements.txt
       
4. Production server is only available on UNIX. Follow instructions below for your desired environment.

.. code-block:: shell
    :caption: Production Server using UNIX

       chmod +x ProdServer.sh
       ./ProdServer.sh

.. code-block:: shell
    :caption: Development Server using UNIX

       chmod +x ./DevServer.sh
       ./DevServer.sh

.. code-block:: shell
    :caption: Development Server using windows

       .\DevServerWin.ps1

Updating frontend
-----------------
Important: Only required if you want to make changes to frontend. The build command will replace the contents of static/dist with a new build of the frontend project.

To get started, you will need `Node JS <https://nodejs.org/en/>`_.

1. Install dependencies

.. code-block:: shell

       cd frontend
       npm install

2. Build project

.. code-block:: shell

       npm run build

3. (Only required on Windows) Move build

.. code-block:: shell

       rmdir ../static/dist
       mv dist ../static/dist