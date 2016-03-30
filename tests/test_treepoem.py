from os import path
from PIL import Image, ImageChops

from nose_parameterized import parameterized

import treepoem


@parameterized([
    ('qrcode', "This is qrcode barcode."),
    ('azteccode', "This is azteccode barcode."),
    ('pdf417', "This is pdf417 barcode."),
    ('interleaved2of5', "0123456789"),
    ('code128', "This is code128 barcode."),
    ('code39', "THIS IS CODE39 BARCODE."),
])
def test_barcode(barcode_type, barcode_data):
    actual = treepoem.generate_barcode(
        barcode_type,
        barcode_data,
        {}
    )

    fixture_path = "{dirname}/fixtures/{barcode_type}.png".format(
        dirname=path.dirname(__file__),
        barcode_type=barcode_type,
    )

    # Trying to prevent a `ResourceWarning`.
    # Bug: https://github.com/python-pillow/Pillow/issues/1144
    # Workaround: https://github.com/python-pillow/Pillow/issues/835
    with open(fixture_path, 'rb') as fixture:
        expected = Image.open(fixture)
        bbox = ImageChops.difference(actual, expected).getbbox()
        assert bbox is None

    actual.close()
