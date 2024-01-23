import xml.etree.ElementTree as ET
from django.http import HttpResponse


class ProcessPaymentData:
    def generate_error_response(self, error_code, error_description):
        response_root = ET.Element("COMMAND")
        respomse_type = ET.SubElement(response_root, 'TYPE')
        respomse_type.text = 'SYNC_BILLPAY_RESPONSE'
        response_error_code = ET.SubElement(response_root, 'ERRORCODE')
        response_error_code.text = error_code
        response_error_description = ET.SubElement(response_root, 'ERRORDESCRIPTION')
        response_error_description.text = error_description

        response_data = ET.tostring(response_root, encoding='utf-8', method='xml')
        return response_data


    def process(self, request_data):
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
        msisdn = root.findtext('MSISDN')
        amount = root.findtext('AMOUNT')
        company_name = root.findtext('COMPANYNAME')
        customer_reference_id = root.findtext('CUSTOMERREFERENCEID')
        sender_name = root.findtext('SENDERNAME')






