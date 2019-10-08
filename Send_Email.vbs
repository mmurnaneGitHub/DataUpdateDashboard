Dim Arg, FileToBeUsed
Set Arg = WScript.Arguments
'Parameter 1, sent from calling batch file - \\geobase-win\ced\GADS\R2019\R032\UpdateData\UpdateData.bat
FileToBeUsed = Arg(0)
'msgbox "First parameter passed was " & FileToBeUsed

Dim PublicLink, NetworkLink
PublicLink = "https://wspdsmap.cityoftacoma.org/website/PDS/PermitDashboard/"
NetworkLink = "\\Geobase-win\CED\GADS\R2019\R032\UpdateData\UpdateData.bat"

Const ForReading = 1, ForWriting = 2, ForAppending = 8

Dim fso, f, objCDO1
Set fso = CreateObject("Scripting.FileSystemObject")
Set f = fso.OpenTextFile(FileToBeUsed, ForReading)
Set objCDO1 = CreateObject("CDO.Message")

objCDO1.Textbody = "Please review Permit Dashboard Update Report below. " & vbCrLf & vbCrLf _
			& "Today's Log File: " & FileToBeUsed & vbCrLf & vbCrLf _
			& "View updated Permit Dashboard App: " & PublicLink & vbCrLf _
			& "Rerun Permit Dashboard Update Report: " & NetworkLink & vbCrLf _
			& f.ReadAll

f.Close
objCDO1.TO ="mmurnane@cityoftacoma.org"
objCDO1.From = "mmurnane@cityoftacoma.org"
objCDO1.Subject = "Permit Dashboard Update Report"
objCDO1.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/sendusing") = 2 
objCDO1.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/smtpserver") = "smtp001.tacoma.lcl"
objCDO1.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/smtpserverport") = 25 
objCDO1.Configuration.Fields.Update     
objCDO1.Send

'Clear the objects
Set Arg = Nothing
Set f = Nothing
Set fso = Nothing