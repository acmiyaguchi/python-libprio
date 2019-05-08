# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info

if _swig_python_version_info >= (2, 7, 0):

    def swig_import_helper():
        import importlib

        pkg = __name__.rpartition(".")[0]
        mname = ".".join((pkg, "_libprio")).lstrip(".")
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module("_libprio")

    _libprio = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):

    def swig_import_helper():
        from os.path import dirname
        import imp

        fp = None
        try:
            fp, pathname, description = imp.find_module("_libprio", [dirname(__file__)])
        except ImportError:
            import _libprio

            return _libprio
        try:
            _mod = imp.load_module("_libprio", fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod

    _libprio = swig_import_helper()
    del swig_import_helper
else:
    import _libprio
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if name == "thisown":
        return self.this.own(value)
    if name == "this":
        if type(value).__name__ == "SwigPyObject":
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if not static:
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if name == "thisown":
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError(
        "'%s' object has no attribute '%s'" % (class_type.__name__, name)
    )


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (
        self.__class__.__module__,
        self.__class__.__name__,
        strthis,
    )


try:
    _object = object
    _newclass = 1
except __builtin__.Exception:

    class _object:
        pass

    _newclass = 0


def PublicKey_export(key):
    return _libprio.PublicKey_export(key)


PublicKey_export = _libprio.PublicKey_export


def PublicKey_export_hex(key):
    return _libprio.PublicKey_export_hex(key)


PublicKey_export_hex = _libprio.PublicKey_export_hex


def PrivateKey_export(key):
    return _libprio.PrivateKey_export(key)


PrivateKey_export = _libprio.PrivateKey_export


def PrivateKey_export_hex(key):
    return _libprio.PrivateKey_export_hex(key)


PrivateKey_export_hex = _libprio.PrivateKey_export_hex


def PrioPacketVerify1_write(p):
    return _libprio.PrioPacketVerify1_write(p)


PrioPacketVerify1_write = _libprio.PrioPacketVerify1_write


def PrioPacketVerify2_write(p):
    return _libprio.PrioPacketVerify2_write(p)


PrioPacketVerify2_write = _libprio.PrioPacketVerify2_write


def PrioTotalShare_write(p):
    return _libprio.PrioTotalShare_write(p)


PrioTotalShare_write = _libprio.PrioTotalShare_write


def PrioPacketVerify1_read(p, data, cfg):
    return _libprio.PrioPacketVerify1_read(p, data, cfg)


PrioPacketVerify1_read = _libprio.PrioPacketVerify1_read


def PrioPacketVerify2_read(p, data, cfg):
    return _libprio.PrioPacketVerify2_read(p, data, cfg)


PrioPacketVerify2_read = _libprio.PrioPacketVerify2_read


def PrioTotalShare_read(p, data, cfg):
    return _libprio.PrioTotalShare_read(p, data, cfg)


PrioTotalShare_read = _libprio.PrioTotalShare_read
CURVE25519_KEY_LEN = _libprio.CURVE25519_KEY_LEN
CURVE25519_KEY_LEN_HEX = _libprio.CURVE25519_KEY_LEN_HEX
PRIO_SERVER_A = _libprio.PRIO_SERVER_A
PRIO_SERVER_B = _libprio.PRIO_SERVER_B


def Prio_init():
    return _libprio.Prio_init()


Prio_init = _libprio.Prio_init


def Prio_clear():
    return _libprio.Prio_clear()


Prio_clear = _libprio.Prio_clear


def PrioConfig_new(nFields, serverA, serverB, batchId):
    return _libprio.PrioConfig_new(nFields, serverA, serverB, batchId)


PrioConfig_new = _libprio.PrioConfig_new


def PrioConfig_numDataFields(cfg):
    return _libprio.PrioConfig_numDataFields(cfg)


PrioConfig_numDataFields = _libprio.PrioConfig_numDataFields


def PrioConfig_maxDataFields():
    return _libprio.PrioConfig_maxDataFields()


PrioConfig_maxDataFields = _libprio.PrioConfig_maxDataFields


def PrioConfig_newTest(nFields):
    return _libprio.PrioConfig_newTest(nFields)


PrioConfig_newTest = _libprio.PrioConfig_newTest


def Keypair_new():
    return _libprio.Keypair_new()


Keypair_new = _libprio.Keypair_new


def PublicKey_import(data):
    return _libprio.PublicKey_import(data)


PublicKey_import = _libprio.PublicKey_import


def PrivateKey_import(privData, pubData):
    return _libprio.PrivateKey_import(privData, pubData)


PrivateKey_import = _libprio.PrivateKey_import


def PublicKey_import_hex(hexData):
    return _libprio.PublicKey_import_hex(hexData)


PublicKey_import_hex = _libprio.PublicKey_import_hex


def PrivateKey_import_hex(privHexData, pubHexData):
    return _libprio.PrivateKey_import_hex(privHexData, pubHexData)


PrivateKey_import_hex = _libprio.PrivateKey_import_hex


def PrioClient_encode(cfg, data_in):
    return _libprio.PrioClient_encode(cfg, data_in)


PrioClient_encode = _libprio.PrioClient_encode


def PrioPRGSeed_randomize():
    return _libprio.PrioPRGSeed_randomize()


PrioPRGSeed_randomize = _libprio.PrioPRGSeed_randomize


def PrioServer_new(cfg, serverIdx, serverPriv, serverSharedSecret):
    return _libprio.PrioServer_new(cfg, serverIdx, serverPriv, serverSharedSecret)


PrioServer_new = _libprio.PrioServer_new


def PrioVerifier_new(s):
    return _libprio.PrioVerifier_new(s)


PrioVerifier_new = _libprio.PrioVerifier_new


def PrioVerifier_set_data(v, data):
    return _libprio.PrioVerifier_set_data(v, data)


PrioVerifier_set_data = _libprio.PrioVerifier_set_data


def PrioPacketVerify1_new():
    return _libprio.PrioPacketVerify1_new()


PrioPacketVerify1_new = _libprio.PrioPacketVerify1_new


def PrioPacketVerify1_set_data(p1, v):
    return _libprio.PrioPacketVerify1_set_data(p1, v)


PrioPacketVerify1_set_data = _libprio.PrioPacketVerify1_set_data


def PrioPacketVerify2_new():
    return _libprio.PrioPacketVerify2_new()


PrioPacketVerify2_new = _libprio.PrioPacketVerify2_new


def PrioPacketVerify2_set_data(p2, v, p1A, p1B):
    return _libprio.PrioPacketVerify2_set_data(p2, v, p1A, p1B)


PrioPacketVerify2_set_data = _libprio.PrioPacketVerify2_set_data


def PrioVerifier_isValid(v, pA, pB):
    return _libprio.PrioVerifier_isValid(v, pA, pB)


PrioVerifier_isValid = _libprio.PrioVerifier_isValid


def PrioServer_aggregate(s, v):
    return _libprio.PrioServer_aggregate(s, v)


PrioServer_aggregate = _libprio.PrioServer_aggregate


def PrioTotalShare_new():
    return _libprio.PrioTotalShare_new()


PrioTotalShare_new = _libprio.PrioTotalShare_new


def PrioTotalShare_set_data(t, s):
    return _libprio.PrioTotalShare_set_data(t, s)


PrioTotalShare_set_data = _libprio.PrioTotalShare_set_data


def PrioTotalShare_final(cfg, tA, tB):
    return _libprio.PrioTotalShare_final(cfg, tA, tB)


PrioTotalShare_final = _libprio.PrioTotalShare_final
# This file is compatible with both classic and new-style classes.
