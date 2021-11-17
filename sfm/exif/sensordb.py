"""Modules Desines Sensor DB Management."""


import csv
import os
from functools import lru_cache
from typing import ClassVar, List, Optional, Tuple, Union


class SensorDB(object):
    """Sensordb Primaryly Load the  'sensordb.txt' file and Search the File to return sendor width."""

    __db_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "./sensordb.txt"
    )

    @classmethod
    def validate_db_path(cls) -> bool:
        """Class method to validate the db path."""
        if os.path.isfile(cls.__db_path) is not True:
            raise FileNotFoundError(f"Path {cls.__db_path} is not Valid")
        return True

    @classmethod
    def set_db_path(cls, dbpath: str):
        """Reset the DB path."""
        if os.path.isfile(dbpath) is not True:
            raise FileNotFoundError(f"Path {dbpath} is not Valid")
        else:
            cls.__db_path = dbpath

    @staticmethod
    def format_query(query: Union[Tuple[str], List[Tuple[str]]]) -> List[str]:
        """Converts query string to List , removes dulicate, then changes to lowercase."""
        if isinstance(query, list) is False:
            queryList = [query]
        else:
            queryList = list(set(query.copy()))
        return list(map(lambda x: x.lower(), queryList))

    @staticmethod
    def format_result_to_original_case(query, result_in_lower_case):
        """Convert the result back to original case."""
        if isinstance(query, list) is False:
            queryList = [query]
        else:
            queryList = query.copy()
        result_list = []
        for item in queryList:
            result_dim = list(
                filter(lambda x: x[0] == item.lower(), result_in_lower_case)
            )
            if len(result_dim) > 0:
                result_list.append((item, result_dim[0][1]))
            else:
                result_list.append((item, None))
        return result_list

    def get_sersor_dimension(
        self, query: Union[str, List[str]]
    ) -> Optional[list[Tuple[str, float]]]:
        query_lowercase = SensorDB.format_query(query)
        db_data = []
        with open(self.__db_path, "r") as db_obj:
            csv_reader = csv.reader(db_obj, delimiter=";")
            for row in csv_reader:
                db_data.append((str(row[0]).lower(), float(row[1])))
        result_in_lower_case = list(filter(lambda x: x[0] in query_lowercase, db_data))
        if len(result_in_lower_case) == 0:
            return None
        else:
            return SensorDB.format_result_to_original_case(query, result_in_lower_case)
