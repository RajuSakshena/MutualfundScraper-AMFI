import json
from pathlib import Path
from datetime import datetime

import pandas as pd


class SIFParser:

    def __init__(self, excel_file):

        self.excel_file = Path(excel_file)

        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

    def clean(self, df):

        df = df.dropna(how="all")

        df = df.dropna(axis=1, how="all")

        df = df.fillna("")

        return df

    def parse(self):

        print("\nReading SIF Workbook...\n")

        workbook = pd.ExcelFile(
            self.excel_file,
            engine="xlrd"
        )

        data = {

            "metadata": {

                "source": "SIF",

                "file": self.excel_file.name,

                "generated_at": datetime.now().isoformat(),

                "sheet_count": len(workbook.sheet_names),

                "sheet_names": workbook.sheet_names

            },

            "sheets": {}

        }

        for sheet in workbook.sheet_names:

            print("Reading :", sheet)

            df = pd.read_excel(

                self.excel_file,

                sheet_name=sheet,

                header=None,

                engine="xlrd"

            )

            df = self.clean(df)

            data["sheets"][sheet] = df.values.tolist()

        workbook.close()

        output = self.output_dir / "sif_monthly_data.json"

        with open(

                output,

                "w",

                encoding="utf-8"

        ) as f:

            json.dump(

                data,

                f,

                indent=4,

                ensure_ascii=False,

                default=str

            )

        print()

        print("JSON Saved :", output)

        return output
