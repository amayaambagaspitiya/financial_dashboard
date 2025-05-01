import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const NetIncomeChart = ({ data }) => {
  return (
    <div style={{ marginBottom: '50px' }}>
      <h2>Net Income Over Time</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={(d) => d.file.split('_')[1].slice(0, 7)} />
          <YAxis tickFormatter={(value) => `${(value/1000000).toFixed(1)}M`} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="NetIncome" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default NetIncomeChart;
