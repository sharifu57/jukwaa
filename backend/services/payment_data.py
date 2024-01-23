import xml.etree.ElementTree as ET
from django.http import HttpResponse


class ProcessPaymentData:
    def generate_error_response(self, error_code, error_description):
        response_root = ET.Element("COMMAND")
        response_type = ET.SubElement(response_root, 'TYPE')
        response_type.text = 'SYNC_BILLPAY_RESPONSE'
        response_error_code = ET.SubElement(response_root, 'ERRORCODE')
        response_error_code.text = error_code
        response_error_description = ET.SubElement(response_root, 'ERRORDESCRIPTION')
        response_error_description.text = error_description

        response_data = ET.tostring(response_root, encoding='utf-8', method='xml')
        return response_data

    def generate_sync_billpay_response(self, txn_id):
        response_root = ET.Element('COMMAND')
        response_type = ET.SubElement(response_root, 'TYPE')
        response_type.text = 'SYNC_BILLPAY_RESPONSE'
        response_txn_id = ET.SubElement(response_root, 'TXNID')
        response_txn_id.text = txn_id
        response_ref_id = ET.SubElement(response_root, 'REFID')
        response_ref_id.text = '000217605331'
        response_result = ET.SubElement(response_root, 'RESULT')
        response_result.text = 'TS'
        response_error_code = ET.SubElement(response_root, 'ERRORCODE')
        response_error_code.text = 'error000'
        response_msisdn = ET.SubElement(response_root, 'MSISDN')
        response_msisdn.text = '0714405395'
        response_flag = ET.SubElement(response_root, 'FLAG')
        response_flag.text = 'Y'
        response_content = ET.SubElement(response_root, 'CONTENT')
        response_content.text = 'SUCCESS'

        # Convert the XML response to a string
        response_data = ET.tostring(response_root, encoding='utf-8', method='xml')

        return response_data



    def sync_billpay(self, request_data):
        TYPE = None
        TXNID = None
        MSISDN = None
        AMOUNT = None
        COMPANYNAME = None
        CUSTOMERREFERENCEID = None
        SENDERNAME = None

        xml_request_data = request_data.body.decode('utf-8')

        try:
            root = ET.fromstring(xml_request_data)

        except ET.ParseError as e:
            error_response = ProcessPaymentData().generate_error_response("error100", "General Error")
            return HttpResponse(error_response, content_type="text/xml", status=400)

        type = root.findtext('type')
        txn_id = root.findtext('TXNID')

        print("=================txnId", txn_id)
        msisdn = root.findtext('MSISDN')
        amount = root.findtext('AMOUNT')
        company_name = root.findtext('COMPANYNAME')
        customer_reference_id = root.findtext('CUSTOMERREFERENCEID')
        sender_name = root.findtext('SENDERNAME')

        response_data = ProcessPaymentData().generate_sync_billpay_response(txn_id)
        return HttpResponse(response_data, content_type='text/xml')






