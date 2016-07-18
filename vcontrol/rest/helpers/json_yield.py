def json_yield_none(fn):
    """
    converts yields from request functions to JSON chunks
    sent back to sender
    """
    import functools
    import json

    json_yield_none._fn_id += 1
    fn_id = json_yield_none._fn_id

    @functools.wraps(fn)
    def _(self, key, *o, **k):
        """
        key should be unique to a session.
        Multiple overlapping calls with the same
        key should not happen (will result in
        ValueError: generator already executing)
        """
        if (fn_id,key) not in json_yield_none._gen_dict:
            new_gen = fn(self, key, *o, **k)
            json_yield_none._gen_dict[(fn_id,key)] = new_gen

        try:
           gen = json_yield_none._gen_dict[(fn_id, key)]
           content = gen.next()
           return json.dumps({'state': 'ready',
                              'content':content})
        except StopIteration:
           del json_yield_none._gen_dict[(fn_id,key)]
           return json.dumps({'state': 'done',
                              'content': None})
    return _

def json_yield_one(fn):
    """
    converts yields from request functions to JSON chunks
    sent back to sender
    """
    import functools
    import json

    json_yield_one._fn_id += 1
    fn_id = json_yield_one._fn_id

    @functools.wraps(fn)
    def _(self, arg, key, *o, **k):
        """
        key should be unique to a session.
        Multiple overlapping calls with the same
        key should not happen (will result in
        ValueError: generator already executing)
        """
        if (fn_id,key) not in json_yield_one._gen_dict:
            new_gen = fn(self, arg, key, *o, **k)
            json_yield_one._gen_dict[(fn_id,key)] = new_gen

        try:
           gen = json_yield_one._gen_dict[(fn_id, key)]
           content = gen.next()
           return json.dumps({'state': 'ready',
                              'content':content})
        except StopIteration:
           del json_yield_one._gen_dict[(fn_id,key)]
           return json.dumps({'state': 'done',
                              'content': None})
    return _

def json_yield_two(fn):
    """
    converts yields from request functions to JSON chunks
    sent back to sender
    """
    import functools
    import json

    json_yield_two._fn_id += 1
    fn_id = json_yield_two._fn_id

    @functools.wraps(fn)
    def _(self, arg1, arg2, key, *o, **k):
        """
        key should be unique to a session.
        Multiple overlapping calls with the same
        key should not happen (will result in
        ValueError: generator already executing)
        """
        if (fn_id,key) not in json_yield_two._gen_dict:
            new_gen = fn(self, arg1, arg2, key, *o, **k)
            json_yield_two._gen_dict[(fn_id,key)] = new_gen

        try:
           gen = json_yield_two._gen_dict[(fn_id, key)]
           content = gen.next()
           return json.dumps({'state': 'ready',
                              'content':content})
        except StopIteration:
           del json_yield_two._gen_dict[(fn_id,key)]
           return json.dumps({'state': 'done',
                              'content': None})
    return _
