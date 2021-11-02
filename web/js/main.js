// document.addEventListener('contextmenu', event => event.preventDefault());

var visitData = ["", ""];

var myChart = new Chart(document.getElementById('mychart'), {
    type: 'doughnut',
    data: {
        labels: ["Efficiency", ""],
        datasets: [{
            label: 'Visitor',
            data: ["20", "80"],
            backgroundColor: [
                "#a2d6c4",
                "transparent"
            ]
        }]
    },
    options: {
        responsive: true,
        legend: false,
        animation: {
            duration: 0
        }
    }
});

function addData(data) {
    myChart.data.datasets = [{
        label: 'Visitor',
        data: data,
        backgroundColor: [
            "#a2d6c4",
            "transparent"
        ]
    }]
    document.getElementById('efficiency').innerHTML = data[0] + '%'
    myChart.update(0);
}

function openmodal() {
    $('#passwordmodal').modal('show')
}


// setInterval(function() {
//     var data1 = (Math.floor((Math.random() * 100) + 1));
//     addData([data1, data1 - 100])

// }, 500);

$('#submit').click(function() {
    //Serialize the data
    const confs = $("form").serialize();
    // send the data to python
    eel.set_pyconfigs(confs.client_id, confs.team, confs.canspercase, confs.target)
});


// retrieve settings from python, and save on js
eel.expose(set_jsconfigs);

function set_jsconfigs(client_id, team, canspercase, target, shift) {
    // client title
    document.getElementById('client_id').innerHTML = client_id.replace(/^\D+/g, '');
    //team
    document.getElementById("team").innerHTML = team
        //shift
    document.getElementById("shift").innerHTML = shift

}

eel.expose(set_metrics);

function set_metrics(s_cans, s_cases, damages, downtime, effic) {
    // efficiency
    addData([effic, 100 - effic])

    //seamed cans
    document.getElementById("s_cans").innerHTML = s_cans

    //seamed cases 
    document.getElementById("s_cases").innerHTML = s_cases

    //damaged cans
    document.getElementById("damages").innerHTML = damages

    //downtime
    document.getElementById("downtime").innerHTML = downtime

}