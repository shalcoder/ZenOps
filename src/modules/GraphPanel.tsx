import { useMemo, useState } from 'react';
import { useFocusContext } from '../FocusContext';
import { useWorkbenchData } from '../WorkbenchDataContext';

export function GraphPanel() {
  const { focus, focusGraphNode } = useFocusContext();
  const { data } = useWorkbenchData();
  const { graphEdges, graphNodes } = data;
  const [hideWeak, setHideWeak] = useState(true);
  const [afterIntervention, setAfterIntervention] = useState(false);

  const visibleEdges = useMemo(
    () => graphEdges.filter((edge) => !hideWeak || edge.strength >= 0.2),
    [hideWeak],
  );
  const nodeById = (id: string) => graphNodes.find((node) => node.id === id)!;

  return (
    <section className="module-panel graph-panel">
      <header className="module-header compact-header">
        <div>
          <p className="section-kicker">Module 03</p>
          <h2>Root cause graph</h2>
          <span>Influence, evidence type, and confidence</span>
        </div>
        <div className="graph-controls">
          <button className={`toggle-button${hideWeak ? ' active' : ''}`} onClick={() => setHideWeak((value) => !value)}><i /> Hide weak</button>
          <button className={`toggle-button${afterIntervention ? ' active' : ''}`} onClick={() => setAfterIntervention((value) => !value)}><i /> Post-intervention</button>
        </div>
      </header>

      <div className={`graph-canvas${afterIntervention ? ' intervention' : ''}`}>
        <svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
          <defs>
            <marker id="arrow-observed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
              <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#889da5" />
            </marker>
            <marker id="arrow-estimated" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
              <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="var(--amber)" />
            </marker>
            <marker id="arrow-simulated" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
              <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="var(--teal)" />
            </marker>
          </defs>
          {visibleEdges.map((edge) => {
            const from = nodeById(edge.from);
            const to = nodeById(edge.to);
            const faded = afterIntervention && edge.from === 'node_queue_delay';

            // Calculate anchor points (node width is ~15.2%, node center height offset is ~10.8%)
            const nodeW = 15.2;
            const nodeH = 10.8;

            const x1 = from.position.x + nodeW;
            const y1 = from.position.y + nodeH;
            const x2 = to.position.x;
            const y2 = to.position.y + nodeH;

            const dx = Math.max(6, Math.abs(x2 - x1) * 0.45);
            const pathData = `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;

            let markerUrl = 'url(#arrow-observed)';
            if (edge.evidenceType === 'model_estimated') markerUrl = 'url(#arrow-estimated)';
            if (edge.evidenceType === 'counterfactual_simulated') markerUrl = 'url(#arrow-simulated)';

            return (
              <path
                key={edge.id}
                d={pathData}
                className={`${edge.evidenceType}${faded ? ' faded' : ''}`}
                strokeWidth={Math.max(0.6, edge.strength * 1.5)}
                markerEnd={markerUrl}
              />
            );
          })}
        </svg>
        {graphNodes.map((node) => {
          const active = focus.graphNodeIds.includes(node.id);
          const aiActive = active && focus.origin === 'assistant';
          const reduced = afterIntervention && node.id === 'node_queue_delay';
          return (
            <button
              key={node.id}
              className={`cause-node type-${node.type}${active ? ' active' : ''}${aiActive ? ' ai-active' : ''}${reduced ? ' reduced' : ''}`}
              style={{ left: `${node.position.x}%`, top: `${node.position.y}%` }}
              onClick={() => focusGraphNode(node.id)}
              aria-pressed={active}
            >
              <span className="cause-node-top"><i /> {node.controllable ? 'Controllable' : node.source}</span>
              <strong>{node.label}</strong>
              <em>{reduced ? '< 60 min' : node.value}</em>
              <small>{Math.round((reduced ? 0.16 : node.influence) * 100)}% influence · {Math.round(node.confidence * 100)}% conf.</small>
            </button>
          );
        })}
      </div>
      <div className="graph-legend">
        <span><i className="edge observed" /> Observed</span>
        <span><i className="edge estimated" /> Model-estimated</span>
        <span><i className="edge simulated" /> Counterfactual</span>
        {afterIntervention && <strong>Queue-delay influence reduced after intervention</strong>}
      </div>
    </section>
  );
}
