import os
import json
import pyjq
import xmltodict
import sys
import collections

def extract_po_detail(child_po_dir, poa_filename):
    base_po_dir = 'po'
    po_dir = os.path.join(base_po_dir, child_po_dir)
    childs = os.listdir(po_dir)
    json_expr = '.["po:Order"]["cac:AdditionalDocumentReference"]["cbc:ID"] as $po'\
                '|'\
                '.["po:Order"]["cac:SellerSupplierParty"]["cbc:CustomerAssignedAccountID"] as $factory'\
                '|'\
		        '.["po:Order"]["cac:OrderLine"][]'\
                '|'\
		        '{"po": $po, "factory": $factory, "line": .["cac:LineItem"]["cbc:ID"],'\
                '"quantity": .["cac:LineItem"]["cbc:Quantity"]["#text"],'\
                '"unitprice": .["cac:LineItem"]["cac:Price"]["cbc:PriceAmount"]["#text"],'\
                '"totalprice": .["cac:LineItem"]["cbc:LineExtensionAmount"]["#text"],'\
                '"item": .["cac:LineItem"]["cac:Item"]["cbc:BrandName"]}'
    fp = open(poa_filename, 'a')
    
    for child in childs:
        #print(child)
        child_path = os.path.join(po_dir, child)
        #print(child_path)
        if os.path.isfile(child_path):
            file_content = open(child_path).read()
            json_data = json.loads(json.dumps(xmltodict.parse(file_content)))
            results = pyjq.all(json_expr, json_data)
            
            for result in results:
                print(result)
                tmplist = collections.OrderedDict(sorted(result.items()))
                tmpstr = ','.join([v if v != None else 'null' for v in tmplist.values()])
                fp.write(tmpstr + '\n')
                # factory,item,line,po,quantity,totalprice,unitprice
                print(tmpstr)

if __name__ == '__main__':
    poa_filename = 'poa.csv'
    extract_po_detail(sys.argv[1], poa_filename)
