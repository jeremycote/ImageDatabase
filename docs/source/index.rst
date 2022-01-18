.. Image Database documentation master file, created by
   sphinx-quickstart on Thu Jan 13 10:16:18 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Image Database's documentation!
==========================================
ImageDatabase has two methods for finding images: a metadata search and recommendations for similar looking images. The metadata search looks through an SQL database created using the `EXIF <https://en.wikipedia.org/wiki/Exif>`_ data and filename of each image file in the PATH_IMAGES_RAW directory. The recommendations for similar looking images are generated using `resnet18 <https://pytorch.org/hub/pytorch_vision_resnet/>`_, a library for Deep residual networks pre-trained on ImageNet.

To get started, visit :doc:`installation`

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   modules


.. include:: ../README.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
