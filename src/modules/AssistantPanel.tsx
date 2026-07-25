import { useEffect, useState } from 'react';
import { useFocusContext } from '../FocusContext';
import { askAgent, getRuntimeStatus, type RuntimeStatus } from '../integrations/forgeOpsClient';
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
  const [runtime, setRuntime] = useState<RuntimeStatus | null>(null);

  useEffect(() => {
    let active = true;
    getRuntimeStatus().then((result) => { if (active) setRuntime(result); });
    return () => { active = false; };
  }, []);

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
            <span className="assistant-orb" aria-hidden="true"><i /><i /></span>
            <div>
              <strong>Decision assistant</strong>
              <small className={runtime?.online ? 'online' : runtime ? 'offline' : 'checking'}>
                <i /> {runtime?.online ? 'Live agents online' : runtime ? 'Backend offline' : 'Checking agents'}
              </small>
            </div>
          </div>
          <span className="assistant-mode-label">
            {runtime?.online
              ? `${runtime.agentRoles} LLM roles · ${runtime.orchestratorProcesses} orchestrator · ${runtime.toolCount} MCP tools`
              : 'Offline fallback'}
          </span>
        </header>

        <div className="assistant-context-strip">
          <span>Context</span>
          <strong>{focus.pinned ? `Pinned at +${focus.timeMinute} min` : focus.eventId ?? 'Incident overview'}</strong>
          <small>{focus.graphNodeIds.length} graph nodes · {focus.evidenceIds.length} evidence refs</small>
        </div>

        <div className="assistant-conversation" aria-live="polite">
          {!response && status !== 'loading' && (
            <div className="assistant-intro">
              <span className="assistant-orb small"><i /><i /></span>
              <p>Four specialized NitroCloud agents plan, retrieve live MCP evidence, analyze counterfactuals, and prepare an approval-safe decision for <strong>INC-2407-001</strong>.</p>
            </div>
          )}
          {status === 'loading' && (
            <div className="assistant-thinking">
              <span className="assistant-orb small"><i /><i /></span>
              <div><strong>Running the four-agent investigation</strong><p>Planning, calling MCP tools, analyzing scenarios, and preparing the decision...</p><span><i /><i /><i /></span></div>
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
                <p className="output-footnote">
                  {response.pipelineMode === 'live_nitrocloud'
                    ? `Live NitroCloud reasoning · ${response.model}`
                    : 'Degraded fallback mode · verify before acting'}
                </p>
                <div className="assistant-evidence-links">
                  {response.evidenceRefs.map((ref) => (
                    <button key={ref} onClick={() => focusEvidenceRefs([ref], response.conclusion)}>{ref} ↗</button>
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
          {response?.agentTrace && response.agentTrace.length > 0 && (
            <div className="assistant-context-strip">
              <span>Agent run</span>
              <strong>{response.agentTrace.map((step) => step.agent).join(' → ')}</strong>
              <small>{response.agentTrace.map((step) => `${step.agent}: ${step.status}`).join(' · ')}</small>
            </div>
          )}
          <button onClick={() => setTraceOpen((value) => !value)} aria-expanded={traceOpen}>
            <span><i /> Live MCP tool trace</span>
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
              <h3>{response?.conclusion ?? 'Review the agent recommendation.'}</h3>
              <p>{response?.effect}</p>
            </div>
            <div className="report-columns">
              <section><span>Evidence</span><p>{response?.evidenceRefs.join(' · ')}</p></section>
              <section><span>Confidence</span><p>{Math.round((response?.confidence ?? 0) * 100)}% based on live MCP evidence and scenario analysis.</p></section>
            </div>
            <div className="report-guardrail"><strong>Approval status</strong><p>Draft only. An authorized manager must approve before any operational action or notification.</p></div>
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
