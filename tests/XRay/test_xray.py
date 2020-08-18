import pytest

from mock import patch
from AwAws.XRay.xray import XRay

xray_class = 'aws_xray_sdk.core.async_recorder.AsyncAWSXRayRecorder'


def test_init():
    xray = XRay(turn_it_on=True)
    assert type(xray) == XRay
    assert str(type(xray.xray_recorder)) == "<class '" + xray_class + "'>"


def test_init_off():
    xray = XRay()
    assert type(xray) == XRay
    with pytest.raises(AttributeError):
        assert str(type(xray.xray_recorder)) == "<class '" + xray_class + "'>"


@patch(xray_class + '.begin_segment', autospec=True)
def test_begin_segment(xray_sdk):
    xray = XRay(turn_it_on=True)
    xray.begin_segment('test_name')
    xray_sdk.assert_called_once_with(xray.xray_recorder, 'test_name')


@patch(xray_class + '.begin_segment', autospec=True)
def test_begin_segment_off(xray_sdk):
    xray = XRay()
    xray.begin_segment('test_name')
    xray_sdk.assert_not_called()


@patch(xray_class + '.begin_subsegment', autospec=True)
def test_begin_subsegment(xray_sdk):
    xray = XRay(turn_it_on=True)
    xray.begin_subsegment('test_sub_name')
    xray_sdk.assert_called_with(xray.xray_recorder, 'test_sub_name')


@patch(xray_class + '.begin_subsegment', autospec=True)
def test_begin_subsegment_off(xray_sdk):
    xray = XRay()
    xray.begin_subsegment('test_name')
    xray_sdk.assert_not_called()


@patch(xray_class + '.put_annotation', autospec=True)
def test_put_annotation(xray_sdk):
    xray = XRay(turn_it_on=True)
    xray.put_annotation('test_key', 'test_value')
    xray_sdk.assert_called_with(xray.xray_recorder, 'test_key', 'test_value')


@patch(xray_class + '.begin_subsegment', autospec=True)
def test_put_annotation_off(xray_sdk):
    xray = XRay()
    xray.put_annotation('test_key', 'test_value')
    xray_sdk.assert_not_called()


@patch(xray_class + '.put_metadata', autospec=True)
def test_put_metadata(xray_sdk):
    xray = XRay(turn_it_on=True)
    xray.put_metadata('test_key', {'a': 1})
    xray_sdk.assert_called_with(xray.xray_recorder, 'test_key', {'a': 1})


@patch(xray_class + '.begin_subsegment', autospec=True)
def test_put_metadata_off(xray_sdk):
    xray = XRay()
    xray.put_metadata('test_key', {'a': 1})
    xray_sdk.assert_not_called()


@patch(xray_class + '.end_segment', autospec=True)
def test_end_segment(xray_sdk):
    xray = XRay(turn_it_on=True)
    xray.end_segment()
    xray_sdk.assert_called_with(xray.xray_recorder)


@patch(xray_class + '.end_subsegment', autospec=True)
def test_end_segment_off(xray_sdk):
    xray = XRay()
    xray.end_segment()
    xray_sdk.assert_not_called()


@patch(xray_class + '.end_subsegment', autospec=True)
def test_end_subsegment(xray_sdk):
    xray = XRay(turn_it_on=True)
    xray.end_subsegment()
    xray_sdk.assert_called_with(xray.xray_recorder)


@patch(xray_class + '.begin_subsegment', autospec=True)
def test_end_subsegment_off(xray_sdk):
    xray = XRay()
    xray.end_subsegment()
    xray_sdk.assert_not_called()
