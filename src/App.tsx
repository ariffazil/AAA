import { useEffect, useState } from 'react';
import TrinityNav from './components/TrinityNav';
import Cockpit from './Cockpit';

function App() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <>
      <TrinityNav />
      <Cockpit />
    </>
  );
}

export default App;
