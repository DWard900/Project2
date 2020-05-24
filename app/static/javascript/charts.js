// Results page
// HTTP request to get user exercise graph
function getGraph(userId) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() { 
        if (this.readyState == 4 && this.status == 200) {
        const myData = JSON.parse(this.responseText);
        exerciseGraph(myData);
        }
    };
    let url = "http://localhost:5000/api/users/" + userId + "/exercise/time_graph";
    xhttp.open("GET", url, true);
    xhttp.send();
  }

// Creates graph
function exerciseGraph(arr) {
    let ctx = document.getElementById("barChart").getContext('2d');
    let walktime = 0;
    let runtime = 0;
    for (x in arr) {
        if (arr[x].style == "Walk") {
            walktime += parseFloat(arr[x].time);
        } else if (arr[x].style == "Run") {
            runtime += parseFloat(arr[x].time);
        }
    }

    var barChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Run", "Walk"],
            datasets: [{
                data: [runtime, walktime],
                backgroundColor: ["#331E36", "#A5FFD6"],
                }]
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
        
    });
};