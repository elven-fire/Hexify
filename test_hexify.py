import unittest
from hexify import *


class TestDrawings(unittest.TestCase):

    """Verify each created image."""

    def test_check_mark(self):
        """Verify the simple green checkmark."""
        self.assertEqual(CHECK_MARK.histogram(), [7625, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2375, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7355, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 270, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2375, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7355, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2645])

    def test_trash_can(self):
        """Verify the simple red trash can."""
        self.assertEqual(TRASH_CAN.histogram(), [3572, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 683, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5745, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3572, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6428])

    def test_drop_image(self):
        """Verify the dropped image landing pad."""
        self.assertEqual(DROP_IMAGE.histogram(), [360687, 0, 0, 0, 0, 0, 0, 0, 25, 46, 25, 9, 21, 55, 14, 11, 23, 18, 24, 36, 30, 37, 28, 27, 13, 24, 16, 15, 17, 13, 8, 19, 25, 19, 29, 26, 27, 29, 18, 20, 26, 10, 43, 24, 21, 9, 29, 22, 28, 14, 22, 39, 29, 24, 12, 15, 7, 24, 17, 24, 26, 7, 11, 31, 41, 19, 21, 28, 6, 28, 22, 6, 45, 15, 26, 21, 37, 3, 22, 14, 13, 12, 34, 44, 22, 31, 12, 13, 23, 28, 28, 26, 51, 38, 7, 39, 38, 42, 66, 34, 5183, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6914, 360687, 0, 0, 0, 0, 0, 0, 0, 25, 46, 25, 9, 21, 55, 14, 11, 23, 18, 24, 36, 30, 37, 28, 27, 13, 24, 16, 15, 17, 13, 8, 19, 25, 19, 29, 26, 27, 29, 18, 20, 26, 10, 43, 24, 21, 9, 29, 22, 28, 14, 22, 39, 29, 24, 12, 15, 7, 24, 17, 24, 26, 7, 11, 31, 41, 19, 21, 28, 6, 28, 22, 6, 45, 15, 26, 21, 37, 3, 22, 14, 13, 12, 34, 44, 22, 31, 12, 13, 23, 28, 28, 26, 51, 38, 7, 39, 38, 42, 66, 34, 3871, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8226, 360687, 0, 0, 0, 0, 0, 0, 0, 25, 46, 25, 9, 21, 55, 14, 11, 23, 18, 24, 36, 30, 37, 28, 27, 13, 24, 16, 15, 17, 13, 8, 19, 25, 19, 29, 26, 27, 29, 18, 20, 26, 10, 43, 24, 21, 9, 29, 22, 28, 14, 22, 39, 29, 24, 12, 15, 7, 24, 17, 24, 26, 7, 11, 31, 41, 19, 21, 28, 6, 28, 22, 6, 45, 15, 26, 21, 37, 3, 22, 14, 13, 12, 34, 44, 22, 31, 12, 13, 23, 28, 28, 26, 51, 38, 7, 39, 38, 42, 66, 34, 12097, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 359294, 60, 30, 30, 27, 26, 19, 26, 19, 8, 17, 10, 15, 5, 8, 9, 6, 21, 8, 25, 13, 8, 3, 6, 8, 17, 25, 10, 11, 9, 13, 3, 1, 4, 6, 9, 5, 4, 21, 5, 13, 8, 8, 5, 6, 7, 15, 8, 11, 5, 6, 19, 8, 15, 8, 9, 20, 8, 18, 8, 9, 8, 5, 8, 10, 8, 7, 11, 5, 5, 2, 4, 13, 4, 4, 3, 5, 4, 9, 11, 2, 7, 10, 3, 11, 5, 14, 7, 11, 8, 10, 11, 11, 19, 12, 8, 9, 5, 9, 10, 8, 6, 14, 11, 4, 6, 6, 20, 14, 3, 3, 7, 8, 6, 11, 7, 9, 6, 3, 6, 17, 12, 9, 16, 8, 14, 5, 11, 6, 22, 8, 11, 8, 9, 7, 12, 9, 6, 11, 4, 2, 10, 5, 6, 6, 1, 19, 5, 10, 7, 16, 5, 6, 2, 3, 3, 15, 3, 4, 11, 13, 9, 11, 5, 9, 3, 22, 9, 10, 8, 7, 9, 13, 4, 8, 6, 5, 17, 11, 6, 4, 7, 6, 13, 13, 5, 19, 10, 3, 10, 13, 6, 7, 9, 13, 8, 7, 8, 4, 11, 3, 7, 7, 5, 2, 7, 6, 8, 8, 4, 11, 12, 15, 5, 27, 12, 16, 10, 8, 2, 7, 5, 10, 5, 3, 12, 9, 11, 5, 12, 14, 11, 10, 5, 16, 30, 6, 15, 9, 13, 16, 15, 7, 19, 12, 5, 8, 8, 18, 18, 9, 25, 34, 48, 41, 13105])


class TestHexifiedImageWidget(unittest.TestCase):

    """Test the HexifiedImageWidget class."""

    def setUp(self):
        """Prepare widgets for use in testing."""
        app = QtGui.QApplication(sys.argv)
        self.main = HexifyWidget()
        self.hexed = HexifiedImage(None, "A")
        self.widget = self.main.add_image(self.hexed)
        
    def test_init(self):
        """Verify default attributes."""
        self.assertIs(self.widget.main, self.main)
        self.assertIs(self.widget.hexed, self.hexed)
        self.assertFalse(self.widget.confirmed)
        self.assertFalse(self.widget.selected)

    def test_GUI_attributes(self):
        """Verify attributes saving GUI components properly created."""
        self.assertIsInstance(self.widget._preview, QtGui.QPushButton)
        self.assertIsInstance(self.widget._image, QtGui.QPushButton)
        self.assertIsInstance(self.widget._image, QtGui.QPushButton)

    def test_selected(self):
        """Verify selected property."""
        self.widget.selected = True
        self.assertTrue(self.widget.selected)
        self.widget.selected = False
        self.assertFalse(self.widget.selected)
        self.widget.selected = False
        self.assertFalse(self.widget.selected)

    def test_confirmed(self):
        """Verify confirmed property."""
        self.widget.confirmed = True
        self.assertTrue(self.widget.confirmed)
        self.widget.confirmed = False
        self.assertFalse(self.widget.confirmed)
        self.widget.confirmed = False
        self.assertFalse(self.widget.confirmed)

    def test_toggle_confirm(self):
        """Verify toggling of confirmed status."""
        self.widget.toggle_confirm()
        self.assertTrue(self.widget.confirmed)
        self.widget.toggle_confirm()
        self.assertFalse(self.widget.confirmed)


@unittest.skip("Unknown error in preview generation??")
class TestHexifiedImagePreviews(unittest.TestCase):

    """Test the functions for modifying the HexifiedImage."""

    def setUp(self):
        """Prepare widgets for use in testing."""
        app = QtGui.QApplication(sys.argv)
        self.main = HexifyWidget()
        self.hexed = HexifiedImage(None, "A")
        self.widget = self.main.add_image(self.hexed)

    def test_resize(self):
        """Verify next shape/size."""
        self.widget.next_hex_configuration()
        self.assertEqual(self.hexed.size, 2)
        self.assertEqual(self.hexed.shape, HexDraw.SHAPE_LONG)
        self.widget.next_hex_configuration()
        self.assertEqual(self.hexed.size, 3)
        self.assertEqual(self.hexed.shape, HexDraw.SHAPE_LONG)
        self.widget.next_hex_configuration()
        self.assertEqual(self.hexed.size, 3)
        self.assertEqual(self.hexed.shape, HexDraw.SHAPE_ROUND)
        self.widget.next_hex_configuration()
        self.assertEqual(self.hexed.size, 1)
        self.assertEqual(self.hexed.shape, HexDraw.SHAPE_LONG)

    def test_randomize(self):
        """Verify random letter."""
        self.widget.randomize_letter()
        self.assertNotEqual(self.hexed.letter, "A")

    def test_letter(self):
        """Verify custom letter."""
        self.widget.set_letter("Ch")
        self.assertEqual(self.hexed.letter, "Ch")

    def test_image(self):
        """Verify custom image."""
        image = Image.new("RGBA", (100, 100))
        self.widget.set_image(image)
        self.assertIs(self.hexed.image, image)

    def test_size(self):
        """Verify custom size/shape."""
        self.widget.set_hex_detail(3, HexDraw.SHAPE_ROUND)
        self.assertEqual(self.hexed.size, 3)
        self.assertEqual(self.hexed.shape, HexDraw.SHAPE_ROUND)


class TestHexifyWidget(unittest.TestCase):

    """Test the HexifyWidget class."""

    def setUp(self):
        """Prepare widgets for use in testing."""
        app = QtGui.QApplication(sys.argv)
        self.main = HexifyWidget()

    def test_init(self):
        """Verify default attributes."""
        self.assertFalse(self.main._pause_selection_watch)
        self.assertEqual(self.main._confirmed_count, 0)
        self.assertEqual(self.main._preview_page, 0)
        
    def test_GUI_attributes(self):
        """Verify attributes saving GUI components properly created."""
        self.assertIsInstance(self.main.drop_UI, QtGui.QWidget)
        self.assertIsInstance(self.main.main_UI, QtGui.QWidget)
        self.assertIsInstance(self.main._selected, QtGui.QCheckBox)
        self.assertIsInstance(self.main._resize_btn, QtGui.QPushButton)
        self.assertIsInstance(self.main._random_btn, QtGui.QPushButton)
        self.assertIsInstance(self.main._confirm_btn, QtGui.QPushButton)
        self.assertIsInstance(self.main._delete_btn, QtGui.QPushButton)
        self.assertIsInstance(self.main.scroller, QtGui.QWidget)
        self.assertIsInstance(self.main.scroller.parent().parent(), # why 2?
                              QtGui.QScrollArea)
        self.assertIsInstance(self.main._pagepreview, QtGui.QLabel)
        self.assertIsInstance(self.main._pagepreviewlabel, QtGui.QLabel)


@unittest.skip("Perhaps with QTest?")
class TestDragAndDrop(unittest.TestCase):
    pass


class TestBulkActions(unittest.TestCase):

    """Test bulk action / selection combinations and permutations."""

    def setUp(self):
        """Prepare widgets for use in testing."""
        app = QtGui.QApplication(sys.argv)
        self.main = HexifyWidget()
        self.widget1 = self.main.add_image(HexifiedImage(None, "A"))
        self.widget2 = self.main.add_image(HexifiedImage(None, "B"))
        self.widget3 = self.main.add_image(HexifiedImage(None, "C"))


    ## Selections

    def test_select_partial(self):
        """Verify "select unconfirmed" action."""
        self.widget1.confirmed = True
        self.main._selected.setCheckState(QtCore.Qt.PartiallyChecked)
        self.assertFalse(self.widget1.selected)
        self.assertTrue(self.widget2.selected)
        self.assertTrue(self.widget3.selected)

    def test_select_all(self):
        """Verify "select all" action."""
        self.widget1.confirmed = True
        self.main._selected.setCheckState(QtCore.Qt.Checked)
        self.assertTrue(self.widget1.selected)
        self.assertTrue(self.widget2.selected)
        self.assertTrue(self.widget3.selected)

    def test_select_none(self):
        """Verify "select all" action."""
        self.widget1.confirmed = True
        self.main._selected.setCheckState(QtCore.Qt.PartiallyChecked)
        self.assertFalse(self.widget1.selected)
        self.assertTrue(self.widget2.selected)
        self.assertTrue(self.widget3.selected)
        self.main._selected.setCheckState(QtCore.Qt.Unchecked)
        self.assertFalse(self.widget1.selected)
        self.assertFalse(self.widget2.selected)
        self.assertFalse(self.widget3.selected)

    def test_manual_deselect(self):
        """Verify "select all" box is cleared on manual deselect."""
        self.main._selected.setCheckState(QtCore.Qt.Checked)
        self.widget1.selected = False
        self.assertEqual(self.main._selected.checkState(), QtCore.Qt.Unchecked)
        self.assertFalse(self.widget1.selected)
        self.assertTrue(self.widget2.selected)
        self.assertTrue(self.widget3.selected)
        
    def test_manual_select(self):
        """Verify "select all" box is cleared on manual select."""
        self.main._selected.setCheckState(QtCore.Qt.Checked)
        self.widget1.confirmed = True
        self.widget2.confirmed = True
        self.main._selected.setCheckState(QtCore.Qt.PartiallyChecked)
        self.widget1.selected = True
        self.assertEqual(self.main._selected.checkState(), QtCore.Qt.Unchecked)
        self.assertTrue(self.widget1.selected)
        self.assertFalse(self.widget2.selected)
        self.assertTrue(self.widget3.selected)

    @unittest.expectedFailure
    def test_manual_select_partial(self):
        """Verify "select all" box is set correctly on manual select."""
        self.widget1.confirmed = True
        self.widget2.confirmed = True
        self.widget3.selected = True
        self.assertEqual(self.main._selected.checkState(), QtCore.Qt.PartiallyChecked)
        self.assertFalse(self.widget1.selected)
        self.assertFalse(self.widget2.selected)
        self.assertTrue(self.widget3.selected)
        
    @unittest.expectedFailure
    def test_manual_select_all(self):
        """Verify "select all" box is set correctly on manual select."""
        self.widget1.confirmed = True
        self.main._selected.setCheckState(QtCore.Qt.PartiallyChecked)
        self.widget1.selected = True
        self.assertEqual(self.main._selected.checkState(), QtCore.Qt.Checked)
        self.assertTrue(self.widget1.selected)
        self.assertTrue(self.widget2.selected)
        self.assertTrue(self.widget3.selected)

    @unittest.expectedFailure
    def test_partial_is_all(self):
        """Verify "select all" skips straight to "all" when none confirmed."""
        self.main._selected.setCheckState(QtCore.Qt.PartiallyChecked)
        self.assertEqual(self.main._selected.checkState(), QtCore.Qt.Checked)


    ## Button Text

    def test_button_text_none(self):
        """Verify button text when nothing is selected."""
        self.assertEqual(self.main._resize_btn.text(), "Resize Selected")
        self.assertEqual(self.main._random_btn.text(), "Randomize Selected")
        self.assertEqual(self.main._confirm_btn.text(), "[Un]confirm Selected")
        self.assertEqual(self.main._delete_btn.text(), "Delete Selected")
        
    def test_button_text_manual(self):
        """Verify button text after a manual selection."""
        self.widget1.selected = True
        self.assertEqual(self.main._resize_btn.text(), "Resize Selected")
        self.assertEqual(self.main._random_btn.text(), "Randomize Selected")
        self.assertEqual(self.main._confirm_btn.text(), "[Un]confirm Selected")
        self.assertEqual(self.main._delete_btn.text(), "Delete Selected")
        
    def test_button_text_partial(self):
        """Verify button text for a partial selection."""
        self.widget1.confirmed = True
        self.main._selected.setCheckState(QtCore.Qt.PartiallyChecked)
        self.assertEqual(self.main._resize_btn.text(), "Resize Unconfirmed")
        self.assertEqual(self.main._random_btn.text(), "Randomize Unconfirmed")
        self.assertEqual(self.main._confirm_btn.text(), "Confirm Unconfirmed")
        self.assertEqual(self.main._delete_btn.text(), "Delete Unconfirmed")
        
    def test_button_text_all(self):
        """Verify button text for select all."""
        self.main._selected.setCheckState(QtCore.Qt.Checked)
        self.assertEqual(self.main._resize_btn.text(), "Resize All")
        self.assertEqual(self.main._random_btn.text(), "Randomize All")
        self.assertEqual(self.main._confirm_btn.text(), "Confirm All")
        self.assertEqual(self.main._delete_btn.text(), "Delete All")
        
    def test_button_text_remanual(self):
        """Verify button text reverts after manual selection."""
        self.main._selected.setCheckState(QtCore.Qt.Checked)
        self.widget1.selected = False
        self.assertEqual(self.main._resize_btn.text(), "Resize Selected")
        self.assertEqual(self.main._random_btn.text(), "Randomize Selected")
        self.assertEqual(self.main._confirm_btn.text(), "[Un]confirm Selected")
        self.assertEqual(self.main._delete_btn.text(), "Delete Selected")

    def test_button_text_unconfirm(self):
        """Verify button text shifts after a Confirm All."""
        self.main._selected.setCheckState(QtCore.Qt.Checked)
        self.main.confirm_selected()
        self.assertEqual(self.main._confirm_btn.text(), "Unconfirm All")
        self.main.confirm_selected()
        self.assertEqual(self.main._confirm_btn.text(), "Confirm All")

    @unittest.skip("??")
    def test_add_more_partial_select(self):
        """Verify that new items are selected when selecting unconfirmed."""
        self.widget1.confirmed = True
        self.main._selected.setCheckState(QtCore.Qt.PartiallyChecked)
        widget4 = self.main.add_image(HexifiedImage(None, "D"))
        self.assertTrue(widget4.selected)

    @unittest.skip("??")
    def test_add_more_select_all(self):
        """Verify that new items are selected when selecting all."""
        self.main._selected.setCheckState(QtCore.Qt.Checked)
        widget4 = self.main.add_image(HexifiedImage(None, "D"))
        self.assertTrue(widget4.selected)


    ## Bulk Actions
        
    @unittest.skip("Unknown error in preview generation from unittest?")
    def test_resize_selected(self):
        """Verify selected items (only) are resized."""
        self.widget1.selected = True
        self.main.resize_selected()
        self.assertEqual(self.widget1.hexed.size, 2)
        self.assertEqual(self.widget2.hexed.size, 1)
        self.assertEqual(self.widget3.hexed.size, 1)

    def test_resize_none(self):
        """Verify no effect when resizing without a selection."""
        self.main.resize_selected()
        self.assertEqual(self.widget1.hexed.size, 1)
        self.assertEqual(self.widget2.hexed.size, 1)
        self.assertEqual(self.widget3.hexed.size, 1)
        
    @unittest.skip("Unknown error in preview generation from unittest?")
    def test_randomize_selected(self):
        """Verify selected items (only) are randomized."""
        self.widget1.selected = True
        self.main.randomize_selected()
        self.assertNotEqual(self.widget1.hexed.letter, "A")
        self.assertEqual(self.widget2.hexed.letter, "B")
        self.assertEqual(self.widget3.hexed.letter, "C")

    def test_randomize_none(self):
        """Verify no effect when randomizing without a selection."""
        self.main.randomize_selected()
        self.assertEqual(self.widget1.hexed.letter, "A")
        self.assertEqual(self.widget2.hexed.letter, "B")
        self.assertEqual(self.widget3.hexed.letter, "C")

    def test_confirm_selected(self):
        """Verify selected items (only) are confirmed."""
        self.widget1.selected = True
        self.main.confirm_selected()
        self.assertTrue(self.widget1.confirmed)
        self.assertFalse(self.widget2.confirmed)
        self.assertFalse(self.widget3.confirmed)

    def test_confirm_none(self):
        """Verify no effect when confirming without a selection."""
        self.main.confirm_selected()
        self.assertFalse(self.widget1.confirmed)
        self.assertFalse(self.widget2.confirmed)
        self.assertFalse(self.widget3.confirmed)

    def test_confirm_selected_toggles(self):
        """Verify items can be confirmed OR unconfirmed on selection."""
        self.widget1.confirmed = True
        self.widget1.selected = True
        self.widget2.selected = True
        self.main.confirm_selected()
        self.assertFalse(self.widget1.confirmed)
        self.assertTrue(self.widget2.confirmed)
        self.assertFalse(self.widget3.confirmed)
        self.assertTrue(self.widget1.selected)
        self.assertTrue(self.widget2.selected)
        self.assertFalse(self.widget3.selected)

    def test_confirm_all_notoggle(self):
        """Verify Confirm All does NOT unconfirm confirmed."""
        self.widget1.confirmed = True
        self.main._selected.setCheckState(QtCore.Qt.Checked)
        self.main.confirm_selected()
        self.assertTrue(self.widget1.confirmed)
        self.assertTrue(self.widget2.confirmed)
        self.assertTrue(self.widget3.confirmed)

    def test_confirm_all_manual_toggle(self):
        """Verify [Un]confirm All does unconfirm manual selections."""
        self.widget1.confirmed = True
        self.widget1.selected = True
        self.widget2.selected = True
        self.widget3.selected = True
        self.main.confirm_selected()
        self.assertFalse(self.widget1.confirmed)
        self.assertTrue(self.widget2.confirmed)
        self.assertTrue(self.widget3.confirmed)
        
    @unittest.skip("deleteLater hasn't run yet")
    def test_delete_selected(self):
        """Verify selected items (only) are deleted."""
        self.widget1.selected = True
        self.widget2.selected = True
        self.main.delete_selected()
        self.assertEqual(len(self.main._get_items()), 1)
        self.assertIs(self.main._get_items()[0], self.widget3)

    @unittest.skip("deleteLater hasn't run yet")
    def test_delete_all(self):
        """Verify no effect when deleting without a selection."""
        self.main.delete_selected()
        self.assertEqual(len(self.main._get_items()), 3)

    def test_unselect_after_delete_all(self):
        """Verify select all is unchecked after Delete All."""
        self.main._selected.setCheckState(QtCore.Qt.Checked)
        self.main.delete_selected()
        self.assertEqual(self.main._selected.checkState(), QtCore.Qt.Unchecked)

    def test_unselect_after_delete_any(self):
        """Verify select all is unchecked after deletion."""
        self.widget1.confirmed = True
        self.main._selected.setCheckState(QtCore.Qt.PartiallyChecked)
        self.main.delete_selected()
        self.assertEqual(self.main._selected.checkState(), QtCore.Qt.Unchecked)


@unittest.skip("Unknown error in preview generation from unittest?")
class TestPagePreview(unittest.TestCase):

    """Test pagination of the preview."""

    def setUp(self):
        """Prepare widgets for use in testing."""
        app = QtGui.QApplication(sys.argv)
        self.main = HexifyWidget()

    def test_single_page_next(self):
        """Confirm no behavior for a single-page document."""
        self.main.next_preview_page()
        self.assertEquals(self.main._preview_page, 0)

    def test_single_page_prev(self):
        """Confirm no behavior for a single-page document."""
        self.main.prev_preview_page()
        self.assertEquals(self.main._preview_page, 0)

    def test_two_page_next(self):
        """Confirm advancement and wrap-around."""
        for i in range(31):
            self.main.add_image(HexifiedImage(None, "A", 3))
        self.assertEquals(self.main._pages, 2)
        self.assertEquals(self.main._preview_page, 0)
        self.main.next_preview_page()
        self.assertEquals(self.main._preview_page, 1)
        self.main.next_preview_page()
        self.assertEquals(self.main._preview_page, 0)

    def test_two_page_prev(self):
        """Confirm advancement and wrap-around."""
        for i in range(31):
            self.main.add_image(HexifiedImage(None, "A", 3))
        self.assertEquals(self.main._preview_page, 0)
        self.main.prev_preview_page()
        self.assertEquals(self.main._preview_page, 1)
        self.main.prev_preview_page()
        self.assertEquals(self.main._preview_page, 0)


@unittest.skip("How to verify output?")
class TestExportAndPrint(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
