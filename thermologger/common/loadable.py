import __main__
import os.path
import json
class Loadable:

    @classmethod
    def load(cls, config):
        try:
            if hasattr(__main__, '__file__'):
                main_file = __main__.__file__
                prefix = os.path.dirname(main_file)
                config = os.path.join(prefix, config)
            # print(f'Config is now {config}')
            with open(config, mode='r') as conf:
                j = json.load(conf)
        except Exception as e:
            print(f'Error: {e}')
            j = dict()
        print('\n'.join([f'{key} = {value}' for key, value in j.items()]))
        return cls(**j)

    def __init__(self,**kwargs):
        self.dict=kwargs

