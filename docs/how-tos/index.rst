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


Styling Cells
=============

The styling of cells is done using the html :code:`class` attribute on an element.
Using a style works similarly to the normal html. To apply a style "class", you simply
set :code:`class="style-name"` on an element.

You can compose a specific style from a number of more generic styles
by simply including all the styles separated by a space i.e. :code:`class="xl-centered xl-underlined"`.
Simlar to html, in the event 2 styles set the same style attribute, the last one to set a particular
style attribute "wins".

Make use of default styles
--------------------------

The library exposes some basic builtin styles for convenience. To see the full
set, for the current version of your library you can run:

.. code-block:: python

   >>> from htmxl.compose.style import default_styles
   >>> print([style['name'] for style in default_styles])
   ['xl-centered', 'xl-underlined']

And to use those styles, the classes would

.. code-block:: html

   <tr class="xl-centered">
     <td>c1</td>
     <td>c2</td>
   </tr>


Combining styles together
-------------------------

.. code-block:: html

   <tr class="xl-centered xl-underlined">
     <td>c1</td>
     <td>c2</td>
   </tr>


Define custom styles
--------------------

.. code-block:: python

   from htmxl.compose import Workbook

   template = """
       <body>
           <div>
               <span class="title">foo</span>
           </div>
           <div>
               {% for column_name in column_names %}
                   <span class="xl-centered xl-underlined {{ loop.cycle('odd', 'even')}}">{{ column_name }}</span>
               {% endfor %}
           </div>
       </body>
   """

   styles = [
       {"name": "title", "pattern_fill": {"patternType": "solid", "fgColor": "DDDDDD"}},
       {"name": "odd", "pattern_fill": {"patternType": "solid", "fgColor": "FBEAFB"}},
       {"name": "even", "pattern_fill": {"patternType": "solid", "fgColor": "DFE7F8"}},
   ]


   workbook = Workbook(styles=styles)
   workbook.add_sheet_from_template(template=template, data=dict(column_names=["bar", "baz", "bax"]))
   workbook.compose("filename.xslx")

.. image:: /_static/custom_styles.png
