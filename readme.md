# Lab Sweet

## Distinctiveness and Complexity
This web application is distinct from all of the other projects in this course, as it is not related to social networking, email or e-commerce. It is a LIMS (Laboratory Information Management System) application, consisting of two parts. The first allows customers to register samples to the lab and assign the attributes they would like their samples to be tested for. The customers can also view their samples and check for results. The second part of the app is used by the laboratory staff for sample management. Staff can create worklists from tests the customers have registered, download the worklists as a csv template, and then use the template to upload the results. 
Allowing for the downloading and uploading of of files is a function not explored in previous projects and adds functionality and complexity to the project.
My experience with LIMS systems and how they are used in a real working environment helped me to deal with the complexity of how all the models are related to each other and how they represent real world samples and processes. On the customer side there are jobs containing multiple samples, which can have multiple tests, each of a particular attribute. On the staff side there are worklists containing multiple tests of a particular attribute, each associated with a sample.

The only additional python package used is the Django REST framework, which offers a good way of returning JSON. It was useful for making serializers for each model, to allow querysets to be converted into JSON. These are found in 'serializers.py'. It also displays the data nicely when accessing an API in the browser.


## Explanation of models
### Attribute
In this project I have chosen a few chemical compounds that are found in honey as the attributes, but they could be anything that a lab tests a sample for, such as chemical compounds, micro organisms or physical properties. The attribute model consists of a long name, an abbreviated name, and the units used to measure the attribute. An attribute is always used with the Test model, with a test representing a test for a particular attribute. A sample can be tested for multiple attributes. The model has a 'create_table' function, which will create the database table of attributes if it doesn't exist.
A migration file was created in order to initially populate the attribute table with each attribute. This allows the table to be set up automatically when the database is first created with the 'migrate' command.

### Sample
A sample represents the physical sample that will be sent to the lab to be tested. Each sample requires a sample ID and a batch number. There can be multiple samples in a batch. The customers will refer to the sample ID when looking for their results, but the lab will refer to the actual unique ID field in the database to ensure they are using a unique value, as multiple samples could be registered as a 'sample 1' for example. The sample model has a 'complete' field. A sample is complete if all of its tests have results.

### Job
Multiple samples can be registered at one time using the sample submission form. Each submission is assigned a 'job number'. Therefore, multiple samples can be assigned the same job number. The model has a 'create' function, that will generate a unique job number and assign it to each submission. The numbers increment from 1, and are prefixed by the current year. Customers can also use the job number to refer back to their sample submissions. The job model has a 'complete' field. A job is complete when all of its samples are complete.

### Test
A test represents an instance of a test for a particular attribute. A test requires an attribute, a sample ID and a batch number.

### Worklist
A worklist can be generated for all the tests of a particular attribute that currently have no results. It is useful for the lab to group the tests this way, as they will typically test a large number of samples for the same attribute at one time.


## Using the website
### Part 1 - Sample submission and viewing results
#### Sample Submission 
This page consists of a form, where a customer can submit one or more samples for testing, and choose one or more attributes to be tested for each sample, using the checkboxes. Extra rows can be added or deleted. When samples are submitted, a job number is created and assigned to the samples.

#### Viewing samples and jobs
There are links on the navbar to view samples and jobs in a table. The links are dropdowns, where 'all', 'outstanding' and 'complete' can be selected. When the 'get_samples' and 'get_jobs' functions are called to build the sample and jobs tables, the 'check_complete' functions are called to update the status of samples/jobs before filtering the data that is returned. There are also search boxes that allow the for samples to be searched by sample ID or job number.
Staff can view all submitted jobs and samples, and regular users can only see samples that they have submitted.


### Part 2 - Sample Management
The sample management page is visible to users with staff permissions, and allows lab staff to generate worklists of outstanding tests and download it as a csv template. The template can then be populated with results, and uploaded in order to save each result in the database. Two tables are displayed on this page:

#### Outstanding Work
The outstanding work table is table of all the tests, grouped by attribute, that have not yet been assigned a worklist. Clicking on a row will generate a worklist and assign it to all of the outstanding tests of that attribute. The created worklist will then appear in the Worklists table.

#### Worklists table
The worklist table displays the created worklists. Each row displays the worklist number, the attribute of each test, and the number of tests in the worklist.The buttons below the table are used to toggle between 'outstanding' and 'complete' worklists. A worklist is considered outstanding if it contains tests without results, and complete if results are present for all tests. 
Clicking on a worklist from this table will display the worklist details table.

#### Worklist Details Table
Displays the sample details for each test in the worklist and any available results. Below this table is a button which allows the worklist to be downloaded as a csv file. To avoid duplicate files being created if the same worklist is downloaded multiple times, the function will check if the file already exists before creating it.

#### Upload results
Staff also have access to the 'upload results' page. This allows the lab staff to upload results using a worklist csv template downloaded from the sample management page. In a real environment, allowing for file uploads may introduce some extra security considerations that haven't been explored in this project.
