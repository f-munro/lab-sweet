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

    function loadOutstandingWork() {
        fetch(`/outstanding`)
            .then(response => response.json())
            .then(tests => {
                tests.forEach(test => {
                    const row = document.createElement('tr');
                    row.innerHTML = `<td>${test.full_name}</td>
                                <td>${test.test_count}</td>`
                    row.className = 'clickable'
                    row.addEventListener('click', () => loadWorklist(test.name))
                    bod.appendChild(row)
                })
            })
    }

    function loadWorklist(test) {
        tHead.innerHTML = '';
        tBody.innerHTML = '';
        downloadBtn.innerHTML = '';
        tableView.style.display = 'block';
        fetch('/worklist/' + test)
            .then(response => response.json())
            .then(test => {
                tableName.innerHTML = `Outstanding ${test[0].attribute.full_name} tests`
                tHead.innerHTML = `<th>LIMS ID</th>
                                   <th>Sample</th>
                                   <th>Batch</th>`
                test.forEach(test => {
                    const row = document.createElement('tr');
                    row.innerHTML = `<td>${test.sample.id}</td>
                                    <td>${test.sample.sample_id}</td>
                                    <td>${test.sample.batch}</td>`
                    tBody.appendChild(row)
                })
                const downloadWorklist = document.createElement("a")
                downloadWorklist.setAttribute("href", "#");
                downloadWorklist.className = 'btn btn-primary'
                // downloadWorklist.innerHTML = `<a href='/download_worklist/${test[0].attribute.id}' class="btn btn-primary">Download Worklist</a>                `
                downloadWorklist.textContent = `Download File`
                downloadWorklist.addEventListener('click', download_worklist)
                downloadBtn.appendChild(downloadWorklist)
            })
    }

    function download_worklist() {
        tableName.innerHTML = "Worklist Downloaded"
        tHead.innerHTML = '';
        tBody.innerHTML = '';
        downloadBtn.innerHTML = '';
        loadOutstandingWork;
        //window.location.href = '/download_template'
    }

    const csrftoken = getCookie("csrftoken");
    //document.querySelector('#download-template').addEventListener('click', download_button)
    const testLinks = document.querySelectorAll('.test-link')
    testLinks.forEach(link => link.addEventListener('click', loadWorklist))
    const tableView = document.querySelector("#table-view")
    const tHead = document.querySelector("#thead")
    const tBody = document.querySelector("#tbody")
    const tableName = document.querySelector('#table-name');
    const bod = document.querySelector('#bod')
    const downloadBtn = document.querySelector('#download-btn')

    tableView.style.display = 'none';
    loadOutstandingWork()
})