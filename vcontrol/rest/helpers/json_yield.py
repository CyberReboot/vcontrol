def json_yield(fn):
    """
    converts yields from request functions to JSON chunks
    sent back to sender
    """
    import functools
    import json

    json_yield._fn_id += 1
    fn_id = json_yield._fn_id

    @functools.wraps(fn)
    def _(self, arg, key, *o, **k):
        """
        key should be unique to a session.
        Multiple overlapping calls with the same
        key should not happen (will result in
        ValueError: generator already executing)
        """
        if (fn_id,key) not in json_yield._gen_dict:
            new_gen = fn(self, arg, key, *o, **k)
            json_yield._gen_dict[(fn_id,key)] = new_gen

        try:
           gen = json_yield._gen_dict[(fn_id, key)]
           content = gen.next()
           return json.dumps({'state': 'ready',
                              'content':content})
        except StopIteration:
           del json_yield._gen_dict[(fn_id,key)]
           return json.dumps({'state': 'done',
                              'content': None})
    return _
