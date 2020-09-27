from unittest import TestCase
from app import app
from flask import session, request
from currencies import set_cookies, calculate_total, handle_all, check_value, check_currency, handle_errors

class CurrencyConverterTestCase(TestCase):

    def test_get_form(self):
        """check if session works"""
        with app.test_client() as client:
            with client.session_transaction() as check_session:
                defaults = {
                    "val": "",
                    "valid": ""
                }
                check_session.setdefault("amount",defaults)
                check_session["amount"]["val"] = 25

            resp = client.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIsNotNone(session)
            self.assertIn("amount",session)
            self.assertEqual(session["amount"]["val"], 25)

    def test_set_cookies(self):
        """test on session initialization"""
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session["amount"]["val"], " ")
            self.assertEqual(session["curr_1"]["val"], " ")
            self.assertEqual(session["curr_2"]["val"], " ")

    def test_calculate_total(self):
        """test the result of conversion and calculations"""
        self.assertEqual(calculate_total(1, "USD", "USD"),"The result is US$ 1.0")

    def test_result_success(self):
        """calculate if the requests are valid inputs"""
        with app.test_client() as client:
            with client.session_transaction() as check_session:
                defaults = {
                    "val": "",
                    "valid": ""
                }
                check_session.setdefault("amount",defaults)
                check_session.setdefault("curr_1",defaults)
                check_session.setdefault("curr_2",defaults)

            resp = client.get('/res?from=USD&to=USD&amount=1')
            html = resp.get_data(as_text=True)
            from_curr = request.args['from']
            to_curr = request.args['to']
            amount = request.args['amount']
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(amount, "1")
            self.assertEqual(check_value(amount),'1')
            self.assertEqual(handle_errors(amount,check_value,"amount"),amount)
            self.assertEqual(check_currency(from_curr),"USD")
            self.assertEqual(handle_all(from_curr,to_curr,amount),("USD", "USD", "1"))
            self.assertIn('<h2 class="display-5 text-center mb-4">The result is US$ 1.0</h2>', html)
    
    def test_check_value_exception(self):
        """checking if wrong entered value raises an error"""
        self.assertRaises(Exception, check_value, "USD")
    
    def test_redirect_on_failure(self):
        """redirect on failure"""
        with app.test_client() as client:
            with client.session_transaction() as check_session:
                defaults = {
                    "val": "",
                    "valid": ""
                }
                check_session.setdefault("amount",defaults)
                check_session.setdefault("curr_1",defaults)
                check_session.setdefault("curr_2",defaults)

            resp = client.get('/res?from=USK&to=USD&amount=1')
            from_curr = request.args['from']
            self.assertRaises(ValueError, check_currency, "USK")
            self.assertIsNone(handle_errors(from_curr,check_currency,"curr_1"))
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/")