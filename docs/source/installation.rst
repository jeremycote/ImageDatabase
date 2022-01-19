Installation
============ 

To run ImageDatabase, there are two options.

1. Run as Docker container (Recommended).
2. Setup server manually (For Development).

Docker Setup
------------
To get started, you will need `Docker <https://www.docker.com/get-started>`_.

.. code-block:: shell
    :caption: For standalone Container.

       git clone https://github.com/jeremycote/ImageDatabase.git
       cd ImageDatabase
       docker build -f SelfSignDockerfile -t "image-database:SelfSignDockerfile" .
       docker run --env PORT=5000 --name ImageDatabase -d -p 5000:5000 image-database:SelfSignDockerfile

.. code-block:: shell
    :caption: If ssl is handled externally. Ex: Google Cloud Run.

       git clone https://github.com/jeremycote/ImageDatabase.git
       cd ImageDatabase
       docker build -t "image-database:Dockerfile" .
       docker run --env PORT=5000 --name ImageDatabase -d -p 5000:5000 image-database:Dockerfile

Manual/Dev Setup
----------------
To get started, you will need `Python3 <https://www.python.org/downloads/>`_ and `Node JS <https://nodejs.org/en/>`_.

1. Install pip and virtualenv

.. code-block:: shell

       python -m ensurepip --upgrade
       python -m pip install virtualenv

2. Download git repository

.. code-block:: shell

       git clone https://github.com/jeremycote/ImageDatabase.git
       cd ImageDatabase

3. Activate virtual python environment.

.. code-block:: shell
    :caption: Linux and MacOS
       
       virtualenv venv
       source venv/bin/activate

.. code-block:: shell
    :caption: Windows

       virtualenv venv
       venv/Scripts/activate

4. Install required packages

.. code-block:: shell

       python -m pip install -r requirements.txt

5. Build frontend.

.. code-block:: shell

       cd frontend
       npm install
       npm run build

       Only if using Windows:
       rmdir ../static/dist
       mv dist ../static/dist

6. Start development server

.. code-block:: shell

       python app/main
