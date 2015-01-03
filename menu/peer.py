from itertools import izip_longest


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

test_obj = [[{u'ingredientName': u'eggs', u'dishId': u'54a2faed0eaefa65a4b78c9e', u'children': [[{u'ingredientName': u'chicken', u'dishId': u'54a2faed0eaefa65a4b78c9e', u'children': [[{u'ingredientName': u'eggs', u'dishId': u'54a2faed0eaefa65a4b78c9e'}]]}, {u'ingredientName': u'eggs', u'dishId': u'54a2faed0eaefa65a4b78c9e'}]]}]]
