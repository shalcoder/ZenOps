import { useMemo, useState } from 'react';
import { incidents } from '../mockData';

const formatInr = (value: number) => `₹${(value / 100000).toFixed(value >= 1000000 ? 0 : 1)}L`;

export function HomeDashboard({ onOpen }: { onOpen: () => void }) {
  const [plant, setPlant] = useState('All plants');
  const [status, setStatus] = useState('All statuses');
  const filtered = useMemo(() => incidents.filter((incident) => {
    const plantMatch = plant === 'All plants' || incident.plant === plant;
    const statusMatch = status === 'All statuses' || incident.status === status;
    return plantMatch && statusMatch;
  }), [plant, status]);

  return (
    <main className="dashboard-page">
      <section className="dashboard-hero">
        <div>
          <p className="section-kicker">Production overview</p>
          <h1>Good afternoon, Vaishak.</h1>
          <p>Three production signals need attention. One requires an evidence-backed decision.</p>
        </div>
        <div className="hero-actions">
          <button className="secondary-button" onClick={() => window.print()}>
            <span className="button-icon">↗</span>
            Export shift brief
          </button>
          <button className="primary-button" onClick={onOpen}>
            Open priority incident
            <span>→</span>
          </button>
        </div>
      </section>

      <section className="metric-grid" aria-label="Production KPIs">
        <article className="metric-card metric-critical">
          <div className="metric-topline"><span>Yield</span><span className="metric-delta negative">↓ 14.0 pts</span></div>
          <strong>82.0<span>%</span></strong>
          <div className="mini-bars" aria-label="Yield trend">
            {[68, 72, 75, 70, 62, 49, 42, 36].map((height, index) => <i key={index} style={{ height: `${height}%` }} />)}
          </div>
          <small>Target 96% · Assembly Line 3</small>
        </article>
        <article className="metric-card">
          <div className="metric-topline"><span>Overall equipment effectiveness</span><span className="metric-delta positive">↑ 1.8%</span></div>
          <strong>88.4<span>%</span></strong>
          <div className="progress-track"><i style={{ width: '88.4%' }} /></div>
          <small>Plant target 90%</small>
        </article>
        <article className="metric-card">
          <div className="metric-topline"><span>Active incidents</span><span className="metric-delta neutral">3 open</span></div>
          <strong>03</strong>
          <div className="severity-counts">
            <span><i className="dot critical" />1 high</span>
            <span><i className="dot warning" />1 medium</span>
            <span><i className="dot info" />1 low</span>
          </div>
          <small>1 incident escalated</small>
        </article>
        <article className="metric-card">
          <div className="metric-topline"><span>Machine health</span><span className="metric-delta warning-text">M7 degraded</span></div>
          <strong>89<span>%</span></strong>
          <div className="machine-health-row">
            {[98, 94, 91, 89, 72].map((value, index) => (
              <i key={index} className={value < 80 ? 'warning' : ''} title={`Machine ${index + 3}: ${value}%`} />
            ))}
          </div>
          <small>Machine 7 health score 72%</small>
        </article>
      </section>

      <section className="dashboard-body">
        <div className="incident-section">
          <div className="section-heading">
            <div>
              <p className="section-kicker">Decision queue</p>
              <h2>Active incidents</h2>
            </div>
            <div className="filter-row">
              <label>
                <span className="sr-only">Filter by plant</span>
                <select value={plant} onChange={(event) => setPlant(event.target.value)}>
                  <option>All plants</option>
                  <option>Plant Mumbai-1</option>
                  <option>Plant Pune-2</option>
                </select>
              </label>
              <label>
                <span className="sr-only">Filter by status</span>
                <select value={status} onChange={(event) => setStatus(event.target.value)}>
                  <option>All statuses</option>
                  <option value="open">Open</option>
                  <option value="investigating">Investigating</option>
                  <option value="monitoring">Monitoring</option>
                </select>
              </label>
            </div>
          </div>

          <div className="incident-list">
            {filtered.map((incident, index) => (
              <article key={incident.id} className={`incident-row${index === 0 ? ' priority' : ''}`}>
                <div className={`severity-rail ${incident.severity}`} />
                <div className="incident-main">
                  <div className="incident-title-row">
                    <div>
                      <span className={`severity-label ${incident.severity}`}>{incident.severity}</span>
                      <span className="incident-id">{incident.id}</span>
                    </div>
                    <span className={`status-label ${incident.status}`}>{incident.status}</span>
                  </div>
                  <h3>{incident.title}</h3>
                  <p>{incident.summary}</p>
                  <div className="incident-meta">
                    <span>{incident.plant}</span>
                    <span>{incident.line}</span>
                    <span>Batch {incident.batchId}</span>
                    <span>{incident.product}</span>
                  </div>
                </div>
                <div className="incident-kpi">
                  <span>Current yield</span>
                  <strong>{incident.currentYield}%</strong>
                  <small>from {incident.baselineYield}%</small>
                </div>
                <div className="incident-exposure">
                  <span>Loss exposure</span>
                  <strong>{formatInr(incident.exposureInr)}</strong>
                  <small>per month</small>
                </div>
                <button className={index === 0 ? 'primary-button compact' : 'secondary-button compact'} onClick={onOpen}>
                  {index === 0 ? 'Open workbench' : 'Review'}
                  <span>→</span>
                </button>
              </article>
            ))}
            {filtered.length === 0 && <div className="empty-state">No incidents match these filters.</div>}
          </div>
        </div>

        <aside className="signal-panel">
          <div className="section-heading">
            <div>
              <p className="section-kicker">Signal stream</p>
              <h2>Recent alerts</h2>
            </div>
            <span className="dataset-label">Golden-path dataset</span>
          </div>
          <ol className="signal-list">
            <li>
              <span className="signal-time">14:28</span>
              <i className="signal-icon sensor">H</i>
              <div><strong>High humidity</strong><p>Queue area · 68.5% RH</p></div>
              <span className="signal-state warning">Warning</span>
            </li>
            <li>
              <span className="signal-time">14:19</span>
              <i className="signal-icon queue">Q</i>
              <div><strong>Conveyor delay</strong><p>Line 2 · +11% cycle time</p></div>
              <span className="signal-state info">Monitor</span>
            </li>
            <li>
              <span className="signal-time">14:12</span>
              <i className="signal-icon machine">M7</i>
              <div><strong>Machine 7 vibration</strong><p>4.7 mm/s · limit 3.5</p></div>
              <span className="signal-state critical">Critical</span>
            </li>
            <li>
              <span className="signal-time">13:56</span>
              <i className="signal-icon quality">Q</i>
              <div><strong>Quality score</strong><p>Batch B-2407-184 · 62.3</p></div>
              <span className="signal-state critical">Failed</span>
            </li>
          </ol>
        </aside>
      </section>
    </main>
  );
}
