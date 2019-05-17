from _common.utility import Utility


class CreateData():
    def __init__(self):
        self._data = Utility.GetData()

    def create_data_form_excel(self, excel_path, rows):
        Utility.ExcelHandle().write_to_excel(excel_path, rows)


if __name__ == '__main__':
    t = CreateData()
    excel_path = '/Users/linkinpark/Desktop/creditcarddata'
    t.create_data_form_excel(excel_path, 4)
