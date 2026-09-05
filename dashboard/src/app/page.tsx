import data from './data.json';

export default function Home() {
  const totalCases = data.length;
  const totalRisk = data.reduce((acc, curr) => acc + (curr.amount || 0), 0);
  const totalRecovered = data.reduce((acc, curr) => acc + (curr.recovered_amount || 0), 0);
  const recoveryRate = totalRisk > 0 ? ((totalRecovered / totalRisk) * 100).toFixed(2) : '0';

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-8 font-sans">
      <header className="mb-8 border-b border-slate-800 pb-4 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-blue-400">RecoveryOS Dashboard</h1>
          <p className="text-slate-400 text-sm mt-1">Autonomous Revenue Recovery & Policy Guardrails</p>
        </div>
        <div className="bg-blue-950 border border-blue-800 text-blue-300 text-xs px-3 py-1 rounded-full font-mono">
          System Status: ACTIVE
        </div>
      </header>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="text-slate-400 text-xs font-semibold uppercase">Total Revenue at Risk</div>
          <div className="text-2xl font-bold text-white mt-1">₹{totalRisk.toLocaleString()}</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="text-slate-400 text-xs font-semibold uppercase">Simulated Recovered</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">₹{totalRecovered.toLocaleString()}</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="text-slate-400 text-xs font-semibold uppercase">Recovery Rate</div>
          <div className="text-2xl font-bold text-blue-400 mt-1">{recoveryRate}%</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="text-slate-400 text-xs font-semibold uppercase">Cases Processed</div>
          <div className="text-2xl font-bold text-white mt-1">{totalCases}</div>
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-slate-800 font-semibold text-slate-200">
          Active Recovery Cases & Audit Trail
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950 text-slate-400 border-b border-slate-800 uppercase font-mono">
              <tr>
                <th className="p-3">Payment ID</th>
                <th className="p-3">Amount</th>
                <th className="p-3">Failure Reason</th>
                <th className="p-3">ML Score</th>
                <th className="p-3">Policy Action</th>
                <th className="p-3">Policy Rule</th>
                <th className="p-3">Razorpay Link / Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {data.map((item: any) => (
                <tr key={item.payment_id} className="hover:bg-slate-800/50 transition-colors">
                  <td className="p-3 font-mono text-blue-400">{item.payment_id}</td>
                  <td className="p-3 font-semibold text-white">₹{item.amount}</td>
                  <td className="p-3 text-slate-300">{item.failure_reason}</td>
                  <td className="p-3 font-mono">
                    <span className={`px-2 py-0.5 rounded ${item.ml_predicted_recovery_prob > 0.5 ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-amber-950 text-amber-400 border border-amber-800'}`}>
                      {(item.ml_predicted_recovery_prob * 100).toFixed(0)}%
                    </span>
                  </td>
                  <td className="p-3 font-mono font-semibold text-indigo-300">{item.policy_action}</td>
                  <td className="p-3 text-slate-400 text-[11px] max-w-xs truncate">{item.policy_rule}</td>
                  <td className="p-3 font-mono">
                    {item.short_url ? (
                      <a href={item.short_url} target="_blank" rel="noreferrer" className="text-blue-400 hover:underline">
                        {item.short_url}
                      </a>
                    ) : (
                      <span className="text-slate-500">{item.execution_notes || '-'}</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}