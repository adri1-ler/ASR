import React, { useMemo } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

interface SectionConfig {
  title: string;
  eyebrow: string;
  description: string;
  accent: string;
  highlight: string;
  route: string;
  links: Array<{ label: string; to: string }>;
}

const sections: Record<string, SectionConfig> = {
  "live-operations": {
    title: "Live Operations",
    eyebrow: "Channel center",
    description: "Monitor channels, messages, and live updates without dropping into a raw data table.",
    accent: "var(--accent-cyan)",
    highlight: "Keep the conversation layer visible and easy to reach.",
    route: "/overview/live-operations",
    links: [
      { label: "Open dashboard", to: "/" },
      { label: "Open matches overview", to: "/overview/matches" },
      { label: "Open messaging overview", to: "/overview/messaging" },
    ],
  },
  competitions: {
    title: "Competitions",
    eyebrow: "Season hub",
    description: "Track seasons, standings, and tournament structure from a guided overview page.",
    accent: "var(--accent-gold)",
    highlight: "Use this page as the entry point for competition-level analysis.",
    route: "/overview/competitions",
    links: [
      { label: "Open dashboard", to: "/" },
      { label: "Open matches overview", to: "/overview/matches" },
      { label: "Open teams overview", to: "/overview/teams" },
    ],
  },
  matches: {
    title: "Matches",
    eyebrow: "Match desk",
    description: "Review fixtures, scores, previews, and match events from one dedicated page.",
    accent: "var(--accent-coral)",
    highlight: "Stay on the match story without being pushed into the tables by default.",
    route: "/overview/matches",
    links: [
      { label: "Open dashboard", to: "/" },
      { label: "Open competitions overview", to: "/overview/competitions" },
      { label: "Open teams overview", to: "/overview/teams" },
    ],
  },
  "teams-players": {
    title: "Teams & Players",
    eyebrow: "Squad room",
    description: "Work with teams, lineups, players, and stadiums in a cleaner operational view.",
    accent: "var(--accent-green)",
    highlight: "Move from squad context into the underlying entities only when needed.",
    route: "/overview/teams",
    links: [
      { label: "Open dashboard", to: "/" },
      { label: "Open matches overview", to: "/overview/matches" },
      { label: "Open community overview", to: "/overview/community" },
    ],
  },
  community: {
    title: "Community",
    eyebrow: "People hub",
    description: "Follow users, friendships, favorites, and reactions from a social overview.",
    accent: "var(--accent-blue)",
    highlight: "Useful for community management and relationship inspection.",
    route: "/overview/community",
    links: [
      { label: "Open dashboard", to: "/" },
      { label: "Open messaging overview", to: "/overview/messaging" },
      { label: "Open live operations", to: "/overview/live-operations" },
    ],
  },
  messaging: {
    title: "Messaging",
    eyebrow: "Conversation hub",
    description: "Manage channels, messages, and membership from a focus page built for navigation.",
    accent: "var(--accent-violet)",
    highlight: "Keep the messaging area separate from the rest of the admin surface.",
    route: "/overview/messaging",
    links: [
      { label: "Open dashboard", to: "/" },
      { label: "Open live operations", to: "/overview/live-operations" },
      { label: "Open community overview", to: "/overview/community" },
    ],
  },
};

const SectionPage: React.FC = () => {
  const { sectionId } = useParams<{ sectionId: string }>();
  const navigate = useNavigate();
  const section = useMemo(() => sections[sectionId || ""], [sectionId]);

  if (!section) {
    return (
      <div className="section-page">
        <div className="section-page-card">
          <div className="eyebrow">Unknown section</div>
          <h1>That page does not exist.</h1>
          <p>Use the dashboard to open one of the supported overview pages.</p>
          <button className="primary-button" type="button" onClick={() => navigate("/")}>Back to dashboard</button>
        </div>
      </div>
    );
  }

  return (
    <div className="section-page">
      <div className="section-page-card">
        <div className="section-page-topline" style={{ background: section.accent }} />
        <div className="eyebrow">{section.eyebrow}</div>
        <h1>{section.title}</h1>
        <p>{section.description}</p>
        <div className="section-page-actions">
          <button className="primary-button" type="button" onClick={() => navigate("/")}>Back to dashboard</button>
        </div>
      </div>

      <div className="section-page-grid">
        <article className="section-page-panel">
          <h2>Why this page exists</h2>
          <p>{section.highlight}</p>
        </article>

        <article className="section-page-panel">
          <h2>Quick actions</h2>
          <div className="section-page-links">
            {section.links.map((link) => (
              <Link key={link.to} to={link.to} className="section-page-link">
                {link.label}
              </Link>
            ))}
          </div>
        </article>

        <article className="section-page-panel">
          <h2>Next move</h2>
          <p>Use the links above when you want the underlying entity data, or stay on this page for the overview.</p>
        </article>
      </div>
    </div>
  );
};

export default SectionPage;
