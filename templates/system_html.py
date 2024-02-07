# Autogenerated file
def render(*a, **d):
    yield """<!DOCTYPE html>
<html>
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <meta name=\"author\" content=\"MS\">
  <meta name=\"description\" content=\"Universal ESC Programmer\">
  <title>ESCProg</title>
  <link rel=\"stylesheet\" href=\"static/system.css\">
</head>

<script>
    function toggleField(hideObj,showObj)"""
    yield """{
      hideObj.disabled=true;        
      hideObj.style.display='none';
      showObj.disabled=false;   
      showObj.style.display='inline';
      showObj.focus();
    }
</script>

<body>
	
<div class=\"wrapper\"> 
    <div class=\"one\">
       <label class=\"label\" for=\"selectssid\">Select SSID from List:</label>
       <select class=\"sel\" name=\"selectssid\" id=\"selectssid\"
            onchange=\"if(this.options[this.selectedIndex].value=='customOption')"""
    yield """{
              toggleField(this,this.nextSibling);
              this.selectedIndex='0';
            }\">
            <option></option>
            <option value=\"customOption\">Enter custom SSID</option>
       </select>
       <input class=\"sel\" name=\"customssid\" id=\"customssid\" style=\"display:none;\" disabled=\"disabled\" 
            onblur=\"if(this.value=='')"""
    yield """{toggleField(this,this.previousSibling);}\">
    </div>       
    <div class=\"two\">   
       <label class=\"label\" for=\"pw\">Enter Password:</label>
       <input class=\"sel\" name=\"pw\" id=\"pw\">
    </div>
    <div class=\"three\">     
        <input type=\"button\" value=\"Del\" id=\"wifibtn\" onclick=\"fnbtnremove()\" />
    </div>   
    <div class=\"four\">  
        <input type=\"button\" value=\"Scan\" id=\"wifibtn\" onclick=\"fnbtnscan()\" />
    </div>  
    <div class=\"five\">  
        <input type=\"button\" value=\"Add\" id=\"wifibtn\" onclick=\"fnbtnsave()\" />
    </div>
    <div class=\"six\" >
		<label class=\"label\" for=\"updatebtn\"><br></label>
        <input type=\"button\" value=\"Update\" id=\"updatebtn\" onclick=\"fnbtnota()\" />
    </div>
    <div class=\"seven\">
		<label class=\"label\" for=\"info\"><br></label>
	    <input type=\"text\" class=\"info-box\" id=\"info\" disabled>
    </div>
</div>

<script src=\"static/system.js\"></script>

</body>

</html>
"""
