from unittest import TestCase
from models import ElasticQuery

class TestElasticQuery(TestCase):

	def setUp(self):
		self.query = ElasticQuery("http://otto.csrg.cl:9200", "sl-repository", "line", "support")
		self.maxDiff = None

	def test_range_upper_and_lower(self):
		expected_output = {"range": {"Freq": {"gte": 1.0, "lte": 1.2}}}
		term = "Freq"
		params = ["1", "1.2"]
		output = self.query.range(params, term)
		self.assertEquals(expected_output, output)

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

	def test_equality_numeric(self):
		term = "Frequency"
		param = "1"
		expected_output = {"term": {"Frequency": 1.0}}
		output = self.query.equality(param, term)
		self.assertEquals(output, expected_output)

	def test_equality_string(self):
		term = "molecular_name"
		param = "acid"
		expected_output = {"match": {"molecular_name": "acid"}}
		output = self.query.equality(param, term)
		self.assertEquals(output, expected_output)

	def test_constrain_parser_list_equality_numeric(self):
		term = "Frequency"
		values = "1.2,2.5,3"
		input = {term : values}
		expected_output = {
			"bool":
				{
					"should":
						[
							{
								"term":
									{
										"Frequency": 1.2
									}
							},
							{
								"term": {
									"Frequency": 2.5
								}
							},
							{
								"term": {
									"Frequency": 3
								}
							}
						],
					"minimum_should_match": 1
				}
		}

		output = self.query.constrain_parser(values,term)
		self.assertEqual(output,expected_output)

	def test_constrain_parser_list_range_numeric(self):
		term = "Frequency"
		values = "1.2/2.5,3/5,6/7"
		input = {term : values}
		expected_output = {
			"bool":
				{
					"should":
						[
							{
								"range":
									{
										"Frequency":
											{
												"gte": 1.2,
												"lte": 2.5
											}
									}
							},
							{
								"range":
									{
										"Frequency":
											{
												"gte": 3.0,
												"lte": 5.0
											}
									}
							},
							{
								"range":
									{
										"Frequency":
											{
												"gte": 6,
												"lte": 7
											}
									}
							}
						],
					"minimum_should_match": 1
				}
		}

		output = self.query.constrain_parser(values,term)
		self.assertEqual(output,expected_output)

	def test_constrain_parser_list_mix_numeric(self):
		term = "Frequency"
		values = "1.2/2.5,3/5,6/7,1.2,2.5,3"
		input = {term : values}
		expected_output = {
			"bool":
				{
					"should":
						[
							{
								"range":
									{
										"Frequency":
											{
												"gte": 1.2,
												"lte": 2.5
											}
									}
							},
							{
								"range":
									{
										"Frequency":
											{
												"gte": 3.0,
												"lte": 5.0
											}
									}
							},
							{
								"range":
									{
										"Frequency":
											{
												"gte": 6,
												"lte": 7
											}
									}
							},
							{
								"term":
									{
										"Frequency": 1.2
									}
							},
							{
								"term": {
									"Frequency": 2.5
								}
							},
							{
								"term": {
									"Frequency": 3
								}
							}
						],
					"minimum_should_match": 1
				}
		}

		output = self.query.constrain_parser(values,term)
		self.assertEqual(output,expected_output)

	def test_constrain_parser_list_equality_string(self):
		term = "Chemical Name"
		values = "Formic Acid,Formyl Chloride"

		expected_output = {
			"bool":
				{
					"should":
						[
							{"match": {"Chemical Name": "Formic Acid"}},
							{"match": {"Chemical Name": "Formyl Chloride"}}
						],
					"minimum_should_match": 1
				}
		}

		output = self.query.constrain_parser(values,term)
		self.assertEqual(output,expected_output)

	def test_parser_single_equality(self):
		input = {
			"Chemical Name": "Formic Acid,Formyl Chloride"
		}
		expected_output = {
			"query":
				{
					"bool":
						{
							"must":
								[
									{
										"bool":
											{
												"should":
													[
														{"match": {"Chemical Name": "Formic Acid"}},
														{"match": {"Chemical Name": "Formyl Chloride"}}
													],
												"minimum_should_match": 1
											}
									}
								]
						}
				}
		}
		output = self.query.parser(input)
		self.assertEqual(output,expected_output)

	def test_parser_multiple_all_equality(self):
		input = {
			"Chemical Name": "Formic Acid,Formyl Chloride",
			"Frequency": "1.2,2.5,3"
		}
		expected_output = {
			"query":
				{
					"bool":
						{
							"must":
								[
									{
										"bool":
											{
												"should":
													[
														{
															"term":
																{
																	"Frequency": 1.2
																}
														},
														{
															"term": {
																"Frequency": 2.5
															}
														},
														{
															"term": {
																"Frequency": 3.0
															}
														}
													],
												"minimum_should_match": 1
											}
									},
									{
										"bool":
											{
												"should":
													[
														{"match": {"Chemical Name": "Formic Acid"}},
														{"match": {"Chemical Name": "Formyl Chloride"}}
													],
												"minimum_should_match": 1
											}
									}

								]
						}
				}
		}
		output = self.query.parser(input)

		self.assertEqual(output,expected_output)

	def test_parser_single_range(self):
		input = {
			"Frequency": "1.2/2.5,3/5,6/7"
		}
		expected_output = {
			"query":
				{
					"bool":
						{
							"must":
								[
									{
										"bool":
											{
												"should":
													[
														{
															"range":
																{
																	"Frequency":
																		{
																			"gte": 1.2,
																			"lte": 2.5
																		}
																}
														},
														{
															"range":
																{
																	"Frequency":
																		{
																			"gte": 3.0,
																			"lte": 5.0
																		}
																}
														},
														{
															"range":
																{
																	"Frequency":
																		{
																			"gte": 6,
																			"lte": 7
																		}
																}
														}
													],
												"minimum_should_match": 1
											}
									}
								]
						}
				}
		}
		output = self.query.parser(input)

		self.assertEqual(output,expected_output)

	def test_parser_multiple_range_equality(self):
		input = {
			"Frequency": "1584800/1584900,1585000/1585100",
			"Chemical Name": "Formic Acid,Formyl Chloride"
		}
		expected_output = {
			"query": {
				"bool": {
					"must": [
						{
							"bool": {
								"should":
									[
										{
											"range":
												{
													"Frequency":
														{
															"gte": 1584800,
															"lte": 1584900
														}
												}
										},
										{
											"range":
												{
													"Frequency": {
														"gte": 1585000,
														"lte": 1585100
												}
											}
										}
									],
								"minimum_should_match": 1
							}
						},
						{
							"bool": {
								"should": [
									{
										"match": {
											"Chemical Name": "Formic Acid"
										}
									},
									{
										"match": {
											"Chemical Name": "Formyl Chloride"
										}
									}
								],
								"minimum_should_match": 1
							}
						}
					]
				}
			}
		}
		output = self.query.parser(input)

		self.assertEqual(output,expected_output)

	def test_parser_multiple_mix(self):
		input = {
			"Frequency": "1584800/1584900,1585000/1585100,1529943.39901",
			"Chemical Name": "Formic Acid,Formyl Chloride"
		}
		expected_output = {
			"query": {
				"bool": {
					"must": [
						{
							"bool": {
								"should":
									[
										{
											"range":
												{
													"Frequency":
														{
															"gte": 1584800,
															"lte": 1584900
														}
												}
										},
										{
											"range": {
												"Frequency": {
													"gte": 1585000,
													"lte": 1585100
												}
											}
										},
										{
											"term": {
												"Frequency": 1529943.39901
											}
										}
									],
								"minimum_should_match": 1
							}
						},
						{
							"bool": {
								"should": [
									{
										"match": {
											"Chemical Name": "Formic Acid"
										}
									},
									{
										"match": {
											"Chemical Name": "Formyl Chloride"
										}
									}
								],
								"minimum_should_match": 1
							}
						}
					]
				}
			}
		}
		output = self.query.parser(input)

		self.assertEqual(output,expected_output)

	def test_parser_white_list(self):
		input = {
			"Frequency": "1584800/1584900,1585000/1585100,1529943.39901",
			"Chemical Name": "Formic Acid,Formyl Chloride",
			"This is baaad": "this, is, a / try, to ,brake / you"
		}
		expected_output = {
			"query": {
				"bool": {
					"must": [
						{
							"bool": {
								"should":
									[
										{
											"range":
												{
													"Frequency":
														{
															"gte": 1584800,
															"lte": 1584900
														}
												}
										},
										{
											"range": {
												"Frequency": {
													"gte": 1585000,
													"lte": 1585100
												}
											}
										},
										{
											"term": {
												"Frequency": 1529943.39901
											}
										}
									],
								"minimum_should_match": 1
							}
						},
						{
							"bool": {
								"should": [
									{
										"match": {
											"Chemical Name": "Formic Acid"
										}
									},
									{
										"match": {
											"Chemical Name": "Formyl Chloride"
										}
									}
								],
								"minimum_should_match": 1
							}
						}
					]
				}
			}
		}
		output = self.query.parser(input)

		self.assertEqual(output,expected_output)