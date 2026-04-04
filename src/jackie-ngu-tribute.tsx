import { useState, useEffect } from 'react'

const timeline = [
  { year: '2014', event: 'Joined PETRONAS Carigali — Exploration Geoscientist' },
  { year: '2016', event: 'First deepwater campaign — Baram Delta Systems' },
  { year: '2018', event: 'Lead Geologist — Shallow Water Development Portfolio' },
  { year: '2020', event: 'Cross-discipline integration — Carbonate & Clastic dual systems' },
  { year: '2022', event: 'Senior Geoscientist — AI-assisted prospect maturation' },
  { year: '2024', event: '12 years. Hundreds of wells. Zero shortcuts.' },
]

const qualities = [
  { label: 'Tactical', desc: 'Reads the subsurface like a map of intentions' },
  { label: 'Patient', desc: '12 years in one basin — mastery takes time' },
  { label: 'Dual thinker', desc: 'Clastic by day, carbonate by night — both fluent' },
  { label: 'Grounded', desc: 'Field geologist. Hands on. Not a theory.' },
]

export default function JackieTribute() {
  const [visible, setVisible] = useState(false)
  const [typed, setTyped] = useState('')
  const fullText = 'Fallen Soldier. Forged, not given.'

  useEffect(() => {
    setVisible(true)
    let i = 0
    const interval = setInterval(() => {
      if (i <= fullText.length) {
        setTyped(fullText.slice(0, i))
        i++
      } else {
        clearInterval(interval)
      }
    }, 55)
    return () => clearInterval(interval)
  }, [])

  return (
    <div style={{
      minHeight: '100vh',
      background: '#0a0806',
      color: '#e8e0d5',
      fontFamily: 'Inter, sans-serif',
      overflowX: 'hidden',
    }}>
      {/* Hero */}
      <section style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        padding: '4rem 2rem',
        position: 'relative',
      }}>
        {/* Radial glow */}
        <div style={{
          position: 'absolute', inset: 0, pointerEvents: 'none',
          background: 'radial-gradient(ellipse 80% 60% at 50% 40%, rgba(180,120,60,0.12) 0%, transparent 70%)',
        }} />

        <div style={{
          opacity: visible ? 1 : 0, transform: visible ? 'translateY(0)' : 'translateY(30px)',
          transition: 'all 1.2s cubic-bezier(0.16, 1, 0.3, 1)',
        }}>
          <div style={{
            width: 120, height: 120, borderRadius: '50%',
            background: 'linear-gradient(135deg, #2a1f14, #1a2530)',
            border: '2px solid rgba(200,140,80,0.5)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '2.5rem', fontFamily: 'Space Mono, monospace',
            fontWeight: 700, color: '#c88b50',
            margin: '0 auto 3rem',
            boxShadow: '0 0 60px rgba(200,140,80,0.2)',
            letterSpacing: '-0.02em',
          }}>
            JN
          </div>

          <h1 style={{
            fontSize: 'clamp(2rem, 5vw, 3.5rem)',
            fontWeight: 700, letterSpacing: '-0.03em',
            marginBottom: '0.5rem', lineHeight: 1.1,
            background: 'linear-gradient(135deg, #e8e0d5 0%, #c88b50 100%)',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
          }}>
            Jackie Ngu
          </h1>

          <div style={{
            fontFamily: 'Space Mono, monospace',
            fontSize: '0.8rem', color: '#c88b50',
            letterSpacing: '0.15em', textTransform: 'uppercase',
            marginBottom: '2rem', opacity: 0.8,
          }}>
            {typed}<span style={{ opacity: 1 }}>|</span>
          </div>

          <p style={{
            maxWidth: 560, margin: '0 auto 3rem',
            fontSize: '1.1rem', lineHeight: 1.8,
            color: '#a09890', fontWeight: 300,
          }}>
            12 years in the field. Hundreds of wells across clastic and carbonate systems.
            Shallow water to deepwater. A geoscientist forged in the Baram Delta,
            tempered by Malaysian Basins, and emerged as one of PETRONAS Carigali's
            most trusted subsurface minds.
          </p>

          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <a href="/jackie-ngu.html" style={{
              background: 'rgba(200,140,80,0.15)', border: '1px solid rgba(200,140,80,0.4)',
              color: '#c88b50', padding: '0.6rem 1.4rem', borderRadius: 8,
              fontFamily: 'Space Mono, monospace', fontSize: '0.75rem',
              textDecoration: 'none', letterSpacing: '0.05em',
            }}>Professional Profile</a>
            <span style={{
              display: 'inline-flex', alignItems: 'center', gap: '0.4rem',
              background: 'rgba(80,100,80,0.15)', border: '1px solid rgba(80,100,80,0.4)',
              color: '#7a9a7a', padding: '0.6rem 1.4rem', borderRadius: 8,
              fontFamily: 'Space Mono, monospace', fontSize: '0.75rem',
            }}>
              <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#5a8a5a', boxShadow: '0 0 6px #5a8a5a' }} />
              PETRONAS Carigali — 2012 to 2024
            </span>
          </div>
        </div>

        {/* Scroll indicator */}
        <div style={{
          position: 'absolute', bottom: '2rem', left: '50%', transform: 'translateX(-50%)',
          display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem',
          opacity: 0.4,
        }}>
          <div style={{ width: 1, height: 40, background: 'linear-gradient(to bottom, #c88b50, transparent)' }} />
          <span style={{ fontFamily: 'Space Mono, monospace', fontSize: '0.6rem', letterSpacing: '0.1em' }}>SCROLL</span>
        </div>
      </section>

      {/* Timeline */}
      <section style={{
        padding: '6rem 2rem',
        maxWidth: 720, margin: '0 auto',
        borderTop: '1px solid rgba(200,140,80,0.1)',
      }}>
        <h2 style={{
          fontFamily: 'Space Mono, monospace', fontSize: '0.7rem',
          letterSpacing: '0.15em', textTransform: 'uppercase',
          color: '#c88b50', marginBottom: '3rem', opacity: 0.7,
        }}>
          12 Years of Ground Truth
        </h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
          {timeline.map((t, i) => (
            <div key={i} style={{
              display: 'grid', gridTemplateColumns: '4rem 1fr',
              gap: '1.5rem', paddingBottom: '2rem',
              position: 'relative',
            }}>
              <div style={{
                fontFamily: 'Space Mono, monospace', fontSize: '0.75rem',
                color: '#c88b50', paddingTop: '0.1rem', opacity: 0.8,
              }}>{t.year}</div>
              <div style={{ position: 'relative' }}>
                <div style={{
                  position: 'absolute', left: '-1.25rem', top: '0.35rem',
                  width: 6, height: 6, borderRadius: '50%',
                  background: '#c88b50', opacity: 0.6,
                }} />
                {i < timeline.length - 1 && (
                  <div style={{
                    position: 'absolute', left: '-1rem', top: '0.6rem',
                    width: 1, height: 'calc(100% + 1.5rem)',
                    background: 'rgba(200,140,80,0.2)',
                  }} />
                )}
                <p style={{ fontSize: '0.9rem', lineHeight: 1.6, color: '#c0b8b0' }}>{t.event}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Character */}
      <section style={{
        padding: '6rem 2rem',
        background: 'rgba(200,140,80,0.04)',
        borderTop: '1px solid rgba(200,140,80,0.1)',
        borderBottom: '1px solid rgba(200,140,80,0.1)',
      }}>
        <div style={{ maxWidth: 720, margin: '0 auto' }}>
          <h2 style={{
            fontFamily: 'Space Mono, monospace', fontSize: '0.7rem',
            letterSpacing: '0.15em', textTransform: 'uppercase',
            color: '#c88b50', marginBottom: '3rem', opacity: 0.7,
          }}>
            How He Works
          </h2>
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
            gap: '1.25rem',
          }}>
            {qualities.map((q, i) => (
              <div key={i} style={{
                background: 'rgba(20,16,12,0.8)',
                border: '1px solid rgba(200,140,80,0.2)',
                borderRadius: 12, padding: '1.5rem',
              }}>
                <div style={{
                  fontFamily: 'Space Mono, monospace', fontSize: '0.75rem',
                  color: '#c88b50', marginBottom: '0.5rem', fontWeight: 700,
                }}>{q.label}</div>
                <p style={{ fontSize: '0.85rem', color: '#8a8278', lineHeight: 1.6 }}>{q.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Quote */}
      <section style={{
        padding: '8rem 2rem', textAlign: 'center',
        position: 'relative',
      }}>
        <div style={{
          position: 'absolute', inset: 0, pointerEvents: 'none',
          background: 'radial-gradient(ellipse 60% 40% at 50% 50%, rgba(200,140,80,0.08) 0%, transparent 70%)',
        }} />
        <blockquote style={{
          maxWidth: 560, margin: '0 auto',
          fontSize: 'clamp(1.2rem, 3vw, 1.8rem)',
          fontWeight: 300, lineHeight: 1.6,
          color: '#d8d0c8', fontStyle: 'italic',
          opacity: 0.9,
        }}>
          "Every log tells the truth. The question is whether you're patient enough to read it."
        </blockquote>
        <div style={{
          marginTop: '2rem', fontFamily: 'Space Mono, monospace',
          fontSize: '0.7rem', color: '#c88b50', opacity: 0.6,
          letterSpacing: '0.1em',
        }}>— Jackie Ngu</div>
      </section>

      {/* Footer */}
      <footer style={{
        borderTop: '1px solid rgba(200,140,80,0.1)',
        padding: '3rem 2rem',
        textAlign: 'center',
      }}>
        <div style={{
          fontFamily: 'Space Mono, monospace', fontSize: '0.65rem',
          color: '#5a5550', letterSpacing: '0.1em',
        }}>
          A tribute page forged in the spirit of PETRONAS Carigali · Kuala Lumpur
        </div>
        <div style={{
          marginTop: '0.75rem', fontFamily: 'Space Mono, monospace',
          fontSize: '0.6rem', color: '#3a3530',
        }}>
          arifOS · jackie.arif-fazil.com
        </div>
      </footer>
    </div>
  )
}
