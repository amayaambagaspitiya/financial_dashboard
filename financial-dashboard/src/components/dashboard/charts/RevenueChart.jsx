import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const RevenueChart = ({ data }) => {
  return (
    <div style={{ marginBottom: '50px' }}>
      <h2>Revenue Over Time</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={(d) => d.file.split('_')[1].slice(0, 7)} />
          <YAxis tickFormatter={(value) => `${(value/1000000).toFixed(1)}M`} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Revenue" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RevenueChart;
