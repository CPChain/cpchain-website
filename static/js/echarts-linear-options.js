echartOption = {
  tooltip: {
    trigger: 'axis',
    backgroundColor: '#fff',
    borderRadius: 9,
    textStyle: {
      color: '#305278',
      fontSize: 16
    },
    formatter: function(params, ticker, callback) {
      var res = `Date: ${params[0].name}<br/>`
      params.forEach(param => {
        res += `<br/>${param.seriesName}: ${param.value}`
      })
      return res
    }
  },
  calculable: true,
  legend: {
    data: ['Transaction History', 'Address Growth']
  },
  xAxis: [
    {
      type: 'category',
      // data: ['9/17', '9/18', '9/19', '9/20', '9/21', '9/22', '9/23', '9/24', '9/25']
      data: []
    }
  ],
  yAxis: [
    {
      type: 'value',
      splitNumber: 5,
      axisLabel: {
        formatter: '{value} '
      }
    },
    {
      type: 'value',
      name: 'Byte',
      splitNumber: 5,
      axisLabel: {
        formatter: '{value}'
      }
    }
  ],
  series: [
    {
      name: 'Address Growth',
      type: 'line',
      // data: [5, 8, 7, 12, 10, 29, 18, 22, 25],
      data: [],
      lineStyle: {
        color: '#191970',
      }
    },
    {
      name: 'Transaction History',
      type: 'line',
      yAxisIndex: 1,
      // data: [1000, 2000, 1800, 2200, 2000, 4000, 3500, 4200, 5000],
      data: [],
      lineStyle: {
        color: '#00abf1'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [{
            offset: 0, color: 'rgba(0,171,241,1.0)' // 0% 处的颜色
          }, {
            offset: 1, color: 'rgba(0,115,223,0.12)' // 100% 处的颜色
          }],
          globalCoord: false // 缺省为 false
        }
      },
    }
  ]
};
