Read Me

Lab Sweet is a web app for laboratory sample management. 
There are two parts to the web app. The first is the customer part, which allows customers to register samples and assign the attributes they would like their samples to be tested for. Customers can also view their samples and check for results.
The second part of the app is the sample management part, which allows the laboratory staff to create worklists from tests the customers have registered, download the worklists as a csv template, and then use the template to upload the results.

Explanation of models

Attribute
In this project I have chosen a few chemical compounds that are found in honey as the attributes, but they could be anything that a lab tests a sample for, such as chemical compounds, micro organisms or physical properties.
Multiple attributes can be assigned to each sample, and in the sample submission form, multiple checkboxes can be ticked to select the desired attributes.

Sample
A sample represents the physical sample that will be sent to the lab to be tested. Each sample should be registered with a sample ID and a batch number. There can be multiple samples in a batch. The customers will refer to the sample ID when looking for their results, but the lab will refer to the actual unique ID field in the database to ensure they are using a unique value, as multiple samples could be registered as a 'sample 1' for example.

Job
Multiple samples can be registered at one time using the sample submission form. Each submission is assigned a 'job number'. Therefore, multiple samples can be assigned the same job number. To ensure each submission is assinged a unique job number, the job numbers increment from 1, and are prefixed by the current year. Customers can also use the job number to refer back to their sample submissions.

Test
A test represents an instance of a test for a particular attribute. A test requires an attribute, a sample ID and a batch number.

Worklist
A worklist can be generated for all the tests of a particular attribute that currently have no results. It is useful to assign a worklist number to a group of tests, as this is how tests are grouped in the lab - all the samples that need to be tested for a particular attribute will be run together.

Part 1 - Sample submission and viewing results



Part 2 - Sample Management
The sample management page is visible to users with staff permissions, and allows lab staff to generate worklists of outstanding tests and download it as a csv template. The template can then be populated with results, and uploaded in order to save each result in the database. Two tables are displayed on this page:

Outstanding Work
The outstanding work table is table of all the tests, grouped by attribute, that have not yet been assigned a worklist. Clicking on a row will generate a worklist number and assign it to all of the outstanding tests of that attribute. The created worklist will then appear in the Worklists table.

Worklists table
The worklist table displays the created worklists. Each row displays the worklist number, the attribute of each test, and the number of tests in the worklist.The buttons below the table are used to toggle between 'outstanding' and 'complete' worklists. A worklist is considered outstanding if it contains tests without results, and complete if results are present for all tests. 
Clicking on a worklist from this table will display the worklist details table, which displays the sample details for each test in the worklist and any available results. Below this table is a button which allows the worklist to be downloaded as a csv file. To avoid duplicate files being created if the same worklist is downloaded multiple times, the function will check if the file already exists before creating it.

Upload results
Staff also have access to the 'upload results' page. This allows the lab staff to upload results using a worklist csv template downloaded from the sample management page. In a real environment, allowing for file uploads may introduce some extra security considerations that haven't been explored in this project.
