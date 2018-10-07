import os
import pytest

from distutils import dir_util

# This fixture allows use of the 'support' directory for any
# files with test data or json blobs, etc.


@pytest.fixture
def datadir(tmpdir, request):
    filename = request.module.__file__
    parent_dir, _ = os.path.split(filename)
    support_dir = os.path.join(parent_dir, 'support')

    if os.path.isdir(support_dir):
        dir_util.copy_tree(support_dir, str(tmpdir))
    return tmpdir
