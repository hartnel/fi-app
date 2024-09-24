from typing import Dict
from common.singleton import Singleton
from common.models import Key

class KeyManager(metaclass=Singleton):
    _cache: Dict[str, Key] = {}


    @staticmethod
    def get(name:str, default=None):
        if name in KeyManager._cache:
            return KeyManager._cache[name].value
        else:
            key:Key = KeyManager._load_from_db(name)
            if key:
                return key.value
            
        return default
    
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
       
    