import React from 'react';

const StatsCards = ({ data }) => {
  const totalRevenue = data.reduce((acc, curr) => acc + (curr.Revenue || 0), 0);
  const totalNetIncome = data.reduce((acc, curr) => acc + (curr.NetIncome || 0), 0);
  const totalGrossProfit = data.reduce((acc, curr) => acc + (curr.GrossProfit || 0), 0);

  return (
    <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginBottom: '40px' }}>
      <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '10px', minWidth: '150px', textAlign: 'center' }}>
        <h3>Revenue</h3>
        <p>{totalRevenue.toLocaleString()}</p>
      </div>
      <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '10px', minWidth: '150px', textAlign: 'center' }}>
        <h3>Net Income</h3>
        <p>{totalNetIncome.toLocaleString()}</p>
      </div>
      <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '10px', minWidth: '150px', textAlign: 'center' }}>
        <h3>Gross Profit</h3>
        <p>{totalGrossProfit.toLocaleString()}</p>
      </div>
    </div>
  );
};

export default StatsCards;
