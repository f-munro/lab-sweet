// Clean up load job function
// Add feedback after samples are submitted
// Clear form after samples submitted

document.addEventListener('DOMContentLoaded', function () {
    // Get the csrf cookie (taken from the Django documentation)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
            }
        }
        }
        return cookieValue;
    }; 


    function add_row() {
        const formRow = document.createElement('div')
        formRow.className = "row form-row mb-2"
        formRow.innerHTML = 
            `<div class="col-sm-3">
            <input type="text" class="form-control" name="sample-id" placeholder="Sample ID">
            </div>
            <div class="col-sm-3">
                <div class="input-group">
                <div class="input-group-text">Batch</div>
                <input type="text" class="form-control" name="batch" placeholder="Batch">
                </div>
            </div>
            <div class="col-auto">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" name="test-checkbox" value="AFB">
                <label class="form-check-label" for="me">
                    AFB
                </label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" name="test-checkbox" value="DIA">
                <label class="form-check-label" for="be">
                    Diastase
                </label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" name="test-checkbox" value="TUT">
                <label class="form-check-label" for="we">
                    Tutin
                </label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" name="test-checkbox" value="GLY">
                <label class="form-check-label" for="we">
                    Glyphosate
                </label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" name="test-checkbox" value="LPS">
                <label class="form-check-label" for="we">
                    Leptosperin
                </label>
                </div>
            </div`
        form.append(formRow)
        updateButtonVisibility();
    }


    function delete_row() {
        if (form.childElementCount > 1) {
            form.lastElementChild.remove();
        }
        updateButtonVisibility();
    }


    function updateButtonVisibility() {
        if (form.childElementCount <= 1) {
            deleteRowBtn.style.display = "none";
        } else {
          deleteRowBtn.style.display = "block";
        }
    }


    function submit_samples() {
        let formRows = form.getElementsByClassName("form-row")
        let submission = []
        let requiredFieldEmpty = false;

        Array.from(formRows).forEach(function (row) {
            var checkBoxes = row.querySelectorAll('input[name="test-checkbox"]:checked');
            var tests = Array.from(checkBoxes).map(function(checkbox) {
                return checkbox.value;
            });
            let sampleId = row.querySelector("input[name='sample-id']")
            let batch = row.querySelector("input[name='batch']")

            if (tests.length == 0 || sampleId.value.trim() === "") {
                requiredFieldEmpty = true;
                return
            }

            let sample = {
                "sampleId": sampleId.value,
                "batch": batch.value,
                "tests": tests
            }

            submission.push(sample)

        })

        if (requiredFieldEmpty == true) {
            alert("A sample ID and at least one test is required for each sample", "info")
            return
        }

        fetch('/submitsample', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(submission)
        })
        .then(response => response.json())
        .then(result => {
          alert(result.content, "success")
          if (result.error) {
            alert(result.error, "warning")
          }
        })

        form.innerHTML = ""
        add_row()
    
    }
    
    
    function fetchSamples(filter) {
        submissionView.style.display = 'none';
        detailsView.style.display = 'none';
        resultsView.style.display = 'block';
        tableView.style.display = 'block';
        detailsDiv.innerHTML = '';
        tHead.innerHTML = '';
        tBody.innerHTML = '';
        tableName.innerHTML = `<h3>${filter} Samples</h3>`;
        fetch(`/samples?filter=${filter}`)
            .then(response => response.json())
            .then(samples => {
                if (samples.error) {
                    tBody.innerHTML = samples.error;
                } else {
                    samples.forEach(sample => {
                        const testBadges = document.createElement('span');
                        sample.tests.forEach(test => {
                            const badge = `<span class="badge rounded-pill bg-secondary-subtle text-secondary-emphasis">${test.attribute.name}</span>`
                            testBadges.innerHTML  += badge
                        })
                        const row = document.createElement('tr');
                        row.innerHTML = `<td>${sample.job.job_number}</td>
                                        <td>${sample.sample_id}</td>
                                        <td>${sample.batch}</td>
                                        <td>${testBadges.innerHTML}</td>`
                        row.addEventListener('click', () => showSampleDetails(sample))
                        tBody.appendChild(row);
                    });
                    tHead.innerHTML = '<th>Job Number</th><th>Sample ID</th><th>Batch</h><th>Tests</th>'
                }
            });
    }
    

    function fetchJobs(filter) {
        submissionView.style.display = 'none';
        detailsView.style.display = 'none';
        resultsView.style.display = 'block';
        tableView.style.display = 'block';
        detailsDiv.innerHTML = '';
        tHead.innerHTML = '';
        tBody.innerHTML = '';
        tableName.innerHTML = `<h3>${filter} Jobs</h3>`;
        fetch(`/jobs?filter=${filter}`)
            .then(response => response.json())
            .then(jobs => {
                jobs.forEach(job => {
                    const row = document.createElement('tr');
                    row.innerHTML = `<td>${job.job_number}</td>
                                    <td>${job.samples.length}</td>
                                    <td>${job.due_date}</td>`
                    if (job.complete == true) {
                        row.innerHTML += `<td>Yes</td>`
                    } else {
                        row.innerHTML += `<td>No</td>`
                    }
                    row.addEventListener('click', () => showJobDetails(job))
                    tBody.appendChild(row);
                });
                tHead.innerHTML = '<th>Job Number</th><th>Samples</th><th>Due</th><th>Complete</th>'
            });
    }
    
    
    function showSampleDetails(sample) {
        const testResults = document.createElement('p')
        testResults.innerHTML = '<h4><svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="none" viewBox="0 0 16 16" aria-hidden="true" focusable="false" class="icon__test-smallest"><path stroke="currentColor" stroke-width="2" d="M4 1h2v5l-4.175 7.514A1 1 0 002.7 15h10.6a1 1 0 00.875-1.486L10 6V1h2M6 1h4"></path><path fill="currentColor" d="M4.5 13L6 10h4l1.5 3h-7z"></path></svg> Results</h4>'
    
        sample.tests.forEach(test => {
            if (test.result !== null) {
            const test_name = test.attribute.full_name
            const test_result = test.result
            const units = `<i><small>${test.attribute.units}</small></i>`
            testResults.innerHTML += `<p><strong>${test_name}</strong>: ${test_result} ${units}</p>`
            }
        })
    
        detailsDiv.innerHTML = `<h3><svg xmlns="http://www.w3.org/2000/svg" width="20" height="32" fill="none" viewBox="0 0 20 32" aria-hidden="true" focusable="false" class="icon__pottle"><path stroke="currentColor" stroke-width="2" d="M19 31V12a2 2 0 00-2-2H3a2 2 0 00-2 2v19h18zM4 1v6m3 0V1h3v6h3V1h3v6"></path><rect width="18" height="6" x="1" y="1" stroke="currentColor" stroke-width="2" rx="1"></rect><path fill="currentColor" d="M4 17v11h12V17H4z"></path></svg> ${sample.sample_id}</h3>
                                    <p>Date Submitted: ${sample.submitted}</p>
                                    <p>Batch: ${sample.batch}</p>
                                    <p>Job: ${sample.job.job_number}</p>`
        detailsDiv.appendChild(testResults)
        tableView.style.display = "none";  
        detailsView.style.display = "block";
    }
    

    function showJobDetails(job) {
        detailsDiv.innerHTML = "";
    
        job.samples.forEach(sample => {
            const sampleDetails = document.createElement('p')
            sampleDetails.innerHTML = `<h3>${sample.sample_id}</h3>
                                        <p>Batch: ${sample.batch}</p>
                                        <p>Date: ${sample.submitted}</p>`
            detailsDiv.appendChild(sampleDetails)
        })
        tableView.style.display = "none";  
        detailsView.style.display = "block";
    }


    function loadSubmitSampleView() {
        detailsView.style.display = "none";
        resultsView.style.display = "none";
        submissionView.style.display = "block";
        detailsDiv.innerHTML = ""
    }


    function back_button() {
        detailsView.style.display = "none";
        tableView.style.display = "block";
        detailsDiv.innerHTML = ""
    }


    const currentUser = document.getElementById("current-user").textContent
    const csrftoken = getCookie("csrftoken");
    const detailsView = document.querySelector('#details-view');
    const detailsDiv = document.querySelector('#details-div');
    const resultsView = document.querySelector('#results-view');
    const submissionView = document.querySelector('#submission-view');
    const tableView = document.querySelector('#table-view');
    const tableName = document.querySelector('#table-name');
    const tHead = document.querySelector('#thead')
    const tBody = document.querySelector('#tbody')
    const submitBtn = document.querySelector('#submit-btn')
    const deleteRowBtn = document.querySelector('#delete-row-btn')
    let form = document.querySelector("#sample-submit")

    const alert = (message, type) => {
        const wrapper = document.createElement("div");
        wrapper.innerHTML = [
          `<div class="alert alert-${type} alert-dismissible fade show text-center mx-5" role="alert">`,
          `   <div>${message}</div>`,
          '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
          "</div>",
        ].join("");
        document.querySelector("#alert").innerHTML = "";
        document.querySelector("#alert").append(wrapper);
    };

    document.querySelector('#all-samples').addEventListener('click', () => fetchSamples('All'));
    document.querySelector('#complete-samples').addEventListener('click', () => fetchSamples('Complete'));
    document.querySelector('#outstanding-samples').addEventListener('click', () => fetchSamples('Outstanding'));
    document.querySelector('#all-jobs').addEventListener('click', () => fetchJobs('All'));
    document.querySelector('#complete-jobs').addEventListener('click', () => fetchJobs('Complete'));
    document.querySelector('#outstanding-jobs').addEventListener('click', () => fetchJobs('Outstanding'));
    document.querySelector('#submit-link').addEventListener('click', loadSubmitSampleView);
    document.querySelector("#add-row-btn").addEventListener('click', add_row);
    document.querySelector("#back-btn").addEventListener('click', back_button);
    deleteRowBtn.addEventListener('click', delete_row);
    submitBtn.addEventListener('click', submit_samples)

    detailsView.style.display = 'none';
    submissionView.style.display = 'none';
    deleteRowBtn.style.display = 'none';

});