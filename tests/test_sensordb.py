"""Unittesting for SensorDb class."""


import unittest

from sfm.exif.sensordb import SensorDB


class TestSensorDB(unittest.TestCase):
    def test_search_db_with_singel_item(self):
        """Unit Testing get_sersor_dimension."""
        sensordb = SensorDB()
        query = [("Xiaomi Redmi 3S 32GB", 4.69)]
        result = sensordb.get_sersor_dimension(query[0][0])
        self.assertListEqual(result, query)
        self.assertEqual(result[0][1], 4.69)

    def test_search_db_with_singel_list(self):
        """Unit Testing get_sersor_dimension for list of item."""
        sensordb = SensorDB()
        items = [("Xiaomi Redmi 3S 32GB", 4.69), ("AgfaPhoto Compact 103", 6.08), ("Acer CR-6530", 7.11)]
        query_list = list(map(lambda x: x[0], items))
        result = sensordb.get_sersor_dimension(query_list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][1], 4.69)
        self.assertEqual(result[1][1], 7.11)
        self.assertEqual(result[2][1], 7.11)
        self.assertListEqual(result, items)

    def test_search_db_with_singel_list(self):
        """Unit Testing get_sersor_dimension for non existance item."""
        sensordb = SensorDB()
        query = [("Loose yourself", 4.69)]
        result = sensordb.get_sersor_dimension(query[0][0])
        self.assertIsNone(result)

    def test_search_db_with_singel_list(self):
        """Unit Testing get_sersor_dimension for list of item + non existance item."""
        sensordb = SensorDB()
        items = [("Xiaomi Redmi 3S 32GB", 4.69), ("Loose yourself", 6.08), ("Acer CR-6530", 7.11)]
        query_list = list(map(lambda x: x[0], items))
        result = sensordb.get_sersor_dimension(query_list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][1], 4.69)
        self.assertEqual(result[1][1], None)
        self.assertEqual(result[2][1], 7.11)


if __name__ == "__main__":
    unittest.main()
