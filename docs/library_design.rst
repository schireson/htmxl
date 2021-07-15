Library Design
==============

Key Ideas:

    * Custom composed excel documents require a markdown capability to design and update
    * HTML is an exceptional markdown languagge for this:
        * Native support for styling of blocks of content
        * Commonly understood semantics for basic tags
        * syntax for adding style and attributes to blocks
        * Existing templating dialects
        * Extremely good support for table design
    * Templating languages exist to dynamically generate HTML from data

Libraries being used:

    * openpyxl
        * Reads and writes excel files
        * Applies built in styles
        * Provides low and medium level APIs for doing excel manipulation
    * beautifulsoup4
        * Parse raw HTML and provides iterables for writing out cells in excel
        * Provides access to tag level attribute and style notions
    * Jinja2
        * Provides good python support for in-template flow control and variable access and templating
        * Could be replaced by any templating engine. It is only used to create raw HTML.

Implementation Design
---------------------

This information is not necessary to use this library, but might help contribution, and reduction of "magic".

The writing implementation is built on few concepts:

    * A "cursor" or "write head" concept, implemenated in part by :class:`htmxl.compose.write.Writer`.
        * This cursor moves around a sheet, writing data and applying styles, etc.
        * This cursor keeps "recordings" of where it has been within the context of writing a "tag".
            * This permits nested tags each applying/overriding styles from their parents
            * This also allows for the implementation of cell merging
    * A :function:`htmxl.compose.write.write` function
        * Knowns how to interpret each HTML tag, or delegates to a specific tag implementation function
        * Is a recursive function, allowing deeply nested tags
    * Tag specific implementation functions
        * Specify where the cursor should end up after the tag is finished being written.
        * Typically calls the generic :function:`htmxl.compose.write.write` function on all its child elements.
    * A mix of supported inline styles and single class based styling. While the underlying excel library supports "adding" styles together, the current implementation only permits one class per element.



