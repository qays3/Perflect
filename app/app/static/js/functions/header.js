<<<<<<< HEAD
document.addEventListener('DOMContentLoaded', () => {
    const cpuChart = Highcharts.chart('cpuChart', {
        chart: {
            type: 'area',
            backgroundColor: 'transparent',
            height: 40,
            width: 300,
            animation: {
                duration: 2000,
                easing: 'easeOutBounce'
            }
        },
        title: {
            text: '',
        },
        xAxis: {
            visible: false,
        },
        yAxis: {
            visible: false,
        },
        plotOptions: {
            series: {
                marker: {
                    enabled: false
                },
                animation: {
                    duration: 2000,
                    easing: 'easeOutBounce'
                },
                dataLabels: {
                    enabled: false
                }
            }
        },
        tooltip: {
            formatter: function() {
                return 'Perflect CPU Usage: <b>' + this.y.toFixed(1) + '%</b>';
            }
        },
        series: [{
            name: 'Perflect CPU Usage',
            data: [],
            color: '#8a2be2',
            fillColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, 'rgba(138, 43, 226, 0.4)'],
                    [1, 'rgba(138, 43, 226, 0)'],
                ],
            },
        }],
        legend: {
            enabled: false,
        },
        credits: {
            enabled: false,
        },
    });

    const ramChart = Highcharts.chart('ramChart', {
        chart: {
            type: 'area',
            backgroundColor: 'transparent',
            height: 40,
            width: 300,
            animation: {
                duration: 2000,
                easing: 'easeOutBounce'
            }
        },
        title: {
            text: '',
        },
        xAxis: {
            visible: false,
        },
        yAxis: {
            visible: false,
        },
        plotOptions: {
            series: {
                marker: {
                    enabled: false
                },
                animation: {
                    duration: 2000,
                    easing: 'easeOutBounce'
                },
                dataLabels: {
                    enabled: false
                }
            }
        },
        tooltip: {
            formatter: function() {
                return 'Perflect RAM Usage: <b>' + this.y.toFixed(3) + '%</b>';
            }
        },
        series: [{
            name: 'Perflect RAM Usage',
            data: [],
            color: '#8a2be2',
            fillColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, 'rgba(138, 43, 226, 0.4)'],
                    [1, 'rgba(138, 43, 226, 0)'],
                ],
            },
        }],
        legend: {
            enabled: false,
        },
        credits: {
            enabled: false,
        },
    });

    async function fetchResourceHistory() {
        try {
            const response = await fetch('/api/resource-history');
            const data = await response.json();
            cpuChart.series[0].setData(data.cpu_history, true, { duration: 2000 });
            ramChart.series[0].setData(data.ram_history, true, { duration: 2000 });
        } catch (error) {
            console.error('Error fetching resource history:', error);
        }
    }

    async function fetchResourceUsage() {
        try {
            const response = await fetch('/api/resource-usage');
            const data = await response.json();
            cpuChart.series[0].addPoint(data.cpu_usage, true, cpuChart.series[0].data.length > 30, { duration: 2000 });
            ramChart.series[0].addPoint(data.ram_usage, true, ramChart.series[0].data.length > 30, { duration: 2000 });
        } catch (error) {
            console.error('Error fetching resource usage:', error);
        }
    }

    fetchResourceHistory().then(() => {
        setInterval(fetchResourceUsage, 1000);
    });

    document.getElementById('reboot').addEventListener('click', function() {
        if (confirm("Are you sure you want to reboot the system?")) {
            fetch('/reboot_system', {
                method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('System rebooting...');
                } else {
                    alert('Failed to reboot the system.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while attempting to reboot.');
            });
        }
    });
=======
//header.js

document.getElementById('reboot').addEventListener('click', function() {
    if (confirm("Are you sure you want to reboot the system?")) {
        fetch('/reboot_system', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('System rebooting...');
            } else {
                alert('Failed to reboot the system.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while attempting to reboot.');
        });
    }
>>>>>>> 056fad599c7648f2a924f04ea510b355067a52e4
});