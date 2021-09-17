import json
import PyQt5

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from ui import Ui_MainWindow

# to convert ui type "pyuic5 v2.ui -o ui.py -x"
result = {
    "import_file":{
        "encoded":"NONE",
        "delimiter":",",
        "columns":[]
    },
    "transformations":[],
    "validations":[],
    "mapping":{
        "part_number":"",
        "manufacturer":"",
        "description":"",
        "make":"",
        "model":"",
        "year":"",
        "engine":"",
        "trim":"" }
    }


class JsonMaker (QtWidgets.QMainWindow):
    def __init__(self):
        super(JsonMaker, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('JSON Maker v.0.9.b')
        self.setWindowIcon(QIcon('img/arrow.png'))
        # Mandatory fields
        self.ui.inp_pnumber.setPlaceholderText('Part Number')
        self.ui.inp_manufact.setPlaceholderText('Part Manufacturer')
        self.ui.inp_descr.setPlaceholderText('Part Description')
        self.ui.inp_year.setPlaceholderText('Vehicle Year')
        self.ui.inp_make.setPlaceholderText('Vehicle Maker')
        self.ui.inp_model.setPlaceholderText('Vehicle Model')
        self.ui.inp_trim.setPlaceholderText('Vehicle Trim')
        # Optional fields
        self.ui.inp_category.setPlaceholderText('Part Category')
        self.ui.inp_barcode.setPlaceholderText('Barcode')
        self.ui.inp_barcodetype.setPlaceholderText('Barcode Type')
        self.ui.inp_spec.setPlaceholderText('Part Specs')
        self.ui.inp_webpage.setPlaceholderText('Webpage Link')
        self.ui.inp_imglink.setPlaceholderText('Link to Image')
        self.ui.inp_width.setPlaceholderText('Width')
        self.ui.inp_length.setPlaceholderText('Length')
        self.ui.inp_height.setPlaceholderText('Height')
        self.ui.inp_warranty.setPlaceholderText('Warranty')
        self.ui.inp_weight.setPlaceholderText('Weight Value')
        self.ui.inp_weightuom.setPlaceholderText('Weight UOM')
        self.ui.inp_notes.setPlaceholderText('Notes')
        self.ui.inp_engine.setPlaceholderText('Engine')

        self.ui.inp_compatib.setPlaceholderText('This option not available')
        self.ui.inp_compatib.setDisabled(True) # fields is temporary disabled
        self.ui.btn_copy.setDisabled(True)
        self.ui.btn_copy.setStyleSheet("QPushButton " "{background: white;" "color: grey;" "border: 1px solid grey;" "border-radius: 5px;" "}")
        # buttons actions
        self.ui.generate.clicked.connect(self.generate)
        self.ui.btn_copy.clicked.connect(self.to_clipboard)

    def generate(self):
        self.receive_data()
        if (self.check_required_fields()):
            self.output = json.dumps(result)
        else:
            self.output = "Fill all required fields!"
        if self.ui.output_text.textChanged and (self.ui.output_text != "Fill all required fields!"):
            self.ui.btn_copy.setDisabled(False)
            self.ui.btn_copy.setStyleSheet(
                "QPushButton {" "background: white;" "color: black;" "border: 1px solid black;" "border-radius: 5px;" "}")
        self.ui.output_text.setText(self.output)

    def receive_data(self):
        inp = {}
        inp["part_number"] = self.ui.inp_pnumber.text()
        inp["manufacturer"] = self.ui.inp_manufact.text()
        inp["category"] = self.ui.inp_category.text()
        inp["barcode_type"] = self.ui.inp_barcodetype.text()
        inp["barcode"] = self.ui.inp_barcode.text()
        inp["description"] = self.ui.inp_descr.text()
        inp["specification"] = self.ui.inp_spec.text()
        inp["warranty"] = self.ui.inp_warranty.text()
        inp["link_image"] = self.ui.inp_imglink.text()
        inp["link_webpage"] = self.ui.inp_webpage.text()
        inp["dimension_height"] = self.ui.inp_height.text()
        inp["dimension_width"] = self.ui.inp_width.text()
        inp["dimension_length"] = self.ui.inp_length.text()
        # inp["size_uom"] = self.ui.inp_.text()
        inp["weight"] = self.ui.inp_weight.text()
        inp["weight_uom"] = self.ui.inp_weightuom.text()
        # inp["qty_min"] = self.ui.inp_.text()
        inp["make"] = self.ui.inp_make.text()
        inp["model"] = self.ui.inp_model.text()
        inp["year"] = self.ui.inp_year.text()
        inp["engine"] = self.ui.inp_engine.text()
        inp["trim"] = self.ui.inp_trim.text()
        inp["notes"] = self.ui.inp_notes.text()
        compatibility =  inp["year"] + inp["make"] + inp["model"] + inp["model"]
        res = {}
        col = []
        # item = {"id": ""}
        for i in inp.keys():
            if not (inp[i] == ''):
                res[i] = inp[i]
                item = {"id": inp[i]}
                col.append(item)
        result["mapping"] = res
        result["import_file"]["columns"] = col
        result["import_file"]["delimiter"] = (self.ui.delimiter.currentText()).split("'")[1]

    def check_required_fields(self):
        return bool((bool(self.ui.inp_pnumber.text() != "")
                 * bool(self.ui.inp_manufact.text() != "")
                 * bool(self.ui.inp_descr.text() != "")
                 * bool(self.ui.inp_make.text() != "")
                 * bool(self.ui.inp_model.text() != "")
                 * bool(self.ui.inp_year.text() != "")))

    def to_clipboard(self):
        self.clipboard = QtWidgets.QApplication.clipboard()
        self.clipboard.setText(self.output)
        with open('mapping.json', 'w') as save:
            print(self.clipboard.text(), file=save)
        print('copied and saved to the "mapping.json" file ')


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = JsonMaker()
    window.show()
    sys.exit(app.exec())
