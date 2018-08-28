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

import email_validator

class TestValidInvalidEmails(unittest.TestCase):

    def test_normalization_ascii_domain(self):
        ascii_domain_emails = [
            "Abc@example.com",
            "Abc.123@example.com",
            "user+mailbox/department=shipping@example.com",
        ]
        for email in ascii_domain_emails:
            ret = email_validator.validate_email(email, check_deliverability=False)
            self.assertTrue("smtputf8" in ret)
            self.assertEqual(ret["smtputf8"], False)
            self.assertTrue("email" in ret)
            self.assertEqual(ret["email"], email)
            self.assertTrue("email_ascii" in ret)
            self.assertEqual(ret["email_ascii"], email)


    def test_normalization_unicode_domain(self):
        unicode_domain_emails = [
            (u"jeff@\u81fa\u7db2\u4e2d\u5fc3.tw", None, "jeff@xn--fiqq24b10vi0d.tw"),
            (u"user@example.com", None, "user@example.com"),
            (u"my.name@domain\uff0ecom", "my.name@domain.com", "my.name@domain.com"),
        ]
        for email, out_email, encoded_email in unicode_domain_emails:
            ret = email_validator.validate_email(email, check_deliverability=False)
            if out_email is None:
                out_email = email
            self.assertTrue("smtputf8" in ret)
            self.assertEqual(ret["smtputf8"], False)
            self.assertTrue("email" in ret)
            self.assertEqual(ret["email"], out_email)
            self.assertTrue("email_ascii" in ret)
            self.assertEqual(ret["email_ascii"], encoded_email)


    def test_valid_utf8_smtputf8_enabled(self):
        unicode_local_part_emails = [
            (u"user@example.com", False),
            (u"q\u00f1@domain.com", True),
            (u"my\uff0ename@\u81fa\u7db2\u4e2d\u5fc3.tw", True),
        ]
        for email, smtputf8_out in unicode_local_part_emails:
            ret = email_validator.validate_email(email, check_deliverability=False, allow_smtputf8=True)
            self.assertTrue("smtputf8" in ret)
            self.assertEqual(ret["smtputf8"], smtputf8_out)
            self.assertTrue("email" in ret)
            self.assertEqual(ret["email"], email)


    def test_valid_utf8_smtputf8_disabled(self):
        unicode_local_part_emails = [
            (u"user@example.com", True),
            (u"q\u00f1@domain.com", False),
            (u"my\uff0ename@\u81fa\u7db2\u4e2d\u5fc3.tw", False),
        ]
        for email, should_validate in unicode_local_part_emails:
            try:
                ret = email_validator.validate_email(email, check_deliverability=False, allow_smtputf8=False)
                self.assertTrue(should_validate)
                self.assertTrue("smtputf8" in ret)
                self.assertEqual(ret["smtputf8"], False)
                self.assertTrue("email" in ret)
                self.assertEqual(ret["email"], email)
            except email_validator.EmailSyntaxError:
                self.assertFalse(should_validate)


if __name__ == '__main__':
    unittest.main()

