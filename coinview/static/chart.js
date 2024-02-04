var chart = LightweightCharts.createChart(document.getElementById('chart'), {
    width: window.innerWidth * 0.9, // Make the chart responsive
    height: 600,
    layout: {
        backgroundColor: '#2B2B43',
        textColor: 'rgba(255, 255, 255, 0.9)',
    },
    grid: {
        vertLines: {
            color: 'rgba(197, 203, 206, 0.5)',
        },
        horzLines: {
            color: 'rgba(197, 203, 206, 0.5)',
        },
    },
    crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
    },
    priceScale: {
        borderColor: 'rgba(197, 203, 206, 0.8)',
    },
    timeScale: {
        borderColor: 'rgba(197, 203, 206, 0.8)',
        timeVisible: true,
        secondsVisible: false,
    },
});

// Candlestick series
var candleSeries = chart.addCandlestickSeries({
    upColor: 'rgba(0, 150, 136, 0.8)',
    downColor: 'rgba(255, 82, 82, 0.8)',
    borderDownColor: 'rgba(255, 82, 82, 1)',
    borderUpColor: 'rgba(0, 150, 136, 1)',
    wickDownColor: 'rgba(255, 82, 82, 1)',
    wickUpColor: 'rgba(0, 150, 136, 1)',
});

// Volume series beneath the candlesticks
var volumeSeries = chart.addHistogramSeries({
    color: 'rgba(76, 175, 80, 0.5)',
    priceFormat: {
        type: 'volume',
    },
    priceScaleId: '',
    scaleMargins: {
        top: 0.8,
        bottom: 0,
    },
});

fetch('http://localhost:5000/history')
    .then((r) => r.json())
    .then((response) => {
        console.log(response)

        // Assuming response contains an additional 'volume' field for each data point
        const data = response.map(item => ({
            time: item.time,
            open: item.open,
            high: item.high,
            low: item.low,
            close: item.close,
            volume: item.volume, // Make sure your backend provides volume data
        }));

        candleSeries.setData(data.map(item => ({
            time: item.time,
            open: item.open,
            high: item.high,
            low: item.low,
            close: item.close,
        })));

        volumeSeries.setData(data.map(item => ({
            time: item.time,
            value: item.volume,
        })));
    });

var binanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_15m");

binanceSocket.onmessage = function (event) {
    var message = JSON.parse(event.data);
    var candlestick = message.k;

    console.log(candlestick)

    candleSeries.update({
        time: candlestick.t / 1000,
        open: candlestick.o,
        high: candlestick.h,
        low: candlestick.l,
        close: candlestick.c,
    });

    // Update volume series in real-time as well, if volume data is available
    // volumeSeries.update({
    //     time: candlestick.t / 1000,
    //     value: candlestick.v,
    // });
}
