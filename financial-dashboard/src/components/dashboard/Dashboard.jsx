import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FilterBar from './FilterBar';
import StatsCards from './StatsCards';
import RevenueChart from './charts/RevenueChart';
import NetIncomeChart from './charts/NetIncomeChart';
import GrossProfitChart from './charts/GrossProfitChart';

function Dashboard() {
  const [data, setData] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState('All');
  const [selectedYear, setSelectedYear] = useState('All');
  const [selectedQuarter, setSelectedQuarter] = useState('All');

  useEffect(() => {
    axios.get("http://localhost:8000/dashboard-data")
      .then(res => setData(res.data))
      .catch(err => console.error("Failed to load dashboard data:", err));
  }, []);

  const filterData = () => {
    return data.filter(item => {
      const year = item.file.split('_')[1].split('-')[0];
      const month = item.file.split('_')[1].split('-')[1];
      const quarter =
        (month === '03' && 'Q1') ||
        (month === '06' && 'Q2') ||
        (month === '09' && 'Q3') ||
        (month === '12' && 'Q4') ||
        '';

      return (
        (selectedCompany === 'All' || item.company === selectedCompany) &&
        (selectedYear === 'All' || year === selectedYear) &&
        (selectedQuarter === 'All' || quarter === selectedQuarter)
      );
    });
  };

  const filteredData = filterData();

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ textAlign: 'center' }}>Financial Dashboard (Live Data)</h1>
      <FilterBar
        selectedCompany={selectedCompany}
        setSelectedCompany={setSelectedCompany}
        selectedYear={selectedYear}
        setSelectedYear={setSelectedYear}
        selectedQuarter={selectedQuarter}
        setSelectedQuarter={setSelectedQuarter}
      />
      <StatsCards data={filteredData} />
      <RevenueChart data={filteredData} />
      <NetIncomeChart data={filteredData} />
      <GrossProfitChart data={filteredData} />
    </div>
  );
}

export default Dashboard;
