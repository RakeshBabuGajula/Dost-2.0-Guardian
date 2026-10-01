import React, { useState } from 'react';
import { Bot, Send, ShieldCheck, FileText, Search, BookOpen, AlertCircle, X, Check, Copy } from 'lucide-react';
import { queryAIAssistant, generateAIReport, searchKnowledgeBase, AIQueryResponse, AIReportResponse, SafetyDoc } from '../../services/aiApi';

interface AIAssistantDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AIAssistantDrawer: React.FC<AIAssistantDrawerProps> = ({ isOpen, onClose }) => {
  const [activeTab, setActiveTab] = useState<'QUERY' | 'REPORT' | 'SOP'>('QUERY');
  const [queryInput, setQueryInput] = useState('');
  const [queryResult, setQueryResult] = useState<AIQueryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [reportType, setReportType] = useState('DAILY_SAFETY_SUMMARY');
  const [reportResult, setReportResult] = useState<AIReportResponse | null>(null);
  const [sopQuery, setSopQuery] = useState('');
  const [sopResults, setSopResults] = useState<SafetyDoc[]>([]);
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const handleQuerySubmit = async (e?: React.FormEvent, customQuery?: string) => {
    if (e) e.preventDefault();
    const q = customQuery || queryInput;
    if (!q.trim()) return;

    setIsLoading(true);
    try {
      const res = await queryAIAssistant(q);
      setQueryResult(res);
    } catch (err) {
      setQueryResult({
        query: q,
        status: 'ERROR',
        answer_type: 'AI-GENERATED ANALYSIS',
        answer: 'Failed to connect to backend AI Analytics service. Using offline operational database fallback.',
        disclaimer: 'AI is an analytical assistant only.',
        data_sources: ['Offline Cache'],
        timestamp: new Date().toISOString(),
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleReportGenerate = async () => {
    setIsLoading(true);
    try {
      const res = await generateAIReport(reportType, 'today');
      setReportResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSopSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const docs = await searchKnowledgeBase(sopQuery);
      setSopResults(docs);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const copyReportToClipboard = () => {
    if (reportResult) {
      navigator.clipboard.writeText(reportResult.markdown_content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="fixed inset-y-0 right-0 w-full sm:w-[520px] bg-[#0D131F] border-l border-cyan-500/30 shadow-2xl z-50 flex flex-col font-sans">
      {/* Drawer Header */}
      <div className="p-4 bg-[#121826] border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-cyan-500/20 text-cyan-400">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-100 font-mono tracking-wide flex items-center gap-2">
              DOST GUARDIAN AI ASSISTANT
              <span className="px-2 py-0.5 text-[10px] bg-cyan-500/20 text-cyan-300 rounded font-mono">
                GROUNDED
              </span>
            </h2>
            <p className="text-[11px] text-slate-400">Operational intelligence, grounded queries & reports</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="p-1.5 text-slate-400 hover:text-slate-100 rounded-lg hover:bg-slate-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Safety Policy Disclaimer Banner */}
      <div className="px-4 py-2.5 bg-[#090D16] border-b border-slate-800 flex items-center space-x-2 text-[11px] text-amber-300 font-mono">
        <ShieldCheck className="w-4 h-4 text-amber-400 shrink-0" />
        <span>AI is assistive only. SafetyEngine is authoritative for safety decisions.</span>
      </div>

      {/* Tab Navigation */}
      <div className="flex border-b border-slate-800 bg-[#121826]">
        <button
          onClick={() => setActiveTab('QUERY')}
          className={`flex-1 py-2.5 text-xs font-mono font-bold flex items-center justify-center gap-2 border-b-2 transition-colors ${
            activeTab === 'QUERY'
              ? 'border-cyan-400 text-cyan-400 bg-cyan-500/10'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Bot className="w-4 h-4" />
          NL QUERY
        </button>
        <button
          onClick={() => setActiveTab('REPORT')}
          className={`flex-1 py-2.5 text-xs font-mono font-bold flex items-center justify-center gap-2 border-b-2 transition-colors ${
            activeTab === 'REPORT'
              ? 'border-cyan-400 text-cyan-400 bg-cyan-500/10'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <FileText className="w-4 h-4" />
          REPORTS
        </button>
        <button
          onClick={() => setActiveTab('SOP')}
          className={`flex-1 py-2.5 text-xs font-mono font-bold flex items-center justify-center gap-2 border-b-2 transition-colors ${
            activeTab === 'SOP'
              ? 'border-cyan-400 text-cyan-400 bg-cyan-500/10'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <BookOpen className="w-4 h-4" />
          SAFETY SOP
        </button>
      </div>

      {/* Tab Content Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {activeTab === 'QUERY' && (
          <div className="space-y-4">
            {/* Preset Query Chips */}
            <div className="space-y-2">
              <span className="text-[11px] font-mono text-slate-400 uppercase font-bold">Recommended Operational Queries:</span>
              <div className="flex flex-wrap gap-2">
                {[
                  'How many critical alerts occurred today?',
                  'Which work zones had near misses this week?',
                  'Summarize unresolved alerts',
                  'Show telemetry degradation counts',
                ].map((preset, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setQueryInput(preset);
                      handleQuerySubmit(undefined, preset);
                    }}
                    className="px-2.5 py-1 text-[11px] bg-[#121826] border border-slate-700 hover:border-cyan-500 text-slate-300 hover:text-cyan-300 rounded-lg transition-colors font-mono"
                  >
                    "{preset}"
                  </button>
                ))}
              </div>
            </div>

            {/* Query Result Card */}
            {queryResult && (
              <div className="p-4 bg-[#121826] border border-cyan-500/30 rounded-2xl space-y-3">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <span className="text-[11px] font-mono font-bold text-cyan-400">
                    {queryResult.answer_type}
                  </span>
                  <span className="text-[10px] font-mono text-slate-400">
                    {new Date(queryResult.timestamp).toLocaleTimeString()}
                  </span>
                </div>

                <p className="text-xs text-slate-200 leading-relaxed font-sans">
                  {queryResult.answer}
                </p>

                <div className="space-y-1.5 pt-2 border-t border-slate-800">
                  <span className="text-[10px] font-mono font-bold text-slate-400 uppercase">Grounded Data Sources:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {queryResult.data_sources.map((src, i) => (
                      <span key={i} className="px-2 py-0.5 text-[10px] font-mono bg-slate-900 border border-slate-800 text-cyan-300 rounded">
                        {src}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'REPORT' && (
          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-xs font-mono font-bold text-slate-300 uppercase">Select Report Type:</label>
              <select
                value={reportType}
                onChange={(e) => setReportType(e.target.value)}
                className="w-full bg-[#121826] border border-slate-700 text-slate-200 rounded-xl p-2.5 text-xs font-mono focus:border-cyan-500 outline-none"
              >
                <option value="DAILY_SAFETY_SUMMARY">DAILY SAFETY SUMMARY</option>
                <option value="SHIFT_SUMMARY">SHIFT OPERATIONAL SUMMARY</option>
                <option value="WORK_ZONE_SUMMARY">WORK ZONE INTELLIGENCE REPORT</option>
                <option value="NEAR_MISS_SUMMARY">NEAR-MISS INCIDENT SUMMARY</option>
                <option value="ALERT_SUMMARY">ALERT LIFECYCLE AUDIT REPORT</option>
              </select>

              <button
                onClick={handleReportGenerate}
                disabled={isLoading}
                className="w-full py-2.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl text-xs font-mono font-bold transition-colors flex items-center justify-center gap-2"
              >
                <FileText className="w-4 h-4" />
                {isLoading ? 'GENERATING GROUNDED REPORT...' : 'GENERATE OPERATIONAL REPORT'}
              </button>
            </div>

            {reportResult && (
              <div className="p-4 bg-[#121826] border border-slate-800 rounded-2xl space-y-3">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <span className="text-xs font-mono font-bold text-slate-100">{reportResult.title}</span>
                  <button
                    onClick={copyReportToClipboard}
                    className="p-1.5 bg-slate-800 hover:bg-slate-700 text-cyan-400 rounded-lg text-[10px] font-mono flex items-center gap-1"
                  >
                    {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    {copied ? 'COPIED' : 'COPY'}
                  </button>
                </div>

                <div className="text-xs text-slate-300 font-mono bg-[#090D16] p-3 rounded-xl max-h-72 overflow-y-auto whitespace-pre-wrap">
                  {reportResult.markdown_content}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'SOP' && (
          <div className="space-y-4">
            <form onSubmit={handleSopSearch} className="flex gap-2">
              <input
                type="text"
                value={sopQuery}
                onChange={(e) => setSopQuery(e.target.value)}
                placeholder="Search safety procedures (e.g. clearance, TTD)..."
                className="flex-1 bg-[#121826] border border-slate-700 text-slate-100 rounded-xl px-3 py-2 text-xs font-mono focus:border-cyan-500 outline-none"
              />
              <button
                type="submit"
                className="px-4 bg-slate-800 hover:bg-slate-700 text-cyan-400 rounded-xl text-xs font-mono font-bold"
              >
                <Search className="w-4 h-4" />
              </button>
            </form>

            <div className="space-y-3">
              {sopResults.map((doc) => (
                <div key={doc.id} className="p-3 bg-[#121826] border border-slate-800 rounded-xl space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-cyan-400 font-mono">{doc.title}</span>
                    <span className="px-2 py-0.5 text-[10px] font-mono bg-cyan-500/20 text-cyan-300 rounded">
                      {doc.category}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed font-sans">{doc.content}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Input Bar for Query Tab */}
      {activeTab === 'QUERY' && (
        <form onSubmit={handleQuerySubmit} className="p-3 bg-[#121826] border-t border-slate-800 flex gap-2">
          <input
            type="text"
            value={queryInput}
            onChange={(e) => setQueryInput(e.target.value)}
            placeholder="Ask operational AI (e.g. How many near misses today?)..."
            className="flex-1 bg-[#090D16] border border-slate-700 text-slate-100 rounded-xl px-3 py-2 text-xs font-mono focus:border-cyan-500 outline-none"
          />
          <button
            type="submit"
            disabled={isLoading || !queryInput.trim()}
            className="px-4 bg-cyan-600 hover:bg-cyan-500 disabled:bg-slate-800 text-white rounded-xl text-xs font-mono font-bold transition-colors flex items-center justify-center"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      )}
    </div>
  );
};
