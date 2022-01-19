ImageDatabase
=============
.. image:: https://readthedocs.org/projects/jerrytheberry-imagedatabase/badge/?version=latest
    :target: https://jerrytheberry-imagedatabase.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://github.com/jeremycote/ImageDatabase/actions/workflows/python-app.yml/badge.svg
    :target: https://github.com/jeremycote/ImageDatabase/actions/workflows/python-app.yml
    :alt: Python Tests status

.. image:: https://github.com/jeremycote/ImageDatabase/actions/workflows/node.js.yml/badge.svg
    :target: https://github.com/jeremycote/ImageDatabase/actions/workflows/node.js.yml   
    :alt: Node.js Tests status

.. image:: https://img.shields.io/website-up-down-green-red/https/imagedatabase-thoh6yxbsa-uc.a.run.app/.svg
    :target: https://imagedatabase-thoh6yxbsa-uc.a.run.app/
    :alt: Demo Website Status


Shopify Data Engineer application challenge

.. intro

ImageDatabase has two methods for finding images: a metadata search and recommendations for similar looking images. The metadata search looks through an SQL database created using the `EXIF <https://en.wikipedia.org/wiki/Exif>`_ data and filename of each image file in the images/raw directory. The recommendations for similar looking images are generated using `resnet18 <https://pytorch.org/hub/pytorch_vision_resnet/>`_, a library for Deep residual networks pre-trained on ImageNet.

You can add your own .jpg images by adding them to the images/raw directory. They will be added to the database on startup.

To get started, visit the `Install and Setup Guide <https://jerrytheberry-imagedatabase.readthedocs.io/en/latest/installation.html>`_.

Links
-----
* Documentation: https://jerrytheberry-imagedatabase.readthedocs.io/en/latest/index.html
* Live Demo: https://imagedatabase-thoh6yxbsa-uc.a.run.app/

Note: Live Demo may take 2-3 minutes to serve webpage if it was asleep.
