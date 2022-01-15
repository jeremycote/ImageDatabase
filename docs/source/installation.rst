Installation
============ 

Setup
-----
To get started, you will need `Python3 <https://www.python.org/downloads/>`_.

1. Create a virtual environment

.. code-block:: shell

       python3 -m pip install virtualenv
       virtualenv venv

2. Install required packages

.. code-block:: shell

       source venv/bin/activate
       python3 -m pip install -r requirements.txt
       
3. Run either the development or production server

.. code-block:: shell
    :caption: Production Server

       chmod +x ProdServer.sh
       ./ProdServer.sh

.. code-block:: shell
    :caption: Development Server

       chmod +x DevServer.sh
       ./DevServer.sh

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

