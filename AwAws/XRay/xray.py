# The imports on this module are called from within the constructor.
# The reason for this is that the xray-sdk needs to be loaded last
# so that it can patch the other SDKs.  This also allows us to easily
# turn the globally turn XRay feature on and off as well as moving all
# of the logic for on/off out of the caller functions


class XRay():
    def __init__(self, turn_it_on=False):

        self.status = turn_it_on
        if self.status is True:
            from aws_xray_sdk.core import xray_recorder
            from aws_xray_sdk.core import patch_all
            patch_all()
            self.xray_recorder = xray_recorder


    def begin_segment(self, segment_name):
        "creates a new segment"
        if self.status is True:
            self.xray_recorder.begin_segment(segment_name)


    def begin_subsegment(self, sub_segment_name):
        "Create a new segment - use this in lambda functions"
        if self.status is True:
            self.xray_recorder.begin_subsegment(sub_segment_name)


    def put_annotation(self, key, value):
        "Annotations are used for sorting/indexing traces"
        if self.status is True:
            self.xray_recorder.put_annotation(key, value)


    def put_metadata(self, key, data):
        "Metadata is any data that should be saved with the trace"
        if self.status is True:
            self.xray_recorder.put_metadata(key, data)


    def end_segment(self):
        "End/close the segment"
        if self.status is True:
            self.xray_recorder.end_segment()


    def end_subsegment(self):
        "End/close the subsegment"
        if self.status is True:
            self.xray_recorder.end_subsegment()
