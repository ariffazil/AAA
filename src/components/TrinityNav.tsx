

export default function TrinityNav() {
  return (
    <nav className="trinity-nav">
      <div className="trinity-container">
        <div className="trinity-left">
          <a href="https://arif-fazil.com/" className="trinity-logo">
            <span className="arif">ARIF</span>
            <span className="os">OS</span>
          </a>
          <div className="trinity-badge">HUMAN · THEORY · APPS</div>
        </div>

        <div className="trinity-center">
          <a href="https://arif-fazil.com/" className="trinity-link trinity-human active">HUMAN</a>
          <a href="https://apex.arif-fazil.com/" className="trinity-link trinity-theory">THEORY</a>
          <a href="https://arifos.arif-fazil.com/" className="trinity-link trinity-apps">APPS</a>
        </div>

        <div className="trinity-right">
          <a href="https://github.com/ariffazil/ariffazil" target="_blank" rel="noopener noreferrer">
            GitHub
          </a>
          <a href="https://arif-fazil.com/" className="trinity-enter">
            Enter
          </a>
        </div>
      </div>
    </nav>
  );
}
