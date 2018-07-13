import unittest

from nerd.nerd import NerdClient


class NerdTest(unittest.TestCase):

    def setUp(self):
        self.target = NerdClient()

    def testDisambiguateText_longText(self):
        result = self.target.disambiguateText("We introduce in this paper D-SPACES, an implementation of constraint "
                                              "systems with space and extrusion operators. Constraint systems are "
                                              "algebraic models that allow for a semantic language-like "
                                              "representation of information in systems where the concept of space is "
                                              "a primary structural feature. We give this information mainly an "
                                              "epistemic interpretation and consider various agents as entities "
                                              "acting upon it. D-SPACES is coded as a c++11 library providing "
                                              "implementations for constraint systems, space functions and extrusion "
                                              "functions. The interfaces to access each implementation are minimal "
                                              "and thoroughly documented. D-SPACES also provides property-checking "
                                              "methods as well as an implementation of a specific type of constraint "
                                              "systems (a boolean algebra). This last implementation serves as an "
                                              "entry point for quick access and proof of concept when using these "
                                              "models. Furthermore, we offer an illustrative example in the form of a "
                                              "small social network where users post their beliefs and utter their "
                                              "opinions ")
        assert result is not None or ""
        assert result[1] is 200
        # assert len(result[0]['sentence']) is 2
        assert result[0]['language']['lang'] == "en"

    def testDisambiguateText_shortText(self):
        result = self.target.disambiguateText("This text is ")
        assert result is not None
        assert result[1] is 200

    def testProcessQuery_prepared_simpleText(self):
        query = {'text': "This is a simple text"}
        result = self.target._process_query(query, True)
        assert result is not None
        assert result[1] is 200

    def testProcessQuery_shortText(self):
        query = {'text': "This is a simple text"}
        result = self.target._process_query(query)
        assert result is not None

    def testProcessQuery_longText(self):
        query = {"text": "We introduce in this paper D-SPACES, an implementation of constraint "
                         "systems with space and extrusion operators. Constraint systems are "
                         "algebraic models that allow for a semantic language-like "
                         "representation of information in systems where the concept of space is "
                         "a primary structural feature. We give this information mainly an "
                         "epistemic interpretation and consider various agents as entities "
                         "acting upon it. D-SPACES is coded as a c++11 library providing "
                         "implementations for constraint systems, space functions and extrusion "
                         "functions. The interfaces to access each implementation are minimal "
                         "and thoroughly documented. D-SPACES also provides property-checking "
                         "methods as well as an implementation of a specific type of constraint "
                         "systems (a boolean algebra). This last implementation serves as an "
                         "entry point for quick access and proof of concept when using these "
                         "models. Furthermore, we offer an illustrative example in the form of a "
                         "small social network where users post their beliefs and utter their "
                         "opinions. "
                         "We introduce in this paper D-SPACES, an implementation of constraint "
                         "systems with space and extrusion operators. Constraint systems are "
                         "algebraic models that allow for a semantic language-like "
                         "representation of information in systems where the concept of space is "
                         "a primary structural feature. We give this information mainly an "
                         "epistemic interpretation and consider various agents as entities "
                         "acting upon it. D-SPACES is coded as a c++11 library providing "
                         "implementations for constraint systems, space functions and extrusion "
                         "functions. The interfaces to access each implementation are minimal "
                         "and thoroughly documented. D-SPACES also provides property-checking "
                         "methods as well as an implementation of a specific type of constraint "
                         "systems (a boolean algebra). This last implementation serves as an "
                         "entry point for quick access and proof of concept when using these "
                         "models. Furthermore, we offer an illustrative example in the form of a "
                         "small social network where users post their beliefs and utter their "
                         "opinions. "
                         "We introduce in this paper D-SPACES, an implementation of constraint "
                         "systems with space and extrusion operators. Constraint systems are "
                         "algebraic models that allow for a semantic language-like "
                         "representation of information in systems where the concept of space is "
                         "a primary structural feature. We give this information mainly an "
                         "epistemic interpretation and consider various agents as entities "
                         "acting upon it. D-SPACES is coded as a c++11 library providing "
                         "implementations for constraint systems, space functions and extrusion "
                         "functions. The interfaces to access each implementation are minimal "
                         "and thoroughly documented. D-SPACES also provides property-checking "
                         "methods as well as an implementation of a specific type of constraint "
                         "systems (a boolean algebra). This last implementation serves as an "
                         "entry point for quick access and proof of concept when using these "
                         "models. Furthermore, we offer an illustrative example in the form of a "
                         "small social network where users post their beliefs and utter their "
                         "opinions. "
                         }

        result = self.target._process_query(query)
        assert result is not None


    def testGetConceptWikidata(self):
        result = self.target.get_concept('Q142')
        assert result is not None
        assert result[1] is 200


    def testGetConceptWikipedia(self):
        result = self.target.get_concept('195', 'fr')
        assert result is not None
        assert result[1] is 200


if __name__ == '__main__':
    unittest.main()
