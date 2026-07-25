import { useState } from 'react';
import { useFocusContext } from '../FocusContext';
import { featuredIncident } from '../mockData';
import { AssistantPanel } from './AssistantPanel';
import { EvidencePanel } from './EvidencePanel';
import { GraphPanel } from './GraphPanel';
import { RecommendationsPanel } from './RecommendationsPanel';
import { ReplayPanel } from './ReplayPanel';
import { SimulatorPanel } from './SimulatorPanel';
import { TimelinePanel } from './TimelinePanel';

export function Workbench({ onBack }: { onBack: () => void }) {
  const { focus, clearFocus } = useFocusContext();
  const [activeTab, setActiveTab] = useState<'investigate' | 'decide'>('investigate');

  return (
    <main className="workbench-page">
      <nav className="workbench-breadcrumb" aria-label="Breadcrumb">
        <button onClick={onBack}>Incidents</button>
        <span>/</span>
        <span>{featuredIncident.id}</span>
        <span>/</span>
        <strong>Decision workbench</strong>
      </nav>

      <section className="incident-command-bar">
        <div className="incident-command-title">
          <span className="severity-label high">High severity</span>
          <div>
            <h1>{featuredIncident.title} · {featuredIncident.batchId}</h1>
            <p>{featuredIncident.plant} · {featuredIncident.line} · Yield <strong>96% → 82%</strong></p>
          </div>
        </div>
        <div className="command-status">
          <div>
            <span>Investigation state</span>
            <strong><i className="dot warning" /> Evidence review</strong>
          </div>
          <div>
            <span>Current focus</span>
            <strong>{focus.aiLabel ?? (focus.pinned ? 'Pinned replay moment' : focus.eventId ?? 'Batch overview')}</strong>
          </div>
          <button className="icon-button" onClick={clearFocus} title="Reset workbench focus" aria-label="Reset workbench focus">↺</button>
        </div>
      </section>

      <div className="workbench-tabs" role="tablist" aria-label="Workbench mode">
        <button className={activeTab === 'investigate' ? 'active' : ''} onClick={() => setActiveTab('investigate')}>01 · Investigate</button>
        <button className={activeTab === 'decide' ? 'active' : ''} onClick={() => setActiveTab('decide')}>02 · Decide</button>
        <span className="contract-badge">Integrated tool API · 6 modules</span>
      </div>

      <div className="workbench-with-assistant">
        <div className="workbench-main">
          {activeTab === 'investigate' ? (
            <>
              <TimelinePanel />
              <div className="analysis-grid">
                <ReplayPanel />
                <GraphPanel />
              </div>
              <EvidencePanel />
            </>
          ) : (
            <>
              <SimulatorPanel />
              <RecommendationsPanel />
              <EvidencePanel />
            </>
          )}
        </div>
        <AssistantPanel onOpenDecision={() => setActiveTab('decide')} />
      </div>
    </main>
  );
}
