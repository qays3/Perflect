// analytics.js

const purpleColor = '#8a2be2';

async function fetchAnalyticsData() {
  try {
    const response = await fetch('/api/analytics-data');
    const data = await response.json();
    updateCharts(data.current_data, data.historical_data);
  } catch (error) {
    console.error('Error fetching analytics data:', error);
  }
}

function getChartConfig(title, seriesData, yAxisTitle) {
  const isDarkMode = getTheme();
  const backgroundColor = isDarkMode ? '#191c24' : '#ffffff';
  const textColor = isDarkMode ? '#ffffff' : '#000000';

  return {
    chart: {
      type: 'area',
      backgroundColor: backgroundColor,
      borderRadius: 20,
    },
    title: {
      text: title,
      style: {
        color: textColor,
        fontSize: '10px',
      },
    },
    xAxis: {
      labels: {
        style: {
          color: textColor,
          fontSize: '8px',
        },
      },
    },
    yAxis: {
      title: {
        text: yAxisTitle,
        style: {
          color: textColor,
          fontSize: '8px',
        },
      },
      labels: {
        style: {
          color: textColor,
          fontSize: '8px',
        },
      },
    },
    series: [
      {
        name: title,
        data: seriesData,
        color: purpleColor,
        marker: {
          enabled: false,
        },
        fillColor: {
          linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
          stops: [
            [0, 'rgba(138, 43, 226, 0.4)'],
            [1, 'rgba(138, 43, 226, 0)'],
          ],
        },
      },
    ],
    legend: {
      itemStyle: {
        color: textColor,
        fontSize: '8px',
      },
    },
  };
}

 
const chartInstances = {
  cpuUsageChart: null,
  memoryUsageChart: null,
  diskUsageChart: null,
  networkTrafficChart: null,
  systemLoadChart: null
};

 
function updateCharts(currentData, historicalData) {
  const chartContainers = document.querySelectorAll(
    '#cpuUsageChart, #memoryUsageChart, #diskUsageChart, #networkTrafficChart, #systemLoadChart'
  );
  chartContainers.forEach((container) => {
    container.classList.remove('pulse-animation');
  });

  chartInstances.cpuUsageChart = Highcharts.chart(
    'cpuUsageChart',
    getChartConfig(
      'CPU Usage Over Time',
      historicalData?.map((item) => item.cpu_usage) || [],
      'CPU (%)'
    )
  );
  
  chartInstances.memoryUsageChart = Highcharts.chart(
    'memoryUsageChart',
    getChartConfig(
      'Memory Usage Over Time',
      historicalData?.map((item) => item.memory_usage) || [],
      'Memory (GB)'
    )
  );
  
  chartInstances.diskUsageChart = Highcharts.chart(
    'diskUsageChart',
    getChartConfig(
      'Disk Usage Over Time',
      historicalData?.map((item) => item.disk_usage) || [],
      'Disk Usage (GB)'
    )
  );
  
  chartInstances.networkTrafficChart = Highcharts.chart(
    'networkTrafficChart',
    getChartConfig(
      'Network Traffic Analytics',
      historicalData?.map((item) => item.network_activity) || [],
      'Traffic (Mbps)'
    )
  );
  
  chartInstances.systemLoadChart = Highcharts.chart(
    'systemLoadChart',
    getChartConfig(
      'System Load Over Time',
      historicalData?.map((item) => item.system_load) || [],
      'Load'
    )
  );
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
            color: textColor
          }
        },
        xAxis: {
          labels: {
            style: {
              color: textColor
            }
          }
        },
        yAxis: {
          title: {
            style: {
              color: textColor
            }
          },
          labels: {
            style: {
              color: textColor
            }
          }
        },
        legend: {
          itemStyle: {
            color: textColor
          }
        }
      }, false);
      chart.redraw();
    }
  });
}

 
function renderEmptyCharts() {
  chartInstances.cpuUsageChart = Highcharts.chart(
    'cpuUsageChart',
    getChartConfig('CPU Usage Over Time', [], 'CPU (%)')
  );
  chartInstances.memoryUsageChart = Highcharts.chart(
    'memoryUsageChart',
    getChartConfig('Memory Usage Over Time', [], 'Memory (GB)')
  );
  chartInstances.diskUsageChart = Highcharts.chart(
    'diskUsageChart',
    getChartConfig('Disk Usage Over Time', [], 'Disk Usage (GB)')
  );
  chartInstances.networkTrafficChart = Highcharts.chart(
    'networkTrafficChart',
    getChartConfig('Network Traffic Analytics', [], 'Traffic (Mbps)')
  );
  chartInstances.systemLoadChart = Highcharts.chart(
    'systemLoadChart',
    getChartConfig('System Load Over Time', [], 'Load')
  );
}

 
const themeObserver = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.attributeName === 'class') {
      updateChartThemes();
    }
  });
});

document.addEventListener('DOMContentLoaded', () => {
  renderEmptyCharts();
  fetchAnalyticsData();
  document.documentElement.style.backgroundColor = getTheme() ? '#191c24' : '#ffffff';
  
 
  themeObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  });
});