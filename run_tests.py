from __future__ import print_function
try:
    import unittest2 as unittest
except ImportError:
    #Python 2.7 and 3.x
    import unittest

import codecs
import sys
#This does not make the codecs display correctly, but it
#prevents the code from crashing
try:
    sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
except:
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

import io
import email_validator


DATA_CSV = "test_pass.csv"


class TestValidInvalidEmails(unittest.TestCase):
    VALID = []
    INVALID = []

    @classmethod
    def setUpClass(cls):
        """
        Read the DATA_CSV to get valid and invalid emails
        to test
        """
        with io.open(DATA_CSV, mode="r", encoding="utf-8") as datafh:
            #csv does not work with unicode in python2
            datafh.readline() #header
            for line_num, line in enumerate(datafh.read().splitlines()):
                if line.startswith("#"):
                    continue
                row = line.split(",")
                if len(row) != 2:
                    msg = "Error reading CSV, got an unexpected \",\ on line {}".format(line_num)
                    raise ValueError(msg)
                is_valid = row[0] == "1"
                if is_valid:
                    cls.VALID.append(row[1])
                else:
                    cls.INVALID.append(row[1])


    def test_valid(self):
        invalid = []
        for email in self.VALID:
            try:
                email_validator.validate_email(email, check_deliverability=False)
            except email_validator.EmailSyntaxError as exc:
                raise
                invalid.append(email)
        self.assertListEqual([], invalid)


    def test_invalid(self):
        valid = []
        for email in self.INVALID:
            try:
                email_validator.validate_email(email, check_deliverability=False)
                valid.append(email)
            except email_validator.EmailSyntaxError:
                pass
        self.assertListEqual([], valid)


if __name__ == '__main__':
    unittest.main()

