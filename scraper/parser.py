import json
from pathlib import Path
from datetime import datetime

import pandas as pd


class AMFIParser:

    def __init__(self, excel_file):

        self.excel_file = Path(excel_file)

        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

    def clean_dataframe(self, df):

        # Remove fully empty rows
        df = df.dropna(how="all")

        # Remove fully empty columns
        df = df.dropna(axis=1, how="all")

        # Replace NaN
        df = df.fillna("")

        return df

    def parse(self):

        print("\n" + "=" * 60)
        print("Reading Workbook")
        print("=" * 60)

        # Detect engine automatically
        if self.excel_file.suffix.lower() == ".xls":
            engine = "xlrd"
        else:
            engine = "openpyxl"

        workbook = pd.ExcelFile(
            self.excel_file,
            engine=engine
        )

        output = {
            "metadata": {
                "source": "AMFI",
                "file_name": self.excel_file.name,
                "generated_at": datetime.now().isoformat(),
                "sheet_count": len(workbook.sheet_names),
                "sheet_names": workbook.sheet_names
            },
            "sheets": {}
        }

        for sheet in workbook.sheet_names:

            print(f"Reading : {sheet}")

            df = pd.read_excel(
                self.excel_file,
                sheet_name=sheet,
                header=None,
                engine=engine
            )

            df = self.clean_dataframe(df)

            output["sheets"][sheet] = df.values.tolist()

        workbook.close()

        json_path = self.output_dir / "amfi_monthly_data.json"

        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                output,
                f,
                indent=4,
                ensure_ascii=False,
                default=str
            )

        print("\nJSON Saved :", json_path)

        return json_path