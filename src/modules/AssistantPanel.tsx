import { useState } from 'react';
import { useFocusContext } from '../FocusContext';
import { askAgent } from '../integrations/forgeOpsClient';
import type { AssistantResponse, LoadState } from '../types';

const prompts = [
  { key: 'evidence' as const, label: 'Show me the evidence' },
  { key: 'machine' as const, label: 'Why not Machine 7?' },
  { key: 'compare' as const, label: 'Compare the options' },
  { key: 'report' as const, label: 'Generate manager report' },
];

export function AssistantPanel({ onOpenDecision }: { onOpenDecision: () => void }) {
  const { focus, focusEvidenceRefs } = useFocusContext();
  const [status, setStatus] = useState<LoadState>('idle');
  const [response, setResponse] = useState<AssistantResponse | null>(null);
  const [traceOpen, setTraceOpen] = useState(false);
  const [reportOpen, setReportOpen] = useState(false);

  const runPrompt = async (key: keyof typeof import('../mockData').assistantResponses) => {
    setStatus('loading');
    const result = await askAgent(key);
    setResponse(result);
    setStatus('success');
    focusEvidenceRefs(result.evidenceRefs, result.conclusion);
    if (key === 'compare') onOpenDecision();
    if (key === 'report') setReportOpen(true);
  };

  return (
    <>
      <aside className="assistant-panel">
        <header className="assistant-header">
          <div className="assistant-identity">
            <span className="assistant-orb"><i /><i /></span>
            <div><strong>AI Engineer</strong><small><i /> MCP connected</small></div>
          </div>
          <span className="assistant-mode-label">Read-only tools</span>
        </header>

        <div className="assistant-context-strip">
          <span>Context</span>
          <strong>{focus.pinned ? `Pinned at +${focus.timeMinute} min` : focus.eventId ?? 'Incident overview'}</strong>
          <small>{focus.graphNodeIds.length} graph node{focus.graphNodeIds.length === 1 ? '' : 's'} · {focus.evidenceIds.length} evidence refs</small>
        </div>

        <div className="assistant-conversation" aria-live="polite">
          {!response && status !== 'loading' && (
            <div className="assistant-intro">
              <span className="assistant-orb small"><i /><i /></span>
              <p>I’m anchored to <strong>INC-2407-001</strong>. I can explain the causal chain, compare interventions, focus evidence, and prepare a decision brief.</p>
            </div>
          )}
          {status === 'loading' && (
            <div className="assistant-thinking">
              <span className="assistant-orb small"><i /><i /></span>
              <div><strong>Investigating across MCP tools</strong><p>Retrieving MES, quality, maintenance, and simulation evidence…</p><span><i /><i /><i /></span></div>
            </div>
          )}
          {response && status === 'success' && (
            <div className="assistant-answer">
              <span className="assistant-orb small"><i /><i /></span>
              <div>
                <span className="answer-label">Conclusion</span>
                <h3>{response.conclusion}</h3>
                <p>{response.effect}</p>
                <div className="answer-confidence">
                  <span><i style={{ width: `${response.confidence * 100}%` }} /></span>
                  <strong>{Math.round(response.confidence * 100)}% confidence</strong>
                </div>
                <div className="assistant-evidence-links">
                  {response.evidenceRefs.map((ref) => (
                    <button key={ref} onClick={() => focusEvidenceRefs([ref], response.conclusion)}>{ref.replace('timeline:', '').replace('graph:', '').replace('sim:', '')} ↗</button>
                  ))}
                </div>
                <details className="assumption-details">
                  <summary>Assumptions ({response.assumptions.length})</summary>
                  <ul>{response.assumptions.map((item) => <li key={item}>{item}</li>)}</ul>
                </details>
              </div>
            </div>
          )}
        </div>

        <div className="assistant-prompts">
          <span>Suggested investigations</span>
          {prompts.map((prompt) => (
            <button key={prompt.key} onClick={() => runPrompt(prompt.key)} disabled={status === 'loading'}>
              {prompt.label}<span>→</span>
            </button>
          ))}
        </div>

        {response && (
          <div className="assistant-actions">
            <button className="secondary-button compact" onClick={() => focusEvidenceRefs(response.evidenceRefs, response.conclusion)}>Focus evidence</button>
            <button className="primary-button compact" onClick={() => response.actions.includes('generate_report') ? setReportOpen(true) : onOpenDecision()}>
              {response.actions.includes('generate_report') ? 'Open brief' : 'Open decision'}
            </button>
          </div>
        )}

        <div className="tool-trace">
          <button onClick={() => setTraceOpen((value) => !value)} aria-expanded={traceOpen}>
            <span><i /> MCP tool trace</span>
            <strong>{response?.toolTrace.length ?? 0} calls {traceOpen ? '⌃' : '⌄'}</strong>
          </button>
          {traceOpen && (
            <ol>
              {(response?.toolTrace ?? []).map((step) => (
                <li key={step.id}>
                  <i />
                  <div><span>{step.server}</span><strong>{step.tool}</strong><small>{step.records.join(', ')}</small></div>
                  <time>{step.durationMs} ms</time>
                </li>
              ))}
              {!response && <li className="trace-empty">Run an investigation to populate the audit trail.</li>}
            </ol>
          )}
        </div>
      </aside>

      {reportOpen && (
        <div className="modal-backdrop report-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) setReportOpen(false); }}>
          <article className="report-modal" role="dialog" aria-modal="true" aria-labelledby="report-title">
            <header>
              <div><p className="section-kicker">Plant manager brief · Draft</p><h2 id="report-title">Yield degradation — Batch B-2407-184</h2></div>
              <button className="icon-button" onClick={() => setReportOpen(false)} aria-label="Close report preview">×</button>
            </header>
            <div className="report-summary">
              <span>Decision required</span>
              <h3>Reduce the inter-stage queue delay below 60 minutes.</h3>
              <p>Predicted yield improves from 82% to 96% with low implementation cost and approximately two hours of scheduling effort.</p>
            </div>
            <div className="report-columns">
              <section><span>What happened</span><p>Batch B-2407-184 waited 198 minutes before Machine 7 while queue-area humidity was elevated. Temperature drift and defects followed; final yield was 82%.</p></section>
              <section><span>Why this action</span><p>Queue-delay reduction produces a 14-point predicted recovery. Replacing Machine 7 alone produces only two points and adds significant downtime.</p></section>
              <section><span>Business impact</span><p>Estimated ₹15L monthly loss avoided, 41% downtime reduction, and immediate payback through a scheduling change.</p></section>
              <section><span>Evidence & confidence</span><p>96% confidence · 327 comparable batches · MES queue event · maintenance records · quality inspection · simulation run 014.</p></section>
            </div>
            <div className="report-guardrail"><strong>Approval status</strong><p>Draft only. An authorized shift or plant manager must approve before any operational action or notification.</p></div>
            <footer>
              <button className="secondary-button" onClick={() => window.print()}>Print / save PDF</button>
              <button className="primary-button" onClick={() => setReportOpen(false)}>Return to workbench</button>
            </footer>
          </article>
        </div>
      )}
    </>
  );
}
