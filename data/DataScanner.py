import csv
import os
from typing import List, Union, Collection, Sequence


class DataScanner:
    def __init__(self, data_dir: str = "csv"):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.target_dir = os.path.join(self.base_dir, data_dir)

    def get_filenames(self) -> List[str]:
        files = os.listdir(self.target_dir)
        filtered = filter(lambda f: f.endswith(".csv"), files)
        return list(filtered)

    def get_tables(self) -> List[str]:
        return list(map(lambda fn: fn.split(".")[1], self.get_filenames()))

    def get_files_data(
        self,
    ) -> list[list[Sequence[Collection[str]]]]:
        filenames = self.get_filenames()
        data = []
        for filename in filenames:
            filepath = os.path.join(self.target_dir, filename)
            with open(filepath, "r", encoding="UTF-8") as f:
                reader = csv.reader(f)
                header = next(reader)
                table_name = filename.split(".")[1]
                filedata = []
                for row in reader:
                    filedata.append(
                        {
                            header[idx]: self.parse_value(row[idx])
                            for idx in range(len(row))
                        }
                    )
                data.append([table_name, filedata])
        return data

    @staticmethod
    def parse_value(value: str) -> Union[str, int, float]:
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            return value


if __name__ == "__main__":
    print(list(reversed(DataScanner().get_tables())))
