import React, { useState } from 'react';
import { LineChart } from '../lib';

const App = () => {
    const [clickData, setClickData] = useState(null);
    const [nClicks, setNClicks] = useState(0);

    const setProps = (newProps) => {
        if (newProps.clickData) {
            setClickData(newProps.clickData);
        }
        if (newProps.n_clicks !== undefined) {
            setNClicks(newProps.n_clicks);
        }
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
            <h1>Dash MUI Charts - LineChart Demo</h1>

            <LineChart
                id="demo-chart"
                height={400}
                series={[
                    {
                        data: [2, 5.5, 2, 8.5, 1.5, 5],
                        label: 'Series A',
                        showMark: true,
                    },
                    {
                        data: [4, 3.5, 6, 2.5, 4.5, 3],
                        label: 'Series B',
                        area: true,
                    },
                ]}
                xAxis={[{
                    data: [1, 2, 3, 4, 5, 6],
                    scaleType: 'point',
                }]}
                grid={{ horizontal: true, vertical: true }}
                setProps={setProps}
                clickData={clickData}
                n_clicks={nClicks}
            />

            <div style={{ marginTop: '20px' }}>
                <h3>Click Data:</h3>
                <pre style={{ background: '#f5f5f5', padding: '10px' }}>
                    {clickData ? JSON.stringify(clickData, null, 2) : 'Click on the chart'}
                </pre>
                <p>Total clicks: {nClicks}</p>
            </div>
        </div>
    );
};

export default App;
