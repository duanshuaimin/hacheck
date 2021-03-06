import os.path
import mock
import shutil
import tempfile
from unittest import TestCase

from hacheck import spool

se = mock.sentinel


class TestSpool(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        spool.configure(self.root)

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_configure_creates_root(self):
        spool.configure(os.path.join(self.root, 'spool'))
        assert os.path.exists, 'spool'

    def test_configure_no_write(self):
        new_root = os.path.join(self.root, 'non_writable')
        os.mkdir(new_root)
        os.chmod(new_root, 0o555)
        self.assertRaises(ValueError, spool.configure, new_root, needs_write=True)

    def test_configure_no_write_no_needs_write(self):
        new_root = os.path.join(self.root, 'non_writable')
        os.mkdir(new_root)
        os.chmod(new_root, 0o555)
        spool.configure(new_root, needs_write=False)

    def test_basic(self):
        svcname = 'test_basic'
        self.assertEquals(True, spool.status(svcname)[0])
        spool.down(svcname)
        self.assertEquals(False, spool.status(svcname)[0])
        self.assertEquals(False, spool.is_up(svcname)[0])
        spool.up(svcname)
        self.assertEquals(True, spool.status(svcname)[0])

    def test_all(self):
        svcname = 'test_all'
        self.assertEquals(True, spool.status(svcname)[0])
        spool.down('all')
        self.assertEquals(True, spool.status(svcname)[0])
        self.assertEquals(False, spool.is_up(svcname)[0])

    def test_status_all_down(self):
        self.assertEqual(len(list(spool.status_all_down())), 0)
        spool.down('foo')
        self.assertEqual(list(spool.status_all_down()), [('foo', {'service': 'foo', 'reason': ''})])

    def test_repeated_ups_works(self):
        spool.up('all')
        spool.up('all')
