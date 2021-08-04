Supported Elements
==================

The root :code:`<html>` tag is supported, but optional. One can do any of:

* Define html content nested within an :code:`<html>` block
* Define top-level :code:`<head>` and :code:`<body>` sibling blocks
* Omit :code:`<body>` entirely (if you have no :code:`<head>`) and define all
  markup at the top level.


<head>
------
This block is optional.

Today, any raw content in the :code:`head` section is essentially a shortcut for
specifying a page :code:`<title>`.

<title>
~~~~~~~
Any raw content is interpreted as the Excel sheet name.


<body>
------

This block is optional, should you not define a :code:`<head>` block for setting the
sheet name.


The child elements defined within a body follow a number of different "block" semantics
which essentially attempt to mimic the semantics of HTML itself.

At a high level, they boil down to a few different options that we'll call:

* top-level
* top-right
* bottom-left
* bottom-right

The name indicates where the "cursor" will be left after exiting the context of the enclosing block
being defined.

For example a :code:`<div>` (described in the next section) is a bottom-left-type, which means
that after performing the layout for the content of that div, the bounding box defined by the interior
content of the :code:`<div>` will be calculated and layout for sibling elements **after** that div
will start at the bottom-left of that bounding box.

.. code-block::

   +- div -------------------------------------------+
   |+- table ---------------------------------------+|
   ||+- thead -------------------------------------+||
   |||+- th ----+-- th -----+-- th -----+ -- th --+|||
   |||| example | example 2 | example 3 | example ||||
   |||+---------+-----------+-----------+---------+|||
   ||+---------------------------------------------+||
   ||                                               ||
   ||+- tbody -------------------------------------+||
   |||+- tr --------------------------------------+|||
   ||||+- td ---+-- td ----+-- td ----+ -- td ---+||||
   ||||| qwertu | abcdefgh | 23456789 | 12345678 |||||
   ||||+--------+----------+----------+----------+||||
   ||||                                           ||||
   ||||+- td ---+-- td ----+-- td ----+ -- td ---+||||
   ||||| qwertu | abcdefgh | 23456789 | 12345678 |||||
   ||||+--------+----------+----------+----------+||||
   |||+-------------------------------------------+|||
   ||+---------------------------------------------+||
   |+-----------------------------------------------+|
   +-------------------------------------------------+

   +- div -------------------------------------------+
   + ... more content ...                            |
   +-------------------------------------------------+

Note, ASCII/graphics will not be a perfect visualization, as it pushes the content to the right as
nesting occurs, which will not occur in Excel. However, it should give a sense of where content
will start after certain kinds of elements close, and hopefully should give some initial intuition
what *kind* (top-left, bottom-left, top-right) each element might be.

<div>
~~~~~
A :code:`div` is a bottom-left element. Content after a :code:`div` will resume in the cell directly
below the :code:`div`'s interior content.

It has no behavior other than the laying out of child elements.


<span>
~~~~~~
A :code:`<span>` is a top-right element. Content after a :code:`<span>` will resume in the cell directly
to the right of the :code:`<span>`'s interior content.

Generally a :code:`<span>` will only contain raw text content.


<br>
~~~~
A :code:`<br>` is a bottom-left element. Content after a :code:`<br>` will resume in the cell directly
below the :code:`<br>`. It has no interior content.


<table>
~~~~~~~
A :code:`<table>` is a bottom-left element. Content after a :code:`<table>` will resume in the cell directly
below the :code:`<table>`.

A :code:`<table>` is essentially a :code:`<div>`, but for the purpose of defining a visual table
structure.


<thead/tbody>
~~~~~~~~~~~~~
These elements exist primarily to group the table content, but otherwise will not affect layout,
relative to the table itself. They are both bottom-left element types.

It **can** be a convenient markup location to apply styling (which will naturally cascade to the
relevant subsections of the table).

<tr>
~~~~
A :code:`<tr>` is a bottom-left element. Content after a :code:`<tr>` will resume in the cell directly
below the :code:`<tr>`.

<th/td>
~~~~~~~
These elements are semantically equivalent to a :code:`<span>`, but for the purpose of defining
a table's cell content.

<datalist>
~~~~~~~~~~
A :code:`<datalist>` element does not get directly rendered into the excel file. As such
a datalist element will not have any effect on the placement of the cursor or layout
of actual DOM elements.

Referencing the `documentation <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/datalist>`_ on what a datalist does, it will register the set of :code:`<option>` children as a form of cell validation in the document.

For example:

.. code-block:: html

   <datalist id="truthy-values">
     <option value="true" />
     <option value="false" />
     <option value="maybe" />
   </datalist>

   <input list="truthy-values">

In this case, an excel data validation will be registered and then applied to the cell pointed at by the :code:`<input>`.

That will then be represented in the excel file like so

.. image:: /_static/datalist_example.png
