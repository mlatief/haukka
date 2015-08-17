import unittest
from pyhaukka.converter import convert_xml_to_dict

class XmlToDictTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from fixture import load_sample_trials
        # Load test trials fixtures from xml files
        nct_ids = ['NCT02034110', 'NCT00001160', 'NCT00001163']
        cls.trials = load_sample_trials(nct_ids)

    def test_converter_handle_flat_dict(self):
        xml = '<ct><title>sample trial title</title><purpose>sample trial purpose</purpose></ct>'
        mapping = {'title': './title', 'purpose':'./purpose'}
        d = convert_xml_to_dict(mapping, xml)
        self.assertIsInstance(d, dict)
        self.assertEqual("sample trial title", d.get('title'))
        self.assertEqual("sample trial purpose", d.get('purpose'))

    def test_converter_handle_dict_with_lists(self):
        xml = """<ct>
                 <title>sample trial title</title>
                 <purpose>sample trial purpose</purpose>
                 <location>US</location>
                 <location>EU</location>
                 <condition>Cancer</condition>
                 </ct>"""

        mapping = {'title': './title',
                   'purpose': './purpose',
                   'location': ['./location'],
                   'condition': ['./condition']}

        d = convert_xml_to_dict(mapping, xml)
        self.assertIsInstance(d, dict)

        self.assertIsInstance(d.get('location'), list)
        self.assertEqual(2, len(d.get('location')))
        self.assertEqual('US', d.get('location')[0])
        self.assertEqual('EU', d.get('location')[1])

        self.assertIsInstance(d.get('condition'), list)
        self.assertEqual(len(d.get('condition')), 1)
        self.assertEqual('Cancer', d.get('condition')[0])

    def test_converter_handle_recursive_dict(self):
        xml = """<ct>
                 <title>sample trial title</title>
                 <purpose>sample trial purpose</purpose>
                 <location>US</location>
                 <location>EU</location>
                 <condition>Cancer</condition>
                 </ct>"""

        mapping = {'ct':{'title': './title',
                   'purpose': './purpose',
                   'location': ['./location'],
                   'condition': ['./condition']}}

        d = convert_xml_to_dict(mapping, xml)
        self.assertIsInstance(d, dict)
        self.assertIsInstance(d.get('ct'), dict)
        self.assertEqual("sample trial title", d['ct'].get('title'))
        self.assertEqual("sample trial purpose", d['ct'].get('purpose'))

        self.assertIsInstance(d['ct'].get('location'), list)
        self.assertEqual(2, len(d['ct'].get('location')))
        self.assertEqual('US', d['ct'].get('location')[0])
        self.assertEqual('EU', d['ct'].get('location')[1])

        self.assertIsInstance(d['ct'].get('condition'), list)
        self.assertEqual(len(d['ct'].get('condition')), 1)
        self.assertEqual('Cancer', d['ct'].get('condition')[0])

if __name__ == '__main__':
    unittest.main()
