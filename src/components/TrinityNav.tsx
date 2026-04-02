export default function TrinityNav() {
  const handleEnter = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    const target = document.getElementById('about');
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    else window.scrollTo({ top: window.innerHeight, behavior: 'smooth' });
  };

  return (
    <>
      {/* Trinity strip — unified arifOS ecosystem */}
      <div className="unified-trinity-strip">
        <a href="https://arif-fazil.com" className="utn-node utn-human utn-active">HUMAN</a>
        <span className="utn-div">·</span>
        <a href="https://arifos.arif-fazil.com" className="utn-node utn-theory">THEORY</a>
        <span className="utn-div">·</span>
        <a href="https://arifosmcp.arif-fazil.com" className="utn-node utn-apps">APPS</a>
        <span className="utn-div">·</span>
        <a href="https://forge.arif-fazil.com" className="utn-node utn-apps">FORGE</a>
        <span className="utn-div">·</span>
        <a href="https://aaa.arif-fazil.com" className="utn-node utn-apps">AAA</a>
        <span className="utn-div">·</span>
        <a href="https://aaa.arif-fazil.com/geox" className="utn-node utn-apps">GEOX</a>
        <span className="utn-sep" />
        <span className="utn-sig">ΔΩΨ — DITEMPA BUKAN DIBERI</span>
      </div>

      {/* Main nav — unified 60px height */}
      <nav className="unified-nav">
        <div className="unified-nav-inner">
          {/* Left: Logo */}
          <a href="https://arif-fazil.com/" className="unified-logo">
            <span className="unified-logo-mark">arif<span className="unified-logo-dot">.</span>fazil</span>
          </a>

          {/* Center: Links */}
          <div className="unified-nav-links">
            <a href="#about"   className="unified-nav-link">about</a>
            <a href="#work"    className="unified-nav-link">work</a>
            <a href="#writing" className="unified-nav-link">writing</a>
          </div>

          {/* Right: GitHub + CTA */}
          <div className="unified-nav-right">
            <a
              href="https://github.com/ariffazil"
              target="_blank"
              rel="noopener noreferrer"
              className="unified-nav-ghost"
              title="GitHub"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.164 6.839 9.49.5.09.682-.218.682-.485 0-.236-.009-.866-.014-1.7-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.464-1.11-1.464-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.03-2.683-.103-.253-.447-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.115 2.504.337 1.909-1.294 2.747-1.025 2.747-1.025.546 1.376.202 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.741 0 .269.18.579.688.481C19.138 20.16 22 16.416 22 12c0-5.523-4.477-10-10-10z"/>
              </svg>
              GitHub
            </a>
            <a
              href="#about"
              className="unified-nav-cta unified-nav-cta--human"
              onClick={handleEnter}
            >
              Enter ↓
            </a>
          </div>
        </div>
      </nav>
    </>
  );
}
