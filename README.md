# Module10_Challenge_sqlalchemy-challenge <br>

*************----------Content----------*************<br>
* --Resources Folder - contains source file hawaii.sqlite database and its corresponding csv source files
* --SurfsUp folder - Contains completed analysis
    * climate_starter_completed.ipynb - solved Jupyter Notebook
    * app.py solved python file - API route using FLASK
* Jupyter_KernelSelection_Checklist.pdf - prerequisite checklist for jupyter file
* Python_Checklist.pdf - prerequisite checklist file for python file
* output folder contains JSON response for all 5 API routes along with welcome page
* README.md

*************----------To Execute the Jupyter source file ----------*************<br>

* --Open the climate_starter_completed.ipynb (Jupyter Source File) using Visual studio code
* --Ensure correct Kernell is selected. Please use Jupyter_KernelSelection_Checklist.pdf for detailed steps
* --Ensure required hawaii.sqlite is under Resources folder.
* --Click Run All or Run individual code in sequence it is written. Running the code block in between might throw error as the variables used in that code block might be defined in the prior code block. Hence recommended to Run All to ensure it is run in sequence.

************To Execute app.py python script ***************
  1. Open the app.py using visual Studio Code
  2. Make sure the terminal shows the correct folder path where this app.py is present. if not navigate to that folder. 
   Refer Python_Checklist.pdf for detailed step by step process.
  3. Run the python script and view the output in the browser http://127.0.0.1:5000/ and try out below 5 API routes to view the individual route response
    * /api/v1.0/precipitation - gives precipitation analysis
    * /api/v1.0/stations - gives list of stations
    * /api/v1.0/tobs - gives one year of temperature data for the most active station
    * /api/v1.0/<start_date>   - gives Min,Max,Avg Temperature from the Start date use yyyy-mm-dd date format
    * /api/v1.0/<start>/<end> - gives Min,Max,Avg Temperature for given date range(start/end) use yyyy-mm-dd date format
  All 5 API route JSON response along with welcome page is saved in output folder. Please refer the below pdf<br>
    * API_WelcomePage.pdf
    * API_Precipitation_JSON_Response.pdf
    * API_Stations_JSON_Response.pdf
    * API_TOBs_JSON_Response.pdf
    * DynaminAPI_start_date_JSON_Response.pdf
    * DynaminAPI_start_date_end_date_JSON_Response.pdf

