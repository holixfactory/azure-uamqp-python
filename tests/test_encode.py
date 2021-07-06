#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import datetime
import uuid

import uamqp._encode as encode
from uamqp.types import AMQPTypes
from uamqp.message import Message, Header, Properties

import pytest


LARGE_BYTES = bytes(4294967296)


def test_encode_null():
    output = encode.encode_null(b"")
    assert output == b'\x40'

    output = encode.encode_value(b"", None)
    assert output == b'\x40'

    output = encode.encode_value(b"", {"TYPE": "NULL", "VALUE": None})
    assert output == b'\x40'


def test_encode_boolean():
    output = encode.encode_boolean(b"", True)
    assert output == b"\x56\x01"

    output = encode.encode_boolean(b"", "foo")
    assert output == b"\x56\x01"

    output = encode.encode_boolean(b"", True, with_constructor=False)
    assert output == b"\x41"

    output = encode.encode_value(b"", True)
    assert output == b"\x56\x01"

    output = encode.encode_value(b"", True, with_constructor=False)
    assert output == b"\x41"

    output = encode.encode_value(b"", {"TYPE": "BOOL", "VALUE": True})
    assert output == b"\x56\x01"

    output = encode.encode_value(b"", {"TYPE": "BOOL", "VALUE": True}, with_constructor=False)
    assert output == b"\x41"

    output = encode.encode_boolean(b"", False)
    assert output == b"\x56\x00"

    output = encode.encode_boolean(b"", "")
    assert output == b"\x56\x00"

    output = encode.encode_boolean(b"", False, with_constructor=False)
    assert output == b"\x42"

    output = encode.encode_value(b"", False)
    assert output == b"\x56\x00"

    output = encode.encode_value(b"", False, with_constructor=False)
    assert output == b"\x42"

    output = encode.encode_value(b"", {"TYPE": "BOOL", "VALUE": False})
    assert output == b"\x56\x00"

    output = encode.encode_value(b"", {"TYPE": "BOOL", "VALUE": False}, with_constructor=False)
    assert output == b"\x42"


def test_encode_ubyte():
    output = encode.encode_ubyte(b"", 255)
    assert output == b"\x50\xFF"

    output = encode.encode_ubyte(b"", ord('a'))
    assert output == b"\x50\x61"

    output = encode.encode_ubyte(b"", -1)
    assert output == b"\x50\x01"

    output = encode.encode_ubyte(b"", 0, with_constructor=False)
    assert output == b"\x00"

    with pytest.raises(ValueError):
        encode.encode_ubyte(b"", 256)

    output = encode.encode_value(b"", {"TYPE": "UBYTE", "VALUE": ord('a')})
    assert output == b"\x50\x61"

    output = encode.encode_value(b"", {"TYPE": "UBYTE", "VALUE": ord('a')}, with_constructor=False)
    assert output == b"\x61"


def test_encode_ushort():
    output = encode.encode_ushort(b"", 0)
    assert output == b"\x60\x00\x00"

    output = encode.encode_ushort(b"", 16963)
    assert output == b"\x60\x42\x43"

    output = encode.encode_ushort(b"", 255)
    assert output == b"\x60\x00\xFF"

    output = encode.encode_ushort(b"", -255)
    assert output == b"\x60\x00\xFF"

    output = encode.encode_ushort(b"", 65535)
    assert output == b"\x60\xFF\xFF"

    with pytest.raises(ValueError):
        encode.encode_ushort(b"", 65536)

    output = encode.encode_value(b"", {"TYPE": AMQPTypes.ushort, "VALUE": 0})
    assert output == b"\x60\x00\x00"

    output = encode.encode_value(b"", {"TYPE": AMQPTypes.ushort, "VALUE": 0}, with_constructor=False)
    assert output == b"\x00\x00"


def test_encode_uint():
    output = encode.encode_uint(b"", 0)
    assert output == b"\x43"

    output = encode.encode_uint(b"", 66)
    assert output == b'\x52\x42'

    output = encode.encode_uint(b"", -66)
    assert output == b'\x52\x42'

    output = encode.encode_uint(b"", 66, with_constructor=False)
    assert output == b'\x42'

    output = encode.encode_uint(b"", 255)
    assert output == b'\x52\xFF'

    output = encode.encode_uint(b"", 255, use_smallest=False)
    assert output == b'\x70\x00\x00\x00\xFF'

    output = encode.encode_uint(b"", 4294967295)
    assert output == b"\x70\xFF\xFF\xFF\xFF"

    output = encode.encode_uint(b"", 429496700, with_constructor=False)
    assert output == b"\x19\x99\x99\x7C"

    with pytest.raises(ValueError):
        encode.encode_uint(b"", 4294967296)

    output = encode.encode_value(b"", {"TYPE": AMQPTypes.uint, "VALUE": 66})
    assert output == b'\x52\x42'

    output = encode.encode_value(
        b"", {"TYPE": AMQPTypes.uint, "VALUE": 66}, with_constructor=False, use_smallest=False)
    assert output == b'\x00\x00\x00\x42'


def test_encode_ulong():
    output = encode.encode_ulong(b"", 0)
    assert output == b"\x44"

    output = encode.encode_ulong(b"", 66)
    assert output == b'\x53\x42'

    output = encode.encode_ulong(b"", -66)
    assert output == b'\x53\x42'

    output = encode.encode_ulong(b"", 66, with_constructor=False)
    assert output == b'\x42'

    output = encode.encode_ulong(b"", 255)
    assert output == b'\x53\xFF'

    output = encode.encode_ulong(b"", 255, use_smallest=False)
    assert output == b'\x80\x00\x00\x00\x00\x00\x00\x00\xFF'

    output = encode.encode_ulong(b"", 4294967295)
    assert output == b"\x80\x00\x00\x00\x00\xFF\xFF\xFF\xFF"

    output = encode.encode_ulong(b"", 429496700, with_constructor=False)
    assert output == b"\x00\x00\x00\x00\x19\x99\x99\x7C"

    output = encode.encode_ulong(b"", 18446744073709551615)
    assert output == b"\x80\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"

    with pytest.raises(ValueError):
        encode.encode_ulong(b"", 18446744073709551616)

    output = encode.encode_value(b"", {"TYPE": AMQPTypes.ulong, "VALUE": 66})
    assert output == b'\x53\x42'

    output = encode.encode_value(
        b"", {"TYPE": AMQPTypes.ulong, "VALUE": 66}, with_constructor=False, use_smallest=False)
    assert output == b'\x00\x00\x00\x00\x00\x00\x00\x42'


def test_encode_byte():
    output = encode.encode_byte(b"", 127)
    assert output == b"\x51\x7F"

    output = encode.encode_byte(b"", 0)
    assert output == b"\x51\x00"

    output = encode.encode_byte(b"", -1)
    assert output == b"\x51\xFF"

    output = encode.encode_byte(b"", -128)
    assert output == b"\x51\x80"

    output = encode.encode_byte(b"", 0, with_constructor=False)
    assert output == b"\x00"

    with pytest.raises(ValueError):
        encode.encode_byte(b"", 128)

    with pytest.raises(ValueError):
        encode.encode_byte(b"", -129)

    output = encode.encode_value(b"", {"TYPE": AMQPTypes.byte, "VALUE": 66})
    assert output == b'\x51\x42'

    output = encode.encode_value(
        b"", {"TYPE": AMQPTypes.byte, "VALUE": 66}, with_constructor=False)
    assert output == b'\x42'


def test_encode_short():
    output = encode.encode_short(b"", 0)
    assert output == b"\x61\x00\x00"

    output = encode.encode_short(b"", -32768)
    assert output == b"\x61\x80\x00"

    output = encode.encode_short(b"", 32767)
    assert output == b"\x61\x7F\xFF"

    output = encode.encode_short(b"", 255, with_constructor=False)
    assert output == b"\x00\xFF"

    output = encode.encode_short(b"", -255)
    assert output == b"\x61\xFF\x01"

    with pytest.raises(ValueError):
        encode.encode_short(b"", 32768)
    
    with pytest.raises(ValueError):
        encode.encode_short(b"", -32769)

    output = encode.encode_value(b"", {"TYPE": AMQPTypes.short, "VALUE": 255})
    assert output == b'\x61\x00\xFF'

    output = encode.encode_value(
        b"", {"TYPE": AMQPTypes.short, "VALUE": 255}, with_constructor=False, use_smallest=False)
    assert output == b'\x00\xFF'


def test_encode_int():
    output = encode.encode_int(b"", 0)
    assert output == b"\x54\x00"

    output = encode.encode_int(b"", 66)
    assert output == b'\x54\x42'

    output = encode.encode_int(b"", -66)
    assert output == b'\x54\xBE'

    output = encode.encode_int(b"", 66, with_constructor=False)
    assert output == b'\x42'

    output = encode.encode_int(b"", 127)
    assert output == b'\x54\x7F'

    output = encode.encode_int(b"", -128)
    assert output == b'\x54\x80'

    output = encode.encode_int(b"", 127, use_smallest=False)
    assert output == b'\x71\x00\x00\x00\x7F'

    output = encode.encode_int(b"", -1, with_constructor=False, use_smallest=False)
    assert output == b'\xFF\xFF\xFF\xFF'

    output = encode.encode_int(b"", 2147483647)
    assert output == b"\x71\x7F\xFF\xFF\xFF"

    output = encode.encode_int(b"", -2147483648, with_constructor=False)
    assert output == b"\x80\x00\x00\x00"

    with pytest.raises(ValueError):
        encode.encode_int(b"", 2147483648)

    with pytest.raises(ValueError):
        encode.encode_int(b"", -2147483649)

    output = encode.encode_value(b"", 66)
    assert output == b'\x54\x42'

    output = encode.encode_value(b"", 127, with_constructor=False, use_smallest=False)
    assert output == b'\x00\x00\x00\x7F'

    output = encode.encode_value(b"", {"TYPE": AMQPTypes.int, "VALUE": 127})
    assert output == b'\x54\x7F'

    output = encode.encode_value(
        b"", {"TYPE": AMQPTypes.int, "VALUE": 127}, with_constructor=False, use_smallest=False)
    assert output == b'\x00\x00\x00\x7F'


def test_encode_long():
    output = encode.encode_long(b"", 0)
    assert output == b"\x55\x00"

    output = encode.encode_long(b"", 66)
    assert output == b'\x55\x42'

    output = encode.encode_long(b"", -66)
    assert output == b'\x55\xBE'

    output = encode.encode_long(b"", 66, with_constructor=False)
    assert output == b'\x42'

    output = encode.encode_long(b"", 127)
    assert output == b'\x55\x7F'

    output = encode.encode_long(b"", -128)
    assert output == b'\x55\x80'

    output = encode.encode_long(b"", 127, use_smallest=False)
    assert output == b'\x81\x00\x00\x00\x00\x00\x00\x00\x7F'

    output = encode.encode_long(b"", 9223372036854775807)
    assert output == b"\x81\x7F\xFF\xFF\xFF\xFF\xFF\xFF\xFF"

    output = encode.encode_long(b"", 429496700, with_constructor=False)
    assert output == b"\x00\x00\x00\x00\x19\x99\x99\x7C"

    output = encode.encode_long(b"", -9223372036854775808)
    assert output == b"\x81\x80\x00\x00\x00\x00\x00\x00\x00"

    with pytest.raises(ValueError):
        encode.encode_long(b"", 9223372036854775808)

    with pytest.raises(ValueError):
        encode.encode_long(b"", -9223372036854775809)

    output = encode.encode_value(b"", {"TYPE": AMQPTypes.long, "VALUE": 127})
    assert output == b'\x55\x7F'

    output = encode.encode_value(
        b"", {"TYPE": AMQPTypes.long, "VALUE": 127}, with_constructor=False, use_smallest=False)
    assert output == b'\x00\x00\x00\x00\x00\x00\x00\x7F'


def test_encode_float():
    output = encode.encode_float(b"", -1.0)
    assert output == b"\x72\xBF\x80\x00\x00"

    output = encode.encode_float(b"", 42.0)
    assert output == b"\x72\x42\x28\x00\x00"

    output = encode.encode_value(b"", {"TYPE": AMQPTypes.float, "VALUE": 42.0})
    assert output == b"\x72\x42\x28\x00\x00"

    output = encode.encode_value(
        b"", {"TYPE": AMQPTypes.float, "VALUE": 42.0}, with_constructor=False, use_smallest=False)
    assert output == b"\x42\x28\x00\x00"


def test_encode_double():
    output = encode.encode_double(b"", -1.0)
    assert output == b"\x82\xBF\xF0\x00\x00\x00\x00\x00\x00"

    output = encode.encode_double(b"", 42.0)
    assert output == b"\x82\x40\x45\x00\x00\x00\x00\x00\x00"

    output = encode.encode_value(b"", 42.0)
    assert output == b"\x82\x40\x45\x00\x00\x00\x00\x00\x00"

    output = encode.encode_value(b"", 42.0, with_constructor=False, use_smallest=False)
    assert output == b"\x40\x45\x00\x00\x00\x00\x00\x00"

    output = encode.encode_value(b"", {"TYPE": AMQPTypes.double, "VALUE": 42.0})
    assert output == b"\x82\x40\x45\x00\x00\x00\x00\x00\x00"

    output = encode.encode_value(
        b"", {"TYPE": AMQPTypes.double, "VALUE": 42.0}, with_constructor=False, use_smallest=False)
    assert output == b"\x40\x45\x00\x00\x00\x00\x00\x00"


def test_encode_timestamp():
    output = encode.encode_timestamp(b"", -9223372036854775807 - 1)
    assert output == b"\x83\x80\x00\x00\x00\x00\x00\x00\x00"

    output = encode.encode_timestamp(b"", 0)
    assert output == b"\x83\x00\x00\x00\x00\x00\x00\x00\x00"

    output = encode.encode_timestamp(b"", 9223372036854775807)
    assert output == b"\x83\x7F\xFF\xFF\xFF\xFF\xFF\xFF\xFF"

    output = encode.encode_timestamp(b"", datetime.datetime.min)
    assert output == b"\x83\xFF\xFF\xC7\x7C\xED\xD3\x28\x00"

    output = encode.encode_timestamp(b"", datetime.datetime.max)
    assert output == b"\x83\x00\x00\xE6\x77\xD2\x1F\xDC\x00"


def test_encode_uuid():
    output = encode.encode_uuid(b"", '00000000-0000-0000-0000-000000000000')
    assert output == b"\x98\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    id = uuid.UUID('37f9db00-fbb7-11e7-85ee-ecb1d755839a')
    output = encode.encode_uuid(b"", id)
    assert output == b"\x98\x37\xF9\xDB\x00\xFB\xB7\x11\xE7\x85\xEE\xEC\xB1\xD7\x55\x83\x9A"

    output = encode.encode_uuid(b"", id, with_constructor=False)
    assert output == b"\x37\xF9\xDB\x00\xFB\xB7\x11\xE7\x85\xEE\xEC\xB1\xD7\x55\x83\x9A"

    output = encode.encode_uuid(b"", b"\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4A\x4B\x4C\x4D\x4E\x4F")
    assert output == b"\x98\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4A\x4B\x4C\x4D\x4E\x4F"


def test_encode_binary():
    output = encode.encode_binary(b"", b"")
    assert output == b"\xA0\x00"

    output = encode.encode_binary(b"", b"Test")
    assert output == b"\xA0\x04Test"
    assert output == b"\xA0\x04\x54\x65\x73\x74"

    output = encode.encode_binary(b"", bytes(100))
    assert output == b"\xA0\x64" + bytes(100)

    output = encode.encode_binary(b"", bytes(255))
    assert output == b"\xA0\xFF" + bytes(255)

    output = encode.encode_binary(b"", bytes(255), use_smallest=False)
    assert output == b"\xB0\x00\x00\x00\xFF" + bytes(255)

    output = encode.encode_binary(b"", bytes(255), with_constructor=False)
    assert output == b"\xFF" + bytes(255)

    output = encode.encode_binary(b"", bytes(256))
    assert output == b"\xB0\x00\x00\x01\x00" + bytes(256)

    output = encode.encode_binary(b"", bytearray([50]))
    assert output == b"\xA0\x01\x32"

    output = encode.encode_binary(b"", bytearray(b"Test"))
    assert output == b"\xA0\x04Test"
    assert output == b"\xA0\x04\x54\x65\x73\x74"

    with pytest.raises(ValueError):
        encode.encode_string(b"", LARGE_BYTES)


def test_encode_string():
    output = encode.encode_string(b"", b"")
    assert output == b"\xA1\x00"

    output = encode.encode_string(b"", "")
    assert output == b"\xA1\x00"

    output = encode.encode_string(b"", "Test")
    assert output == b"\xA1\x04Test"
    assert output == b"\xA1\x04\x54\x65\x73\x74"

    output = encode.encode_string(b"", "A" * 100)
    assert output == b"\xA1\x64" + b"A" * 100

    output = encode.encode_string(b"", "A" * 255)
    assert output == b"\xA1\xFF" + b"A" * 255

    output = encode.encode_string(b"", "A" * 255, use_smallest=False)
    assert output == b"\xB1\x00\x00\x00\xFF" + b"A" * 255

    output = encode.encode_string(b"", "A" * 255, with_constructor=False)
    assert output == b"\xFF" + b"A" * 255

    output = encode.encode_string(b"", "A" * 256)
    assert output == b"\xB1\x00\x00\x01\x00" + b"A" * 256

    with pytest.raises(ValueError):
        encode.encode_string(b"", LARGE_BYTES)


def test_encode_symbol():
    output = encode.encode_symbol(b"", b"")
    assert output == b"\xA3\x00"

    output = encode.encode_symbol(b"", "")
    assert output == b"\xA3\x00"

    output = encode.encode_symbol(b"", "Test")
    assert output == b"\xA3\x04Test"
    assert output == b"\xA3\x04\x54\x65\x73\x74"

    output = encode.encode_symbol(b"", "A" * 100)
    assert output == b"\xA3\x64" + b"A" * 100

    output = encode.encode_symbol(b"", "A" * 255)
    assert output == b"\xA3\xFF" + b"A" * 255

    output = encode.encode_symbol(b"", "A" * 255, use_smallest=False)
    assert output == b"\xB3\x00\x00\x00\xFF" + b"A" * 255

    output = encode.encode_symbol(b"", "A" * 255, with_constructor=False)
    assert output == b"\xFF" + b"A" * 255

    output = encode.encode_symbol(b"", "A" * 256)
    assert output == b"\xB3\x00\x00\x01\x00" + b"A" * 256

    with pytest.raises(ValueError):
        encode.encode_symbol(b"", LARGE_BYTES)


def test_encode_list():
    output = encode.encode_list(b"", [])
    assert output == b'\x45'
    
    output = encode.encode_list(b"", [1, 2, 3, 4])
    assert output == b"\xC0\x09\x04\x54\x01\x54\x02\x54\x03\x54\x04"

    output = encode.encode_list(b"", [None])
    assert output == b"\xC0\x02\x01\x40"

    output = encode.encode_list(b"", [None, None])
    assert output == b"\xC0\x03\x02\x40\x40"

    output = encode.encode_list(b"", [None for i in range(254)])
    assert output == b"\xC0\xFF\xFE" + b"\x40" * 254

    output = encode.encode_list(b"", [bytearray(252)])
    assert output == b"\xC0\xFF\x01\xA0\xFC" + bytes(252)

    output = encode.encode_list(b"", [bytearray(253)])
    assert output == b"\xD0\x00\x00\x01\x03\x00\x00\x00\x01\xA0\xFD" + bytes(253)

    output = encode.encode_list(b"", [None for i in range(255)])
    assert output == b"\xD0\x00\x00\x01\x03\x00\x00\x00\xFF" + b"\x40" * 255

    output = encode.encode_list(b"", [b"a"] * 1024 * 256)
    assert output == b"\xD0\x00\x0C\x00\x04\x00\x04\x00\x00" + b"\xA0\x01a" * 1024 * 256

    output = encode.encode_list(b"", [b"xyz~!@123"] * 128)
    assert output == b"\xD0\x00\x00\x05\x84\x00\x00\x00\x80" + b"\xA0\txyz~!@123" * 128

    output = encode.encode_list(b"", [bytearray([66]), None])
    assert output == b"\xC0\x05\x02\xA0\x01\x42\x40"

    output = encode.encode_list(
        b"", [{"TYPE": "BINARY", "VALUE": b"\x42"}, {"TYPE": "NULL", "VALUE": None}])
    assert output == b"\xC0\x05\x02\xA0\x01\x42\x40"

    output = encode.encode_value(b"", {"TYPE": "LIST", "VALUE": []})
    assert output == b'\x45'

    output = encode.encode_value(
        b"", {"TYPE": "LIST", "VALUE": [None]}, with_constructor=False, use_smallest=False)
    assert output == b"\x00\x00\x00\x05\x00\x00\x00\x01\x40"


def test_encode_map():
    output = encode.encode_map(b"", {})
    assert output == b"\xC1\x01\x00"

    output = encode.encode_map(b"", {None: None})
    assert output == b"\xC1\x03\x02\x40\x40"

    output = encode.encode_value(b"", {"TYPE": "MAP", "VALUE": {None: None}})
    assert output == b"\xC1\x03\x02\x40\x40"

    output = encode.encode_value(
        b"", {"TYPE": "MAP", "VALUE": {None: None}}, with_constructor=False, use_smallest=False)
    assert output == b"\x00\x00\x00\x06\x00\x00\x00\x02\x40\x40"

    output = encode.encode_map(
        b"", [({"TYPE": "UINT", "VALUE": 66}, {"TYPE": "UINT", "VALUE": 67})])
    assert output == b"\xC1\x05\x02\x52\x42\x52\x43"

    input = [({"TYPE": "UINT", "VALUE": i}, None) for i in range(85)]
    output = encode.encode_map(b"", input)
    expected = b"\xC1\xFF\xAA\x43\x40"
    for i in range(1, 85):
        expected += b"\x52"
        expected += i.to_bytes(1, 'big')
        expected += b"\x40"
    assert expected == output

    input = [({"TYPE": "UINT", "VALUE": i + 1}, None) for i in range(85)]
    output = encode.encode_map(b"", input)
    expected = b"\xD1\x00\x00\x01\x03\x00\x00\x00\xAA"
    for i in range(85):
        expected += b"\x52"
        expected += (i + 1).to_bytes(1, 'big')
        expected += b"\x40"
    assert expected == output

    input = [({"TYPE": "UINT", "VALUE": i + 1}, None) for i in range(128)]
    output = encode.encode_map(b"", input)
    expected = b"\xD1\x00\x00\x01\x84\x00\x00\x01\x00"
    for i in range(128):
        expected += b"\x52"
        expected += (i + 1).to_bytes(1, 'big')
        expected += b"\x40"
    assert expected == output


def test_encode_array():
    output = encode.encode_array(b"", [])
    assert output == b"\xE0\x01\x00"

    output = encode.encode_array(b"", [None])
    assert output == b"\xE0\x01\x01\x40"

    output = encode.encode_array(b"", [None, None])
    assert output == b"\xE0\x01\x02\x40"

    input = [{'TYPE': 'LONG', 'VALUE': 9223372036854775807}, {'TYPE': 'LONG', 'VALUE': 9223372036854775807}]
    output = encode.encode_array(b"", input)
    assert output == b"\xE0\x12\x02\x81\x7F\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x7F\xFF\xFF\xFF\xFF\xFF\xFF\xFF"

    output = encode.encode_array(b"", [[], []])
    assert output == b"\xE0\x12\x02\xD0\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00"

    input = [uuid.UUID('00000000-0000-0000-0000-000000000000') for i in range(8)]
    output = encode.encode_array(b"", input)
    expected = b"\xE0\x82\x08\x98"
    for i in range(128):
        expected += b"\x00"
    assert output == expected

    output = encode.encode_array(b"", [None for i in range(254)])
    assert output == b"\xE0\x01\xFE\x40"

    output = encode.encode_array(b"", [None for i in range(255)])
    assert output == b"\xE0\x01\xFF\x40"

    output = encode.encode_array(b"", [bytearray(249)])
    assert output == b"\xE0\xFF\x01\xB0\x00\x00\x00\xF9" + bytes(249)

    output = encode.encode_array(b"", [bytearray(250)])
    assert output == b"\xF0\x00\x00\x01\x03\x00\x00\x00\x01\xB0\x00\x00\x00\xFA" + bytes(250)

    with pytest.raises(TypeError):
        encode.encode_array(b"", [bytearray([10]), 42])


def test_encode_payload():
    data_body_msg1 = Message(data=[b'Abc 123 !@#'])
    output = encode.encode_payload(b"", data_body_msg1)
    assert output == b'\x00Su\xa0\x0bAbc 123 !@#'

    data_body_msg2 = Message(data=[b'Abc 123 !@#' * 1024])  # 11 * 1024 = 11264 bytes in total
    output = encode.encode_payload(b"", data_body_msg2)
    assert output == b'\x00Su\xb0\x00\x00\x2c\x00' + b'Abc 123 !@#' * 1024  # 0x00002c00 equals to 11264

    value_body_msg_1 = Message(value='Abc 123 !@#')
    output = encode.encode_payload(b"", value_body_msg_1)
    assert output == b'\x00Sw\xa1\x0bAbc 123 !@#'

    value_body_msg_2 = Message(value=123.456)
    output = encode.encode_payload(b"", value_body_msg_2)
    assert output == b'\x00Sw\x82@^\xdd/\x1a\x9f\xbew'

    value_body_msg_3 = Message(value={"key": "value"})
    output = encode.encode_payload(b"", value_body_msg_3)
    assert output == b'\x00Sw\xc1\r\x02\xa1\x03key\xa1\x05value'

    data_body_with_header_msg1 = Message(
        data=[b'Abc 123 !@#'],
        header=Header(durable=True),
    )
    output = encode.encode_payload(b"", data_body_with_header_msg1)
    assert output == b'\x00\x53\x70\xc0\x07\x05\x56\x01\x40\x40\x40\x40\x00\x53\x75\xa0\x0b\x41\x62\x63\x20\x31\x32\x33\x20\x21\x40\x23'

    data_body_with_header_msg2 = Message(
        data=[b'Abc 123 !@#'],
        header=Header(durable=True, ttl=1000, delivery_count=1),
    )
    output = encode.encode_payload(b"", data_body_with_header_msg2)
    assert output == b'\x00\x53\x70\xc0\x0c\x05\x56\x01\x40\x70\x00\x00\x03\xe8\x40\x52\x01\x00\x53\x75\xa0\x0b\x41\x62\x63\x20\x31\x32\x33\x20\x21\x40\x23'

    data_body_with_header_msg3 = Message(
        data=[b'Abc 123 !@#'],
        header=Header(durable=True, priority=1, ttl=1000, first_acquirer=True, delivery_count=1),
    )
    output = encode.encode_payload(b"", data_body_with_header_msg3)
    assert output == b'\x00\x53\x70\xc0\x0e\x05\x56\x01\x50\x01\x70\x00\x00\x03\xe8\x56\x01\x52\x01\x00\x53\x75\xa0\x0b\x41\x62\x63\x20\x31\x32\x33\x20\x21\x40\x23'

    data_body_with_properties_msg1 = Message(
        data=[b'Abc 123 !@#'],
        properties=Properties(
            message_id=b"1",
            user_id=b'user',
            to=b"t",
            subject=b's',
            reply_to=b"rt",
            correlation_id=b"1",
            content_type=b"ct",
            content_encoding=b"ce",
            absolute_expiry_time=1587603220000,
            creation_time=1587603220000,
            group_id=b"gid",
            group_sequence=100,
            reply_to_group_id=b"rgid"
        )
    )
    output = encode.encode_payload(b"", data_body_with_properties_msg1)
    assert output == b'\x00\x53\x73\xc0\x3e\x0d\xa0\x01\x31\xa0\x04\x75\x73\x65\x72\xa1\x01\x74\xa1\x01\x73\xa1\x02\x72\x74\xa0\x01\x31\xa3\x02\x63\x74\xa3\x02\x63\x65\x83\x00\x00\x01\x71\xa4\x86\xa6\x20\x83\x00\x00\x01\x71\xa4\x86\xa6\x20\xa1\x03\x67\x69\x64\x52\x64\xa1\x04\x72\x67\x69\x64\x00\x53\x75\xa0\x0b\x41\x62\x63\x20\x31\x32\x33\x20\x21\x40\x23'

    data_body_with_properties_msg2 = Message(
        data=[b'Abc 123 !@#'],
        properties=Properties(
            message_id=b"1",
            content_encoding=b"ce",
            creation_time=1587603220000
        )
    )
    output = encode.encode_payload(b"", data_body_with_properties_msg2)
    assert output == b'\x00\x53\x73\xc0\x1b\x0d\xa0\x01\x31\x40\x40\x40\x40\x40\x40\xa3\x02\x63\x65\x40\x83\x00\x00\x01\x71\xa4\x86\xa6\x20\x40\x40\x40\x00\x53\x75\xa0\x0b\x41\x62\x63\x20\x31\x32\x33\x20\x21\x40\x23'

    data_body_with_properties_and_header_msg1 = Message(
        data=[b'Abc 123 !@#'],
        header=Header(durable=True, priority=1, ttl=1000, first_acquirer=True, delivery_count=1),
        properties=Properties(
            message_id=b"1",
            user_id=b'user',
            to=b"t",
            subject=b's',
            reply_to=b"rt",
            correlation_id=b"1",
            content_type=b"ct",
            content_encoding=b"ce",
            absolute_expiry_time=1587603220000,
            creation_time=1587603220000,
            group_id=b"gid",
            group_sequence=100,
            reply_to_group_id=b"rgid"
        )
    )
    output = encode.encode_payload(b"", data_body_with_properties_and_header_msg1)
    assert output == b'\x00\x53\x70\xc0\x0e\x05\x56\x01\x50\x01\x70\x00\x00\x03\xe8\x56\x01\x52\x01\x00\x53\x73\xc0\x3e\x0d\xa0\x01\x31\xa0\x04\x75\x73\x65\x72\xa1\x01\x74\xa1\x01\x73\xa1\x02\x72\x74\xa0\x01\x31\xa3\x02\x63\x74\xa3\x02\x63\x65\x83\x00\x00\x01\x71\xa4\x86\xa6\x20\x83\x00\x00\x01\x71\xa4\x86\xa6\x20\xa1\x03\x67\x69\x64\x52\x64\xa1\x04\x72\x67\x69\x64\x00\x53\x75\xa0\x0b\x41\x62\x63\x20\x31\x32\x33\x20\x21\x40\x23'
