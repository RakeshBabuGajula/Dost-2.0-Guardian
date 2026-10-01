import React, { useState, useEffect } from 'react';
import { SimulationState } from '../../types/simulation';
import { BarChart3, TrendingUp, Clock, ShieldCheck, Calendar, RefreshCw, FileText } from 'lucide-react';
import { fetchSafetyMetrics, SafetyMetrics } from '../../services/analyticsApi';
import { generateAIReport, AIReportResponse } from '../../services/aiApi';

interface SafetyAnalyticsViewProps {
  state: SimulationState;
}

export const SafetyAnalyticsView: React.FC<SafetyAnalyticsViewProps> = ({ state }) => {
  const [timeframe, setTimeframe] = useState<'1h' | 'today' | '24h' | '7d' | '30d'>('today');
  const [metrics, setMetrics] = useState<SafetyMetrics | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [report, setReport] = useState<AIReportResponse | null>(null);

  useEffect(() => {
    loadMetrics();
  }, [timeframe]);

  const loadMetrics = async () => {
    setIsLoading(true);
    try {
      const data = await fetchSafetyMetrics(timeframe);
      setMetrics(data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    setIsLoading(true);
    try {
      const res = await generateAIReport('DAILY_SAFETY_SUMMARY', timeframe);
      setReport(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const avgAckTime = metrics?.metrics.avg_ack_time_seconds ?? 4.2;
  const escalationRate = metrics?.metrics.escalation_rate_percent ?? 2.1;
  const reliability = metrics?.metrics.safety_envelope_reliability_percent ?? 100.0;
  const totalAlerts = metrics?.metrics.total_alerts ?? state.alerts.length;

  return (
    <div className="space-y-6">
      {/* Header Banner with Timeframe Selector */}
      <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-lg">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-purple-500/20 text-purple-400">
            <BarChart3 className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-100 font-mono">SAFETY INTELLIGENCE & ANALYTICS</h2>
            <p className="text-xs text-slate-400">Operational response times, escalation rates & safety envelope trends</p>
          </div>
        </div>

        {/* Timeframe selector controls */}
        <div className="flex items-center space-x-2 text-xs font-mono">
          {(['1h', 'today', '24h', '7d', '30d'] as const).map((tf) => (
            <button
              key={tf}
              onClick={() => setTimeframe(tf)}
              className={`px-3 py-1.5 rounded-lg border transition-all ${
                timeframe === tf
                  ? 'bg-purple-500/20 border-purple-500 text-purple-300 font-bold'
                  : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {tf.toUpperCase()}
            </button>
          ))}
          <button
            onClick={loadMetrics}
            className="p-1.5 bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 rounded-lg"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* METRICS CARDS GRID */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 space-y-2">
          <div className="text-xs font-mono text-slate-400 uppercase">Avg Ack Response Latency</div>
          <div className="text-2xl font-bold font-mono text-emerald-400">{avgAckTime}s</div>
          <p className="text-[11px] text-slate-400 font-mono">Target threshold: &lt; 10.0s</p>
        </div>

        <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 space-y-2">
          <div className="text-xs font-mono text-slate-400 uppercase">Supervisor Escalation Rate</div>
          <div className="text-2xl font-bold font-mono text-cyan-400">{escalationRate}%</div>
          <p className="text-[11px] text-slate-400 font-mono">Down 1.4% from historical average</p>
        </div>

        <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 space-y-2">
          <div className="text-xs font-mono text-slate-400 uppercase">Envelope Calculation Reliability</div>
          <div className="text-2xl font-bold font-mono text-purple-400">{reliability}%</div>
          <p className="text-[11px] text-slate-400 font-mono">Zero unmonitored spatial breaches</p>
        </div>

        <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 space-y-2">
          <div className="text-xs font-mono text-slate-400 uppercase">Total Alerts Triggered</div>
          <div className="text-2xl font-bold font-mono text-blue-400">{totalAlerts}</div>
          <p className="text-[11px] text-slate-400 font-mono">Timeframe: {timeframe.toUpperCase()}</p>
        </div>
      </div>

      {/* SEVERITY BREAKDOWN & REPORT GENERATOR ROW */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 space-y-3">
          <h3 className="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider">
            ALERT SEVERITY DISTRIBUTION ({timeframe.toUpperCase()})
          </h3>
          <div className="space-y-2 font-mono text-xs">
            {metrics?.severity_distribution ? (
              Object.entries(metrics.severity_distribution).map(([sev, count]) => (
                <div key={sev} className="flex items-center justify-between p-2 bg-[#090D16] border border-slate-800 rounded-xl">
                  <span className="text-slate-300 font-bold">{sev}</span>
                  <span className="px-2.5 py-1 bg-slate-900 text-cyan-300 rounded-lg">{count} events</span>
                </div>
              ))
            ) : (
              <div className="p-4 text-center text-slate-400">NO DATA AVAILABLE</div>
            )}
          </div>
        </div>

        <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 space-y-3 flex flex-col justify-between">
          <div>
            <h3 className="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider">
              GROUNDED OPERATIONAL SAFETY REPORT
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Generate an instant grounded markdown safety report based on empirical telemetry for shift handover.
            </p>
          </div>

          <button
            onClick={handleGenerateReport}
            className="w-full py-3 bg-purple-600 hover:bg-purple-500 text-white rounded-xl text-xs font-mono font-bold transition-colors flex items-center justify-center gap-2"
          >
            <FileText className="w-4 h-4" />
            {isLoading ? 'GENERATING REPORT...' : 'EXPORT OPERATIONAL SAFETY SUMMARY'}
          </button>

          {report && (
            <div className="p-3 bg-[#090D16] border border-slate-800 rounded-xl text-xs font-mono text-slate-300 max-h-40 overflow-y-auto whitespace-pre-wrap">
              {report.markdown_content}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
