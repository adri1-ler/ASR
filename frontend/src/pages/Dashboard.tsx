import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

interface Statistics {
  total_entities?: number;
  channel_count?: number;
  competition_count?: number;
  match_count?: number;
  team_count?: number;
  player_count?: number;
  user_count?: number;
  message_count?: number;
}

const appSections = [
  {
    title: "Live Operations",
    description: "Channels, messages, and in-game updates.",
    key: "live-operations",
    route: "/overview/live-operations",
    accent: "var(--accent-cyan)",
  },
  {
    title: "Competitions",
    description: "Seasons, standings, and tournament structure.",
    key: "competitions",
    route: "/overview/competitions",
    accent: "var(--accent-gold)",
  },
  {
    title: "Matches",
    description: "Schedules, scores, previews, and events.",
    key: "matches",
    route: "/overview/matches",
    accent: "var(--accent-coral)",
  },
  {
    title: "Teams & Players",
    description: "Squads, lineups, players, and stadiums.",
    key: "teams-players",
    route: "/overview/teams",
    accent: "var(--accent-green)",
  },
  {
    title: "Community",
    description: "Users, favorites, reactions, and friendships.",
    key: "community",
    route: "/overview/community",
    accent: "var(--accent-blue)",
  },
  {
    title: "Messaging",
    description: "Channels, membership, and threaded messages.",
    key: "messaging",
    route: "/overview/messaging",
    accent: "var(--accent-violet)",
  },
];

const shortcuts = [
  { label: "Live", key: "live-operations", route: "/overview/live-operations" },
  { label: "Matches", key: "matches", route: "/overview/matches" },
  { label: "Competitions", key: "competitions", route: "/overview/competitions" },
  { label: "Teams", key: "teams-players", route: "/overview/teams" },
  { label: "Community", key: "community", route: "/overview/community" },
  { label: "Messaging", key: "messaging", route: "/overview/messaging" },
];

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(false);
  }, []);

  return (
    <div className="dashboard-shell">
      <header className="dashboard-hero">
        <div className="dashboard-hero-copy">
          <div className="eyebrow">Sports live operations</div>
          <h1>Manage live sports data from one place.</h1>
          <p>
            Track competitions, matches, teams, messaging, and community activity in a single,
            cleaner workspace.
          </p>
          <div className="dashboard-actions">
            <Link className="primary-button" to="/overview/matches">Open matches</Link>
            <Link className="secondary-button" to="/overview/competitions">Browse competitions</Link>
          </div>
        </div>
        <div className="dashboard-hero-panel">
          <div className="hero-panel-label">System status</div>
          <div className="hero-panel-value">{loading ? "Loading…" : "Connected"}</div>
          <div className="hero-panel-text">Backend API and SQLite database are available.</div>
          <div className="hero-shortcuts">
            {shortcuts.map((shortcut) => (
              <Link key={shortcut.key} className="hero-shortcut" to={shortcut.route}>
                {shortcut.label}
              </Link>
            ))}
          </div>
        </div>
      </header>
    </div>
  );
};

export default Dashboard;
