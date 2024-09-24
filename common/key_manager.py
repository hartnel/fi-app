from typing import Dict
from common.singleton import Singleton
from common.models import Key

def list_converter(value:str):
    return value.split(",")

def bool_converter(value:str):
    true_values = ["true" , "1", "yes"]
    return value.lower() in true_values

converter = {
    str : lambda x: str(x),
    int : lambda x: int(x),
    list: lambda x: list_converter(x),
    float: lambda x: float(x),
    bool: lambda x: bool_converter(x)
}

class KeyManager(metaclass=Singleton):
    _cache: Dict[str, Key] = {}


    @staticmethod
    def get(name:str,default=None,value_type=str):
        val = default
        if name in KeyManager._cache:
            val =  KeyManager._cache[name].value
        else:
            key:Key = KeyManager._load_from_db(name)
            if key:
                val =  key.value
        
        #try to convert the value to the desired type
        if val and not isinstance(val, value_type):
            val = converter.get(value_type, str)(val)
        return val
    
    @staticmethod
    def _load_from_db(name:str):
        key:Key = Key.objects.filter(name=name).first()
        if key:
            KeyManager._cache[name] = key
            return key
        
    @staticmethod
    def set(name, value):
        #create a new instance
        key = Key()
        key.name = name
        key.value = value
        key.save()

        #update cache
        KeyManager._cache[name] = key

        return key

    @staticmethod
    def update(key_id, name, value):
        key = Key.objects.get(id=key_id)
        key.name = name
        key.value = value
        key.save()

        #filter out the old key from cache
        KeyManager._cache = {k:v for k,v in KeyManager._cache.items() if v.id != key_id}

        #update cache
        KeyManager._cache[name] = key

        return key
       
    