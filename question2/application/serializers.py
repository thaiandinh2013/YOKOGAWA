class HBaseVisualizationSerializer():
    def serialize(self, key, data):
        product1 = data[b'products:product1'].decode('utf-8')
        product2 = data[b'products:product2'].decode('utf-8')
        row = {'row_key': key.decode('utf-8'), 'product1': product1, 'product2': product2}
        source = 'product1.{}'.format(product1)
        target = 'product2.{}'.format(product2)
        source_node = {'id': source, 'group': 1}
        target_node = {'id': target, 'group': 2}
        link = {'source': source, 'target': target}
        return row, source_node, target_node, link
