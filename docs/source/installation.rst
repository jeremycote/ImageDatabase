Installation
============ 

To run ImageDatabase, there are two options.

1. Run as Docker container (Recommended).
2. Setup server manually (For Development).

Docker Setup
------------

.. code-block:: shell
    :caption: If ssl is handled externally. Ex: Google Cloud Run.

       git clone https://github.com/jeremycote/ImageDatabase.git
       cd ImageDatabase
       docker build -t "image-database:Dockerfile" .
       docker run --env PORT=5000 --name ImageDatabase -d -p 5000:5000 image-database:Dockerfile

.. code-block:: shell
    :caption: For standalone Container.

       git clone https://github.com/jeremycote/ImageDatabase.git
       cd ImageDatabase
       docker build -t "image-database:Dockerfile" .
       docker run --env PORT=5000 --name ImageDatabase -d -p 5000:5000 image-database:SelfSignDockerfile

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

4. Build frontend

.. code-block:: shell
    :caption: you will need `Node JS <https://nodejs.org/en/>`_.
       cd frontend
       npm install
       npm run build

       Only if using Windows:
       rmdir ../static/dist
       mv dist ../static/dist

5. Development server

.. code-block:: shell
    :caption: Development Server using UNIX

       source venv/bin/activate
       python app/main

.. code-block:: shell
    :caption: Development Server using Windows

       venv/Scripts/activate
       python app/main
