set /p subject= Subject_ID:

python 04a_AcquisitionCurve_PreSpeed.py %subject%

REM Use whichever program you want to run here
python ./04_tasks_retention/04_Retention_Detect_Letters.py %subject% 

python 04b_AcquisitionCurve_PostSpeed_1.py %subject%

REM Use whichever program you want to run here
python ./04_tasks_retention/04_Retention_Detect_Digits.py %subject% 

python 04c_AcquisitionCurve_PostSpeed_2.py %subject%

pause

