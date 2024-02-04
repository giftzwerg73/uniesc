# Autogenerated file
def render(infolist):
    yield """<!DOCTYPE html>
<html lang=\"en\" dir=\"ltr\">
 
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <meta name=\"author\" content=\"MS\">
  <meta name=\"description\" content=\"Universal ESC Programmer\">
  <title>ESCProg</title>
  <link rel=\"stylesheet\" href=\"static/index.css\">
</head>
 
<body>
 
<table class=\"outline\">
  <tr>
	<td colspan=\"4\"> 
		<select onchange=\"mkdisp()\" class=\"sel\" id=\"escname\">
		  <option value=\"None\"> None </option>
		  """
    for info in infolist:
        yield """            <option value="""
        yield str(info)
        yield """> """
        yield str(info)
        yield """ </option>
          """
    yield """	    </select> </td>
  </tr>
  <tr>
	<!-- <td colspan=\"2\"> <textarea class=\"nr-box\" id=\"nri\" rows=\"1\" disabled > </textarea> </td> -->
	<!-- <td colspan=\"2\"> <textarea class=\"nr-box\" id=\"nrv\" rows=\"1\" disabled > </textarea> </td> -->
	<td colspan=\"2\"> <input type=\"text\" class=\"nr-box\" id=\"nri\" disabled> </td>
	<td colspan=\"2\"> <input type=\"text\" class=\"nr-box\" id=\"nrv\" disabled> </td>
  </tr>
  <tr>
    <td colspan=\"2\"> <textarea class=\"text-box\" id=\"txti\" rows=\"2\" disabled > </textarea> </td>
    <td colspan=\"2\"> <textarea class=\"text-box\" id=\"txtv\" rows=\"2\" disabled > </textarea> </td>
  </tr>
  <tr>
	<td colspan=\"1\"> <input type=\"button\" value=\"Item--\" onclick=\"dec_item()\" /> </td>
    <td colspan=\"1\"> <input type=\"button\" value=\"Item++\" onclick=\"inc_item()\" /> </td>
    <td colspan=\"1\"> <input type=\"button\" value=\"Value--\" onclick=\"dec_val()\" /> </td>
    <td colspan=\"1\"> <input type=\"button\" value=\"Value++\" onclick=\"inc_val()\" /> </td>
  </tr>
  <tr>
    <td colspan=\"2\"> <input type=\"button\" value=\"Save\" onclick=\"save()\" /> </td>
    <td colspan=\"2\"> <input type=\"button\" value=\"Reset\" onclick=\"reset()\" /> </td>
  </tr>
  <tr>
    <td colspan=\"4\"> <input type=\"text\" class=\"info-box\" id=\"info\" disabled> </td>
  </tr>
</table>
 
<script type=\"text/javascript\" src=\"static/index.js\"></script>
 
</body>
 
</html>
"""
