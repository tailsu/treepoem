import subprocess
import unittest


class GhostscriptTest(unittest.TestCase):

    def test_installed(self):
        process = subprocess.Popen(
            ['gs', '--version'],
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        self.assertEqual(process.returncode, 0)
        self.assertEqual(str(stderr), "")
        self.assertRegexpMatches(str(stdout), r'9\.\d\d')
