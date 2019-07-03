How To's
********

Writing Files Excel
===================

Single Page
-----------

TODO

Multi Page
-----------

TODO

Merging Cells
=============

Merging cells is performed in the template, and tries to match the html spec
by making use of the existing :code:`colspan` and :code:`rowspan` attributes
that you can set on elements like :code:`<th>` to change how many visual
cells they span across.

**Note** Currently merging cells are only supported in :code:`<th>` elements.


Merging Cells Horizontally
--------------------------

.. image:: /_static/colspan_row.png

.. code-block:: html

   <table>
     <thead>
       <tr>
         <th colspan="2">I'm spanning 2 columns!</th>
       </tr>
     </thead>
   </table>

Merging Cells Vertically
------------------------

.. image:: /_static/rowspan_row.png

.. code-block:: html

   <table>
     <thead>
       <tr>
         <th rowspan="3">I'm spanning 3 rows!</th>
       </tr>
     </thead>
   </table>


Creating a "container" row
--------------------------

.. image:: /_static/rowspan_contained_row.png

.. code-block:: html

   <table>
     <thead>
       <tr>
         <th rowspan="2">bar</th>
         <tr>
           <th>top1</th>
           <th>top2</th>
         </tr>
         <tr>
           <td>bottom1</td>
           <td>bottom2</td>
         </tr>
       </tr>
     </thead>
   </table>
