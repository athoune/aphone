Aphone
======

Reading Aspell grammar format and exposing the result as a plain JSON.
Now you can implement your automat with any language, any variants.

Soon, a Java Lucene Filter, python, cython, ruby, javascript…

Install
-------

From pypi:

    sudo pip install aphone

Or from source:

    python setup.py build
    sudo python setup.py install

Usage
-----

Download a dictionnary from [Aspell](ftp://ftp.gnu.org/gnu/aspell/dict/0index.html)
or find it in your Linux. In Ubuntu, they are in _/usr/lib/aspell/_ folder.

Now, you are looking a file like _fr.dat_ if you are looking for fr dictionnary.

    aphone path/to/fr.dat

It will print phonetic rules as a json.

You can test one word:

    aphone path/to/fr.dat carotte

It answers

    KAROTE


Licence
-------

It's a tool which generate JSON for other tools, why not GPL like GCC?

GPL v3.
