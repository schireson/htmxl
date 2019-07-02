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
