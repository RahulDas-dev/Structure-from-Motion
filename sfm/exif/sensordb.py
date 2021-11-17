"""Modules Desines Sensor DB Management.""""



import os
import csv
from typing import ClassVar, Union, List, Tuple, Optional

class SensorDB(object):

    __db_path: ClassVar[str] = os.path.abspath('./sensordb.csv')

    @classmethod
    def validate_db_path(cls) -> bool:
        if os.path.isfile(cls.__db_path) is not True:
            raise FileNotFoundError(f'Path {cls.__db_path} is not Valid')
        return True

    @classmethod
    def set_db_path(cls, dbpath: str):
        if os.path.isfile(dbpath) is not True:
            raise FileNotFoundError(f'Path {dbpath} is not Valid')
        else:
            cls.__db_path = dbpath

    def search_db(self, query: Union[Tuple[str], List[Tuple[str]]]) -> Optional[Union[Tuple[str], List[Tuple[str]]]]:
        if isinstance(query, list) is False:
            query = [query]
        query_lowercase = list(map(lambda x: x.lower(), query))
        db_data=[]
        with open(self.__db_path, 'r') as db_obj:
            csv_reader = csv.reader(db_obj, delimiter=';')
            for row in csv_reader:
                db_data.append((str(row[0]).lower(), float(row[1])))
        return list(filter(lambda x: x[0] in query_lowercase, db_data))
