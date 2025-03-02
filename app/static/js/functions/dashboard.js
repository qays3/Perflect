const chartInstances = {
  cpuUsageChart: null,
  memoryUsageChart: null,
  diskUsageChart: null,
  networkTrafficChart: null
};

function toggleTheme() {
  const darkMode = document.documentElement.classList.toggle('theme-dark');
  updateChartThemes();
}

function getTheme() {
  return document.documentElement.classList.contains('theme-dark');
}

function updateChartThemes() {
  const isDarkMode = getTheme();
  const backgroundColor = isDarkMode ? '#191c24' : '#ffffff';
  const textColor = isDarkMode ? '#ffffff' : '#000000';

  Object.values(chartInstances).forEach(chart => {
    if (chart) {
      chart.update({
        chart: {
          backgroundColor: backgroundColor
        },
        title: {
          style: {
            color: textColor,
            fontSize: '10px'
          }
        },
        xAxis: {
          labels: {
            style: {
              color: textColor,
              fontSize: '8px'
            }
          }
        },
        yAxis: {
          title: {
            style: {
              color: textColor,
              fontSize: '8px'
            }
          },
          labels: {
            style: {
              color: textColor,
              fontSize: '8px'
            }
          }
        },
        legend: {
          itemStyle: {
            color: textColor,
            fontSize: '8px'
          }
        }
      }, false);
      chart.redraw();
    }
  });
}

async function fetchSystemData() {
  try {
    const response = await fetch("/api/system-data");
    const data = await response.json();

    document.querySelector("#uptime").textContent = data.current_data.uptime;
    document.querySelector("#firewall").textContent = data.current_data.firewall_status;
    document.querySelector("#cpu").textContent = `${data.current_data.cpu_usage.current}% | Peak: ${data.current_data.cpu_usage.peak}% | Load: ${data.current_data.cpu_usage.load.join(" / ")}`;
    document.querySelector("#memory").textContent = `${data.current_data.memory_usage.used} GB / Total: ${data.current_data.memory_usage.total} GB`;
    document.querySelector("#disk").textContent = `${data.current_data.disk_usage.used} GB / Total: ${data.current_data.disk_usage.total} GB`;
    document.querySelector("#network").textContent = `${(data.current_data.network_activity.inbound / 1024).toFixed(3)} KB/s`;

    updateCharts(data.current_data, data.historical_data);

    const sections = document.querySelectorAll('.pulse-animation');
    sections.forEach(section => section.classList.remove('pulse-animation'));
  } catch (error) {
    console.error("Error fetching system data:", error);
  }
}

function updateCharts(currentData, historicalData) {
  if (!chartInstances.cpuUsageChart) {
    chartInstances.cpuUsageChart = Highcharts.chart('cpuUsageChart', 
      getChartConfig('CPU Usage Over Time', getChartData(historicalData, 'cpu_usage'), 'CPU Usage')
    );
  } else {
    chartInstances.cpuUsageChart.series[0].setData(getChartData(historicalData, 'cpu_usage'));
  }

  if (!chartInstances.memoryUsageChart) {
    chartInstances.memoryUsageChart = Highcharts.chart('memoryUsageChart', 
      getChartConfig('Memory Usage Over Time', getChartData(historicalData, 'memory_usage'), 'Memory (GB)')
    );
  } else {
    chartInstances.memoryUsageChart.series[0].setData(getChartData(historicalData, 'memory_usage'));
  }

  if (!chartInstances.diskUsageChart) {
    chartInstances.diskUsageChart = Highcharts.chart('diskUsageChart', 
      getChartConfig('Disk Usage Over Time', getChartData(historicalData, 'disk_usage'), 'Disk Space (GB)')
    );
  } else {
    chartInstances.diskUsageChart.series[0].setData(getChartData(historicalData, 'disk_usage'));
  }

  if (!chartInstances.networkTrafficChart) {
    chartInstances.networkTrafficChart = Highcharts.chart('networkTrafficChart', 
      getChartConfig('Network Traffic', getChartData(historicalData, 'network_activity'), 'Traffic (KB/s)')
    );
  } else {
    chartInstances.networkTrafficChart.series[0].setData(getChartData(historicalData, 'network_activity'));
  }
}

function getChartData(historicalData, field) {
  const last20Data = historicalData.slice(-20);
  return last20Data.map(item => {
    if (field === 'cpu_usage') {
      return item[field].current;
    } else if (field === 'memory_usage') {
      return item[field].used;
    } else if (field === 'disk_usage') {
      return item[field].used;
    } else if (field === 'network_activity') {
      return parseFloat((item[field].inbound / 1024).toFixed(3));
    }
  });
}

function getChartConfig(title, seriesData, yAxisTitle) {
  const isDarkMode = getTheme();
  const backgroundColor = isDarkMode ? '#191c24' : '#ffffff';
  const textColor = isDarkMode ? '#ffffff' : '#000000';

  const purpleColor = 'rgba(138, 43, 226, 0.8)';
  const fillGradient = {
    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
    stops: [
      [0, 'rgba(138, 43, 226, 0.4)'],
      [1, 'rgba(138, 43, 226, 0)']
    ]
  };

  return {
    chart: {
      type: 'area',
      backgroundColor: backgroundColor,
      borderRadius: 20,
    },
    title: {
      text: title,
      style: { color: textColor, fontSize: '10px' }
    },
    xAxis: {
      labels: { style: { color: textColor, fontSize: '8px' } }
    },
    yAxis: {
      title: { text: yAxisTitle, style: { color: textColor, fontSize: '8px' } },
      labels: { style: { color: textColor, fontSize: '8px' } }
    },
    series: [{
      name: title,
      data: seriesData,
      color: purpleColor,
      fillColor: fillGradient
    }],
    plotOptions: {
      area: {
        marker: { enabled: false },
        lineWidth: 2,
        states: { hover: { lineWidth: 2 } },
        threshold: null
      }
    },
    legend: {
      itemStyle: { color: textColor, fontSize: '8px' }
    }
  };
}

function fetchAnalyticsData() {
  fetchSystemData();
}

const themeObserver = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.attributeName === 'class') {
      updateChartThemes();
    }
  });
});

document.addEventListener('DOMContentLoaded', () => {
  fetchAnalyticsData();
  document.documentElement.style.backgroundColor = getTheme() ? '#191c24' : '#ffffff';

  setInterval(fetchSystemData, 300000);

  themeObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  });
});
