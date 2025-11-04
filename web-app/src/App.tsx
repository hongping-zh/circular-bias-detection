import React, { useState, useCallback, useMemo } from 'react';
import { generateJossReview, generatePrFollowupAdvice, generateCodeOptimizationAdvice } from './services/geminiService';
import type { ReviewSection, JossReview } from './types';

// --- ICONS ---
const GithubIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => ( <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>);
const BotIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => ( <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><path d="M12 8V4H8" /><rect width="16" height="12" x="4" y="8" rx="2" /><path d="M2 14h2" /><path d="M20 14h2" /><path d="M15 13v2" /><path d="M9 13v2" /></svg>);
const SpinnerIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="animate-spin" {...props}><path d="M21 12a9 9 0 1 1-6.219-8.56" /></svg>);
const ChevronDownIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><path d="m6 9 6 6 6-6"/></svg>);
const ClipboardIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/></svg>);
const CheckCircleIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>);
const AlertTriangleIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><path d="m21.73 18-8-14a2 2 0 0 0-3.46 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>);
const XCircleIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/></svg>);
const PullRequestIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><path d="M6 9v12"/></svg>);
const PaperIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>);
const ExternalLinkIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>);
const CodeIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>);


// --- UI COMPONENTS ---

const formatLine = (line: string): string => {
  return line
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/__(.*?)__/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/_(.*?)_/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code class="bg-slate-200 dark:bg-slate-700 rounded px-1 py-0.5 text-sm font-mono text-emerald-500">$1</code>');
};

const MarkdownRenderer: React.FC<{ content: string }> = ({ content }) => {
  const sections = content.split(/(```[\s\S]*?```)/g);

  return (
    <div className="space-y-3 text-slate-600 dark:text-slate-300 text-sm leading-relaxed">
      {sections.map((section, i) => {
        if (section.startsWith('```')) {
          const code = section.replace(/```/g, '').trim();
          return (
            <pre key={i} className="bg-slate-100 dark:bg-slate-900/50 p-4 rounded-lg overflow-x-auto">
              <code className="font-mono text-xs">{code}</code>
            </pre>
          );
        }
        return (
          <div key={i}>
            {section.trim().split('\n').map((line, j) => {
              const trimmedLine = line.trim();
              if (trimmedLine.startsWith('- ') || trimmedLine.startsWith('* ')) {
                const liContent = trimmedLine.substring(2);
                return (
                  <ul key={j} className="list-disc pl-5">
                    <li dangerouslySetInnerHTML={{ __html: formatLine(liContent) }} />
                  </ul>
                );
              }
              if (trimmedLine.length === 0) return null;
              return <p key={j} dangerouslySetInnerHTML={{ __html: formatLine(line) }} />;
            })}
          </div>
        );
      })}
    </div>
  );
};

const AccordionItem: React.FC<{ section: ReviewSection; index: number }> = ({ section, index }) => {
  const [isOpen, setIsOpen] = useState(false);
  const { icon, color, title } = useMemo(() => {
    let icon, color, title = section.title;
    if (title.includes('✅')) {
      icon = <CheckCircleIcon className="w-6 h-6 text-green-500" />;
      color = 'border-green-500/50';
    } else if (title.includes('⚠️')) {
      icon = <AlertTriangleIcon className="w-6 h-6 text-amber-500" />;
      color = 'border-amber-500/50';
    } else if (title.includes('❌')) {
      icon = <XCircleIcon className="w-6 h-6 text-red-500" />;
      color = 'border-red-500/50';
    } else {
      icon = <div className="w-6 h-6"></div>; // Placeholder for alignment
      color = 'border-slate-300 dark:border-slate-700';
    }
    title = title.replace(/([✅⚠️❌📄⚙️📖📚📝🧪🤝📜🚀])/g, '').trim();
    return { icon, color, title };
  }, [section.title]);

  return (
    <div className={`border-l-4 rounded-r-lg bg-white dark:bg-slate-800/50 overflow-hidden transition-all duration-300 fade-in shadow-md hover:shadow-lg ${color}`} style={{ animationDelay: `${index * 50}ms` }}>
      <button onClick={() => setIsOpen(!isOpen)} className="w-full flex items-center justify-between p-4 text-left">
        <div className="flex items-center gap-4">
          {icon}
          <h3 className="text-md font-semibold text-slate-800 dark:text-slate-100">{title}</h3>
        </div>
        <ChevronDownIcon className={`w-5 h-5 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`} />
      </button>
      <div className={`transition-all duration-500 ease-in-out grid ${isOpen ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'}`}>
        <div className="overflow-hidden">
          <div className="px-6 pb-6 pt-2">
            <MarkdownRenderer content={section.content} />
          </div>
        </div>
      </div>
    </div>
  );
};

const TabButton: React.FC<{ active: boolean; onClick: () => void; icon: React.ReactNode; children: React.ReactNode }> = ({ active, onClick, icon, children }) => (
  <button
    onClick={onClick}
    className={`flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-t-lg border-b-2 transition-colors ${
      active
        ? 'text-indigo-600 dark:text-indigo-400 border-indigo-600 dark:border-indigo-400'
        : 'text-slate-500 dark:text-slate-400 border-transparent hover:text-slate-700 dark:hover:text-slate-200 hover:border-slate-300 dark:hover:border-slate-600'
    }`}
  >
    {icon}
    {children}
  </button>
);

const CopyButton: React.FC<{ text: string }> = ({ text }) => {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <button onClick={handleCopy} className="absolute top-2 right-2 p-2 bg-slate-200 dark:bg-slate-700 rounded-md hover:bg-slate-300 dark:hover:bg-slate-600 transition">
      {copied ? <CheckCircleIcon className="w-4 h-4 text-green-500" /> : <ClipboardIcon className="w-4 h-4 text-slate-500" />}
    </button>
  );
};


// --- FEATURE COMPONENTS ---

const JossReviewer: React.FC = () => {
  const [repoUrl, setRepoUrl] = useState('https://github.com/hongping-zh/circular-bias-detection');
  const [review, setReview] = useState<JossReview | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = useCallback(async () => {
    if (!repoUrl || isLoading) return;
    setIsLoading(true);
    setError(null);
    setReview(null);
    try {
      const result = await generateJossReview(repoUrl);
      setReview(result);
    } catch (e: unknown) {
      if (e instanceof Error) setError(e.message);
      else setError("An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  }, [repoUrl, isLoading]);

  return (
    <div className="fade-in">
      <section className="bg-white dark:bg-slate-800/50 p-8 rounded-xl shadow-lg">
        <h2 className="text-2xl font-semibold text-center mb-2 text-slate-700 dark:text-slate-200">JOSS Pre-Review</h2>
        <p className="text-center text-slate-500 dark:text-slate-400 mb-6">Enter a public GitHub repository URL to begin the pre-review process.</p>
        <div className="flex flex-col sm:flex-row items-center gap-4">
          <div className="relative flex-grow w-full">
            <GithubIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input type="text" value={repoUrl} onChange={(e) => setRepoUrl(e.target.value)} placeholder="https://github.com/user/repo" className="w-full pl-10 pr-4 py-3 bg-slate-100 dark:bg-slate-700 border-2 border-transparent focus:border-indigo-500 focus:ring-indigo-500 rounded-lg transition" disabled={isLoading} />
          </div>
          <button onClick={handleAnalyze} disabled={isLoading || !repoUrl} className="w-full sm:w-auto flex items-center justify-center px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105">
            {isLoading ? (<><SpinnerIcon className="w-5 h-5 mr-2" />Analyzing...</>) : "Start Analysis"}
          </button>
        </div>
        {repoUrl && (
          <div className="text-center mt-4">
            <a
              href={repoUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-sm text-indigo-600 dark:text-indigo-400 hover:underline transition-colors"
            >
              <ExternalLinkIcon className="w-4 h-4" />
              <span>View Repository</span>
            </a>
          </div>
        )}
      </section>

      <section className="mt-12">
        {isLoading && (<div className="flex flex-col items-center justify-center text-center text-slate-500 dark:text-slate-400"><SpinnerIcon className="w-12 h-12 mb-4" /><p className="text-lg font-semibold">AI review in progress...</p><p>This may take a moment. Please be patient.</p></div>)}
        {error && (<div className="max-w-2xl mx-auto text-center bg-red-100 dark:bg-red-900/50 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg" role="alert"><strong className="font-bold">Error: </strong><span className="block sm:inline">{error}</span></div>)}
        {review && (
          <div className="space-y-6">
            <div className="bg-white dark:bg-slate-800/50 p-6 rounded-xl shadow-lg fade-in">
              <h3 className="text-xl font-bold text-slate-800 dark:text-slate-100 mb-4">Summary & Key Recommendations</h3>
              <MarkdownRenderer content={review.summary} />
            </div>
            <div className="space-y-4">
              {review.sections.map((section, index) => (<AccordionItem key={index} section={section} index={index} />))}
            </div>
          </div>
        )}
      </section>
    </div>
  );
}

const PrHelper: React.FC = () => {
    const [prUrl, setPrUrl] = useState('https://github.com/sgl-project/sglang/pull/12074');
    const [advice, setAdvice] = useState<ReviewSection[] | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
  
    const handleAnalyze = useCallback(async () => {
      if (!prUrl || isLoading) return;
      setIsLoading(true);
      setError(null);
      setAdvice(null);
      try {
        const result = await generatePrFollowupAdvice(prUrl);
        setAdvice(result);
      } catch (e: unknown) {
        if (e instanceof Error) setError(e.message);
        else setError("An unexpected error occurred.");
      } finally {
        setIsLoading(false);
      }
    }, [prUrl, isLoading]);

    const suggestedMessage = useMemo(() => {
      if (!advice) return '';
      const messageSection = advice.find(s => s.title.toLowerCase().includes('suggested message'));
      return messageSection ? messageSection.content.replace(/```/g, '').trim() : '';
    }, [advice]);
  
    return (
      <div className="fade-in">
        <section className="bg-white dark:bg-slate-800/50 p-8 rounded-xl shadow-lg">
          <h2 className="text-2xl font-semibold text-center mb-2 text-slate-700 dark:text-slate-200">PR Follow-up Helper</h2>
          <p className="text-center text-slate-500 dark:text-slate-400 mb-6">Get AI-powered advice on how to follow up on a stalled Pull Request.</p>
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <div className="relative flex-grow w-full">
              <PullRequestIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input type="text" value={prUrl} onChange={(e) => setPrUrl(e.target.value)} placeholder="https://github.com/user/repo/pull/123" className="w-full pl-10 pr-4 py-3 bg-slate-100 dark:bg-slate-700 border-2 border-transparent focus:border-indigo-500 focus:ring-indigo-500 rounded-lg transition" disabled={isLoading} />
            </div>
            <button onClick={handleAnalyze} disabled={isLoading || !prUrl} className="w-full sm:w-auto flex items-center justify-center px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105">
              {isLoading ? (<><SpinnerIcon className="w-5 h-5 mr-2" />Getting Advice...</>) : "Get Advice"}
            </button>
          </div>
        </section>

        <section className="mt-12">
            {isLoading && (<div className="flex flex-col items-center justify中心 text-center text-slate-500 dark:text-slate-400"><SpinnerIcon className="w-12 h-12 mb-4" /><p className="text-lg font-semibold">Generating advice...</p></div>)}
            {error && (<div className="max-w-2xl mx-auto text-center bg-red-100 dark:bg-red-900/50 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg" role="alert"><strong className="font-bold">Error: </strong><span className="block sm:inline">{error}</span></div>)}
            {advice && (
                <div className="grid grid-cols-1 md:grid-cols-5 gap-8">
                    <div className="md:col-span-3 space-y-4">
                        {advice.map((section, index) => (
                           section.title.toLowerCase().includes('suggested message') ? null : (
                            <div key={index} className="bg-white dark:bg-slate-800/50 p-6 rounded-xl shadow-lg fade-in" style={{ animationDelay: `${index * 100}ms` }}>
                                <h3 className="text-xl font-bold text-slate-800 dark:text-slate-100 mb-4">{section.title}</h3>
                                <MarkdownRenderer content={section.content} />
                            </div>)
                        ))}
                    </div>
                    <div className="md:col-span-2">
                        {advice.find(s => s.title.toLowerCase().includes('suggested message')) && (
                            <div className="bg-white dark:bg-slate-800/50 p-6 rounded-xl shadow-lg fade-in sticky top-12" style={{ animationDelay: `100ms` }}>
                                <h3 className="text-xl font-bold text-slate-800 dark:text-slate-100 mb-4">Suggested Message</h3>
                                <div className="relative">
                                  <MarkdownRenderer content={suggestedMessage} />
                                  <CopyButton text={suggestedMessage} />
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </section>
      </div>
    );
}

const CodeOptimizer: React.FC = () => {
    const [repoUrl] = useState('https://github.com/hongping-zh/circular-bias-detection');
    const [advice, setAdvice] = useState<ReviewSection[] | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
  
    const handleOptimize = useCallback(async () => {
      if (!repoUrl || isLoading) return;
      setIsLoading(true);
      setError(null);
      setAdvice(null);
      try {
        const result = await generateCodeOptimizationAdvice(repoUrl);
        setAdvice(result);
      } catch (e: unknown) {
        if (e instanceof Error) setError(e.message);
        else setError("An unexpected error occurred.");
      } finally {
        setIsLoading(false);
      }
    }, [repoUrl, isLoading]);
  
    return (
      <div className="fade-in">
        <section className="bg-white dark:bg-slate-800/50 p-8 rounded-xl shadow-lg text-center">
          <h2 className="text-2xl font-semibold mb-2 text-slate-700 dark:text-slate-200">AI-Powered Code Optimizer</h2>
          <p className="text-slate-500 dark:text-slate-400 mb-6">Analyzes your repository against best practices from similar projects and provides actionable advice.</p>
          <div className="bg-slate-100 dark:bg-slate-700/50 p-4 rounded-lg flex items-center justify-between gap-4 mb-6">
              <div className="flex items-center gap-3 text-left">
                  <GithubIcon className="w-6 h-6 text-slate-500 dark:text-slate-400 flex-shrink-0" />
                  <span className="font-mono text-sm text-slate-600 dark:text-slate-300 truncate">{repoUrl}</span>
              </div>
              <a href={repoUrl} target="_blank" rel="noopener noreferrer" className="text-indigo-600 dark:text-indigo-400 hover:underline flex-shrink-0">
                  <ExternalLinkIcon className="w-5 h-5"/>
              </a>
          </div>
          <button onClick={handleOptimize} disabled={isLoading} className="w-full sm:w-auto flex items-center justify-center px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105 mx-auto">
            {isLoading ? (<><SpinnerIcon className="w-5 h-5 mr-2" />Optimizing...</>) : "Start Optimization"}
          </button>
        </section>
  
        <section className="mt-12">
          {isLoading && (
            <div className="flex flex-col items-center justify-center text-center text-slate-500 dark:text-slate-400">
              <SpinnerIcon className="w-12 h-12 mb-4" />
              <p className="text-lg font-semibold">AI analysis in progress...</p>
              <p>Comparing your code against top open-source projects. This may take a moment.</p>
            </div>
          )}
          {error && (
            <div className="max-w-2xl mx-auto text-center bg-red-100 dark:bg-red-900/50 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg" role="alert">
              <strong className="font-bold">Error: </strong>
              <span className="block sm:inline">{error}</span>
            </div>
          )}
          {advice && (
            <div className="space-y-6">
              {advice.map((section, index) => (
                <div key={index} className="bg-white dark:bg-slate-800/50 p-6 rounded-xl shadow-lg fade-in" style={{ animationDelay: `${index * 100}ms` }}>
                  <h3 className="text-xl font-bold text-slate-800 dark:text-slate-100 mb-4">
                    {section.title.replace(/([🏛️✨⚡️📦🧪])/g, '').trim()}
                  </h3>
                  <MarkdownRenderer content={section.content} />
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    );
}

// --- MAIN APP ---

export default function App() {
  const [activeTab, setActiveTab] = useState('joss');

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-800 dark:text-slate-200 font-sans">
      <header className="bg-gradient-to-r from-sky-500 to-indigo-600 dark:from-sky-800 dark:to-indigo-900 p-6 shadow-md sticky top-0 z-10 backdrop-blur-lg bg-opacity-80 dark:bg-opacity-80">
        <div className="container mx-auto flex items-center justify-center text白">
          <BotIcon className="w-10 h-10 mr-4" />
          <div>
            <h1 className="text-3xl font-bold">AI Assistant for Open Source</h1>
            <p className="text-sm opacity-90">JOSS Pre-Reviews and Contribution Guidance</p>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-10 sm:py-16 max-w-5xl">
        <div className="flex justify-center border-b border-slate-300 dark:border-slate-700 mb-8">
          <TabButton active={activeTab === 'joss'} onClick={() => setActiveTab('joss')} icon={<PaperIcon className="w-5 h-5"/>}>
            JOSS Pre-Review
          </TabButton>
          <TabButton active={activeTab === 'pr'} onClick={() => setActiveTab('pr')} icon={<PullRequestIcon className="w-5 h-5"/>}>
            PR Follow-up
          </TabButton>
          <TabButton active={activeTab === 'optimizer'} onClick={() => setActiveTab('optimizer')} icon={<CodeIcon className="w-5 h-5"/>}>
            Code Optimizer
          </TabButton>
        </div>

        {activeTab === 'joss' && <JossReviewer />}
        {activeTab === 'pr' && <PrHelper />}
        {activeTab === 'optimizer' && <CodeOptimizer />}

      </main>
      
      <footer className="text-center p-6 text-sm text-slate-500 dark:text-slate-400">
        <p>Generated by Google Gemini. For educational and guidance purposes only.</p>
        <p>Always refer to official documentation and community guidelines.</p>
      </footer>
    </div>
  );
}
