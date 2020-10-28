import defcon
from babelfont.font import Font
from babelfont.layer import Layer
from babelfont.lib import Lib
from babelfont.glyph import Glyph
from babelfont.point import Point
from babelfont.contour import Contour
from babelfont.component import Component
from babelfont.anchor import Anchor
from copy import copy


def can_handle(filename):
    return filename.endswith(".ufo")


def open(filename):
    dcfont = defcon.Font(filename)
    return _load_dcfont(dcfont)

def save(font, filename):
    dcfont = _save_dcfont(font)
    dcfont.save(filename)

# defcon -> babelfont


def _load_dcfont(dcf):
    bbf = Font(dcf)

    # XXX Create: groups, kerning, features
    for k,v in dcf.info.getDataForSerialization().items():
        bbf.info._setAttr(k, copy(v))
    for k,v in dcf.lib.items():
        bbf.lib._setItem(k, copy(v))
    for dclayer in dcf.layers:
        bblayer = _load_dclayer(dclayer)
        bblayer.font = bbf
        bbf._layers.append(bblayer)
        bbf._layerOrder.append(bblayer.name)

    return bbf


def _load_dclayer(dclayer):  # -> Layer
    bblayer = Layer()
    for k,v in dclayer.lib.items():
        bblayer.lib._setItem(k, copy(v))
    bblayer.color = dclayer.color
    bblayer.name = dclayer.name
    for k in dclayer.keys():
        bblayer._glyphs[k] = _load_dcglyph(dclayer[k], bblayer)
    return bblayer

def _load_dcglyph(dcglyph, layer):
    glyph = Glyph()
    glyph._layer = layer
    glyph._lib = Lib()
    glyph._lib.glyph = glyph
    for k,v in dcglyph.lib.items():
        glyph._lib._setItem(k, copy(v))
    glyph._name = dcglyph.name
    glyph._unicodes = copy(dcglyph.unicodes)
    glyph._width = dcglyph.width
    glyph._height = dcglyph.height
    # components, anchors, guidelines, image
    # glyph._components = [_load_dccomponent(c, glyph) for c in dclayer.components]
    glyph._contours = [_load_dccontour(p, glyph) for p in dcglyph]
    return glyph


def _load_dccontour(dccontour, glyph):
    contour = Contour()
    contour._glyph = glyph
    contour._points = [_load_dcpoint(p, contour) for p in dccontour]
    contour.clockwise = dccontour.clockwise
    return contour


# def _load_dccomponent(dccomponent, glyph):
#     component = Component()
#     component._glyph = glyph
#     # XXX
#     return component


# def _load_dcanchor(dcanchor, glyph):
#     anchor = Anchor()
#     anchor._glyph = glyph
#     # XXX
#     return anchor


def _load_dcpoint(dcpoint, contour):
    point = Point()
    point._contour = contour
    point._x = dcpoint.x
    point._y = dcpoint.y
    if not dcpoint.segmentType:
        point.type = "offcurve"
    else:
        point.type = dcpoint.segmentType
    point.smooth = dcpoint.smooth
    return point


# # babelfont -> defcon


def _save_point(point):
    if point.type == "offcurve":
        dctype = None
    else:
        dctype = point.type
    return defcon.Point ((point.x, point.y), dctype, point.smooth)


def _save_contour(contour):
    path = defcon.Contour()
    for p in contour._points:
        path.appendPoint(_save_point(p))
    path.clockwise = contour.clockwise
    return path


# def _save_component(component):
#     c = defcon.Component(component.glyph)
#     # XXX
#     return c

def _save_glyph(glyph):
    dcglyph = defcon.Glyph()
    dcglyph.unicodes = copy(glyph._unicodes)
    for c in glyph.contours:
        dccontour = _save_contour(c)
        dcglyph.appendContour(dccontour)
    # dclayer.components = [_save_component(c) for c in glyph.components]
    # Anchors
    for k,v in glyph.lib._dict.items():
        if k == "glyph":
            continue
        dcglyph.lib[k] = copy(v)

    dcglyph.name = glyph.name
    dcglyph.rightMargin = glyph.rightMargin
    dcglyph.leftMargin = glyph.leftMargin
    dcglyph.width = glyph.width
    dcglyph.name = glyph.name
    return dcglyph

def _save_layer(layer, dclayer):
    for g in layer:
        dclayer.insertGlyph(_save_glyph(g))
    dclayer.color = layer.color

def _save_dcfont(font):
    dcf = defcon.Font()
    for k,v in font.lib._dict.items():
        dcf.lib[k] = copy(v)
    dcf.info.setDataFromSerialization(font.info._dict)
    for l in font.layers:
        if l.name in dcf.layers.layerOrder:
            newLayer = dcf.layers[l.name]
        else:
            newLayer = dcf.newLayer(l.name)
        _save_layer(l, newLayer)
    return dcf

# # Random stuff

# def _glyphs_date_to_ufo(d):
#     return d.strftime('%Y/%m/%d %H:%M:%S')

# def _ufo_date_to_glyphs(d):
#     return datetime.strptime(d, '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S +0000')
