# -*- coding: utf-8
from dataplicity.m2m.bencode import encode, decode, EncodingError, DecodeError
import pytest
import six


def test_bencode_encoder():
    """ test bencoding capabilities
    """
    assert encode({}) == six.b('de')  # empty dict
    assert encode({b'foo': 'bar'}) == six.b('d3:foo3:bare')
    assert encode({
        b'foo': 'bar',
        b'fooo': 'bbar'
    }) == six.b('d3:foo3:bar4:fooo4:bbare')
    assert encode([]) == six.b('le')  # empty list
    assert encode(()) == six.b('le')  # empty list
    assert encode([1, 2, 3]) == six.b('li1ei2ei3ee')
    assert encode([1, 'foo']) == six.b('li1e3:fooe')
    assert encode(1) == six.b('i1e')
    # utf-8 string
    assert encode(b'a\xc5\xbc') == six.b('3:a\xc5\xbc')
    assert encode("aż") == six.b("3:a\xc5\xbc")
    with pytest.raises(EncodingError):
        encode(1.38)
    # since bytes == str in python2, this exception won't be raised
    if six.PY3:
        with pytest.raises(EncodingError):
            encode({'foo': 'bar'})

    assert encode(-41) == six.b("i-41e")


def test_bencode_decoder():
    """ test decoding capabilities of bencode module
    """
    # portable (python2+3) way of testing whether object is instance
    # of bytes ;)
    with pytest.raises(Exception) as exc:
        decode(123)
    assert str(exc.value) == 'decode takes bytes'

    assert decode(b'de') == {}
    assert decode(b'i-41e') == -41
    assert decode(b'd3:foo3:bare') == {b'foo': b'bar'}
    assert decode(b'd3:foo3:bar4:fooo4:bbare') == {
        b'foo': b'bar', b'fooo': b'bbar'}
    with pytest.raises(DecodeError) as exc:
        decode(b'i.123e')
    assert str(exc.value) == 'illegal digit in size'
    assert decode(b'le') == []
    assert decode(b'li1ei2ee') == [1, 2]
    assert decode(b'13:aaaaaaaaaaa\xc5\xbc') == b'aaaaaaaaaaa\xc5\xbc'