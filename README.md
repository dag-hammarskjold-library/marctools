I put together a basic conversion tool we can re-use to make pymarc readable JSON from JMARC data. 

https://github.com/dag-hammarskjold-library/marctools

You can install it in your virtualenv by running:

pip install 'git+https://github.com/dag-hammarskjold-library/marctools.git'

There’s only one tool included right now, but we can always expand it to include others. Reference it in your code like so:

from marctools import pymarcer

pmjson = pymarcer.make_json(jmarc)

OR

from marctools.pymarcer import make_json

pmjson = make_json(jmarc)

If you run into any issues, let me know. We should be able to use this to make MARC21, which is our next step, I think.
