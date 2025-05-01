import React from 'react';

const FilterBar = ({ selectedCompany, setSelectedCompany, selectedYear, setSelectedYear, selectedQuarter, setSelectedQuarter }) => {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginBottom: '30px' }}>
      <select value={selectedCompany} onChange={(e) => setSelectedCompany(e.target.value)}>
        <option value="All">All Companies</option>
        <option value="DIPD">DIPD</option>
        <option value="REXP">REXP</option>
      </select>

      <select value={selectedYear} onChange={(e) => setSelectedYear(e.target.value)}>
        <option value="All">All Years</option>
        <option value="2021">2021</option>
        <option value="2022">2022</option>
        <option value="2023">2023</option>
        <option value="2024">2024</option>
      </select>

      <select value={selectedQuarter} onChange={(e) => setSelectedQuarter(e.target.value)}>
        <option value="All">All Quarters</option>
        <option value="Q1">Q1</option>
        <option value="Q2">Q2</option>
        <option value="Q3">Q3</option>
        <option value="Q4">Q4</option>
      </select>
    </div>
  );
};

export default FilterBar;
