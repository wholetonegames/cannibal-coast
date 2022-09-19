import os
import errno
import json
import base64
import abc


class SaveLoadJSON(metaclass=abc.ABCMeta):
    def __init__(self, filepath):
        self.datatypes = (int, str, bool, float, dict, list, tuple)
        self.key = '74zrm66FpK0072ce48082b1ba9c07588551d4d3c090072ce48082b1ba9c07588551d4d3c09WlpvHi'
        self.isEncoding = True
        self.protectedFields = ['protectedFields',
                                'filepath', 'datatypes', 'key', 'isEncoding']
        self.filepath = filepath

    def checkFolder(self):
        if not os.path.exists(os.path.dirname(self.filepath)):
            try:
                os.makedirs(os.path.dirname(self.filepath))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    def saveGame(self):
        if getattr(self, 'runManualUpdates'):
            self.runManualUpdates()
        obj = self.iterateObj()
        self.checkFolder()
        self.writeReadme()
        with open(self.filepath, 'w') as fp:
            if self.isEncoding:
                json_obj = json.dumps(obj)
                enc = self.encode(str(json_obj)).decode("utf-8")
                fp.write(enc)
            else:
                json.dump(obj, fp, indent=4)

    def writeReadme(self):
        dirPath = os.path.dirname(self.filepath)
        readmePath = dirPath + "/readme.txt"
        with open(readmePath, 'w') as fp:
            fp.write(
                'Please do not try to manually edit any of the files in this folder.')

    def iterateObj(self):
        obj = {}
        for key in self.__dict__:
            isValid = self.isValidType(key)
            if isValid:
                obj[key] = self.__dict__[key]
        return obj

    def isValidType(self, key):
        return self.isInbuilt(self.__dict__[key]) and not self.isProtected(key)

    def isInbuilt(self, thing):
        return type(thing) in self.datatypes

    def isProtected(self, key):
        return key in self.protectedFields

    def loadGame(self):
        if getattr(self, 'runManualUpdates'):
            self.runManualUpdates()
        json_data = self.get_text(self.filepath)
        for key, val in json_data.items():
            self.__dict__[key] = val

    def get_text(self, filename):
        json_data = None
        with open(filename, encoding='utf-8-sig') as json_file:
            text = json_file.read()
            if self.isEncoding:
                dec = self.decode(text).replace("'", '"')
            else:
                dec = text
            json_data = json.loads(dec)
        return json_data

    @abc.abstractmethod
    def getSaveFileInfo(self, filename):
        raise NotImplementedError('subclass must define this method')

    def encode(self, clear):
        key = self.key
        enc = []
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = (ord(clear[i]) + ord(key_c)) % 256
            enc.append(enc_c)
        return base64.urlsafe_b64encode(bytes(enc))

    def decode(self, enc):
        key = self.key
        dec = []
        enc = base64.urlsafe_b64decode(enc)
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + enc[i] - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)

    @abc.abstractmethod
    def runManualUpdates(self):
        raise NotImplementedError('subclass must define this method')


if __name__ == "__main__":
    class GameThatSaves(SaveLoadJSON):
        def __init__(self, filepath):
            SaveLoadJSON.__init__(self, filepath)
            self.x = 1.0
            self.y = 2
            self.z = 3
            self.no = self.saveGame
            self.data = {'a': 21, 'b': 22}

        def runManualUpdates(self):
            pass

        def getSaveFileInfo(self, filename):
            pass

    s = GameThatSaves('./test/result.json')
    s.saveGame()
    print('s.x =', s.x)
    for key in s.__dict__:
        if not key in s.protectedFields:
            s.__dict__[key] = None
    print('s.x =', s.x)
    s.loadGame()
    print('s.x =', s.x)
