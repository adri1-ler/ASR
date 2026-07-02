import React, { useMemo, useState } from "react";
import { Link } from "react-router-dom";

type SportKey = "football" | "tennis" | "rugby";

interface CompetitionItem {
  name: string;
  level: string;
  region: string;
  season: string;
  description: string;
  href: string;
}

interface SportConfig {
  title: string;
  eyebrow: string;
  description: string;
  accent: string;
  competitions: CompetitionItem[];
}

const sports: Record<SportKey, SportConfig> = {
  football: {
    title: "Football",
    eyebrow: "Global football",
    description: "Pick a football competition set and browse the most recognizable official competition hubs.",
    accent: "var(--accent-coral)",
    competitions: [
      {
        name: "UEFA Champions League",
        level: "Club",
        region: "Europe",
        season: "2026/27",
        description: "Europe's premier club competition.",
        href: "https://www.uefa.com/uefachampionsleague/",
      },
      {
        name: "UEFA Europa League",
        level: "Club",
        region: "Europe",
        season: "2026/27",
        description: "Second-tier UEFA club competition.",
        href: "https://www.uefa.com/uefaeuropaleague/",
      },
      {
        name: "UEFA Conference League",
        level: "Club",
        region: "Europe",
        season: "2026/27",
        description: "UEFA's third club competition tier.",
        href: "https://www.uefa.com/uefaconferenceleague/",
      },
      {
        name: "FIFA World Cup",
        level: "International",
        region: "Global",
        season: "2026",
        description: "The biggest international football tournament.",
        href: "https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup",
      },
      {
        name: "Premier League",
        level: "Domestic",
        region: "England",
        season: "2026/27",
        description: "The top flight of English football.",
        href: "https://www.premierleague.com/",
      },
    ],
  },
  tennis: {
    title: "Tennis",
    eyebrow: "Professional tennis",
    description: "Browse the major tours and championship-level tennis competitions from the official calendars.",
    accent: "var(--accent-gold)",
    competitions: [
      {
        name: "Wimbledon",
        level: "Grand Slam",
        region: "United Kingdom",
        season: "2026",
        description: "The championships at the All England Club.",
        href: "https://www.wimbledon.com/",
      },
      {
        name: "US Open",
        level: "Grand Slam",
        region: "United States",
        season: "2026",
        description: "The final Grand Slam of the season.",
        href: "https://www.usopen.org/",
      },
      {
        name: "Roland-Garros",
        level: "Grand Slam",
        region: "France",
        season: "2026",
        description: "The premier clay-court major.",
        href: "https://www.rolandgarros.com/",
      },
      {
        name: "Nitto ATP Finals",
        level: "Year-end Finals",
        region: "Italy",
        season: "2026",
        description: "The ATP season finale for the top singles and doubles players.",
        href: "https://www.nittoatpfinals.com/",
      },
      {
        name: "WTA Finals",
        level: "Year-end Finals",
        region: "Global",
        season: "2026",
        description: "The WTA's championship finale.",
        href: "https://www.wtatennis.com/finals",
      },
    ],
  },
  rugby: {
    title: "Rugby",
    eyebrow: "Union rugby",
    description: "Switch between elite international and club rugby competitions from official tournament sources.",
    accent: "var(--accent-green)",
    competitions: [
      {
        name: "Guinness Men's Six Nations",
        level: "International",
        region: "Europe",
        season: "2026",
        description: "The annual men’s northern hemisphere championship.",
        href: "https://www.sixnationsrugby.com/en/m6n",
      },
      {
        name: "Guinness Women's Six Nations",
        level: "International",
        region: "Europe",
        season: "2026",
        description: "The annual women’s Six Nations championship.",
        href: "https://www.sixnationsrugby.com/en/w6n",
      },
      {
        name: "Nations Championship",
        level: "International",
        region: "Global",
        season: "2026",
        description: "World Rugby's new global national-team competition.",
        href: "https://www.sixnationsrugby.com/en/autumn-nations-series",
      },
      {
        name: "Investec Champions Cup",
        level: "Club",
        region: "Europe",
        season: "2026/27",
        description: "Europe's top-tier club rugby competition.",
        href: "https://www.epcrugby.com/champions-cup",
      },
      {
        name: "EPCR Challenge Cup",
        level: "Club",
        region: "Europe",
        season: "2026/27",
        description: "The secondary European club competition.",
        href: "https://www.epcrugby.com/challenge-cup",
      },
    ],
  },
};

const sportOrder: SportKey[] = ["football", "tennis", "rugby"];

const Competition: React.FC = () => {
  const [selectedSport, setSelectedSport] = useState<SportKey>("tennis");

  const sport = sports[selectedSport];
  const competitionCount = sport.competitions.length;

  const sportTabs = useMemo(() => {
    return sportOrder.map((sportKey) => ({
      key: sportKey,
      label: sports[sportKey].title,
    }));
  }, []);

  return (
    <div className="competition-page">
      <div className="competition-shell">
        <header className="competition-hero">
          <div>
            <div className="eyebrow">Competition browser</div>
            <h1>Choose a sport, then open its competitions.</h1>
            <p>
              Pick tennis, football, or rugby to filter the competitions below. Each card links to an official web page.
            </p>
          </div>

          <Link className="secondary-button" to="/">Back to dashboard</Link>
        </header>

        <section className="competition-selector" aria-label="Sport selector">
          {sportTabs.map((tab) => (
            <button
              key={tab.key}
              type="button"
              className={`sport-tab ${selectedSport === tab.key ? "is-active" : ""}`}
              onClick={() => setSelectedSport(tab.key as SportKey)}
            >
              {tab.label}
            </button>
          ))}
        </section>

        <section className="competition-summary">
          <div>
            <div className="eyebrow" style={{ color: sport.accent }}>Selected sport</div>
            <h2>{sport.title}</h2>
            <p>{sport.description}</p>
          </div>
          <div className="competition-summary-metric">
            <span>Available competitions</span>
            <strong>{competitionCount}</strong>
          </div>
        </section>

        <section className="competition-grid" aria-label="Competition list">
          {sport.competitions.map((competition) => (
            <a key={competition.name} className="competition-card" href={competition.href} target="_blank" rel="noreferrer">
              <div className="competition-card-top">
                <span>{competition.level}</span>
                <span>{competition.season}</span>
              </div>
              <h3>{competition.name}</h3>
              <p>{competition.description}</p>
              <div className="competition-card-footer">
                <span>{competition.region}</span>
                <span>Open official page</span>
              </div>
            </a>
          ))}
        </section>
      </div>
    </div>
  );
};

export default Competition;