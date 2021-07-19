Parser Compatibility
====================

By default, the package will detect installed parser libraries and choose the first one we find, so
a vanilla `Workbook()` instantiation should Just Work.

``` python
from htmxl.compose import Workbook

workbook = Workbook(parser='beautifulsoup')
workbook = Workbook(parser='lxml')
```

Importantly, the parsers will not exhibit identical behavior when handed the same templates.
In general the :code:`lxml` parser will be stricter and more prone to requiring "correct" HTML, while
:code:`beautifulsoup` is more permissive and will allow erroneous HTML. That tradeoff, however, generally
leads to lxml being noticeably faster with large amounts of data.

While you can look to the specific libraries for a comprehensive set of behaviors, we can
identify those which we've we've seen in the wild during the use of this library.

Closing Tags
------------
Lxml requires closing tags to be explicitly closed.

This manifests itself in two obvious ways that might allow a template to succeed with the BeautifulSoup
parser, while it might fail (raise an Exception) with lxml.

Consider 

.. code-block::

   <div>
      <span>Foo
   </div>

BeautifulSoup will happily allow the above template, while lxml will complain about the unclosed `<span>`
block.

Also consider

.. code-block::

   <div>
      Foo
      <br>
      Bar
   </div>

Self-closing tags, like :code:`br` must **also** have the closing part, i..e :code:`<br />` with
lxml.
