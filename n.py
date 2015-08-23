# -*- coding: UTF-8 -*-
import json

organs = {'organs': [{'args': ['arg0', 'arg1'],
                      'calculated_args': [['arg2', 'arg0 + arg1'],
                                          ['arg3', 'arg2 + arg1']],
                      'name': 'Heart'}]}


def organ_to_class(organ):
    class_name = organ['name']
    class_args = organ['args']
    class_calculated_args = organ['calculated_args']

    print(class_name)
    print(class_args)
    print(class_calculated_args)


def json_to_class(json_string):
    organs = json.loads(json_string)['organs']
    for each in organs:
        organ_to_class(each)


def __calc(self):
    for x in self.evals:
        exec(x)


if __name__ == '__main__':
    evals = ['self.c = self.a + self.b', 'self.d = self.a - self.b']
    type('Foo', (), {})
    organs = [type(name, (), {'calc': __calc, 'evals': evals, 'a': 10, 'b': 5})
              for name in ('Foo', 'Bar', 'FooBar')]
    a = organs[0]()
    print(a.__class__.__name__, a.calc(), a.c, a.d)
    # json_to_class(json.dumps(organs))
