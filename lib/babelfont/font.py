from fontParts.base.font import BaseFont
from fontParts.base.groups import BaseGroups
from fontParts.base.kerning import BaseKerning
from fontParts.base.features import BaseFeatures
from fontParts.base.lib import BaseLib
from babelfont import addUnderscoreProperty
from babelfont.glyph import Glyph
from babelfont.info import Info
from babelfont.layer import Layer


@addUnderscoreProperty("path")
@addUnderscoreProperty("format")
@addUnderscoreProperty("info")
@addUnderscoreProperty("groups")
@addUnderscoreProperty("kerning")
@addUnderscoreProperty("features")
@addUnderscoreProperty("lib")
@addUnderscoreProperty("layers")
@addUnderscoreProperty("layerOrder")
class Font(BaseFont):
    def _init(self, **kwargs):
        self._layerOrder = []
        self._layers = []
        self._info = Info()
        self._info.font = self
        self._groups = BaseGroups()
        self._kerning = BaseKerning()
        self._features = BaseFeatures()
        self._lib = BaseLib()

    def __eq__(self, other):
        return NotImplemented

    def _save(self, path=None, **kwargs):
        if not path:
            path = self._path
        if not path:
            raise ValueError
        Babelfont.save(self, path)

    def _close(self, **kwargs):
        pass

    def _keys(self, **kwargs):
        if len(self._layers) > 0:
            return self.defaultLayer.keys()
        return []

    def _get_defaultLayerName(self):
        if len(self._layers) > 0:
            return self._layers[0].name
        return None

    def _set_defaultLayerName(self, name):
        self._layers[0].name = name

    def _newLayer(self, name, color, **kwargs):
        layer = Layer()
        layer.name = name
        self._layers.append(layer)
        self._layerOrder.append(name)
        return layer

    def _removeLayer(self, name, **kwargs):
        self._layers = [ l for l in self._layers if l.name != name ]

