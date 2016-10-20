from flask import current_app as app
import happybase
from io import TextIOWrapper
import csv
from . import serializers

class HBaseService():
    def __init__(self):
        self.connection = happybase.Connection(app.config['HBASE_HOST'], app.config['HBASE_PORT'])
    def retrieve_data(self): 
        table = self.connection.table('data')
        result = dict(rows=[], nodes=[], links=[])
        serializer = serializers.HBaseVisualizationSerializer()
        for key, data in table.scan():
            row, source_node, target_node, link = serializer.serialize(key, data)
            result['rows'].append(row)
            if source_node not in result['nodes']:
                result['nodes'].append(source_node)
            if target_node not in result['nodes']:
                result['nodes'].append(target_node)
            result['links'].append(link)
        return result

    def flush_data(self):
        self.connection.delete_table('data', True)
        self.connection.create_table('data', { 'products': dict() })
    
    def put_data_from_line(self, row, line):
        table = self.connection.table('data')
        table.put(str(row), {'products:product1': line[0], 'products:product2': line[1]})

class DataService():
    def import_from_file(self, file):
        hbase = HBaseService()
        hbase.flush_data()
        f = TextIOWrapper(file, encoding='utf-8')
        reader = csv.reader(f, delimiter=',', quotechar='|')
        next(reader, None)
        i = 1
        for line in reader:
            hbase.put_data_from_line(i, line)
            i += 1
