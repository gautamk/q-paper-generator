import gdata.spreadsheet
import gdata.spreadsheet.service
gd_client = gdata.spreadsheet.service.SpreadsheetsService()
feed = gd_client.GetSpreadsheetsFeed()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:   File "gdata/spreadsheet/service.py", line 96, in GetSpreadsheetsFeed
# OUT:     converter=gdata.spreadsheet.SpreadsheetsSpreadsheetsFeedFromString)
# OUT:   File "gdata/service.py", line 1108, in Get
# OUT:     'reason': server_response.reason, 'body': result_body}
# OUT: RequestError: {'status': 404, 'body': '<HTML>\n<HEAD>\n<TITLE>Not Found</TITLE>\n</HEAD>\n<BODY BGCOLOR="#FFFFFF" TEXT="#000000">\n<H1>Not Found</H1>\n<H2>Error 404</H2>\n</BODY>\n</HTML>\n', 'reason': 'Not Found'}
