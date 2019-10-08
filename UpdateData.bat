:: *****************************************************************************
:: UpdateData.bat  8/7/2019 
:: Summary: Tacoma Permit Dashboard Data Update
::
:: Description: Update json/CSV data used for the Tacoma Permit Dashboard App 
::    		@ https://wspdsmap.cityoftacoma.org/website/PDS/PermitDashboard/
::   
:: Scheduled Task: Every day @ 7:00 am (CivicData updated @ 1:30 am)
::
:: Path: \\Geobase-win\CED\GADS\R2019\R032\UpdateData\UpdateData.bat
:: *****************************************************************************

:: Set log directory for process verification file
    SET LogDir=\\Geobase-win\CED\GADS\R2019\R032\UpdateData\log\PermitDashboard

:: Set variable %theDate% to today's date (YYYYMMDD)
    for /f "tokens=2,3,4 delims=/ " %%a in ('date/t') do set theDate=%%c%%a%%b

:: Record starting time
    time /T > %LogDir%%theDate%.log

Echo Archiving current CSV data ... >> %LogDir%%theDate%.log
    COPY \\wsitd01\c$\GADS\website\PDS\PermitDashboard\data\PermitNewApplications30.csv \\wsitd01\c$\GADS\website\PDS\PermitDashboard\data\_archive\PermitNewApplications30_%theDate%.csv
    COPY \\wsitd01\c$\GADS\website\PDS\PermitDashboard\data\PermitIssued30.csv \\wsitd01\c$\GADS\website\PDS\PermitDashboard\data\_archive\PermitIssued30_%theDate%.csv

Echo Downloading data and updating AGO ... >> %LogDir%%theDate%.log
 ::Send standard output (1) & errors (2) to log file
    "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" \\Geobase-win\CED\GADS\R2019\R032\UpdateData\UpdateIssued.py 1>>%LogDir%%theDate%.log 2>&1
    "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" \\Geobase-win\CED\GADS\R2019\R032\UpdateData\UpdateNewApplications.py 1>>%LogDir%%theDate%.log 2>&1

:: Record ending time
    time /T >> %LogDir%%theDate%.log

Echo  See Tacoma Permit Dashboard for latest data - https://wspdsmap.cityoftacoma.org/website/PDS/PermitDashboard/ >> %LogDir%%theDate%.log

::Send Email with log file content
cscript \\geobase-win\ced\GADS\R2019\R032\UpdateData\Send_Email.vbs %LogDir%%theDate%.log

::For manual testing -
::pause
 
