REM 01 is the subject number
python 04a_AcquisitionCurve_PreSpeed.py 01

REM Use whichever program you want to run here
python ./04_tasks_retention/04_Retention_Detect_Letters.py 01

python 04b_AcquisitionCurve_PostSpeed_1.py 01

REM Use whichever program you want to run here
python ./04_tasks_retention/04_Retention_Detect_Digits.py 01

python 04c_AcquisitionCurve_PostSpeed_2.py 01

pause

