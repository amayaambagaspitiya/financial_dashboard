import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const RevenueChart = ({ data }) => {
  const quarterOrder = { Q1: 1, Q2: 2, Q3: 3, Q4: 4 };

  const formattedData = [...data]
    .map((item) => ({
      ...item,
      label: `${item.quarter}-${item.year}`,
    }))
    .sort((a, b) => {
      if (a.year !== b.year) return a.year - b.year;
      return quarterOrder[a.quarter] - quarterOrder[b.quarter];
    });

  return (
    <div style={{ marginBottom: '50px' }}>
      <h2>Revenue Over Time</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={formattedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="label" />
          <YAxis tickFormatter={(value) => `${(value / 1_000_000).toFixed(1)}M`} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Revenue" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RevenueChart;
