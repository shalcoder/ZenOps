import { useState } from 'react';
import { FocusProvider } from './FocusContext';
import { HomeDashboard } from './modules/HomeDashboard';
import { Workbench } from './modules/Workbench';

function BrandMark() {
  return (
    <div className="brand-mark" aria-hidden="true">
      <span />
      <span />
      <span />
    </div>
  );
}

function App() {
  const [view, setView] = useState<'dashboard' | 'workbench'>('dashboard');

  return (
    <FocusProvider>
      <div className="app-shell">
        <header className="app-header">
          <button className="brand-button" onClick={() => setView('dashboard')} aria-label="Go to ForgeOps dashboard">
            <BrandMark />
            <span>
              <strong>FORGE<span>OPS</span></strong>
              <small>Decision intelligence</small>
            </span>
          </button>
          <div className="header-context">
            <span className="live-indicator"><i /> Plant Mumbai-1 · Live</span>
            <span className="header-divider" />
            <span className="shift-label">Shift A · 14:32 IST</span>
            <span className="avatar-button" aria-label="Signed in as Vaishak">VK</span>
          </div>
        </header>

        {view === 'dashboard'
          ? <HomeDashboard onOpen={() => setView('workbench')} />
          : <Workbench onBack={() => setView('dashboard')} />}
      </div>
    </FocusProvider>
  );
}

export default App;
