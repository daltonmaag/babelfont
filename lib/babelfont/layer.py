from fontParts.base.layer import BaseLayer
from babelfont.lib import Lib
from babelfont import addUnderscoreProperty
from babelfont.glyph import Glyph

@addUnderscoreProperty("name")
@addUnderscoreProperty("color")
@addUnderscoreProperty("lib")
@addUnderscoreProperty("glyphs")
class Layer(BaseLayer):
    def _init(self, **kwargs):
        self._lib = Lib()
        self._glyphs = {}

    def keys(self):
        return self._glyphs.keys()

    def _getItem(self,name):
        return self._glyphs[name]
    pass
