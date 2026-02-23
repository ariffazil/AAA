import { useEffect, useState } from 'react';
import {
  Github,
  Linkedin,
  Mail,
  ExternalLink,
  MapPin,
  Mountain,
  TrendingUp,
  Cpu,
  ChevronRight,
  Menu,
  X,
  Code,
  Compass,
  Triangle,
  Terminal,
  Bot
} from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import TrinityNav from './components/TrinityNav';

const ARTICLES = [
  { title: 'Prompt · Physics · Paradox', desc: 'What happens when you treat AI prompts like physics experiments', url: 'https://medium.com/@arifbfazil/prompt-physics-paradox-1f1581b95acb' },
  { title: 'Einstein vs Oppenheimer', desc: 'The difference between knowing how and knowing why', url: 'https://medium.com/@arifbfazil/einstein-vs-oppenheimer-ab8b642720eb' },
  { title: 'The ARIF Test', desc: 'A simple test for whether AI systems are actually governed', url: 'https://medium.com/@arifbfazil/the-arif-test-df63c074d521' },
  { title: 'Rukun AGI', desc: 'Five pillars for building AI that respects boundaries', url: 'https://medium.com/@arifbfazil/rukun-agi-the-five-pillars-of-artificial-general-intelligence-bba2fb97e4dc' },
];

// Animated Geological Strata SVG Component
function GeologyVisual() {
  return (
    <svg viewBox="0 0 120 80" className="w-full h-full">
      <defs>
        <linearGradient id="strata1" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#3D2314" />
          <stop offset="100%" stopColor="#5C3A1E" />
        </linearGradient>
        <linearGradient id="strata2" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#5C3A1E" />
          <stop offset="100%" stopColor="#8B5A2B" />
        </linearGradient>
        <linearGradient id="strata3" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#8B5A2B" />
          <stop offset="100%" stopColor="#A67B5B" />
        </linearGradient>
        <linearGradient id="magma" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#8B0000" />
          <stop offset="50%" stopColor="#FF2D2D" />
          <stop offset="100%" stopColor="#8B0000" />
        </linearGradient>
      </defs>
      {/* Geological strata layers */}
      <path d="M0,60 Q30,55 60,58 T120,52 L120,80 L0,80 Z" fill="url(#strata1)">
        <animate attributeName="d" values="M0,60 Q30,55 60,58 T120,52 L120,80 L0,80 Z;M0,62 Q30,57 60,60 T120,54 L120,80 L0,80 Z;M0,60 Q30,55 60,58 T120,52 L120,80 L0,80 Z" dur="8s" repeatCount="indefinite"/>
      </path>
      <path d="M0,40 Q40,35 80,42 T120,38 L120,60 L0,60 Z" fill="url(#strata2)">
        <animate attributeName="d" values="M0,40 Q40,35 80,42 T120,38 L120,60 L0,60 Z;M0,42 Q40,37 80,44 T120,40 L120,60 L0,60 Z;M0,40 Q40,35 80,42 T120,38 L120,60 L0,60 Z" dur="6s" repeatCount="indefinite"/>
      </path>
      <path d="M0,20 Q35,15 70,22 T120,18 L120,40 L0,40 Z" fill="url(#strata3)">
        <animate attributeName="d" values="M0,20 Q35,15 70,22 T120,18 L120,40 L0,40 Z;M0,22 Q35,17 70,24 T120,20 L120,40 L0,40 Z;M0,20 Q35,15 70,22 T120,18 L120,40 L0,40 Z" dur="7s" repeatCount="indefinite"/>
      </path>
      {/* Magma core */}
      <circle cx="60" cy="70" r="8" fill="url(#magma)" opacity="0.8">
        <animate attributeName="r" values="8;10;8" dur="3s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.8;0.5;0.8" dur="3s" repeatCount="indefinite"/>
      </circle>
      {/* Seismic waves */}
      <ellipse cx="60" cy="70" rx="20" ry="6" fill="none" stroke="#FF2D2D" strokeWidth="0.5" opacity="0.3">
        <animate attributeName="rx" values="20;40;60" dur="2s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.5;0.2;0" dur="2s" repeatCount="indefinite"/>
      </ellipse>
    </svg>
  );
}

// Animated Economics/Market Visual
function EconomicsVisual() {
  return (
    <svg viewBox="0 0 120 80" className="w-full h-full">
      <defs>
        <linearGradient id="chartGrad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#8B0000" stopOpacity="0.3" />
          <stop offset="100%" stopColor="#8B0000" stopOpacity="0" />
        </linearGradient>
      </defs>
      {/* Grid lines */}
      <line x1="10" y1="20" x2="110" y2="20" stroke="#333" strokeWidth="0.5" opacity="0.3"/>
      <line x1="10" y1="40" x2="110" y2="40" stroke="#333" strokeWidth="0.5" opacity="0.3"/>
      <line x1="10" y1="60" x2="110" y2="60" stroke="#333" strokeWidth="0.5" opacity="0.3"/>
      {/* Area chart */}
      <path d="M10,60 L25,45 L40,50 L55,30 L70,35 L85,20 L100,25 L110,15 L110,70 L10,70 Z" fill="url(#chartGrad)" opacity="0.6"/>
      {/* Line chart */}
      <path d="M10,60 L25,45 L40,50 L55,30 L70,35 L85,20 L100,25 L110,15" fill="none" stroke="#FF2D2D" strokeWidth="2" strokeLinecap="round">
        <animate attributeName="stroke-dasharray" values="0,200;200,0" dur="3s" fill="freeze"/>
      </path>
      {/* Data points */}
      <circle cx="25" cy="45" r="3" fill="#FF2D2D">
        <animate attributeName="r" values="0;3" dur="0.3s" begin="0.5s" fill="freeze"/>
      </circle>
      <circle cx="40" cy="50" r="3" fill="#FF2D2D">
        <animate attributeName="r" values="0;3" dur="0.3s" begin="0.7s" fill="freeze"/>
      </circle>
      <circle cx="55" cy="30" r="3" fill="#FF2D2D">
        <animate attributeName="r" values="0;3" dur="0.3s" begin="0.9s" fill="freeze"/>
      </circle>
      <circle cx="70" cy="35" r="3" fill="#FF2D2D">
        <animate attributeName="r" values="0;3" dur="0.3s" begin="1.1s" fill="freeze"/>
      </circle>
      <circle cx="85" cy="20" r="3" fill="#FF2D2D">
        <animate attributeName="r" values="0;3" dur="0.3s" begin="1.3s" fill="freeze"/>
      </circle>
      <circle cx="100" cy="25" r="3" fill="#FF2D2D">
        <animate attributeName="r" values="0;3" dur="0.3s" begin="1.5s" fill="freeze"/>
      </circle>
      {/* Candlestick */}
      <line x1="95" y1="15" x2="95" y2="30" stroke="#00C853" strokeWidth="1"/>
      <rect x="92" y="18" width="6" height="8" fill="#00C853" opacity="0.8">
        <animate attributeName="height" values="0;8" dur="0.5s" begin="2s" fill="freeze"/>
      </rect>
    </svg>
  );
}

// Animated AI/Neural Network Visual
function AIVisual() {
  return (
    <svg viewBox="0 0 120 80" className="w-full h-full">
      <defs>
        <radialGradient id="nodeGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#FF2D2D" />
          <stop offset="100%" stopColor="#8B0000" />
        </radialGradient>
        <linearGradient id="pulseGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="transparent" />
          <stop offset="50%" stopColor="#FF2D2D" />
          <stop offset="100%" stopColor="transparent" />
        </linearGradient>
      </defs>
      {/* Neural connections */}
      <line x1="20" y1="25" x2="50" y2="30" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="20" y1="25" x2="50" y2="50" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="20" y1="55" x2="50" y2="30" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="20" y1="55" x2="50" y2="50" stroke="#444" strokeWidth="1" opacity="0.5"/>
      
      <line x1="50" y1="30" x2="80" y2="25" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="50" y1="30" x2="80" y2="55" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="50" y1="50" x2="80" y2="25" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="50" y1="50" x2="80" y2="55" stroke="#444" strokeWidth="1" opacity="0.5"/>
      
      <line x1="80" y1="25" x2="100" y2="40" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="80" y1="55" x2="100" y2="40" stroke="#444" strokeWidth="1" opacity="0.5"/>
      
      {/* Animated data pulses */}
      <circle cx="35" cy="28" r="2" fill="#FF2D2D" opacity="0">
        <animate attributeName="opacity" values="0;1;0" dur="1.5s" repeatCount="indefinite"/>
        <animate attributeName="cx" values="20;50" dur="1.5s" repeatCount="indefinite"/>
        <animate attributeName="cy" values="25;30" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <circle cx="35" cy="42" r="2" fill="#FF2D2D" opacity="0">
        <animate attributeName="opacity" values="0;1;0" dur="1.5s" begin="0.5s" repeatCount="indefinite"/>
        <animate attributeName="cx" values="20;50" dur="1.5s" begin="0.5s" repeatCount="indefinite"/>
        <animate attributeName="cy" values="55;50" dur="1.5s" begin="0.5s" repeatCount="indefinite"/>
      </circle>
      <circle cx="65" cy="32" r="2" fill="#FF2D2D" opacity="0">
        <animate attributeName="opacity" values="0;1;0" dur="1.5s" begin="0.3s" repeatCount="indefinite"/>
        <animate attributeName="cx" values="50;80" dur="1.5s" begin="0.3s" repeatCount="indefinite"/>
        <animate attributeName="cy" values="30;25" dur="1.5s" begin="0.3s" repeatCount="indefinite"/>
      </circle>
      <circle cx="90" cy="47" r="2" fill="#FF2D2D" opacity="0">
        <animate attributeName="opacity" values="0;1;0" dur="1.5s" begin="0.8s" repeatCount="indefinite"/>
        <animate attributeName="cx" values="80;100" dur="1.5s" begin="0.8s" repeatCount="indefinite"/>
        <animate attributeName="cy" values="55;40" dur="1.5s" begin="0.8s" repeatCount="indefinite"/>
      </circle>
      
      {/* Nodes */}
      <circle cx="20" cy="25" r="6" fill="url(#nodeGrad)"/>
      <circle cx="20" cy="55" r="6" fill="url(#nodeGrad)"/>
      <circle cx="50" cy="30" r="8" fill="url(#nodeGrad)"/>
      <circle cx="50" cy="50" r="8" fill="url(#nodeGrad)"/>
      <circle cx="80" cy="25" r="6" fill="url(#nodeGrad)"/>
      <circle cx="80" cy="55" r="6" fill="url(#nodeGrad)"/>
      <circle cx="100" cy="40" r="10" fill="url(#nodeGrad)"/>
      
      {/* Binary code rain effect */}
      <text x="105" y="15" fontSize="6" fill="#8B0000" fontFamily="JetBrains Mono" opacity="0.6">101</text>
      <text x="10" y="70" fontSize="6" fill="#8B0000" fontFamily="JetBrains Mono" opacity="0.6">010</text>
    </svg>
  );
}

function App() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <>
      <TrinityNav />
      <div className="min-h-screen bg-[#0a0a0a] text-gray-200 font-sans selection:bg-red-900/30 selection:text-red-200">
      {/* Navigation - Minimal */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-[#0a0a0a]/90 backdrop-blur-md border-b border-gray-800/50' : ''}`}>
        <div className="max-w-3xl mx-auto px-6">
          <div className="flex items-center justify-between py-5">
            {/* Logo / Name */}
            <a href="#" className="text-sm font-medium text-gray-300 hover:text-white transition-colors font-mono">
              arif<span className="text-red-500">.</span>fazil
            </a>

            {/* Desktop links */}
            <div className="hidden md:flex items-center gap-6">
              <a href="#about" className="px-3 py-1.5 rounded-md text-sm text-gray-400 hover:text-white hover:bg-gray-800/50 border border-transparent hover:border-gray-700 transition-all">about</a>
              <a href="#work" className="px-3 py-1.5 rounded-md text-sm text-gray-400 hover:text-white hover:bg-gray-800/50 border border-transparent hover:border-gray-700 transition-all">work</a>
              <a href="#writing" className="px-3 py-1.5 rounded-md text-sm text-gray-400 hover:text-white hover:bg-gray-800/50 border border-transparent hover:border-gray-700 transition-all">writing</a>
              <div className="h-4 w-px bg-gray-800 mx-1" />
              <a href="https://github.com/ariffazil" target="_blank" rel="noopener noreferrer" className="p-1.5 text-gray-500 hover:text-white transition-colors" title="GitHub Profile">
                <Github className="w-4 h-4" />
              </a>
              <a href="https://linkedin.com/in/arif-fazil" target="_blank" rel="noopener noreferrer" className="p-1.5 text-gray-500 hover:text-white transition-colors" title="LinkedIn Profile">
                <Linkedin className="w-4 h-4" />
              </a>
              <a href="https://medium.com/@arifbfazil" target="_blank" rel="noopener noreferrer" className="p-1.5 text-gray-500 hover:text-white transition-colors" title="Medium Articles">
                <ExternalLink className="w-4 h-4" />
              </a>
              <div className="h-4 w-px bg-gray-800 mx-1" />
              <a href="/llms.txt" className="px-3 py-1.5 rounded-md text-sm text-gray-400 hover:text-red-400 hover:bg-red-950/20 border border-transparent hover:border-red-800/50 transition-all font-mono">llms.txt</a>
            </div>

            {/* Trinity nav - pill style */}
            <div className="hidden md:flex items-center gap-1 bg-gray-900/50 rounded-full px-1 py-1 border border-gray-700">
              <a href="https://arif-fazil.com" className="px-3 py-1.5 rounded-full bg-red-500/20 text-red-400 text-xs font-medium border border-red-500/30 hover:bg-red-500/30 transition-colors">
                HUMAN
              </a>
              <a href="https://apex.arif-fazil.com" className="px-3 py-1.5 rounded-full text-gray-400 text-xs font-medium border border-transparent hover:border-amber-500/30 hover:text-amber-400 hover:bg-amber-950/20 transition-all">
                THEORY
              </a>
              <a href="https://arifos.arif-fazil.com" className="px-3 py-1.5 rounded-full text-gray-400 text-xs font-medium border border-transparent hover:border-cyan-500/30 hover:text-cyan-400 hover:bg-cyan-950/20 transition-all">
                APPS
              </a>
            </div>

            {/* Mobile menu */}
            <button type="button" className="md:hidden p-2 text-gray-400" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {mobileMenuOpen && (
          <div className="md:hidden bg-[#0a0a0a] border-b border-gray-800 px-6 py-4 space-y-3">
            <a href="#about" className="block px-3 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800/50 border border-transparent hover:border-gray-700 transition-all" onClick={() => setMobileMenuOpen(false)}>about</a>
            <a href="#work" className="block px-3 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800/50 border border-transparent hover:border-gray-700 transition-all" onClick={() => setMobileMenuOpen(false)}>work</a>
            <a href="#writing" className="block px-3 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800/50 border border-transparent hover:border-gray-700 transition-all" onClick={() => setMobileMenuOpen(false)}>writing</a>
            <a href="/llms.txt" className="block px-3 py-2 rounded-lg text-gray-400 hover:text-red-400 hover:bg-red-950/20 border border-transparent hover:border-red-800/50 transition-all font-mono" onClick={() => setMobileMenuOpen(false)}>llms.txt</a>
            <Separator className="bg-gray-800 my-3" />
            <div className="flex gap-2">
              <a href="https://arif-fazil.com" className="px-4 py-2 rounded-full bg-red-500/20 text-red-400 text-xs border border-red-500/30">HUMAN</a>
              <a href="https://apex.arif-fazil.com" className="px-4 py-2 rounded-full text-amber-400 text-xs border border-amber-500/30 bg-amber-950/10">THEORY</a>
              <a href="https://arifos.arif-fazil.com" className="px-4 py-2 rounded-full text-cyan-400 text-xs border border-cyan-500/30 bg-cyan-950/10">APPS</a>
            </div>
          </div>
        )}
      </nav>

      {/* Hero - Banner Style */}
      <section className="relative min-h-screen flex items-center justify-center pt-24 pb-20 overflow-hidden">
        {/* Animated Background Layers */}
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-[#050505]" />
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#1a0a0a_1px,transparent_1px),linear-gradient(to_bottom,#1a0a0a_1px,transparent_1px)] bg-[size:6rem_6rem] opacity-20" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(139,0,0,0.1),transparent_70%)] animate-pulse" />
          <div className="absolute bottom-0 left-0 right-0 h-96 bg-gradient-to-t from-[#0a0a0a] to-transparent" />
        </div>

        <div className="relative z-10 max-w-3xl mx-auto px-6 text-center">
          {/* Creed Badge */}
          <div className="flex justify-center mb-8">
            <div className="inline-flex items-center gap-3 px-5 py-2.5 rounded-full border border-red-500/30 bg-red-950/20 text-red-400 text-xs font-mono tracking-[0.2em] shadow-lg shadow-red-950/40">
              <Triangle className="w-3 h-3 fill-red-500/30" />
              DITEMPA BUKAN DIBERI
            </div>
          </div>

          {/* Trinity Logo - Large & Glow */}
          <div className="flex justify-center mb-10 scale-110 sm:scale-125">
            <img 
              src="/images/arifos-logo.webp" 
              alt="arifOS Trinity Logo" 
              className="w-40 h-40 object-contain drop-shadow-[0_0_50px_rgba(255,0,0,0.3)] hover:drop-shadow-[0_0_60px_rgba(255,0,0,0.5)] transition-all duration-700"
            />
          </div>

          {/* Name & Title */}
          <h1 className="text-6xl sm:text-8xl font-bold mb-6 tracking-tighter text-white">
            ARIF<span className="text-red-600">.</span>FAZIL
          </h1>

          {/* Disciplines - Primary */}
          <div className="flex items-center justify-center gap-4 mb-8">
            <span className="text-xs font-mono text-gray-500 uppercase tracking-widest">Geoscience</span>
            <span className="w-1.5 h-1.5 rounded-full bg-red-800" />
            <span className="text-xs font-mono text-gray-500 uppercase tracking-widest">Economics</span>
            <span className="w-1.5 h-1.5 rounded-full bg-red-800" />
            <span className="text-xs font-mono text-gray-500 uppercase tracking-widest">AI Governance</span>
          </div>

          {/* Bio - refined one-liner */}
          <p className="text-lg sm:text-xl text-gray-300 leading-relaxed max-w-xl mx-auto mb-12 font-light">
            Explorationist by nature. Architect of <a href="https://arifos.arif-fazil.com" className="text-white font-medium border-b border-red-900 hover:border-red-500 transition-colors">arifOS</a> by necessity. 
            Bridging the gap between subsurface physical truth and digital governance.
          </p>

          <div className="flex items-center justify-center gap-4">
            <a href="#work" className="px-8 py-3 rounded-full bg-red-600 hover:bg-red-500 text-white font-medium transition-all shadow-lg shadow-red-900/40 hover:scale-105 active:scale-95">
              Explore Ecosystem
            </a>
            <a href="https://medium.com/@arifbfazil" target="_blank" rel="noopener noreferrer" className="px-8 py-3 rounded-full bg-gray-900 border border-gray-700 text-gray-300 hover:text-white hover:bg-gray-800 transition-all">
              Read Writing
            </a>
          </div>
        </div>
      </section>

      {/* Three Disciplines - Visual Cards */}
      <section id="about" className="py-24 border-t border-gray-800/50">
        <div className="max-w-4xl mx-auto px-6">
          <div className="flex items-center gap-3 mb-12">
            <span className="h-px w-8 bg-red-600/50" />
            <h2 className="text-sm font-mono text-gray-500 uppercase tracking-widest">Three Disciplines</h2>
          </div>

          <div className="grid md:grid-cols-3 gap-10">
            {/* Geology */}
            <div className="group">
              <div className="h-40 mb-6 rounded-2xl bg-gray-900/50 border border-gray-800 overflow-hidden relative shadow-inner">
                <div className="absolute inset-0 opacity-40 group-hover:opacity-60 transition-opacity">
                  <GeologyVisual />
                </div>
                <div className="absolute bottom-4 left-4">
                  <div className="w-10 h-10 rounded-lg bg-[#0a0a0a]/80 backdrop-blur-sm border border-gray-800 flex items-center justify-center">
                    <Mountain className="w-5 h-5 text-red-500" />
                  </div>
                </div>
              </div>
              <h3 className="text-lg font-medium text-white mb-3">Geoscience</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Specializing in subsurface interpretation and frontier basin studies. 
                Applying earth systems logic to complex data landscapes.
              </p>
            </div>

            {/* Economics */}
            <div className="group">
              <div className="h-40 mb-6 rounded-2xl bg-gray-900/50 border border-gray-800 overflow-hidden relative shadow-inner">
                <div className="absolute inset-0 opacity-40 group-hover:opacity-60 transition-opacity">
                  <EconomicsVisual />
                </div>
                <div className="absolute bottom-4 left-4">
                  <div className="w-10 h-10 rounded-lg bg-[#0a0a0a]/80 backdrop-blur-sm border border-gray-800 flex items-center justify-center">
                    <TrendingUp className="w-5 h-5 text-red-500" />
                  </div>
                </div>
              </div>
              <h3 className="text-lg font-medium text-white mb-3">Economics</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Analyzing incentive structures and risk pricing. Understanding how 
                value and agency intersect in constrained environments.
              </p>
            </div>

            {/* AI */}
            <div className="group">
              <div className="h-40 mb-6 rounded-2xl bg-gray-900/50 border border-gray-800 overflow-hidden relative shadow-inner">
                <div className="absolute inset-0 opacity-40 group-hover:opacity-60 transition-opacity">
                  <AIVisual />
                </div>
                <div className="absolute bottom-4 left-4">
                  <div className="w-10 h-10 rounded-lg bg-[#0a0a0a]/80 backdrop-blur-sm border border-gray-800 flex items-center justify-center">
                    <Cpu className="w-5 h-5 text-red-500" />
                  </div>
                </div>
              </div>
              <h3 className="text-lg font-medium text-white mb-3">AI Governance</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Developing the htaMind: constitutional safeguards and thermodynamic 
                constraints for safety-critical AI decision systems.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Biography — Sovereign Memory */}
      <section id="biography" className="py-24 border-t border-gray-800/50 bg-gray-950/20">
        <div className="max-w-3xl mx-auto px-6">
          <div className="flex items-center gap-3 mb-10">
            <span className="h-px w-8 bg-red-600/50" />
            <h2 className="text-sm font-mono text-gray-500 uppercase tracking-widest">Sovereign Memory</h2>
          </div>

          <div className="space-y-10">
            {/* Identity Core */}
            <div className="p-8 rounded-2xl border border-gray-800 bg-gray-900/20 hover:bg-gray-900/30 transition-colors">
              <h3 className="text-xl font-medium text-white mb-6 flex items-center gap-3">
                <div className="w-2 h-2 rounded-full bg-red-600 shadow-[0_0_8px_rgba(220,38,38,0.8)]" />
                Identity Core
              </h3>
              <div className="grid sm:grid-cols-2 gap-y-4 gap-x-8 text-gray-300">
                <p><strong className="text-gray-500 font-mono text-xs uppercase block mb-1">Name</strong> ARIF FAZIL</p>
                <p><strong className="text-gray-500 font-mono text-xs uppercase block mb-1">Born</strong> May 22, 1990 — Penang, MY</p>
                <p><strong className="text-gray-500 font-mono text-xs uppercase block mb-1">Heritage</strong> Northern Malay / Loghat Utara</p>
                <p><strong className="text-gray-500 font-mono text-xs uppercase block mb-1">Email</strong> arifos@arif-fazil.com</p>
                <p><strong className="text-gray-500 font-mono text-xs uppercase block mb-1">Creed</strong> "FORGED, NOT GIVEN"</p>
              </div>
            </div>

            {/* Professional Background */}
            <div className="p-8 rounded-2xl border border-gray-800 bg-gray-900/20">
              <h3 className="text-xl font-medium text-white mb-6 flex items-center gap-3">
                <div className="w-2 h-2 rounded-full bg-red-600 shadow-[0_0_8px_rgba(220,38,38,0.8)]" />
                Experience & Impact
              </h3>
              
              <div className="space-y-8">
                <div>
                  <h4 className="text-white font-medium mb-3 flex items-center justify-between">
                    <span>PETRONAS — Explorationist</span>
                    <span className="text-xs text-gray-500">2013 – Present</span>
                  </h4>
                  <ul className="grid sm:grid-cols-2 gap-3 text-gray-400 text-sm">
                    <li className="flex gap-2">
                      <span className="text-red-500">01</span>
                      <span>12+ years in frontier basin analysis</span>
                    </li>
                    <li className="flex gap-2">
                      <span className="text-red-500">02</span>
                      <span>100% exploration drilling success rate</span>
                    </li>
                    <li className="flex gap-2">
                      <span className="text-red-500">03</span>
                      <span>Shallowest flowing oil discovery in MY</span>
                    </li>
                    <li className="flex gap-2">
                      <span className="text-red-500">04</span>
                      <span>Instrumental to PM318 realization</span>
                    </li>
                  </ul>
                </div>

                <Separator className="bg-gray-800/50" />

                <div>
                  <h4 className="text-white font-medium mb-3">Foundations</h4>
                  <p className="text-sm text-gray-400 font-light leading-relaxed">
                    Double Major in <strong className="text-white">Geology & Geophysics</strong> and <strong className="text-white">Economics</strong> from <strong className="text-white">UW-Madison</strong>. 
                    PETRONAS Scholar. Alumnus of the Environmental Studies program.
                  </p>
                </div>
              </div>
            </div>

            {/* Current Mission */}
            <div className="p-8 rounded-2xl border border-red-900/40 bg-red-950/10 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <Bot className="w-24 h-24 text-red-500" />
              </div>
              <h3 className="text-xl font-medium text-white mb-4 flex items-center gap-3">
                <Bot className="w-5 h-5 text-red-500" />
                Active Forge (2025–2026)
              </h3>
              <p className="text-gray-300 leading-relaxed relative z-10">
                Developing <strong className="text-white">arifOS</strong>: the constitutional governance kernel for artificial intelligence. 
                Applying geoscientific rigor and economic incentives to build safety-critical AI systems.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Trinity Ecosystem - Clean Table */}
      <section id="work" className="py-24 border-t border-gray-800/50">
        <div className="max-w-3xl mx-auto px-6">
          <div className="flex items-center gap-3 mb-2">
            <span className="h-px w-8 bg-red-600/50" />
            <h2 className="text-sm font-mono text-gray-500 uppercase tracking-widest">Ecosystem</h2>
          </div>
          <p className="text-gray-400 text-sm mb-12">The Trinity Architecture: Three layers of sovereign cognition.</p>

          {/* Trinity Links */}
          <div className="grid sm:grid-cols-2 gap-4 mb-12">
            <a href="https://apex.arif-fazil.com" className="group p-6 rounded-2xl border border-gray-800 hover:border-amber-600/50 bg-gray-900/30 transition-all">
              <div className="w-12 h-12 rounded-xl bg-amber-950/30 border border-amber-800/30 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Compass className="w-6 h-6 text-amber-500" />
              </div>
              <h3 className="font-medium text-white mb-2 underline-offset-4 group-hover:underline">The Theory</h3>
              <p className="text-xs text-gray-500 leading-relaxed">Constitutional canon, axioms, and philosophical grounding.</p>
            </a>
            
            <a href="https://arifos.arif-fazil.com" className="group p-6 rounded-2xl border border-gray-800 hover:border-cyan-600/50 bg-gray-900/30 transition-all">
              <div className="w-12 h-12 rounded-xl bg-cyan-950/30 border border-cyan-800/30 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Code className="w-6 h-6 text-cyan-500" />
              </div>
              <h3 className="font-medium text-white mb-2 underline-offset-4 group-hover:underline">The Kernel</h3>
              <p className="text-xs text-gray-500 leading-relaxed">API, MCP tools, and technical implementation guides.</p>
            </a>
          </div>

          {/* Trinity Table */}
          <div className="rounded-xl border border-gray-800 overflow-x-auto shadow-2xl">
            <table className="w-full text-sm min-w-[500px]">
              <thead>
                <tr className="border-b border-gray-800 bg-gray-900/30">
                  <th className="text-left px-6 py-4 text-gray-500 font-normal font-mono text-xs uppercase tracking-tighter">Layer</th>
                  <th className="text-left px-6 py-4 text-gray-500 font-normal font-mono text-xs uppercase tracking-tighter">Site</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/50">
                {[
                  { id: 'HUMAN', url: 'https://arif-fazil.com', site: 'arif-fazil.com', color: 'red' },
                  { id: 'THEORY', url: 'https://apex.arif-fazil.com', site: 'apex.arif-fazil.com', color: 'amber' },
                  { id: 'APPS', url: 'https://arifos.arif-fazil.com', site: 'arifos.arif-fazil.com', color: 'cyan' },
                ].map((row) => (
                  <tr key={row.id} className="hover:bg-gray-900/30 transition-colors cursor-pointer" onClick={() => window.open(row.url, '_blank')}>
                    <td className="px-6 py-5">
                      <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-md bg-${row.color}-500/10 text-${row.color}-400 font-mono text-[10px] border border-${row.color}-500/20`}>
                        {row.id}
                      </span>
                    </td>
                    <td className="px-6 py-5">
                      <span className="text-gray-300 font-medium">{row.site}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* Project Highlight */}
      <section className="py-24 border-t border-gray-800/50 bg-red-950/[0.02]">
        <div className="max-w-3xl mx-auto px-6">
          <div className="flex items-center gap-3 mb-8">
            <span className="h-px w-8 bg-red-600/50" />
            <h2 className="text-sm font-mono text-gray-500 uppercase tracking-widest">System Highlight</h2>
          </div>

          <div className="p-10 rounded-3xl border border-red-500/20 bg-gradient-to-br from-gray-900/40 to-red-950/10 relative overflow-hidden group">
            <div className="absolute -top-24 -right-24 w-64 h-64 bg-red-600/10 rounded-full blur-[100px] group-hover:bg-red-600/20 transition-all duration-1000" />
            
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 rounded-2xl bg-red-600 flex items-center justify-center shadow-lg shadow-red-900/40">
                <Triangle className="w-7 h-7 text-white" />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-white tracking-tight">arifOS</h3>
                <p className="text-xs font-mono text-red-500">v64.1-GAGI</p>
              </div>
            </div>
            
            <p className="text-gray-300 text-lg leading-relaxed mb-8 font-light">
              arifOS is a specialized operating system designed and forged to provide 
              governance for AI agents. By integrating 13 constitutional floors (F1-F13) 
              at the kernel level, arifOS ensures that AI cognition is bound by mathematical 
              fidelity, thermodynamic stability, and human empathy.
            </p>

            <div className="flex flex-wrap gap-4">
              <a href="https://arifos.arif-fazil.com" className="px-6 py-3 rounded-2xl bg-white text-black font-semibold hover:bg-gray-200 transition-colors flex items-center gap-2">
                <Terminal className="w-4 h-4" /> Documentation
              </a>
              <a href="https://github.com/ariffazil/arifOS" title="View Source on GitHub" className="px-6 py-3 rounded-2xl bg-gray-900 border border-gray-700 text-white font-medium hover:bg-gray-800 transition-colors flex items-center gap-2">
                <Github className="w-4 h-4" /> GitHub
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Writing */}
      <section id="writing" className="py-24 border-t border-gray-800/50">
        <div className="max-w-3xl mx-auto px-6">
          <div className="flex items-center gap-3 mb-10">
            <span className="h-px w-8 bg-red-600/50" />
            <h2 className="text-sm font-mono text-gray-500 uppercase tracking-widest">Writing</h2>
          </div>

          <div className="grid gap-4">
            {ARTICLES.map((article) => (
              <a
                key={article.url}
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="group p-6 rounded-2xl border border-gray-800 bg-gray-900/20 hover:border-red-900/50 hover:bg-red-950/[0.05] transition-all"
              >
                <div className="flex items-start justify-between gap-6">
                  <div>
                    <h3 className="text-lg font-medium text-gray-100 group-hover:text-red-500 transition-colors mb-1">
                      {article.title}
                    </h3>
                    <p className="text-sm text-gray-500 font-light">{article.desc}</p>
                  </div>
                  <div className="w-10 h-10 rounded-full bg-gray-800/50 flex items-center justify-center group-hover:bg-red-600 transition-colors flex-shrink-0">
                    <ExternalLink className="w-4 h-4 text-gray-400 group-hover:text-white" />
                  </div>
                </div>
              </a>
            ))}
          </div>

          <div className="mt-10 text-center">
            <a
              href="https://medium.com/@arifbfazil"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors group"
            >
              View all articles on Medium 
              <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </a>
          </div>
        </div>
      </section>

      {/* For AI Agents */}
      <section className="py-20 border-t border-gray-900/50 bg-[#080808]">
        <div className="max-w-3xl mx-auto px-6">
          <div className="flex items-center gap-3 mb-6">
            <Bot className="w-5 h-5 text-gray-600" />
            <h2 className="text-xs font-mono text-gray-600 uppercase tracking-[0.3em]">Machine Context</h2>
          </div>
          <p className="text-gray-500 text-sm mb-10 font-light max-w-md italic">
            "We build for the machines that will build with us."
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { id: 'llms.txt', url: '/llms.txt', icon: Terminal },
              { id: 'llms.json', url: '/llms.json', icon: Terminal },
              { id: 'humans.txt', url: '/humans.txt', icon: Code },
              { id: 'robots.txt', url: '/robots.txt', icon: Bot },
            ].map((file) => (
              <a key={file.id} href={file.id} title={`Go to ${file.id}`} className="p-4 rounded-xl border border-gray-800 bg-[#0a0a0a] hover:border-red-600/40 hover:text-red-500 transition-all flex flex-col items-center gap-3">
                <file.icon className="w-5 h-5 opacity-40" />
                <span className="text-xs font-mono">{file.id}</span>
              </a>
            ))}
          </div>
        </div>
      </section>

      <footer className="trinity-footer mt-24">
        <div className="links">
          <a href="https://arif-fazil.com/"><b>HUMAN</b></a>
          <a href="https://apex.arif-fazil.com/">THEORY</a>
          <a href="https://arifos.arif-fazil.com/">APPS</a>
        </div>
        THE TRINITY • HUMAN • THEORY • APPS<br />
        <b>Ditempa Bukan Diberi</b> • AGPL-3.0 • 2026.2.23
        <div className="mt-8 text-[10px] opacity-30 uppercase tracking-[0.2em]">
          Copyright © 2013 – 2026 Sovereign Records • LAST UPDATED: FEB 23, 2026
        </div>
      </footer>
    </div>
    </>
  );
}

export default App;
