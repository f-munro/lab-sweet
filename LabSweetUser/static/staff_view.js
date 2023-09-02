document.addEventListener('DOMContentLoaded', function () {

    // Gets the csrf cookie (taken from the Django documentation)
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


    /**
     * Fetches all the tests that have not yet been
     * assigned a worklist, and uses them to build a table
     * of outstanding tests, grouped by attribute. When a
     * row is clicked, generates a new worklist.
     */
    function loadOutstandingWork() {
        outstandingBody.innerHTML = ""
        fetch(`/outstanding`)
            .then(response => response.json())
            .then(attributes => {
                attributes.forEach(attribute => {
                    const row = document.createElement('tr');
                    row.innerHTML = `<td>${attribute.full_name}</td>
                                <td>${attribute.test_count}</td>`
                    row.className = 'clickable'
                    row.addEventListener('click', () => generateWorklist(attribute.name))
                    outstandingBody.appendChild(row)
                })
            })
    }


    /**
     * Generates the worklists table that displays the
     * worklist number and quantity of tests for each worklist.
     * When a worklist is clicked, it appears below the table.
     */
    function loadWorklists(filter) {
        worklistsBody.innerHTML = ""
        worklistsTable.style.display = 'block';
        worklistsHeader.innerHTML = `${filter} Worklists`
        fetch(`/worklists?filter=${filter}`)
            .then(response => response.json())
            .then(worklists => {
                worklists.forEach(worklist => {
                    const row = document.createElement('tr');
                    row.innerHTML = `<td>${worklist.worklist_number}</td>
                                <td>${worklist.tests[0].attribute.full_name}</td>
                                <td>${worklist.tests.length}</td>`
                    row.className = 'clickable';
                    row.addEventListener('click', () => showWorklistDetails(worklist))
                    worklistsBody.appendChild(row);
                })
            })
    }


    /**
     * Initiates the download of the csv template of a worklist.
     */
    function downloadWorklist(worklist) {
        worklistName.innerHTML = "Worklist Downloaded"
        WorklistHead.innerHTML = '';
        worklistBody.innerHTML = '';
        downloadBtnDiv.innerHTML = '';
        window.location.href = `/download_worklist/${worklist}`
    }


    /**
     * Creates and displays a table containing the details 
     * of each test in a worklist, including results if present.
     * Also creates a download button, which will call 'downloadWorklist'
     */
    function showWorklistDetails(worklist) {
        WorklistHead.innerHTML = '';
        worklistBody.innerHTML = '';
        downloadBtnDiv.innerHTML = '';
        worklistView.style.display = 'block';

        const tests = worklist.tests

        worklistName.innerHTML =
            `<p>Test: ${tests[0].attribute.full_name}<p>
            <p>Worklist: ${worklist.worklist_number}</p`
        WorklistHead.innerHTML =
            `<th>LIMS ID</th>
            <th>Sample</th>
            <th>Batch</th>
            <th>Result (${tests[0].attribute.units})</th>`


        const downloadBtn = document.createElement("a")
        downloadBtn.setAttribute("href", "#");
        downloadBtn.className = 'btn btn-primary'
        downloadBtn.textContent = `Download File`
        downloadBtn.addEventListener('click', () => downloadWorklist(worklist.worklist_number))
        downloadBtnDiv.appendChild(downloadBtn)

        tests.forEach(test => {
            const row = document.createElement('tr');
            var result = ""
            if (test.result !== null) {
                result = test.result
            }
            row.innerHTML =
                `<td>${test.id}</td>
                <td>${test.sample.sample_id}</td>
                <td>${test.sample.batch}</td>
                <td>${result}</td>`
            worklistBody.appendChild(row)
        })
    }


    /** 
     * Sends the given attribute to 'generate_worklist' in views.py,
     * which will generate a new worklist and apply it to all
     * outstanding tests of the given attribute. The created
     * worklist will be shown, and the outstanding and worklists
     * tables will be reloaded.
    */
    function generateWorklist(attribute) {
        worklistView.style.display = 'block';
        fetch('/generate/' + attribute, {
            method: "PUT",
            headers: {
                "X-CSRFToken": csrftoken
            },
        })
            .then(response => response.json())
            .then(worklist => {
                showWorklistDetails(worklist)
                loadOutstandingWork()
                loadWorklists("Outstanding")
            })
    }


    const csrftoken = getCookie("csrftoken");
    const WorklistHead = document.querySelector("#worklist-view-head")
    const worklistBody = document.querySelector("#worklist-view-body")
    const worklistName = document.querySelector('#worklist-name');
    const outstandingBody = document.querySelector('#outstanding-body')
    const downloadBtnDiv = document.querySelector('#download-btn')
    const worklistsHeader = document.querySelector('#worklists-header')
    const worklistsTable = document.querySelector('#worklists-table')
    const worklistsBody = document.querySelector('#worklists-body')
    const worklistView = document.querySelector('#worklist-view')

    document.querySelector('#complete-worklists-btn').addEventListener('click', () => loadWorklists("Complete"))
    document.querySelector('#outstanding-worklists-btn').addEventListener('click', () => loadWorklists("Outstanding"))


    worklistView.style.display = 'none';
    loadOutstandingWork()
    loadWorklists("Outstanding")
})