=========================================
``Sept``: Simple Extensible Path Template
=========================================

Introduction
============

``Sept`` is a simple to configure templating system designed at relatively simple path translation or path generation from a dictionary of data.

With ``Sept``, non developers can modify templates that will allow them to conform to a wide range of file naming requirements.

Why was ``Sept`` created?
=========================
Sept was created due to a problem that I have experienced several times thoughout my time in the visual effects industry.

A visual effects studios will be working on several projects at the same time, often from different movies studios. Each of these movie studios will have very strict naming conventions that the visual effects studio will have to conform to when delivering finished work back.

Many legacy visual effects studios will often write automation software that relies on specific strict naming, often with critical differences from the movie studio's requirements.
Because of this, the visual effects studios will usually work with a standardized internal naming scheme and will provide a way to customize renaming the files before they leave.
Sometimes this is a complex templating language, often built on top of languages like `jinj2 <https://palletsprojects.com/p/jinja/>`_, which while powerful, almost requires you to know how to program in python just to make it syntactically correct.
Other times, studios may just rely on batch renaming tools and a poor employee having to rename things by hand.

In all cases, this method and the specifics of implementation are propriatry and must be learned by employees joining the company.
``SEPT`` proposes a standard baseline template language that can be used across any studio that wishes to accept it.

In addition to the language syntax, ``SEPT`` also provides a set of modular graphical components that can be used to get developers up and running quickly.

What does ``SEPT`` look like?
=============================

At a barebones level, ``SEPT`` is a ``Token`` surrounded by two sets of open and close brackets.
.. code-block:: python

   My name is {{name}} and my job is {{job}}

When you get more complex with ``SEPT``, you may see the use of an ``Operator`` in front of the ``Token``.
The syntax for this is a small step up, instead of putting your ``Token`` within the brackets, you first write your ``Operator`` followed by a full colon ``:`` and then your ``Token``
.. code-block::

   My name is {{upper:name}} and my job is {{lower:job}}

In the above example you see usage of :ref:`lower-token-api<lower>` and :ref:`upper-token-api<upper>`
There are several different ``Operator`` keywords that are provided by this library, however developers can include their own custom ``Operator`` functions depending on the specific use case.

Learning More
=============
If you would like to learn more, we have a :ref:`developer-introduction<developer introduction>` and :ref:`non-developer-introduction<user introduction>`

You can also visit the :ref:`api<Api Reference Page>`.