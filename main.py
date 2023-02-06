from reader.recordreader import RecordReader
import sys

recordReader = RecordReader()

file_path = sys.argv[1]
try:
    record_boolean = sys.argv[2]
except:
    record_boolean = False # default
    
recordReader.set_record_result(record_boolean)
recordReader.load_file(file_path)
#recordReader.display_file_content()
recordReader.crypto_com_scan()
print(recordReader.get_proceeds())