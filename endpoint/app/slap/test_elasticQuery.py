from unittest import TestCase
from models import ElasticQuery


class TestElasticQuery(TestCase):

	def setUp(self):
		self.query = ElasticQuery("http://otto.csrg.cl:9200", "sl-repository", "line","support")


	def test_range_upper_and_lower(self):
		expected_output = { "range":{"Freq": {"gte": 1.0,"lte": 1.2}}}
		term = "Freq"
		params = ["1", "1.2"]
		output = self.query.range(params,term)
		self.assertEquals(expected_output,output)

	def test_range_upper(self):
		expected_output = {"range": {"Freq": {"lte": 1.2}}}
		term = "Freq"
		params = ["", "1.2"]
		output = self.query.range(params, term)
		self.assertEquals(expected_output, output)

	def test_range_lower(self):
		expected_output = {"range": {"Freq": {"gte": 1.0}}}
		term = "Freq"
		params = ["1", ""]
		output = self.query.range(params, term)
		self.assertEquals(expected_output, output)



	def test_equality_numeric_single(self):
		term = "Frequency"
		param = "1"
		expected_output = {"term": { "Frequency": 1.0}}
		output = self.query.equality(param,term)
		self.assertEquals(output,expected_output)

	def test_equality_numeric_multiple(self):
		term = "Frequency"
		param = ["1","1.3","6.34"]
		expected_output = {"term": {"Frequency": [1.0, 1.3, 6.34]}}
		output = self.query.equality(param, term)
		self.assertEquals(output, expected_output)

	def test_equality_string_single(self):
		term = "molecular_name"
		param = "acid"
		expected_output = {"term": {"molecular_name": "acid"}}
		output = self.query.equality(param, term)
		self.assertEquals(output, expected_output)

	def test_equality_string_multiple(self):
		term = "molecular_name"
		param = ["acid", "oxygen", "hydrogen"]
		expected_output = {"term": {"molecular_name": ["acid", "oxygen", "hydrogen"]}}
		output = self.query.equality(param, term)
		self.assertEquals(output, expected_output)

	def test_parser_equality_numeric_single(self):
		self.fail()

	def test_parser_equality_numeric_multiple(self):
		self.fail()

	def test_parser_equality_string_single(self):
		self.fail()

	def test_parser_equality_string_multiple(self):
		self.fail()

	def test_parser_range_upper_and_lower(self):
		self.fail()

	def test_parser_range_upper(self):
		self.fail()

	def test_parser_range_lower(self):
		self.fail()

	def test_parser(self):
		self.fail()





