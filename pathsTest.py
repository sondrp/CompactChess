
import unittest
import re
from paths import paths


class TestCalculations(unittest.TestCase):

    # In this test we are checking if the paths regex is matching correctly.
    def test_leaper(self):
        test_cases = [
            ("N ", True),
            ("n ", True),
            (" ", False),
            ("n", False),
            ("N", False),
            ("Q ", True),
            ("q ", True),
            ("Nn", True),
            ("nN", True),
            ("NN", False),
            ("nn", False),
        ]
        regex, _ = paths["leaper"]
        for case, answer in test_cases:
            self.assertEqual(bool(re.match(regex, case)), answer)
        
    def test_ranger(self):
        test_cases = [
            ("R", False),
            ("r", False),
            (" R", False),
            (" r", False),
            ("RR", False),
            ("rr", False),
            ("K ", True),
            ("k ", True),
            ("R ", True),
            ("R  ", True),
            ("R   ", True),
            ("R   r", True),
            ("R   R", False),
            ("r   r", False),
            ("r   R", True),
            ("r   Rr", False),
            ("R   rR", False),
        ]

        regex, _ = paths["ranger"]
        for case, answer in test_cases:
            self.assertEqual(bool(re.match(regex, case)), answer)

    def test_capture(self):
        test_cases = [
            ("", False),
            (" ", False),
            ("  ", False),
            (" R", False),
            (" r", False),
            ("r ", False),
            ("R ", False),
            ("Rr", True),
            ("rR", True),
            ("rR", True),
            ("rR ", False),
            ("rRR", False),
        ]
        regex, _ = paths["capture"]
        for case, answer in test_cases:
            self.assertEqual(bool(re.match(regex, case)), answer)

    def test_unoccupied(self):
        test_cases = [
            ("", False),
            (" ", False),
            ("  ", False),
            (" R", False),
            (" r", False),
            ("Rr", False),
            ("rR", False),
            ("r ", True),
            ("R ", True),
            ("R  ", False),
            ("rRR", False),
        ]
        regex, _ = paths["unoccupied"]
        for case, answer in test_cases:
            self.assertEqual(bool(re.match(regex, case)), answer)

    def test_pawnDoubleForward(self):
        test_cases = [
            ("P    ", True),
            ("p    ", True),
            ("prr  ", True),
            ("Prr  ", True),
            ("Prrr ", False),
            ("prrr ", False),
            ("prr r", False),
            ("Prr r", False),
            ("Prr   ", False),
            ("Prr   ", False),
            (" Prr ", False),
            (" Prr ", False),
        ]
        regex, _ = paths["pawnDoubleForward"]
        for case, answer in test_cases:
            self.assertEqual(bool(re.match(regex, case)), answer)

    def test_enPassant(self):
        test_cases = [
            ("P  p ", True),
            ("p  P ", True),
            ("P  P ", False),
            (" p P ", False),
            (" P p ", False),
            ("Prrp ", True),
            ("prrP ", True),
            ("prrPr", False),
        ]
        regex, _ = paths["enPassant"]
        for case, answer in test_cases:
            self.assertEqual(bool(re.match(regex, case)), answer)

    def test_castle(self):
        test_cases = [
            ("K  Rr", True),
            ("K   Rr", True),
            ("k  rR", True),
            ("k   rR", True),
            ("kp  rR", False),
        ]
        regex, _ = paths["castle"]
        for case, answer in test_cases:
            self.assertEqual(bool(re.match(regex, case)), answer)

    def test_subs(self):
        test_cases = [
            ("leaper", "N ", " N"),
            ("leaper", "Nn", " N"),
            ("ranger", "Q   ", "   Q"),
            ("ranger", "Q  r", "   Q"),
            ("capture", "Kr", " K"),
            ("capture", "Kr", " K"),
            ("unoccupied", "K ", " K"),
            ("unoccupied", "K ", " K"),
            ("pawnDoubleForward", "Prr  ", " rr P"),
            ("pawnDoubleForward", "prr  ", " rr p"),
            ("enPassant", "pqqP ", " qq p"),
            ("enPassant", "Pqqp ", " qq P"),
            ("castle", "K  Rr", " RK r"),
            ("castle", "K   Rr", " RK  r"),
            ("castle", "k  rR", " rk R"),
            ("castle", "k   rR", " rk  R"),
        ]
        for movetype, path, res in test_cases:
            regex, replacement = paths[movetype]
            self.assertEqual(re.sub(regex, replacement, path), res)

if __name__ == '__main__':
    unittest.main()