echartOption = {
    tooltip: {
        trigger: 'axis',
        backgroundColor: '#fff',
        borderRadius: 9,
        textStyle: {
            color: '#305278',
            fontSize: 16,
            fontFamily: 'poppins',
        },
        padding: [14, 26],
        formatter: function (params, ticker, callback) {
            var res = `Date: ${params[0].name}`
            params.forEach(param => {
                res += `<br/>${param.seriesName}: ${param.value}`
            })
            return res
        },
        itemGap: 2,
        itemWidth: 100,
        itemHeight: 262,
        extraCssText: 'box-shadow: 0 3px 21px rgba(0,0,0,.3)'
    },
    calculable: true,
    legend: {
        data: ['Transaction History', 'Address Growth'],
        textStyle: {
            color: '#a9bcd4',
            fontSize: 16,
            fontFamily: 'poppins',

        },
        left: 40,

    },
    xAxis: [
        {
            type: 'category',
            data: [],
            boundaryGap: false,
            onZero: false,
            axisLine: {
                lineStyle: {
                    color: 'rgba(169,188,212,.8)'
                }
            },
            axisLabel: {
                color: '#a9bcd4',
                fontSize: 12,
                fontFamily: 'poppins',
            }
        }
    ],

    yAxis: [

        {
            type: 'value',
            axisLabel: {
                formatter: '{value}',
                color: '#a9bcd4',
                fontSize: 16,
                padding: [0, 10],
                fontFamily: 'poppins',
            },
            axisLine: {
                lineStyle: {
                    color: 'rgba(169,188,212,.8)',
                    width: 2,
                }
            },
            splitLine: {show: true, lineStyle: {type: 'dotted'}},
        },
        {
            type: 'value',
            name: 'Byte',
            axisLabel: {
                formatter: '{value}',
                color: '#a9bcd4',
                fontSize: 16,
                padding: [0, 10],
                fontFamily: 'poppins',
            },
            axisLine: {
                lineStyle: {
                    color: 'rgba(169,188,212,.8)',
                    width: 2,
                }
            },
            splitLine: {show: true, lineStyle: {type: 'dotted'}},
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
            },
            areaStyle: {
                color: {
                    type: 'linear',
                    x: 0,
                    y: 0,
                    x2: 0,
                    y2: 1,
                    colorStops: [{
                        offset: 0, color: 'rgba(119,136,153,.4)' // 0% 处的颜色
                    }, {
                        offset: 1, color: 'rgba(119,136,153,0.12)' // 100% 处的颜色
                    }],
                    globalCoord: false // 缺省为 false
                }
            },
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
    ],

};
